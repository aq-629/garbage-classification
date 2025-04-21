# 垃圾分类识别项目

## 项目概述
本项目使用YOLOv8实现了一个垃圾分类识别系统，能够识别有害垃圾、厨余垃圾、可回收物和其他垃圾四个大类。通过训练YOLOv8模型，利用其强大的目标检测能力，对垃圾图像进行分类，为智能垃圾分类提供了有效的解决方案。此外，项目还提供了基于FastAPI的Web界面，方便用户上传图片并查看分类结果。

第一次大提问：利用yolov8为我实现一个垃圾分类识别的项目，类别包括有害垃圾、厨余垃圾、可回收物和其他垃圾四个大类，同时要生成工程类的目录格式，具体目录也需要生成出来。
回答：项目框架及代码模板

第二次大提问：我已经训练出了自己的模型，detect.py可以同时预测所有上传的图片，并生成到一个predict文件夹中，lables下分别是每一个预测图片生成的标签，要求按图片上传顺序排序。并且请根据我的代码，为我生成一个前端页面，要求上传一张或者多张图片，并且根据lables目录下对应的txt文件内容在同一页面下生成识别的文字结果，并且将输出图片也显示出来，图片的位置位于predict中，与lables位于同一级，目录结构如下

├── runs/
│   └── detect/
│       └── predict/
│           └── labels/

，可以使用fastapi作为前后端通讯工具。



## 项目结构
```
garbage-classification-yolov8-project/
├── data/
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
├── models/
│   └── yolov8n.pt
├── config/
│   └── yolov8n.yaml
├── utils/
│   ├── dataset.py
│   ├── transforms.py
│   └── utils.py
├── templates/
│   └── index.html
├── runs/
│   └── detect/
│       └── predict/
│           └── labels/
├── garbage-classification/
│   └── train/
│       └── args.yaml
├── .idea/
│   ├── inspectionProfiles/
│   │   └── profiles_settings.xml
│   ├── misc.xml
│   └── workspace.xml
├── main.py
├── train.py
├── detect.py
├── README.md
└── __pycache__/
```

### 各部分说明
- **`data/`**：存放数据集，包括训练集、验证集和测试集的图像和标签。
- **`models/`**：存放预训练模型，如`yolov8n.pt`。
- **`config/`**：存放模型配置文件，如`yolov8n.yaml`。
- **`utils/`**：存放工具类和数据处理脚本，包括数据集加载、图像预处理等功能。
- **`templates/`**：存放HTML模板文件，用于构建Web界面。
- **`runs/`**：存储模型训练和检测的结果。
- **`garbage-classification/`**：存放模型训练的相关配置和结果。
- **`.idea/`**：PyCharm集成开发环境的配置目录。
- **`main.py`**：基于FastAPI的Web应用程序入口，提供文件上传和显示检测结果的功能。
- **`train.py`**：训练脚本，用于训练YOLOv8模型。
- **`detect.py`**：检测脚本，使用训练好的模型对输入图像进行目标检测。
- **`README.md`**：项目说明文档。

## 数据集准备
1. 将图像数据存放在`data/images`目录下，按照训练、验证和测试集进行划分，分别存放在`train/`、`val/`和`test/`子目录中。
2. 将标签数据存放在`data/labels`目录下，与图像数据对应，同样按照训练、验证和测试集进行划分。

## 模型训练
1. **下载预训练模型**：下载`yolov8n.pt`预训练模型，并放置在`models`目录下。

2. **配置模型参数**：配置`config/yolov8n.yaml`文件，设置数据集路径、类别数量和类别名称等信息。

3. **运行训练脚本**：在终端中运行以下命令开始训练模型：

   ```
    python train.py
   ```

4. **使用模型:**利用公开数据集训练好的模型储存在`garbage-classification/train/weights/best.pt`中吗，`detect.py`预测代码中选用的正是此训练好的模型。



## 启动Web服务

运行以下命令启动基于FastAPI的Web服务：
```bash
uvicorn main:app --reload
```

打开浏览器，访问`http://127.0.0.1:8000`，即可上传图片并查看垃圾分类结果。

## 依赖安装
确保你已经安装了以下依赖库：
```bash
pip install torch torchvision ultralytics fastapi uvicorn jinja2
```



## 注意事项

- 请确保数据集的标签格式与YOLOv8要求的格式一致。
- 训练模型可能需要较长时间，建议使用GPU进行训练。
- 在运行Web服务时，请确保端口未被占用。