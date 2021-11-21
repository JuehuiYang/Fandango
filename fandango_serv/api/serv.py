import os
from fandango_algo.pdf2text import reg_it
from . import singleton


# 设置关键词
def setkeyword(keyword):
    singleton.keyword = keyword
    print(singleton.keyword)
    pass


# 保存上传的pdf文件
def handle_uploaded_file(f):
    save_path = os.path.join(os.getcwd(), 'input', f.name)
    print(f.name)
    print(os.getcwd())
    print(os.getcwd() + "\\input\\")
    print(save_path)
    with open(save_path, 'wb+') as fp:
        for chunk in f.chunks():
            fp.write(chunk)


# 对文件进行分析
def ocr(filename):
    pdf_path = os.path.join(os.getcwd(), 'input', filename)
    pdf = r"./fandango_algo/pdf/pdf_test/test1.pdf"
    with open(pdf, "rb") as f:
        c = f.read()
    reg_it(c, "./fandango_algo/")


# 处理计算关键词出现频率
def get_keywordcount(filename):
    pass


# 将分析的文件压缩到一个zip文件中
def files2zip(filename):
    pdf_path = os.path.join(os.getcwd(), 'input', filename)
    pdf = r"./fandango_algo/pdf/pdf_test/test1.pdf"
    with open(pdf, "rb") as f:
        c = f.read()
    reg_it(c, "./fandango_algo/")