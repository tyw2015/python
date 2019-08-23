#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-13 09:59:30
# @Author  : $Name$
# @Link    : ${link}
# @Version : $Id$

import os
import requests
import urllib
from urllib import unquote

from pyquery import PyQuery as pq
import time
import re
import traceback
import logging

pwd = '/Users/tyw/Desktop/python1'

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename= pwd+'/test.log',
                filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# post 发帖 
# def tieba_post(fid,tid,url,say,tname):

# 	referer = 'https://tieba.baidu.com/p/'+str(tid)

# 	content = "ie=utf-8&kw="+tname+"&fid="+str(fid)+"&tid="+str(tid)+"&vcode_md5=&floor_num=104&rich_text=1&tbs=7a6530b6e74ea97f1513070221&"+say+"&basilisk=1&files=%5B%5D&mouse_pwd=25%2C24%2C26%2C1%2C28%2C30%2C28%2C26%2C26%2C36%2C29%2C1%2C28%2C1%2C29%2C1%2C28%2C1%2C29%2C1%2C28%2C1%2C29%2C1%2C28%2C1%2C29%2C36%2C24%2C21%2C30%2C31%2C36%2C28%2C31%2C21%2C29%2C1%2C21%2C29%2C29%2C15130702232450&mouse_pwd_t=1513070223245&mouse_pwd_isclick=0&__type__=reply&_BSK=JVwWV2cLBlsqBkcSBD8FUQ0CaTU2UAcbWCIEUzYZJTw%2BQzVDVTslEBBAcSQBQUxFPkExUBEnFDc%2FDAQNMR1LWyAbVi1NOBlARgsgOT1RHRtdIQhVIFFqPD5TMRtaJipREVw%2BIglIRB1lRy1dGTlWazAfDAZpWU1YMRpBJk0gGVMLEyw4NEcURRIgAkgwVycifUA1HUAmKhwZUTwlSF5JGyZEM1YfIktlclwMUmcLBkkkBlozCD8dbwsrM2cwQlcbHCNVBH8VMiIkVXxNRHhmR1d9CBsoDwZLLBl9Dl5iCHZpTlRSdB0GSnZXCX8HLRpDD0tnImsHTxVzIh1PKVknf2QeYE8bBCUeHF0pOBdFEUkARitREnB1Jj1eLjBlaQQadSoCbD59XxArFzU7P3IQVXUkEwlwBnF%2BYgZwR3gBEDA5H307DUZPSQ5NPF8ReRgENgwODiAeEhlrRR1sU3xEHlNTZQQ7QxRFV2JSFXIbdWZzHHIDAmt%2BXw9bcBQqDwZLOht9Dl4kSjI7UkMXdBMeCSMAXTwVJRleShMqBC5XHFlZZU4GPhUdPjBEORlWaScSEVYAdxkPBksoHH0OXjZZKy0bTUEmAAYRZQFBKgRgVF5ZRX93aBVEAA54VhdpFzVhcwpwVwN5aF8CAH9tREtLBTpNcxYQYRp9fkxRUnIBERp0WREvUm5MEAwGKSQ%2FCVdFD29dBCNAKDMlWT8BEzslExFcMH9NDVFJEkY%2BQBcmXWc9EQUGGBFZCWlXWm5DdlZEGBIge3hSRxUEbylzCXlkfHNRYk0JaXNMQx9%2FO1YPEEk9WipRUnJIdXxEQy4kUm1FMRBffU1uAgJIXWVmbxRGBwl9VRBzGWQjYxJqTwJ7fE1ZETxmRhcKWHsQbxhcIAllZFxEVAcUFhkxF0B6U35TAytCd2VtREMCDX0FECACcjUwCWcJAnx1TkUEbWVWHA9bew1ocFx8GiNvXFtBC2RoZ2cI"
# 	headers = {'Host':'tieba.baidu.com','Origin': 'https://tieba.baidu.com','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
# 	'Referer': referer,'Cookie':"TIEBA_USERTYPE=d628139f1378d8153cdb6705; FP_UID=6e3656cef26cdb188fe7b00e51784d90; BDUSS=nRaaWsxVWJlOVl3aDh1Y1lDMmROQUc2UVB4MUJlR0ZadERTSzM1RklCektKbGRhQUFBQUFBJCQAAAAAAAAAAAEAAAC~qThyd2RqY21saWxpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMqZL1rKmS9ab; TIEBAUID=eaa5821fef746478e8f74eed; STOKEN=0cdef7ce09d5bbfa375647bae1e6e953f9820b91b4aec2619f72267ca36d0b35; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1513068963; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1513070092; BAIDUID=4E9FC22B9D90443E55F43158AD1775DC:FG=1; wise_device=0"
# 	}

