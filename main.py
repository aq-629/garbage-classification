from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from detect import detect_images
import time
import urllib.parse
import glob

app = FastAPI()

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

# 挂载模板目录
templates = Jinja2Templates(directory=os.path.join(project_root, "templates"))

# 挂载预测结果目录（确保能访问 runs/detect 下的所有子目录）
predict_base_dir = os.path.join(project_root, "runs/detect")
app.mount("/runs/detect", StaticFiles(directory=predict_base_dir), name="predict_results")

# 类别映射
class_mapping = ['可回收物', '有害垃圾', '厨余垃圾', '其他垃圾']


def now():
    return int(time.time())


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "now": now})


@app.post("/upload/")
async def upload_files(request: Request, files: list[UploadFile] = File(...)):
    temp_images_dir = os.path.join(project_root, "temp_images")
    os.makedirs(temp_images_dir, exist_ok=True)

    image_paths = []
    for file in files:
        # 直接使用原始文件名，FastAPI 会处理好编码
        file_path = os.path.join(temp_images_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        image_paths.append(file_path)

    label_file_paths, save_dir = detect_images(image_paths)

    results = []
    for i, file in enumerate(files):
        # 获取原始文件名（不包含路径）
        original_filename = file.filename
        # 去除文件扩展名
        filename_without_ext = os.path.splitext(original_filename)[0]

        label_content = "未找到对应的标签文件"
        label_file_name = f"{filename_without_ext}.txt"
        # 获取最新的预测结果文件夹
        predict_folders = sorted(glob.glob(os.path.join(predict_base_dir, "predict*")), key=os.path.getmtime)
        if predict_folders:
            latest_predict_folder = predict_folders[-1]
            label_file_path = os.path.join(latest_predict_folder, "labels", label_file_name)
            # 使用 os.fsencode 和 os.fsdecode 确保路径编码与文件系统一致
            encoded_label_file_path = os.fsencode(label_file_path)
            absolute_label_file_path = os.fsdecode(os.path.abspath(encoded_label_file_path))
            # 打印标签文件路径，用于调试
            print(f"尝试查找标签文件: {absolute_label_file_path}")
            # 检查文件是否存在，使用绝对路径
            if os.path.exists(absolute_label_file_path):
                try:
                    with open(absolute_label_file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        label_content = []
                        for line_num, line in enumerate(lines):
                            parts = line.split()
                            if len(parts) > 0:
                                try:
                                    class_id = int(parts[0])
                                    class_name = class_mapping[class_id]
                                    label_content.append(class_name)
                                except ValueError:
                                    print(
                                        f"标签文件 {absolute_label_file_path} 第 {line_num + 1} 行的类别 ID 不是有效的整数: {line.strip()}")
                                except IndexError:
                                    print(
                                        f"标签文件 {absolute_label_file_path} 第 {line_num + 1} 行的类别 ID 超出类别映射范围: {line.strip()}")
                            else:
                                print(f"标签文件 {absolute_label_file_path} 第 {line_num + 1} 行为空或格式错误: {line.strip()}")
                        label_content = ', '.join(label_content) if label_content else "标签文件无有效内容"
                except Exception as e:
                    print(f"读取标签文件 {absolute_label_file_path} 出错: {e}")
                    label_content = "读取标签文件出错"
            else:
                print(f"标签文件 {absolute_label_file_path} 不存在。")
        else:
            print("未找到预测结果文件夹。")

        predict_dir_name = os.path.basename(latest_predict_folder) if predict_folders else ""
        predicted_image_name = f"{filename_without_ext}.jpg"
        # 对预测图片文件名进行编码
        encoded_predicted_image_name = urllib.parse.quote(predicted_image_name)
        predicted_image_url = f"/runs/detect/{predict_dir_name}/{encoded_predicted_image_name}"

        results.append({
            "filename": file.filename,
            "label_content": label_content,
            "predicted_image_url": predicted_image_url
        })

    for image_path in image_paths:
        os.remove(image_path)

    return templates.TemplateResponse("index.html", {"request": request, "results": results, "now": now})


# 处理图像请求并设置响应头
@app.get("/runs/detect/{predict_dir_name}/{filename}")
async def get_image(predict_dir_name: str, filename: str, response: Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    # 对文件名进行解码处理
    decoded_filename = urllib.parse.unquote(filename)
    file_path = os.path.join(predict_base_dir, predict_dir_name, decoded_filename)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
        return Response(content=content, media_type="image/jpeg")
    else:
        return Response(status_code=404)