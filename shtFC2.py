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

# logging配置
logging.basicConfig(level=logging.INFO,
                format=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename= pwd+"\\logs\\"+ time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) +".log",
                filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# 获取主页列表
def getPage(pageNum):
    if(pageNum>5):
        return False
    else:
        logging.info("获取第"+pageNum+"页内容")
        baseUrl = "https://www.sehuatang.org/forum.php?mod=forumdisplay&fid=36&typeid=368&filter=typeid&typeid=368&mobile=2&page="+pageNum
        r = requests.get(baseUrl)
        listPage = BeautifulSoup(r.text, "html5lib")
        ul = listPage.find_all("h1")
        try:
            for li in ul:
                movieTitle = li.a.string
                r1 = requests.get('https://www.sehuatang.org/'+li.a["href"],verify=False)
                detailPage = BeautifulSoup(r1.text, "html5lib")
                imgArr = detailPage.find_all("img",id=re.compile("aimg_"))
                torrnt = detailPage.find("a",id=re.compile("aid"))
                torrentName = torrnt.string
                torrentLink = "https://www.sehuatang.org/"+torrnt['href']
                maglink = detailPage.find("div",class_="blockcode").find('li').string
                for img in imgArr:
                    getImage(movieTitle,img.get('src'),torrentName,torrentLink,maglink)
        except Exception as e:
            logging.warn("爬取失败:"+str(e))
            time.sleep(5)
            getPage(pageNum)
        finally:
            getPage(pageNum+1)

# 下载图片
def getImage(title,url,torrentName,torrentLink,maglink):
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
                logging.info("下载完成：",torrentName.split('.')[0]+"图片"+url.split('/')[-1])
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
                logging.info("下载完成：",torrentName.split('.')[0]+"图片"+url.split('/')[-1])
            else:
                logging.info("文件已存在:")
                logging.info("title:"+title)
                logging.info("图片src:"+url)
        
        try:
            torrentContent = requests.get(torrentLink).content
            print('下载种子'+torrentName+'中')
            logging.info("下载种子"+torrentName+"完成")
            file = open(root+'\\'+torrentName, 'wb')
            file.write(torrentContent)
            file.close()
        except IOError,e:
            print e
    except Exception as e:        
        logging.warn("爬取失败:"+str(e))
        time.sleep(5)
        logging.info("重新爬取")
        getImage(title,url,torrentName,torrentLink,maglink)

def save(filename, content):

    try:
        file = open(filename, 'wb')
        file.write(content)
        file.close()
    except IOError,e:
        print e

def testTorrent():
    url='https://www.sehuatang.org/forum.php?mod=attachment&aid=MjE0MjU2fDYxZTdjOWYxfDE1NjY0ODUzMzN8MHwxNTY2MzM%3D&mobile=2'
    r = requests.get(url)
    logging.info(r.text)
    logging.info(r.content)
    file = open(os.getcwd()+'\\test.torrent', 'wb')
    file.write(r.content)
    file.close()

def callback(num):
    logging.info(num)
    if num==4:
        logging.info('sleep')
        time.sleep(3)
        callback(num+1)
    elif num==6:
        logging.info('end')
    else:
        callback(num+1)

if __name__ == '__main__':
    print('start======================================')
    getImage(1)
    # urls = getPage()
    # for url in urls:
    #     print url
    print('end-----------------------------------------')
