# -*- coding: utf-8 -*-
import os
import time
from contextlib import closing

import json
import requests


class PhotoSpider(object):

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.download_url = []
        self.per_page = 12
        self.page = 1
        self.target = 'https://unsplash.com/napi/photos'
        self.loadAll = False

    # 获取图片下载链接
    def get_download_url(self):
        payload = {
            'per_page': self.per_page,
            'page': self.page
        }
        response = requests.get(self.target, params=payload, headers=self.headers, timeout=10)
        resource = json.loads(response.text)
        for item in resource:
            self.download_url.append(item['links']['download'])

    # 依次获取前n页数据
    def poll(self, page):
        while self.page <= page:
            self.get_download_url()
            self.page += 1
            time.sleep(1)
        self.loadAll = True

    # 下载图片
    def download_picture(self, target, filename):
        project_dir = os.path.abspath(os.path.dirname('.'))
        image_dir = os.path.join(project_dir, 'images', '%d.jpg' % filename)
        with closing(requests.get(url=target, stream=True, headers=self.headers)) as r:
            with open(image_dir, 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()


def actuator():
    photo_spider = PhotoSpider()
    print('开始获取图片下载链接...')
    photo_spider.poll(6)
    if not photo_spider.loadAll:
        return
    print('开始下载图片...')
    for i in range(len(photo_spider.download_url)):
        print('正在下载第%d张图片' % (i + 1))
        photo_spider.download_picture(photo_spider.download_url[i], (i + 1))
    print('图片下载完成！')


if __name__ == "__main__":
    actuator()
