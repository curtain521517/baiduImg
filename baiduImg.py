#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib2
import requests
import re

# "objURL":"http://img.taopic.com/uploads/allimg/121107/240508-12110H3412737.jpg",

	# 保存图片
def save_to_file(pic,filename):
	fp = open(filename, 'wb')
	fp.write(pic.content)
	fp.close()
    # print "保存图片成功!"

def getHtml(url):
    #print("正在打开网页并获取....")
    request = urllib2.Request(url)
    page=urllib2.urlopen(request)

    Html=str(page.read())
    print("成功获取....")
    return Html

def getImg(html):
    img_re=re.compile(r'"objURL":"(.*?)"')
    img_list=re.findall(img_re, html)
    print '共有%d张图片待下载' % len(img_list)

    current = 0;
    for i in range(len(img_list)):
        try:
        	current = current + 1
        	img= requests.get(img_list[i], timeout = 10)
        	print '正在下载第%d张图片:%s' % (i,img_list[i])
        except requests.exceptions.ConnectionError as e:
        	print '无法下载第%d张图片:%s' % (i,img_list[i])
        	current = current - 1
        	continue
        except requests.exceptions.TooManyRedirects as e:
			print '无法下载第%d张图片:%s' % (i,img_list[i])
        	# current = current - 1
        	# continue
        finally:
        	# print '无法下载第%d张图片:%s' % (i,img_list[i])
        	# current = current - 1;
        	# continue
        	pass
        filename = 'pic/'+str(current) + '.jpg'
        save_to_file(img,filename)
    print("完成图片下载......")
    print("一共下载了%d张图片" % current)


# 生成请求链接
def getUrlFromConfig(url,word,pagenumber):
	urlString = '';
	# word = '臭肥猫';
	data = {
		'tn':'baiduimage',
		'ie':'utf-8',
		'word':str(word),
		'pn':pagenumber * 20, # 翻页加20
		'gsm':'8c',
		'ct':'',
		'ic':0,
		'lm':-1,
		'width':0,
		'height':0,
	}

	param = [];
	for key in data:
		item = key+'='+str(data[key])
		param.append(item)

	string = '&'.join(param)
	urlString  = url + string;
	return urlString

if __name__=="__main__":
	# 配置
	url = 'https://image.baidu.com/search/flip?'

	html=getHtml(getUrlFromConfig(url,'臭肥猫',1))
	getImg(html)
