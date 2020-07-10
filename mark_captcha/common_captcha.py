# coding:utf8
import os
import time
import base64
import json
import requests
import platform
import random
from PIL import Image 
from proxy import get_proxy


"""
通过ocr.dll 模型打标签
"""

sysstr = platform.system()
if sysstr == "Windows":
    import ctypes


class CommonCaptcha:
    def __init__(self):
        if sysstr == "Windows":
            self.dll = ctypes.windll.LoadLibrary("ocr.dll")
            self.dll.init()

    def check(self, img):
        if sysstr == "Windows":
            try:
                res = ctypes.string_at(self.dll.ocr(img, len(img))).decode('utf-8')
            except Exception as e:
                print(e)
                res = 'abcd'
        else:
            res = 'abcd'
        return res


    def save_byte(self, name, bs):
        """保存图片"""
        authcode_path = os.path.dirname(__file__) + "/img/"
        suffix = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        path1 = authcode_path + suffix
        filename = path1 + "/" + self.create_name(name)
        if not os.path.exists(path1):
            os.makedirs(path1)
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

    
    def huaxia(self):
        """华夏验证码识别打标"""
        session = requests.session()
        
        headers={
            "Host": "www.ihxlife.com",
            "Connection":"keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        session.get("https://www.baidu.com")
        session.get("http://www.ihxlife.com/login.html", headers=headers, verify=False)

        # 下载验证码s
        getimg_url = "http://www.ihxlife.com/website/server/checkCode/getAuthCode2.do"
        response = session.post(getimg_url, headers=headers)
        rj = json.loads(response.text)
        # 解析验证码地址
        img_url = rj["url"]
        key = rj["key"]
        response_img = session.get(img_url)

        # 识别验证码
        txt = cc.check(response_img.content)[:3]
        # cc.save_byte("test4",response_img.content)
        print(txt)
        # 替换无法识别部位
        code =  int(txt[0]) + int(txt[2])
        print(code)

        # 验证识别
        url1 = "http://www.ihxlife.com/website/server/pcCheckCode/checkVerificationCode.do"
        data = {
            "type": "3",
            "code": str(code),
            "uuid": key
        }
        response = session.post(url1,data=data,headers=headers)
        if "验证码输入正确" in response.text:
            # 保存验证码
            print(response.text)
            self.save_byte("{0}+{1}".format(txt[0],txt[2]),response_img.content)
        else:
            print("error ...")


    def renshou(self):
        session = requests.session()
        phone = "17621972154"
        header = {
            "Host": "ecssmobile.e-chinalife.com:8082",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MTC20L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045310 Mobile Safari/537.36 ECSSMOBILE",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        # 首先获取cookie
        response = session.get("https://ecssmobile.e-chinalife.com:8082/ecss/web/user/vCode/vcode", verify=False)
        rj = json.loads(response.text)
        # verifyImage = "data:image/png;base64,"+rj["data"]["data"]["verifyImage"]
        # 识别验证码
        bs =  rj["data"]["data"]["verifyImage"]
        bs = base64.urlsafe_b64decode(bs + '=' * (4 - len(bs) % 4))
        # yzm = self.captcha_recognize("renshou", rj["data"]["data"]["verifyImage"])
        yzm = self.check(bs)
        data = {"data": {"verifyCode": yzm, "deviceId": "534de2e7cf5b4d23", "mobile": phone, "queryChannel": "mobile"},
                "sn": rj["data"]["sn"]}
        # 忘记密码接口
        resp = session.post(
            url="https://ecssmobile.e-chinalife.com:8082/ecss/web/user/forgetPwd/newQueryRegisterInfos", json=data,
            headers=header, verify=False)
        print(resp.text)
        if "图形验证码输入错误" in resp.text:
            print("eroor")
        elif "此用户信息，请核对后重新输入" in resp.text:
            self.save_byte(yzm, bs)
            print("save img")

    def taikang(self):
        self.session = requests.session()
        phone = "17621972154"
        # 首先获取cookie
        response = self.session.get("http://ecs.tk.cn/eservice/logon/image?now=0.9329707463896919")
        # 识别验证码
        bs = response.content
        yzm = self.check(bs)
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
    
    def mamawang(self):
        proxy = get_proxy()
        session = requests.session()
        header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MTC20L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.117 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "referer": "https://passport.mama.cn/index/forgetPwd",
        }
        response=session.post("https://passport.mama.cn/captcha/getBase64", verify=False, headers=header, proxies=proxy)
        rj = json.loads(response.text)
        bs = rj["data"]["base64"].replace("data:image/png;base64,","")
        bs = base64.urlsafe_b64decode(bs + '=' * (4 - len(bs) % 4))
        yzm = self.check(bs)
        print(yzm)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        data = {
            "account":"17621972154",
            "imgId":yzm    
        }
        response=session.post("https://passport.mama.cn/ajax/checkBind", verify=False, headers=header,data=data,proxies=proxy)
        rj = json.loads(response.text)
        if "验证码错误" in rj["msg"]:
            print("error")
            self.save_byte("error"+yzm,bs)
        elif "用户不存在" in rj["msg"]:
            self.save_byte(yzm,bs)
        print(rj)


cc= CommonCaptcha()
for i in range(100):
    try:
        # cc.huaxia()
        # cc.renshou()
        # cc.taikang()
        cc.mamawang()
    except Exception as e:
        print(e)
        pass
# 本地测试验证码识别
# with open(f'C:\\Workspace\\python\\project\\captcha_download\\下载.png', 'rb') as f:
#     txt = cc.check(f.read())
#     print(txt)







