# from pdf2image import convert_from_path
# im=convert_from_path("./db.pdf",1080)
# im[0].save("t1.png")
import cv2
import fitz
import numpy as np
import math
from pdf.utils import pixmap2array
'''
# 将PDF转化为图片
pdfPath pdf文件的路径
imgPath 图像要保存的文件夹
zoom_x x方向的缩放系数
zoom_y y方向的缩放系数
rotation_angle 旋转角度
'''
from pdf._imgList import *
import os
class pdf2img():
    def __init__(self):
        self.imglist=[]
        self.IMG=ImgList()
        self.output_dir=""
    def get_Rect(self,page):
        rect=page.rect
        return [[rect,""]]
    def format(self,index,row,cow):
        return f"{index}_{row}_{cow}"
    def read(self,path,content):
        pdf=fitz.open(path)
        return pdf
    def pdf_image(self,pdfPath,imgPath,zoom_x,zoom_y,rotation_angle):
        pdf=self.read(pdfPath,"")
        self.output_dir=imgPath
        if not os.path.exists(imgPath):
            os.mkdir(imgPath)
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            rects = self.get_Rect(page)
            for clip,suffix in rects:
                img=self.write_img(page, clip,
                                   self.path_format(imgPath, pg,suffix), zoom_x, zoom_y)
                # height,width=img.shape[0:2]
                # HWC （height：Y轴，width：X轴，channel）
                self.imglist.append(img)
                # a=10
        pdf.close()
    def path_format(self,imgPath, index, dir=""):
        return imgPath + str(index) + dir + ".png"

    def write_img(self,page, clip, path, zoom_x, zoom_y):
        trans = fitz.Matrix(zoom_x, zoom_y)
        pm = page.getPixmap(matrix=trans, clip=clip)
        # 开始写图像
        img=pixmap2array(pm)
        # pm.writePNG(path)
        return img

class pdf2img_empty_cut(pdf2img):
    def __init__(self):
        super().__init__()
        self.set_slice()
    def set_slice(self,slice=5):
        self.slice=slice
    def add_empty(self,img,empty_size=100):
        height,width=img.shape[0:2]
        up=np.full([empty_size,width,3],255,dtype=np.uint8)
        bottem=np.copy(up)
        new_img=np.vstack((up,img,bottem))
        return new_img
    def spectial_process(self,img):
        img=self.add_empty(img)
        h,w,c=img.shape
        img=cv2.resize(img,(int(w),int(h/2)))
        print(img.shape)
        return img
    def empty_cut(self):
        imglist=self.imglist
        for i,img in enumerate(imglist):
            img_gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            height, width = img.shape[0:2]
            img_gray=self.cut(img_gray,img,i)
            cv2.imwrite(f"./litt/{i}.png",img_gray)
    def cut(self,img,ori_img,index):
        height, width = img.shape[0:2]
        avg_h=int(height/self.slice)
        imglist=[]
        _h=0
        _w=0
        for i in range(1,self.slice+1):
            new_h=self.search(img,avg_h*i,width,height)
            tmp_img=ori_img[_h:new_h,:,:]
            _h=new_h
            # print(tmp_img.shape)
            tmp_img=self.spectial_process(tmp_img)
            nh,nw=tmp_img.shape[0:2]
            # print(tmp_img.shape)
            print("_______________________")
            half_width=int(nw/2)
            tmp_img_l=tmp_img[:,0:half_width,:]
            tmp_img_r=tmp_img[:,half_width:-1,:]
            self.IMG.append(tmp_img_l,self.format("",index,f"_1_{i}"))
            self.IMG.append(tmp_img_r,self.format("",index,f"_2_{i}"))
            # cv2.imwrite(f"./{self.output_dir}/{index}_{i}_l.png", tmp_img_l)
            # cv2.imwrite(f"./{self.output_dir}/{index}_{i}_r.png",tmp_img_r )
            # cv2.line(ori_img,(0,new_h),(width,new_h),(0,0,0),1)
        return ori_img
    def search(self,img,avg_h,width,ori_h,maxdep=100):
        m_h=avg_h
        m_n=0
        for i in range(maxdep):
            top=self.cal_sum(img,avg_h+i,width,ori_h)
            bottom=self.cal_sum(img,avg_h-i,width,ori_h)
            if(m_n<top):
                m_n=top
                m_h=avg_h+i
            if(m_n<bottom):
                m_n=bottom
                m_h=avg_h-i
        # print("no ok")
        return m_h
    def cal_sum(self,img,height,wid,ori_h):
        if height<0 or height>=ori_h:
            return 0
        # print("in")
        lsum=np.sum(img[height]/255)
        return lsum
