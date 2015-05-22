#coding:utf-8
__author__ = 'rei'

import urllib2
import re
import os


class Crawler:
    def __init__(self, host, target):
        self.target = target
        self.host = host

    def get_thumb_list(self, page_index):

        request = urllib2.Request(url=page_index)
        response = urllib2.urlopen(request)

        page = response.read().decode('utf-8')

        # 抓取相册列表部分
        pattern = re.compile('</div><div class="c_inner">(.*?)</div>')
        thumb_list = re.search(pattern, page).group(1)

        #抓取相册详情
        pattern_item = re.compile('<a.*?href="(.*?)" title="(.*?)".*?<img.*?src="(.*?)">')
        items = re.findall(pattern_item, thumb_list)

        thumbs = []
        for item in items:
            thumbs.append(item)

        return thumbs

    def save_image(self, img_url, file_name):
        img = urllib2.urlopen(img_url)
        img = img.read()
        img_file = open(file_name, 'wb')
        img_file.write(img)
        print u"%s save successful!" % file_name

    def create_dir(self, path):
        """Create a directory

        :type: string
        :rtype:boolean
        """
        path = path.strip()

        existed = os.path.exists(path)

        if not existed:
            print u"Create a new directory named %s" % path
            os.makedirs(path)
            return True
        else:
            print u"Directory %s has already been created" % path
            return False

    def save_thumb(self, thumb_url, name):
        img_num_request = urllib2.Request(url=thumb_url)
        img_num_response = urllib2.urlopen(img_num_request)
        img_page = img_num_response.read().decode('utf-8')
        img_num_pattern = re.compile('<strong class="diblcok"><span class="fColor">.*?</span>/(.*?)</strong>')

        img_num = re.findall(img_num_pattern, img_page)
        img_num = img_num[0]

        #抓取最后一页来获取所有的图片
        last_img_url = thumb_url[:-5]+"-"+img_num+".html"
        img_url_request = urllib2.Request(url=last_img_url)
        img_url_response = urllib2.urlopen(img_url_request)
        img_url_page = img_url_response.read().decode('utf-8')
        img_url_pattern_1 = re.compile('<div id="box-inner">.*?<div id="imgString">.*?</div><script>(.*?)</script><div')
        img_url = re.findall(img_url_pattern_1, img_url_page)
        img_url_pattern_2 = re.compile('.*?"(.*?)".*?')
        img_url = re.findall(img_url_pattern_2, img_url[0])
        img_url = [i.replace('big', 'pic') for i in img_url]

        print u"Thumb:%s has %d images" % (name, int(img_num))
        self.create_dir("./%s" % name)
        for (index, img) in enumerate(img_url):
            img_tail = img.split('.').pop()
            self.save_image(img, u"./%s/%d.%s" % (name, index+1, img_tail))

    def crawl_mm(self, start, end):
        for i in xrange(start, end+1):
            print u"Crawling page %d" % i
            if i == 1:
                thumb_list_url = self.host+self.target
            else:
                thumb_list_url = self.host+self.target[:-5]+"_"+str(i)+".html"

            thumb_list = self.get_thumb_list(thumb_list_url)

            for thumb in thumb_list:
                self.save_thumb(thumb_url=self.host+thumb[0], name=thumb[1])


if __name__ == "__main__":
    target_host = "http://www.22mm.cc"
    target_url = "/mm/jingyan/index.html"
    mm = Crawler(host=target_host, target=target_url)
    mm.crawl_mm(1, 4)