#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# author：yuanlang 
# creat_time: 2020/7/9 下午6:31
# file: image_update.py

import os
from PIL import Image


class ImageUpdate(object):

    def __init__(self):
        pass

    def resize_img(self, o_path, a_path):
        imgs = os.listdir(o_path)
        if not os.path.exists(o_path): return
        if not os.path.exists(a_path): os.mkdir(a_path)
        for name in imgs:
            img_path = o_path+"/"+name
            img = Image.open(img_path)
            print(img.size)
            if img.mode == "P" or img.mode == "RGBA":
                img = img.convert('RGB')
            cropped = img.crop((0, 0, 119, 50))  # (left, upper, right, lower)
            cropped.save(a_path+"/"+name)


i = ImageUpdate()
i.resize_img("/Users/yuanlang/Downloads/mmw", "/Users/yuanlang/Downloads/mmw_a")