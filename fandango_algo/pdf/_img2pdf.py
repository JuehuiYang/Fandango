import glob
import fitz  # 导入本模块需安装pymupdf库
import os
import shutil
from fitz import Pixmap
from pdf.utils import array2pix
# 将文件夹中所有jpg图片全部转换为一个指定名称的pdf文件，并保存至指定文件夹
# def pic2pdf(img_list,pdf_path,pdf_name):
#     doc = fitz.open()
#
#     for img in img_list:
#         imgdoc=array2pix(img)
#         # imgdoc = Pixmap(img)
#         imgdoc=fitz.open("pdf",imgdoc.pdfocr_tobytes())
#         imgpdf = imgdoc.convertToPDF()
#         # pdfbytes = imgdoc.convertToPDF()
#         # imgpdf = fitz.open("pdf", imgpdf)
#         doc.insertPDF(imgpdf)
#     doc.save(pdf_path + pdf_name)
#     doc.close()
def pic2pdf(imglist, pdf_path, pdf_name):
    name="asxazdasdasdaz"
    if not os.path.exists(f"./{name}"):
        os.mkdir(f"./{name}")
    for i,img in enumerate(imglist):
        cv2.imwrite(f"./{name}/{i}.png",img)
    doc = fitz.open()
    for img in sorted(glob.glob(f"./{name}" + "\*.png")):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(os.path.join(f"./{name}",pdf_path))
    doc.close()
    with open(os.path.join(f"./{name}",pdf_path),"rb") as f:
        c=f.read()
    shutil.rmtree(f"./{name}")
    return c
def pic2pdf_1(img_path, pdf_path, pdf_name):
    doc = fitz.open()

    for img in sorted(glob.glob(img_path + "\*.png")):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(pdf_path + pdf_name)
    doc.close()

# 将文件夹中指定jpg图片转换为指定名称的pdf文件，并保存至指定文件夹
def pic2pdf_2(img_path, pdf_path, img_list, pdf_name):
    doc = fitz.open()
    pic_list = [img_path+i for i in img_list]

    for img in sorted(pic_list):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(pdf_path + pdf_name)
    doc.close()

# 将文件夹中所有jpg图片分别转换为同一名称的pdf文件，并保存至指定文件夹

def pic2pdf_3(img_path, pdf_path):

    for img in glob.glob(img_path + "\*.jpg"):
        file_name = os.path.basename(img).replace('jpg', 'pdf')
        doc = fitz.open()
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
        doc.save(pdf_path + '\\' + file_name)
        doc.close()

import os
import cv2
import numpy as np
from PIL import Image
if __name__ == '__main__':
    img_path = r'./img'
    pdf_path = r'./img'
    dirs=os.listdir(img_path)
    imglist=[]
    for i in dirs:
        img=cv2.imread(os.path.join(img_path,i))
        # img=Image.open(os.path.join(img_path,i))
        # img=np.array(img)
        imglist.append(img)
    pic2pdf(imglist,pdf_path,"1.pdf")
    img_list1, pdf_name1 = [r'\001.jpg', r'\002.jpg'], r'\2.pdf'

    # pic2pdf_1(img_path=img_path, pdf_path=pdf_path, pdf_name=r'\1.pdf')
    # pic2pdf_2(img_path=img_path, pdf_path=pdf_path, img_list=img_list1, pdf_name=pdf_name1)
    # pic2pdf_3(img_path=img_path, pdf_path=pdf_path)