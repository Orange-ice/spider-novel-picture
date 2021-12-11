import time, datetime
import requests
from bs4 import BeautifulSoup

host = 's.weibo.com'


def crawl():
    """
    爬虫模块
    :return: 网页源码
    """

    url = "https://s.weibo.com/top/summary?cate=realtimehot"

    headers = {
        'Host': host,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://weibo.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }

    cookies = "SUB=_2AkMW7nF1f8NxqwJRmPAcym3rao5zygrEieKgsoCuJRMxHRl-yT9jqktatRB6PW5fmkhDxUAfAVsxxwKE5AcDH-EUI-GV; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhLc0uzpFC8o_P1QQmHpe8y; _s_tentry=passport.weibo.com; Apache=6311233265531.729.1639120451861; SINAGLOBAL=6311233265531.729.1639120451861; ULV=1639120451872:1:1:1:6311233265531.729.1639120451861:"  # 获取一个cookie
    cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

    try:
        response = requests.get(url, headers=headers, timeout=10, cookies=cookies)
        return response.text
    except BaseException:
        print('error', '获取热搜数据失败！')
        return 0


def data_processing(response):
    tr_bs4 = BeautifulSoup(response, 'html.parser').find_all('tr')

    hot_list = []

    for i in range(len(tr_bs4)):
        # 去除第一项 （第一项是title【序号，关键字】]）
        if i == 0: continue
        # 全部内容（例：['', '38', '', '冬日懒人版小酥肉', ' 168576', '', '新', '']）
        contents = tr_bs4[i].text.split('\n')

        link = host + tr_bs4[i].a['href']  # 链接
        ranking = contents[1]  # 排名
        title = contents[3]  # 标题
        hot_num = contents[4]  # 热度值
        mark = contents[-2]  # 标记（新/热/爆）

        if ranking != '•':
            if ranking == '':
                ranking = 0
            else:
                ranking = int(ranking)
            hot_item = {ranking, title, hot_num, mark, link}
            hot_list.append(hot_item)

    # print(hot_list)
    current_hour = time.localtime().tm_hour  # 当前小时
    local_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()  # UTC 时间
    print(current_hour, local_time)


if __name__ == '__main__':
    data_processing(crawl())
