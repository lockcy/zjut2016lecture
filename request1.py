#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @auther : lockcy

import requests
import time
from urllib.parse import urlencode
from PIL import Image
import os
from hashlib import md5

class WenJuanXing(object):

    submit_headers = {
        # 'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded;',
        # 'cookie': '.ASPXANONYMOUS=weSCc8wu1AEkAAAANjE3MGMxZGItNDQ5OC00YWI3LTkxZGEtNmVkNTY5MzU5OTdlVi6pfvz50MfKv5R7T8xKFWe2LqE1; UM_distinctid=163b2116ddfbbc-048109171a2d4f-737356c-144000-163b2116de07fd; jac24389107=04539338; CNZZDATA4478442=cnzz_eid%3D1533293032-1527696898-%26ntime%3D1527730790; Hm_lvt_21be24c80829bd7a683b2c536fcf520b=1527700877,1527732232; Hm_lpvt_21be24c80829bd7a683b2c536fcf520b=1527732232',
        'origin': 'https://www.wjx.cn',
        'referer': 'https://www.wjx.cn/m/24389107.aspx',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    def __init__(self, q_num, q_data):
        self.base_url = 'https://www.wjx.cn/jq/%s.aspx'
        self.base_submit = 'https://www.wjx.cn/handler/processjq.ashx?'
        self.base_spam = 'https://www.wjx.cn/AntiSpamImageGen.aspx?'
        self.sess = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.curID = q_num
        self.submitdata = q_data
        self.submittype = '1'
        self.t = str(int(time.time() * 1000))
        self.starttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        self.html = ''
        self.validate_text = ''
        self.rn = 0

    def getHtml(self):
        response = self.sess.get(self.base_url % self.curID)
        self.html = response.text

    def getRandNum(self):
        self.rn = 0
        self.getHtml()
        rnd_part = self.html[self.html.find('rndnum=') + 8:]
        self.rn = rnd_part[:rnd_part.find('"')]

    def stringParams(self):
        return {
            'submittype': self.submittype,
            'curID': self.curID,
            't': self.t,
            'starttime':self.starttime,
            'rn': self.rn,
            'validate_text': self.validate_text
        }

    def antiSpam(self):
        url = self.base_spam + urlencode({'t': self.t, 'q': self.curID})
        response = self.sess.get(url)
        with open('tmp_img.gif', 'wb') as f:
            f.write(response.content)
        # TODO: try captcha solver
        Image.open('tmp_img.gif').convert('RGB').save('tmp_img.jpg')
        self.validate_text = get_code_text('tmp_img.jpg', response.content)
        os.remove('tmp_img.gif')
        os.remove('tmp_img.jpg')
        print(self.validate_text)

    def submitForm(self):
        url = self.base_submit + urlencode(self.stringParams())
        response = self.sess.post(url, data={'submitdata': self.submitdata}, headers=self.submit_headers)
        return response

    def resetData(self):
        self.getRandNum()
        self.t = str(int(time.time() * 1000))
        self.starttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        self.sess.cookies.clear()


def main():
    path=r'C:\Users\admin\Desktop\jiangzuo\awesome\plugins\re.txt'
    size = os.path.getsize(path)
    while size==0:
        size = os.path.getsize(path)
        continue
    with open (path,'r') as f:
        a=f.readline()
        print (a)
    f.close()
    q_num = a

    #添加参数
    q_data = ['1$abc}2$2016xxxx}3$158xxxx']

    #根据参数数量进行多次添加
    iter = len(q_data)
    for i in range(iter):
        wjx = WenJuanXing(q_num, q_data[i])
        wjx.resetData()
        wjx.antiSpam()
        response = wjx.submitForm()
        print(response.content.decode('UTF-8'))

def get_code_text(file_name, content):
    """
    获取验证码
    :param file_name: 验证码本地图片的路径
    :param img_type: 要识别的验证码类型
    :return: 识别后的验证码
    """
    headers = {
        'Connection': 'Keep-Alive',
        'Expect': '100-continue',
        'User-Agent': 'ben',
    }
#将下面的username和password替换为自己在该平台的账号密码
    params = {
        'username': 'username',
        'password': md5('password'.encode('utf8')).hexdigest(),
        'softid': '80032',
        'softkey': 'xxx',
        'typeid': 3040,
        'timeout': 30,
    }
    files = {'image': (file_name, content)}
    res = requests.post('http://api.ruokuai.com/create.json', data=params,
                        files=files, headers=headers)
    return res.json()['Result']


if __name__ == '__main__':
    main()