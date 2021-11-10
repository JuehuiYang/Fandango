from pdf._img2pdf import *
class pdf_struct():
    def __init__(self):
        self.box_img_list=[]
        self.text_img_list=[]
        # self.origin=
        self.txt=[]

    '''
        输入为box，text和orgin。
        返回的为open后file.read()的内容。
    '''
    def img2pdf(self,name):
        imglist=[]
        if name=="box":
            imglist=self.box_img_list
        elif name=="text":
            imglist=self.text_img_list
        elif name=="origin":
            return self.origin
        else:
            raise TypeError("no such type pdf")
        bytes = pic2pdf(imglist, "/img", "1.pdf")
        return bytes

    def set_txt(self,txt):
        self.txt=txt

    def get_txt(self):
        return self.txt

    def add_boximg(self,imglist):
        self.box_img_list=imglist

    def add_textimg(self,imglist):
        self.text_img_list=imglist

    def add_origin(self,bytes):
        self.origin=bytes