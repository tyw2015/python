#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re
import time
import traceback
import urllib2
import os
import requests
from bs4 import BeautifulSoup
import sys
import gzip
from io import BytesIO
reload(sys) 
sys.setdefaultencoding('utf-8')
pwd = os.getcwd()

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename= pwd+"\\logs\\"+ time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) +".log",
                filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# 获取主页列表
def getPage():
    baseUrl = 'https://www.sehuatang.org/forum.php?mod=forumdisplay&fid=36&typeid=368&filter=typeid&typeid=368&mobile=2&page=5'
    r = requests.get(baseUrl)
    listPage = BeautifulSoup(r.text, "html5lib")
    ul = listPage.find_all("h1")
    urls = []
    for li in ul:
        logging.info(li.a["href"])
        movieTitle = li.a.string
        r1 = requests.get('https://www.sehuatang.org/'+li.a["href"],verify=False)
        detailPage = BeautifulSoup(r1.text, "html5lib")
        imgArr = detailPage.find_all("img",id=re.compile("aimg_"))
        maglink = detailPage.find("div",class_="blockcode").find('li').string
        for img in imgArr:
            getImage(movieTitle,img.get('src'),maglink)
    return urls

# 下载图片
def getImage(title,url,maglink):
    # url ="https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/bd_logo1_31bdc765.png"
    root = os.getcwd()+'\\'+title
    path = os.getcwd() + '\\'+title+'\\' + url.split('/')[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
            if not os.path.exists(path):
                r = requests.get(url)
                r.raise_for_status()
                with open(path, "wb") as f:
                    f.write(r.content)
                print('爬取'+url+'中')
                logging.info("爬取完成")
            else:
                logging.info("文件已存在:")
                logging.info("title:"+title)
                logging.info("图片src:"+url)
        else:
            if not os.path.exists(path):
                r = requests.get(url)
                r.raise_for_status()
                with open(path, "wb") as f:
                    f.write(r.content)
                print('爬取'+url+'中')
                logging.info("爬取完成")
            else:
                logging.info("文件已存在:")
                logging.info("title:"+title)
                logging.info("图片src:"+url)
        if os.path.exists(root+'\\'+'link.txt'):
            os.rmdir(root+'\\'+'link.txt' )
        else:
            print(1)
        try:
            file = open(root+'\\'+'link.txt', 'wb')
            file.write(maglink)
            file.close()
        except IOError,e:
            print e
    except Exception as e:
        logging.warn("爬取失败:"+str(e))


def test():
    url = 'https://www.sehuatang.org/forum.php?mod=viewthread&tid=156633&extra=page=2&filter=typeid&typeid=368&mobile=2'
    href="https://www.sehuatang.org/orum.php?mod=attachment&aid=MjE0MjU2fDdjNzc2OTY1fDE1NjY0ODE2NDB8MHwxNTY2MzM%3D&mobile=2"
    r = requests.get(url)
    html = BeautifulSoup(r.text, "html5lib")
    imgArr = html.find_all("img",id=re.compile("aimg_"))
    torrentLink = html.find("div",class_="blockcode").find('li')
    print(torrentLink.string)
    torrent = requests.get(href)
    os.mkdir(os.getcwd()+"\\torrents\\")
    os.mkdir(os.getcwd()+"\\torrents\\"+"123.torrent")
    f=open(os.getcwd()+"\\torrents\\"+"123.torrent",'wb')
    f.write(torrent.content)
    # buffer = BytesIO(torrent.read())
    # gz = gzip.GzipFile(fileobj=buffer)
    # raw_data=gz.read()
    # save(os.getcwd()+".\\torrents\\"+"123.torrent",raw_data)
    # for img in imgArr:
    #     print(img.get('title'))
    #     getImage('123123',img.get('src'))
    #     time.sleep(2)

def save(filename, content):

    try:
        file = open(filename, 'wb')
        file.write(content)
        file.close()
    except IOError,e:
        print e

if __name__ == '__main__':
    print('start======================================')
    getPage()
    # urls = getPage()
    # for url in urls:
    #     print url
    print('end-----------------------------------------')