# 	r = requests.post(url =url ,headers= headers,data = content)

# 	return r

def tieba_tids(url):

	# 得到贴吧fid
	p = re.compile(r'PageData\.forum = {(.*?),',re.S)
	script = pq(url)('script')
	fid = re.findall(p,script.text())[0].split(':')[1].strip()

	p = pq(url)('ul')
	ties = p.filter('#thread_list')('li')
	tids = []
	for i in range(len(ties)):
		if ties.eq(i).attr('data-field') != None:
			tids.append(ties.eq(i)('a').attr('href').split('/')[2].split('?')[0])


	return fid,tids

def emmmm(url,timesleep,say):
	
	logging.info(url)
	post_url = 'https://tieba.baidu.com/f/commit/post/add'
	try:
		fid,tids = tieba_tids(url)
		logging.info("Fid: "+fid+" GET!"+ " TIDS:"+ tids[0])
	except Exception, e:
		logging.warning('URL: '+url+" CAN'T GET TIDS AND FID. TRACE_BACK:"+str(traceback.print_exc()))
		return 

	try:
		tname = url.split('kw=')[1].split('&')[0]
		logging.info("TNAME: "+tname+" GET!")
	except Exception, e:
		logging.warning('URL: '+url+" CAN'T GET TNAME. TRACE_BACK:"+str(traceback.print_exc()))
		tname = '%E5%89%91%E7%BD%913'

	# 记录tid/fid写文件，并去除曾经水过的帖子
	with open(pwd+unquote(tname), 'a+') as f:
		f.seek(0)
		used_tids = [i.strip() for i in f.readlines()]
		tmp_tids = [i for i in tids if i not in used_tids]
		tids = tmp_tids
		f.write('\n'.join(tids)+'\n')

	for tid in tids:
		try:
			tieba_post(fid = fid,tid = tid,url = post_url,say = say,tname = tname)
			logging.info("TID: "+tid+" DONE!")
		except Exception, e:
			logging.warning("TID: "+tid+" POST ERROR! TRACE_BACK:"+str(traceback.print_exc()))
		time.sleep(timesleep)
	logging.info("DONE:"+url)
	return 


say = []
say.append(urllib.urlencode({'content': u'咩萝李大米！认识吗！对！就是咩萝李大米！'.encode('utf8')}))
say.append(urllib.urlencode({'content': u'这里是一只咩萝在给你顶帖，好了我走了。'.encode('utf8')}))
say.append(urllib.urlencode({'content': u'凉凉夜色为你削弱成河～～～没有毫针再呵护我～～~'.encode('utf8')}))
say.append(urllib.urlencode({'content': u'李大米看了你的帖子并打了个吼呵～'.encode('utf8')}))
say.append(urllib.urlencode({'content': u'在我的行天道里，我和我的剑魂都会保护你。所以你在哪里？'.encode('utf8')}))
say.append(urllib.urlencode({'content': u'如果我们活出了体服，万水千山，你愿意陪我一起看吗？'.encode('utf8')}))
say.append(urllib.urlencode({'content': u'乖，别难过，我下行天道抓大师给你玩儿好不好？'.encode('utf8')}))
say.append(urllib.urlencode({'content': u'什么？你说我还在这行天道里等谁？我谁也没等，谁也不会来。'.encode('utf8')}))
'''
kanglong = 'https://tieba.baidu.com/f?kw=%E4%BA%A2%E9%BE%99%E6%9C%89%E6%82%94&ie=utf-8&pn=50'
weimanxia = 'https://tieba.baidu.com/f?kw=%E5%94%AF%E6%BB%A1%E4%BE%A0&ie=utf-8&pn=50'
'''
url = "https://tieba.baidu.com/f?kw=剑网三交易"
emmmm(url+'&ie=utf-8&pn=50',timesleep = 30,say = say[7])

'''
emmmm(url = weimanxia,timesleep = 30,say= say[2])
emmmm(url = kanglong,timesleep = 30,say = say[0])
'''
