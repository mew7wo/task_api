#!/usr/bin/env python
#coding=utf-8
#file Name: parser.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Mon 25 Mar 2013 04:26:28 PM CST


import re
from lxml import etree

class ParseError:
    def __init__(self, user):
        self.msg = '%s parse error' % user

    def __str__(self):
        return self.msg

    def __repr(self):
        return self.msg


def user_followed_parser(page):
    user_xpath = r'//*[@id="content"]/div/div[1]/div[3]/dl/dd/a/@href'
    valid_url = re.compile('http://www.douban.com/people/*')
    user_followed = set()
    try:
        root = etree.HTML(page)
        urls = root.xpath(user_xpath)
        for u in urls:
            if valid_url.search(u):
                user_followed.add(u[29:-1])
    except:
        raise ParseError('followed')
        
    return list(user_followed)
