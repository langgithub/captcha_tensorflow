#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# author：yuanlang 
# creat_time: 2020/7/8 上午10:18
# file: tx_train.py

import io
import os
from PIL import Image
from cnnlib.recognition_object import Recognizer

image_height = 30
image_width = 105
max_captcha = 5
char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
model_save_dir = os.path.dirname(os.path.dirname(__file__))+"/model/"
R = Recognizer(image_height, image_width, max_captcha, char_set, model_save_dir)


def verify_captcha(r_img):
    r_img = Image.open(io.BytesIO(r_img))
    t = R.rec_image(r_img)
    return t


def run():
    with open(f'/Users/yuanlang/work/python/project/captcha_tensorflow/cnn_captcha/sample/test/2auwv_1315774186590738.jpeg', 'rb') as f:
        print(verify_captcha(f.read()))


if __name__ == '__main__':
    run()
