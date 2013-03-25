#!/usr/bin/env python2.7
#coding=utf-8
#author:mew7wo
#mail:mew7wo@gmail.com
#filename:user_followed.py
#create time:Wed 30 Jan 2013 02:49:41 PM CST

import re
from lxml import etree

class Followed():
    ''' get user follower module '''
    def __init__(self):
        self._xpath = r'//*[@id="content"]/div/div[1]/div[3]/dl/dd/a/@href'
        #self._xpath = r'//*[@id="content"]/div/div[1]/div[3]/dl/dd/a'

    def getUrlByUser(self, user):
        return 'http://www.douban.com/people/%s/contacts' % user

    def getFollowedUser(self, page):
        new_users = set()
        try:
            html = etree.HTML(page)
            urls = html.xpath(self._xpath)
            for url in urls:
                if self.__validUrl(url):
                    new_users.add(self.__getUserId(url))
        except Exception, e:
            print repr(e)

        return new_users

    def __validUrl(self, url):
        r = re.compile(r'http://www.douban.com/people/*')
        if url == None: return False
        if r.search(url) == None:
            return False
        else:
            return True

    def __getUserId(self, url):
        return url[29:-1]


if __name__ == '__main__':
   ''' get user followed module'''
   print 'get user followed'
