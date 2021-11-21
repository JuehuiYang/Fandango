import os
import zipfile
from fandango_algo.pdf2text import reg_it
from . import singleton

input_abspath = os.path.join(os.getcwd(), 'input')
output_abspath = os.path.join(os.getcwd(), 'output')
zip_abspath = os.path.join(os.getcwd(), 'output')


# 设置关键词
def setkeyword(keyword):
    singleton.keyword = keyword
    pass


# 保存上传的pdf文件
def handle_uploaded_file(f):
    save_path = os.path.join(input_abspath, f.name)
    print(f.name)
    print(os.getcwd())
    print(os.getcwd() + "\\input\\")
    print(save_path)
    with open(save_path, 'wb+') as fp:
        for chunk in f.chunks():
            fp.write(chunk)
    ocr(f.name)


# 对文件进行分析
def ocr(filename):
    pdf_path = os.path.join(input_abspath, filename)
    with open(pdf_path, "rb") as f:
        c = f.read()
    reg_it(c, output_abspath, "./fandango_algo/")


# TODO 处理计算关键词出现频率
def get_keywordcount(filename):
    pass


# 将分析的文件压缩到一个zip文件中
def get_zip(name):
    zip_path = os.path.join(zip_abspath, name)
    files = [
        os.path.join(output_abspath, 'origin.pdf'),
        os.path.join(output_abspath, 'box.pdf'),
        os.path.join(output_abspath, 'text.pdf'),
    ]
    file2zip(zip_path, files)
    return zip_path


def file2zip(zip_file_name: str, file_names: list):
    """ 将多个文件夹中文件压缩存储为zip

    :param zip_file_name:   /root/Document/test.zip
    :param file_names:      ['/root/user/doc/test.txt', ...]
    :return:
    """
    # 读取写入方式 ZipFile requires mode 'r', 'w', 'x', or 'a'
    # 压缩方式  ZIP_STORED： 存储； ZIP_DEFLATED： 压缩存储
    with zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for fn in file_names:
            parent_path, name = os.path.split(fn)

            # zipfile 内置提供的将文件压缩存储在.zip文件中， arcname即zip文件中存入文件的名称
            # 给予的归档名为 arcname (默认情况下将与 filename 一致，但是不带驱动器盘符并会移除开头的路径分隔符)
            zf.write(fn, arcname=name)

            # 等价于以下两行代码
            # 切换目录， 直接将文件写入。不切换目录，则会在压缩文件中创建文件的整个路径
            # os.chdir(parent_path)
            # zf.write(name)
