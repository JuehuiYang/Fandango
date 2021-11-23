# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
import subprocess

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../..')))

os.environ["FLAGS_allocator_strategy"] = 'auto_growth'

import cv2
import copy
import numpy as np
import time
import logging
from PIL import Image
import mytools.infer.utility as utility
import mytools.infer.predict_rec as predict_rec
import mytools.infer.predict_det as predict_det
import mytools.infer.predict_cls as predict_cls
from ppocr.utils.utility import get_image_file_list, check_and_read_gif
from ppocr.utils.logging import get_logger
from mytools.infer.utility import draw_ocr_box_txt, get_rotate_crop_image

logger = get_logger()


class TextSystem(object):
    def __init__(self, args):
        if not args.show_log:
            logger.setLevel(logging.INFO)

        self.text_detector = predict_det.TextDetector(args)
        self.text_recognizer = predict_rec.TextRecognizer(args)
        self.use_angle_cls = args.use_angle_cls
        self.drop_score = args.drop_score
        if self.use_angle_cls:
            self.text_classifier = predict_cls.TextClassifier(args)

    def print_draw_crop_rec_res(self, img_crop_list, rec_res):
        bbox_num = len(img_crop_list)
        for bno in range(bbox_num):
            cv2.imwrite("./output/img_crop_%d.jpg" % bno, img_crop_list[bno])
            logger.info(bno, rec_res[bno])

    def __call__(self, img, cls=True):
        ori_im = img.copy()
        dt_boxes, elapse = self.text_detector(img)

        logger.debug("dt_boxes num : {}, elapse : {}".format(
            len(dt_boxes), elapse))
        if dt_boxes is None:
            return None, None
        img_crop_list = []

        dt_boxes = sorted_boxes(dt_boxes)

        for bno in range(len(dt_boxes)):
            tmp_box = copy.deepcopy(dt_boxes[bno])
            img_crop = get_rotate_crop_image(ori_im, tmp_box)
            h, w, c = img_crop.shape
            img_crop_list.append(img_crop)
        if self.use_angle_cls and cls:
            img_crop_list, angle_list, elapse = self.text_classifier(
                img_crop_list)
            logger.debug("cls num  : {}, elapse : {}".format(
                len(img_crop_list), elapse))

        rec_res, elapse = self.text_recognizer(img_crop_list)
        logger.debug("rec_res num  : {}, elapse : {}".format(
            len(rec_res), elapse))
        # self.print_draw_crop_rec_res(img_crop_list, rec_res)
        filter_boxes, filter_rec_res = [], []
        for box, rec_reuslt in zip(dt_boxes, rec_res):
            text, score = rec_reuslt
            if score >= self.drop_score:
                filter_boxes.append(box)
                filter_rec_res.append(rec_reuslt)
        return filter_boxes, filter_rec_res


def sorted_boxes(dt_boxes):
    """
    Sort text boxes in order from top to bottom, left to right
    args:
        dt_boxes(array):detected text boxes with shape [4, 2]
    return:
        sorted boxes(array) with shape [4, 2]
    """
    num_boxes = dt_boxes.shape[0]
    sorted_boxes = sorted(dt_boxes, key=lambda x: (x[0][1], x[0][0]))
    _boxes = list(sorted_boxes)

    for i in range(num_boxes - 1):
        if abs(_boxes[i + 1][0][1] - _boxes[i][0][1]) < 10 and \
                (_boxes[i + 1][0][0] < _boxes[i][0][0]):
            tmp = _boxes[i]
            _boxes[i] = _boxes[i + 1]
            _boxes[i + 1] = tmp
    return _boxes


from pdf._pdf2img import *
from pdf._imgList import *


