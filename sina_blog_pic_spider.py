#!/usr/env/bin python
#! _*_ coding:utf-8 _*_

import string, urllib2
import re
import os
import os.path
import uuid
import sys
import math
import datetime

uid = "1217377002"

blog_url = "http://blog.sina.com.cn/u/" + uid


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	'Referer':'http://blog.sina.com.cn',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

image_path = os.getcwd() + "/sina_blog_pic/"

def GetNextPageUrl(num):
	return "http://blog.sina.com.cn/s/article_sort_" + uid + "_10001_" + str(num) + ".html"

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

def GetTotalPageNumber():
	html = GetHtmlByUrl(blog_url)
	totalPageItem = re.findall('<div.*?favmd5=.*?.*?classid="0".*?pagesize="10".*?total="(.*?)".*?id="pagination_.*?".*?class="SG_page">.*?</div>', html, re.I)
	for totalPage in totalPageItem:
		return math.ceil(int(totalPage) / 10.0)

def GetBlogDetailByPage(url, pageNum = 1):
	print 'To get page ' + str(pageNum)
	html = GetHtmlByUrl(url)
	
	detailPageItems = re.findall('<span.*?class="SG_more">.*?<a.*?href="(.*?)".*?>查看全文</a>.*?</span>', html, re.I)
	
	for detailUrl in detailPageItems:
		print detailUrl
		GetBlogDetailHtmlByUrl(detailUrl)

	global totalPageNumber

	nextPageNumber = pageNum + 1

	if nextPageNumber <= totalPageNumber:
		GetBlogDetailByPage(GetNextPageUrl(nextPageNumber), nextPageNumber)

def main():
	startTime = datetime.datetime.now()

	global totalPageNumber
	totalPageNumber = int(GetTotalPageNumber())
	print '=================Start, Total Page:' + str(totalPageNumber) + "================="
	GetBlogDetailByPage(blog_url)

	endTime = datetime.datetime.now()
	print '=================Over, Cost time:' + str((endTime - startTime).seconds) + 's ================='

if __name__ == "__main__":
	main()