#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# author：yuanlang 
# creat_time: 2020/7/10 上午11:09
# file: common_captcha3.py

import io
import os
import time
import base64
import random
import requests
from PIL import Image
from cnnlib.recognition_object import Recognizer


class VerifyHelper(object):
    __model_dict = {}

    def __init__(self):
        self.__model_dict["taikang"] = self.__taikang()

    def __taikang(self):
        image_height = 30
        image_width = 105
        max_captcha = 5
        char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
        model_save_dir = os.path.dirname(os.path.dirname(__file__))+"/cnn_captcha/model/"
        return Recognizer(image_height, image_width, max_captcha, char_set, model_save_dir)

    def verify_captcha(self, key, r_img):
        r_img = Image.open(io.BytesIO(r_img))
        t = self.__model_dict[key].rec_image(r_img)
        return t


vh = VerifyHelper()


class MarkCaptcha(object):

    def __init__(self):
        self.session = requests.session()

    def save_byte(self, name, bs):
        """保存图片"""
        authcode_path = os.path.dirname(os.path.dirname(__file__)) + "/cnn_captcha/sample/train"
        filename = authcode_path + "/" + self.create_name(name)
        if not os.path.exists(authcode_path):
            os.makedirs(authcode_path)
        if type(bs) == str:
            bs = base64.urlsafe_b64decode(bs + '=' * (4 - len(bs) % 4))
        with open(filename, "wb") as f:
            f.write(bs)
        return filename

    @staticmethod
    def create_name(captcha):
        ran = str(random.random()).split('.')[-1]
        name = '{}_{}.jpeg'.format(captcha, ran)
        return name

    def taikang(self):
        phone = "17621972154"
        # 首先获取cookie
        response = self.session.get("http://ecs.tk.cn/eservice/logon/image?now=0.9329707463896919")
        # 识别验证码
        bs = response.content
        yzm = vh.verify_captcha("taikang", bs)
        data = {
            "function_code": "checkMark",
            "check_type_key": "checkMember_username",
            "username": phone,
            "mark": yzm
        }

        # 泰康忘记密码接口
        header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MTC20L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.117 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        resp = self.session.post(url="http://ecs.tk.cn/eservice/change/service", data=data, headers=header)
        print(resp.text)
        if "验证码不正确" in resp.text:
            print("error")
        elif "登录名不存在" in resp.text:
            self.save_byte(yzm, bs)


def run():
    mc = MarkCaptcha()
    for i in range(20000):
        mc.taikang()


if __name__ == '__main__':
    run()
