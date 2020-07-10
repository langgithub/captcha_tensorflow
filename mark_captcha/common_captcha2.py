#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# author：yuanlang 
# creat_time: 2020/7/8 下午4:50
# file: common_captcha2.py

import pytesseract
from PIL import Image

"""
通过testocr识别打标签
"""
# open image
image = Image.open('yunyu.png')
code = pytesseract.image_to_string(image, lang='chi_sim')
print(code)