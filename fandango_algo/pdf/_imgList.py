'''
以行列式的形式进行组合。
先列后行
1_1_1
代表第一张图片的第一列第一行。
'''
import numpy as np
import cv2
class ImgList():
    def  __init__(self):
        self.img_list=[]
        self.num2name={}
        self.name2num={}
        self.len=0
    def setName(self,name=""):
        self.name=name
    def set_pice(self,cow,row):
        self.c=cow
        self.r=row
    def append(self,img,img_name):
        self.img_list.append(img)
        self.name2num[img_name]=self.len
        self.num2name[self.len]=img_name
        self.len+=1
    def decode(self,imgname):
        index,cow,row=imgname.spilt("_")
        return int(index),int(cow),int(row)
    def empty(self,img,empty_size=100):
        return img[:,empty_size:-empty_size,:]
    def rsz(self):
        i_list=[]
        imglist=self.img_list
        img=np.array(imglist)
        _len=int(self.len/(self.c*self.r))
        img=img.reshape((_len,self.c,self.r))
        for index in range(_len):
            for cow in range(self.c):
                for row in range(self.r):
                    now_img=img[index][cow][row]
                    if row==0:
                        last_img =self.empty(img[index][cow][row])

                        continue
                    last_img=np.hstack((last_img,self.empty(now_img)))
                    # cv2.imwrite(f"{index}_{cow}_{row}.png",last_img)
                if(cow==0):
                    last_cow=last_img
                    continue
                last_cow=np.vstack((last_cow,last_img))
            # cv2.imwrite(f"{self.name}_{index}.png", last_cow)
            i_list.append(last_cow)
        self.img_list=i_list
    # def add_copy(self,img):

class ImgListWithTxt(ImgList):
    def  __init__(self):
        self.txt=[]
        super().__init__()
    def append_txt(self,text):
        self.txt.append(text)
    def output_txt(self):
        txt=[]
        for i in range(0,len(self.txt),self.c):
            tmp=[]
            for j in range(self.c):
                tmp+=self.txt[i+j]
            txt.append(tmp)
        return txt
