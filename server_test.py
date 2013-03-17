#!/usr/bin/env python
#coding=utf-8
#file Name: server_test.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Mon 11 Mar 2013 04:49:19 PM CST


import unittest
import requests
import json
from server import *


class APITestCase(unittest.TestCase):
    ''' test api path 
        test return json format
        test charset'''
    def test_tags_API(self):
        with app.test_request_context('/id/tags/', method='GET'):
            self.assertEqual(request.path, '/id/tags/')

    ''' test books api path
        test return json format
        test charset '''
    def test_books_API(self):
        with app.test_request_context('/id/books/', method='GET'):
            self.assertEqual(request.path, '/id/books/')

    ''' test followed api path
        test return json format
        test charset '''
    def test_followed_API(self):
        with app.test_request_context('/id/followed/', method='GET'):
            self.assertEqual(request.path, '/id/followed/')
            
    ''' test upload api path '''
    def test_upload_API(self):  
        with app.test_request_context('/upload/', method='PUT'):
            self.assertEqual(request.path, '/upload/')
            


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
    suite.addTest(APITestCase('test_tags_API'))
    suite.addTest(APITestCase('test_books_API'))
    suite.addTest(APITestCase('test_followed_API'))
    suite.addTest(APITestCase('test_upload_API'))


    suite.addTest(UploadTestCase('test_upload_404'))

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()