class pdf2img_empty_cut_one(pdf2img_empty_cut):
    def __init__(self):
        super().__init__()
    def read(self,path,content):
        pdf=fitz.Document(stream=path, filetype='pdf')
        return pdf
    def cut(self,img,ori_img,index):
        height, width = img.shape[0:2]
        avg_h = int(height / self.slice)
        imglist = []
        _h = 0
        _w = 0
        for i in range(1, self.slice + 1):
            new_h = self.search(img, avg_h * i, width, height)
            tmp_img = ori_img[_h:new_h, :, :]
            _h = new_h
            # print(tmp_img.shape)
            tmp_img = self.spectial_process(tmp_img)
            nh, nw = tmp_img.shape[0:2]
            # print(tmp_img.shape)
            print("_______________________")
            self.IMG.append(tmp_img,self.format("",index,"_1_0"))
            cv2.imwrite(f"./db/{index}_{i}.png", tmp_img)
        return ori_img
class pdf2img_31cut(pdf2img):
    def get_Rect(self,page):
        rect = page.rect
        mp=(rect.bl)/3
        clip_t=fitz.Rect(rect.tl,(rect.tr+rect.tr+rect.br)/3)
        clip_m=fitz.Rect(rect.bl/3,(rect.tr+rect.tr+rect.br+rect.tr+rect.tr+rect.br)/3)
        clip_b = fitz.Rect((rect.bl+rect.bl)/3, rect.br)
        return [[clip_t,"_t"],[clip_m,"_m"],[clip_b,"_b"]]
class pdf2img_21cut(pdf2img):
    def get_Rect(self,page):
        rect = page.rect
        clip_t=fitz.Rect(rect.tl,(rect.br+rect.tr)/2)
        clip_b = fitz.Rect(rect.bl/2, rect.br)
        return [[clip_t,"_t"],[clip_b,"_b"]]
class pdf2img_22cut(pdf2img):
    def get_Rect(self,page):
        rect = page.rect
        midpoint=rect.br/2
        clip_1=fitz.Rect(rect.tl,midpoint)
        clip_2=fitz.Rect((rect.tl+rect.tr)/2,(rect.tr+rect.br)/2)
        clip_3=fitz.Rect(rect.bl/2,(rect.br+rect.bl)/2)
        clip_4=fitz.Rect(midpoint,rect.br)
        return [[clip_1,"_1"],[clip_2,"_2"],[clip_3,"_3"],[clip_4,"_4"]]
def pdf_image(pdfPath, imgPath, zoom_x, zoom_y, rotation_angle):
    pass
    # 打开PDF文件
    # pdf = fitz.open(pdfPath)
    # # 逐页读取PDF
    # for pg in range(0, pdf.pageCount):
    #     page = pdf[pg]
    #     # 设置缩放和旋转系数
    #     rect=page.rect
    #     mp=(rect.bl)/2
    #     clip_t=fitz.Rect(mp,rect.br)
    #     write_img(page,clip_t,path_format(imgPath,pg),zoom_x,zoom_y)
    #     clip_b=fitz.Rect(rect.tl,(rect.tr+rect.br)/2)
    #     write_img(page,clip_b,path_format(imgPath,pg,"_b"),zoom_x,zoom_y)
    #     # trans = fitz.Matrix(zoom_x, zoom_y)
    #     # pm = page.getPixmap(matrix=trans,clip=clip)
    #     # 开始写图像
    #     # pm.writePNG(imgPath + str(pg) + ".png")
    #     # imgPath + str(pg) + ".png"
    # pdf.close()

if __name__ == '__main__':
    # pi=pdf2img()
    pi=pdf2img_empty_cut_one()
    # pi=pdf2img_4cut()
    pi.set_slice(10)
    pi.pdf_image(r"./pdf_test/test3.pdf", r"./cc/", 10,10, 0)
    # pi.pdf_image(r"./TheLittlePrince.pdf", r"./litt/", 10, 10, 0)
    pi.empty_cut()
# pdf_image(r"./db.pdf", r"./db/", 10,10, 0)