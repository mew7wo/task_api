#!/usr/bin/env python
#coding=utf-8
#file Name: client_test.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Wed 13 Mar 2013 12:23:53 PM CST


import requests
import json
import unittest

class UploadTestCase(unittest.TestCase):
    
    def test_upload_404(self):
        js = json.dumps({'test':'test'})
        headers = {'Content-Type':'application/json; charset=utf8'}
        req = requests.put('http://localhost:5000/upload/', data=js, headers=headers)
        self.assertEqual(req.text, json.dumps({'code':404, 'msg':'not found'}))

        js = json.dumps({})
        headers = {'Content-Type':'application/json; charset=utf8'}
        req = requests.put('http://localhost:5000/upload/', data=js, headers=headers)
        self.assertEqual(req.text, json.dumps({'code':404, 'msg':'not found'}))

    def test_upload_tags(self):
        pass

    def test_upload_followed(self):
        pass

    def test_upload_books(self):
        pass


def main():
    suite = unittest.TestSuite()
    suite.addTest(UploadTestCase('test_upload_404'))

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
