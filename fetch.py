#!/usr/bin/env python2.7
#coding=utf-8
#author:mew7wo
#mail:mew7wo@gmail.com
#filename:fetch.py
#create time:Wed 28 Nov 2012 02:20:12 PM CST

import urllib2
import urllib
import cookielib
import socket
import logging
from lxml import etree
from time import sleep


class Fetch(object):
    ''' url fetch class '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) Chrome/23.0.1271.64 Safari/537.11'}
    opener = None

    def __init__(self, username, pw):
        if self.__class__.opener == None:
            cj = cookielib.CookieJar()
            http_handler = urllib2.HTTPHandler()
            self.__class__.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), http_handler)

        self._username = username
        self._pw = pw
        self.__login()

    def __login(self):
        login_url = 'http://www.douban.com/accounts/login'
        login_page = self.get(login_url)
        post_data = self.__get_post_data(login_page)

        login_req = urllib2.Request(login_url, data=post_data, headers=self.__class__.headers)
        login_resp = self.__get(login_req)

        if login_resp.getcode() != 200:
            raise LoginError(login_resp.getcode())

    def __get(self, req):
        resp = None
        while True:
            try:
                resp = self.__class__.opener.open(req, timeout=10)
            except socket.timeout, e:
                print str(e)
            else:
                break
        return resp

    def get(self, url, sleeptime=None):
        if sleeptime != None: 
            sleep(sleeptime)
        req = urllib2.Request(url, headers=self.__class__.headers)
        content = self.__get(req).read()
        return content

    def __get_post_data(self, page):
        img_xpath = r'//*[@id="captcha_image"]'
        value_xpath = r'//*[@id="lzform"]/div[4]/div/div/input[2]'
        root = etree.HTML(page)
        captcha_value = root.xpath(value_xpath)[0].get('value')
        captcha_img_src = root.xpath(img_xpath)[0].get('src')
        with open('./captcha.jpeg', 'w') as f:
            img = self.get(captcha_img_src)
            f.write(img)

        form_data = {}
        form_data['form_email'] = self._username
        form_data['form_password'] = self._pw
        form_data['captcha-id'] = captcha_value
        form_data['captcha-solution'] = raw_input('check captcha.jpeg to get code: ')

        return urllib.urlencode(form_data)

class LoginError(Exception):
    def __init__(self, msg=None):
        self.msg = msg

