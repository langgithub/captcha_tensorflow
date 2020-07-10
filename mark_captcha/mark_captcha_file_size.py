#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# author：yuanlang 
# creat_time: 2020/7/10 上午11:31
# file: mark_captcha_file_size.py


import os

authcode_path = os.path.dirname(os.path.dirname(__file__)) + "/cnn_captcha/sample/train"
l = os.listdir(authcode_path)
print(len(l))