# -*- coding: utf-8 -*-
import requests, sys
from bs4 import BeautifulSoup


class Downloader(object):

    def __init__(self):
        self.server = 'https://www.bqktxt.com/'
        self.target = 'https://www.bqktxt.com/1_1496/'
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节地址
        self.nums = 0  # 章节数

    # 获取下载连接
    def get_download_url(self):
        response = requests.get(url=self.target)
        # 源网页charset=gbk，出现了中文乱码，故指定编码方式
        response.encoding = 'gb18030'
        div_bf = BeautifulSoup(response.text, 'html.parser')
        div_list = div_bf.find('div', class_='listmain')
        a_bf = BeautifulSoup(str(div_list), 'html.parser')
        a_all = a_bf.find_all('a')
        self.nums = len(a_all[12:])  # 去除开头多余的
        for each in a_all[12:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    # 获取章节内容
    @staticmethod
    def get_contents(target):
        response = requests.get(url=target)
        # 指定html解释器
        bf = BeautifulSoup(response.text, 'html.parser')
        # find_all 返回的是数组，text属性提取文本内容，过滤br标签
        # replace： &nbsp（8个） =>  回车
        contents = bf.find('div', id="content").text.replace('\xa0' * 8, '\n\n')
        return contents

    # 讲文章内容写入文件
    @staticmethod
    def write_to_file(name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


# 执行器
def actuator():
    downloader = Downloader()
    downloader.get_download_url()
    print('《斗罗大陆III龙王传说》开始下载：')
    for index in range(downloader.nums):
        downloader.write_to_file(downloader.names[index], '斗罗大陆III龙王传说.txt',
                                 downloader.get_contents(downloader.urls[index]))
        sys.stdout.write('已下载：%.3f%%' % float(index / downloader.nums) + '\r')
        sys.stdout.flush()
    print('《斗罗大陆III龙王传说》下载完成')


if __name__ == '__main__':
    actuator()
