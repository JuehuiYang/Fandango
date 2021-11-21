## code struct
```
├─img
|
├─inference
│  ├─ch_ppocr_mobile_v2.0_cls_infer #旋转模型
│  ├─en_number_mobile_v2.0_rec_infer #识别模型
│  └─en_ppocr_mobile_v2.0_det_infer #文本检测模型
|
├─pdf
│  │  opcv.py # 边缘检测
│  │  pdminer.py 
│  │  st.py
│  │  utils.py 
│  │  _imgList.py # 图片列表类，用于储存pdf切图以及二次切图与结果
│  └─ _pdf2img.py #将pdf转化成图片，并切割为小块图片。
│
├─ppocr
│  │  __init__.py
│  │
│  ├─data
│  ├─losses #损失函数
│  ├─metrics
│  ├─modeling #模型结构
│  │  ├─architectures
│  │  ├─backbones
│  │  ├─heads
│  │  ├─necks
│  │  └─transforms
│  │
│  ├─optimizer
│  ├─postprocess
│  │
│  └─utils
│     ├─dict # 文本字典
│     ├─e2e_metric
│     └─e2e_utils

│
└─tools
    │
    └─infer
        │  predict_cls.py # 旋转预测 
        │  predict_det.py # 目标检测预测
        │  predict_rec.py # 识别预测
        │  predict_system.py # infer目录下的预测合集。   
        └─ utility.py
```
## how to start
入口：tools/infer/predict_system.py

```python
if __name__ == "__main__":
    pdf=r"../../pdf/pdf_test/test2.pdf"
    with open(pdf,"rb") as f:
        c=f.read()
    output=pdf2img2rec(c)
    demo(output)
```
input为文件字节码。
output为tools/infer/pdf_struct.py（txt与pdf接口在此）
所输出的pdf文件皆为字节码文件即file.read().
函数demo为展示输出。

## test file
测试文件在pdf/pdf_test文件夹内
目前推荐测试的文件有test系列以及TheLittlePrince.pdf