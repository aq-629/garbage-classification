import os
from ultralytics import YOLO
import shutil
import glob

model_path = "garbage-classification\\train\weights/best.pt"  # 确保模型路径正确


def detect_images(image_paths):
    model = YOLO(model_path)
    try:
        results = model(image_paths, save=True, save_txt=True, project="runs/detect", name="predict")
        # 获取最新的预测结果文件夹
        predict_base_dir = os.path.join("runs/detect")
        predict_folders = sorted(glob.glob(os.path.join(predict_base_dir, "predict*")), key=os.path.getmtime)
        if predict_folders:
            save_dir = predict_folders[-1]
            print(f"目标检测完成，结果保存路径：{save_dir}")
        else:
            print("未找到预测结果文件夹。")
            return [], None
    except Exception as e:
        print(f"目标检测出错：{e}")
        return [], None

    label_paths = []
    for image_path in image_paths:
        # 获取原始文件名（不包含路径）
        original_filename = os.path.basename(image_path)
        # 去除文件扩展名
        filename_without_ext = os.path.splitext(original_filename)[0]
        label_file_name = f"{filename_without_ext}.txt"
        label_path = os.path.join(save_dir, "labels", label_file_name)
        # 使用 os.fsencode 和 os.fsdecode 确保路径编码与文件系统一致
        encoded_label_path = os.fsencode(label_path)
        absolute_label_path = os.fsdecode(os.path.abspath(encoded_label_path))
        label_paths.append(absolute_label_path)
        # 打印生成的标签文件路径，用于调试
        print(f"生成的标签文件路径: {absolute_label_path}")

    return label_paths, save_dir