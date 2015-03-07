#!/usr/env/bin python
#! _*_ coding:utf-8 _*_

import string, urllib2
import re
import os
import os.path
import uuid

# http://s4.sinaimg.cn/middle/488fb2eatb6550a3fc273&690 > http://s4.sinaimg.cn/orignal/488fb2eatb6550a3fc273&690

blog_url = "http://blog.sina.com.cn/u/1217377002"

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	'Referer':'http://blog.sina.com.cn'
}

image_path = os.getcwd() + "/sina_blog_pic/"

def GetHtmlByUrl(url):
	request = urllib2.Request(url, headers = headers)
	response = urllib2.urlopen(request, timeout = 10)
	return response.read()

def GetBlogDetailHtmlByUrl(url):
	html = GetHtmlByUrl(url)

	m = re.search('<div.*?class="articalTitle">.*?<h2.*?class="titName SG_txta">(.*?)</h2>.*?</div>', html, re.S)

	if m:
		title = m.group(1)
		print 'Begin get blog:' + title
		picDir = image_path + title
		if not os.path.exists(picDir):
			os.makedirs(picDir)
		GetBlogPicsByUrl(html, picDir)


def GetBlogPicsByUrl(html, picDir):
	picItem = re.findall('<a.*?HREF="(.*?)".*?>.*?<img.*?src=".*?".*?real_src =".*?".*?WIDTH="690".*?HEIGHT=".*?".*?NAME=".*?".*?/></a>', html, re.I)
	for picUrl in picItem:
		print 'pirUrl:' + picUrl
		urlItem = re.findall('.*?photo.blog.sina.com.cn/showpic.html.*?&url=(.*)', picUrl, re.S)
		for url in urlItem:
			print 'Begin save picture:' + url
			SavePic(url, picDir)

def SavePic(picUrl, picDir):
	picFile = picDir + '/' + UniqueStr() + '.jpg'
	print 'picFile:' + picFile
	f = open(picFile, 'w+')
	try:
		f.write(urllib2.urlopen(picUrl).read())
	except:
		print 'Get picture faild:' + picUrl
	f.close()

def UniqueStr():
	return str(uuid.uuid1())

def GetBlogDetailByPage():
	html = GetHtmlByUrl(blog_url)

	detailPageItems = re.findall('<div.*?class="more">.*?<span.*?class="SG_more">.*?<a.*?href="(.*?)".*?target="_blank">查看全文</a>.*?</span>.*?</div>', html, re.S)
	
	for detailUrl in detailPageItems:
		GetBlogDetailHtmlByUrl(detailUrl)

GetBlogDetailByPage()