def reg(args, IMG):
    imglist = IMG.img_list
    text_sys = TextSystem(args)
    is_visualize = True
    font_path = args.vis_font_path
    drop_score = args.drop_score
    # warm up 10 times
    if args.warmup:
        img = np.random.uniform(0, 255, [640, 640, 3]).astype(np.uint8)
        for i in range(10):
            res = text_sys(img)

    total_time = 0
    cpu_mem, gpu_mem, gpu_util = 0, 0, 0
    _st = time.time()
    count = 0
    _l = ImgListWithTxt()  # 储存box图片
    _r = ImgListWithTxt()  # 储存text图片
    for idx, img in enumerate(imglist):
        if img is None:
            logger.info("error in loading image:{}".format(idx))
            continue
        starttime = time.time()
        dt_boxes, rec_res = text_sys(img)
        elapse = time.time() - starttime
        total_time += elapse
        print(rec_res)
        logger.info(
            str(idx) + "  Predict time of %s: %.3fs" % (idx, elapse))
        for text, score in rec_res:
            logger.info("{}, {:.3f}".format(text, score))

        if is_visualize:
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            boxes = dt_boxes
            txts = [rec_res[i][0] for i in range(len(rec_res))]
            scores = [rec_res[i][1] for i in range(len(rec_res))]
            # print(txts)
            img_left, img_right = draw_ocr_box_txt(
                image,
                boxes,
                txts,
                scores,
                drop_score=drop_score,
                font_path=font_path)

            _l.append(img_left, IMG.num2name[idx])
            _l.append_txt(txts)
            _r.append(img_right, IMG.num2name[idx])
            _r.append_txt(txts)
            # draw_img_save = "./inference_results/"
            # if not os.path.exists(draw_img_save):
            #     os.makedirs(draw_img_save)
            # cv2.imwrite(
            #     os.path.join(draw_img_save, os.path.basename(IMG.num[idx]+".png")),
            #     img_right[:, :, ::-1])
            # logger.info("The visualized image saved in {}".format(
            #     os.path.join(draw_img_save, os.path.basename(IMG.img_dict[idx]+".png"))))

    logger.info("The predict total time is {}".format(time.time() - _st))
    logger.info("\nThe predict total time is {}".format(total_time))
    return _l, _r


def init_params(prefix):
    args = utility.parse_args()
    args.image_dir = prefix + "./pdf/pdf_test/test1.pdf"
    args.det_model_dir = prefix + "./inference/en_ppocr_mobile_v2.0_det_infer/"
    args.rec_model_dir = prefix + "./inference/en_number_mobile_v2.0_rec_infer/"
    args.cls_model_dir = prefix + "./inference/ch_ppocr_mobile_v2.0_cls_infer/"
    args.use_angle_cls = False
    args.use_space_char = True
    args.rec_char_dict_path = prefix + "./ppocr/utils/en_dict.txt"
    args.use_gpu = False
    return args


from mytools.infer.pdf_struct import pdf_struct


def pdf2img2rec(pdf_path, prefix):
    dimy = 1
    # 切割图片
    pi = pdf2img_empty_cut_one()
    # pi=pdf2img_4cut()
    pi.set_slice(5)
    pi.pdf_image(pdf_path, r"../../pdf/c/", 4, 8, 0)
    # pi.pdf_image(r"./TheLittlePrince.pdf", r"./litt/", 10, 10, 0)
    pi.empty_cut()
    slice = pi.slice
    img = pi.IMG
    # 初始化参数
    args = init_params(prefix)
    # 出图与文字
    _l, _r = reg(args, img)

    # 合并
    _l.set_pice(slice, dimy)
    _l.setName("box")
    _l.rsz()
    txt = _l.output_txt()
    _r.set_pice(slice, dimy)
    _r.setName("text")
    _r.rsz()
    # 整合数据
    output = pdf_struct()
    output.add_boximg(_l.img_list)
    output.add_textimg(_r.img_list)
    output.set_txt(txt)
    output.add_origin(pdf_path)
    return output
    # r=output.img2pdf("text")
    # with open("box.pdf","wb") as f:
    #     f.write(r)


def demo(output_path, pdf_st):
    # 输出文字
    r = pdf_st.get_txt()

    # text pdf
    r = pdf_st.img2pdf("text")
    with open(os.path.join(output_path, "text.pdf"), "wb") as f:
        f.write(r)
    # box pdf
    r = pdf_st.img2pdf("box")
    with open(os.path.join(output_path, "box.pdf"), "wb") as f:
        f.write(r)
    # origin_pdf
    r = pdf_st.img2pdf("origin")
    with open(os.path.join(output_path, "origin.pdf"), "wb") as f:
        f.write(r)



if __name__ == "__main__":
    pdf = r"../../pdf/pdf_test/TheLittlePrince.pdf"
    with open(pdf, "rb") as f:
        c = f.read()
    output = pdf2img2rec(c)
    demo('./', output)
