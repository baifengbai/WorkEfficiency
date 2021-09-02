# -*- coding: utf-8 -*-
# @Time    : 9/2/2021 8:36 PM
# @Author  : Chris.Wang
# @Site    : 
# @File    : qiniu_pic_host.py
# @Software: PyCharm
# @Description:将本地图片转为url，使用临时对象存储七牛云（一个月）
import json

import requests
from qiniu import Auth, put_file, etag
from qiniu import BucketManager
from qiniu.auth import RequestsAuth
import qiniu.config

from typing import Any


with open('qiniu_auth.json','r',encoding='UTF-8') as f:
    auth_info = json.load(f)
    if not auth_info:
        exit('load auth_info failed.')

class QnObS():

    def __init__(self,auth_info):
        self.access_key = auth_info['access_key']
        self.secret_key = auth_info['secret_key']

        self.bucket_name = auth_info['bucket_name']
        self.bucket_domain = None

        self.time_out = 3600
        self.q = None


    def connect(self):
        self.q = Auth(self.access_key,self.secret_key)
        self.bucket_domain = self.get_bucket_domain(self.bucket_name)

    # 上传图片
    def update(self,key,localfile,bucket_name='default_bucket') -> (bool,str):
        if bucket_name == 'default_bucket':
            bucket_name = self.bucket_name
        token = self.q.upload_token(bucket_name,key,self.time_out)
        ret, info = put_file(token,key,localfile,version='v1')
        if (ret['key'] == key) and (ret['hash'] == etag(localfile)):
            url = ''
            return True, url
        else:
            url = ''
            return False, url
        
        
    def get_file_info(self,key,bucket_name='default_bucket') -> dict:
        if bucket_name == 'default_bucket':
            bucket_name = self.bucket_name
        bucket = BucketManager(self.q)
        ret,info = bucket.stat(bucket_name,key)
        return ret

    # 请求获取空间信息
    def get_bucket_info(self, bucket_name):
        access_token = self.q.token_of_request(f"https://uc.qbox.me/v2/domains?tbl={bucket_name}")
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': f'QBox {access_token}'
        }
        response = requests.get(f"https://uc.qbox.me/v2/domains?tbl={bucket_name}", headers=headers)
        return response

    def get_bucket_domain(self, bucket_name):
        ret = self.get_bucket_info(bucket_name)
        return json.loads(ret.text)[0]

    def get_key_url(self,key,bucket_name='default_bucket'):
        if bucket_name == "default_bucket":
            bucket_domain = self.bucket_domain
        else:
            bucket_domain = self.get_bucket_domain(bucket_name)

        return f"http://{bucket_domain}/{key}"



# 根据文件目录生成文件路径列表，并且在文件夹内生成excel。


#直接对表格进行操作，生成url



# 对列表进行操作
# localfile to url
def localfile_to_url(lpath) -> str:
    pass


if __name__ == '__main__':
    qos = QnObS(auth_info)
    qos.connect()
    # qos.file_info('test.jpeg',bucket_name=qos.bucket_name)
    # localfile = r"D:\Users\Pictures\8.jpeg"
    print(qos.get_key_url('test3.jpeg'))
