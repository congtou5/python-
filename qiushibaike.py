# -*-coding:utf8-*-
# !/usr/bin/env python

# import urllib.request
# import urllib.error
from urllib import request, error
import re
import time


# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


# 糗事百科的爬虫
class qiushibaike():
    def __init__(self):
        self.page = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (' \
                          'KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        # self.stories = []  # 存放段子内容
        self.enable = False  # 存放程序是否继续运行的变量

    # 将距1970年1月1日的秒数转成可读的时间格式
    def format_time(self, second):
        timeArray = time.localtime(second)
        styleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return styleTime

    # 传入页码，得到页面代码
    def get_page(self, page):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(page)
            req = request.Request(url, headers=self.headers)
            response = request.urlopen(req)
            html = response.read().decode('utf-8', 'ignore')  # 加了ignore才能显示第3页后的内容，why？
            return html
        except error as e:
            print(u'连接糗事百科失败，请检查')

    # 传入页面代码，得到本页不带图片的段子列表
    def get_items(self, page):
        html = self.get_page(page)
        if not html:
            print(u'页面加载失败')
        pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?content">(.*?)<'
                             '!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
        items = re.findall(pattern, html)
        page_stories = []
        for item in items:
            time_ = self.format_time(int(item[2]))
            haveimg = re.search("img", item[3])
            # 判断是否含有图片，若有则删去
            if not haveimg:
                replace_a = re.compile(r'\n')
                auth = re.sub(replace_a, '', item[0])
                replace_b = re.compile('<br/>')
                duanzi = re.sub(replace_b, r'\n', item[1])
                # item[0]:段子手，item[1]:段子，item[2]:发布时间，item[4]:点赞数
                story = [auth.strip(), duanzi.strip(), time_, item[4]]
                page_stories.append(story)
        return page_stories

    # 每次敲回车打印一个段子
    def get_one_story(self, pagestories, page):
        # 遍历一页的段子
        for story in pagestories:
            input_ = input()  # 等待用户输入
            # 如果输入s则结束
            if input_ is 's':
                self.enable = False
                return
            print('第%d页\t发布人：%s\t发布时间：%s\t点赞数：%s\n%s' % (page, story[0], story[2], story[3], story[1]))

    # 开始运行程序
    def start(self):
        print(u'正在爬取糗事百科段子，按回车键查看新段子，按s键结束退出')
        self.enable = True  # 令enable值为True，使程序运行
        # self.load_page()  # 加载一页内容
        now_page = 1  # 当前页
        while self.enable is True:
            pagestories = self.get_items(now_page)
            self.get_one_story(pagestories, now_page)  # 输出该页的段子
            now_page += 1  # 页数加1


if __name__ == '__main__':
    qsbk = qiushibaike()
    qsbk.start()
