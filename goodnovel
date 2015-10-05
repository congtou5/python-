__author__ = 'congtou5'
# -*-coding:utf8-*-
# !/usr/bin/env python
'''本程序用来爬取龙枪虎豹骑吧的《110本好书推荐（重发》帖子
   version python3.4.3'''
from urllib import request
import re


# 工具类，处理页面标签
class tool():
    remove_img = re.compile('<img.*?>')  # 删除图片标签
    remove_ahref = re.compile('<a href.*?>|</a>')  # 删除超链接
    remove_other = re.compile(r'\[url]http://|\[/url]')  # 删除[url]http://和[/url]
    replace_br = re.compile('(<br>)+')  # 换行符<br>替换为\n
    remove_extra_tag = re.compile('<.*?>')  # 删除其他标签

    def replace(self, x):
        x = re.sub(self.remove_img, '', x)
        x = re.sub(self.remove_ahref, '', x)
        x = re.sub(self.remove_other, '', x)
        x = re.sub(self.replace_br, r'\n', x)
        x = re.sub(self.remove_extra_tag, '', x)
        return x.strip()


class good_novel():
    # 初始化
    def __init__(self, baseurl, seelz, floor_tag):
        self.baseurl = baseurl  # 基本地址，如：http://tieba.baidu.com/p/3587623045/
        self.see_lz = '?see_lz=' + str(seelz)  # 是否只看楼主
        self.tool = tool()
        self.file = None  # 文件标示符
        self.floor = 1
        self.floor_tag = floor_tag  # 写入时是否添加楼层标签

    # 传入页码，获取该页代码
    def get_page_html(self, page_num):
        try:
            url = self.baseurl + self.see_lz + '&pn=' + str(page_num)
            req = request.Request(url)
            response = request.urlopen(req)
            html = response.read()
            return html
        except:
            print(u'连接百度贴吧失败，请检查')
            return None

    # 获取帖子标题
    def get_title(self, page_html):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page_html)
        if result:
            # print(result.group(1))
            return result.group(1)
        else:
            return None

    # 获取帖子共有多少页
    def get_total_page_num(self, page_html):
        pattern = re.compile('<li class="l_reply_num".*?<span class="red">(.*?)</span>', re.S)
        pages = re.search(pattern, page_html)
        if pages:
            # print(pages.group(1))
            return pages.group(1).strip()
        else:
            return None

    # 获取帖子内容
    def get_content(self, page_html):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page_html)
        contents = []
        for item in items:
            content = self.tool.replace(item) + '\n'  # 处理各楼内容
            contents.append(content)
        return contents

    # 得写入文件标题
    def set_file_title(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(u'百度贴吧' + '.txt', 'w+')

    # 将帖子内容写入txt文件
    def write_file(self, contents):
        for content in contents:
            # 判断是否写入楼层
            if self.floor_tag == '1':
                floor_line = '\n---------------' + str(self.floor) + u'楼---------------\n'
                self.file.write(floor_line)
            self.file.write(content)
            self.floor += 1

    # 程序开始
    def start(self):
        html = self.get_page_html(1)  # 载入第一页
        page_html = html.decode('utf-8')  # 得到第一页的代码
        page_num = self.get_total_page_num(page_html)  # 得到总页数
        title = self.get_title(page_html)  # 获取帖子标题
        self.set_file_title(title)
        if page_num is None:
            print(u'URL已失效，请检查')
            return
        try:
            print(u'该帖子共有' + page_num + '页')
            for i in range(1, int(page_num) + 1):
                print(u'正在写入第' + str(i) + u'页内容')
                html = self.get_page_html(i)
                page_html = html.decode('utf-8')
                contents = self.get_content(page_html)
                self.write_file(contents)
        except:
            print(u'写入内容时出现异常，请检查')
        finally:
            print(u'写入成功！')


if __name__ == '__main__':
    print(u'请输入百度贴吧的一个帖子地址，如：http://tieba.baidu.com/p/3587623045/')
    baseurl = input()  # 'http://tieba.baidu.com/p/3587623045/'
    seelz = input(u'是否只看楼主，是则输入1，否则输入0：\n')
    floor_tag = input(u'是否写入楼层信息，是则输入1，否则输入0：\n')
    goodnovel = good_novel(baseurl, seelz, floor_tag)
    goodnovel.start()
