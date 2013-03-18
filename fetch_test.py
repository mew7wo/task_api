#!/usr/bin/env python
#coding=utf-8
#file Name: fetch_test.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Mon 18 Mar 2013 02:55:24 PM CST


import unittest
import urllib2
from fetch import Fetch

class FetchTestCase(unittest.TestCase):
    def setUp(self):
        self.fetch = Fetch(username='1398882026@qq.com', pw='liumengchao')

    def test_get(self):
        req = urllib2.Request('http://www.douban.com/update/')
        resp = self.fetch.get(req)
        print resp


def main():
    suite = unittest.TestSuite()

    suite.addTest(FetchTestCase('test_get'))

    runner = unittest.TextTestRunner()
    runner.run(suite)

    

if __name__ == '__main__':
    main()
