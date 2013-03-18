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


class ServerTestCase(unittest.TestCase):
    def test_tags_API(self):
        with app.test_request_context('/id/tags/', method='GET'):
            self.assertEqual(request.path, '/id/tags/')
            self.assertEqual(request.method, 'GET')

    def test_books_API(self):
        with app.test_request_context('/id/books/', method='GET'):
            self.assertEqual(request.path, '/id/books/')
            self.assertEqual(request.method, 'GET')

    def test_followed_API(self):
        with app.test_request_context('/id/followed/', method='GET'):
            self.assertEqual(request.path, '/id/followed/')
            self.assertEqual(request.method, 'GET')
            
    def test_upload_API(self):  
        with app.test_request_context('/upload/', method='PUT'):
            self.assertEqual(request.path, '/upload/')
            self.assertEqual(request.method, 'PUT')
            

class ClientTestCase(unittest.TestCase):
    def test_tags(self):
        req = requests.get('http://localhost:5000/id/tags/') 
        js = req.json()
        self.assertEqual(js.has_key('ids'), True)
        self.assertEqual(js.has_key('type'), True)
        self.assertEqual(js.get('type'), 'tags')
        
    def test_books(self):
        req = requests.get('http://localhost:5000/id/books/')
        js = req.json()
        self.assertEqual(js.has_key('ids'), True)
        self.assertEqual(js.has_key('type'), True)
        self.assertEqual(js.get('type'), 'books')

    def test_followed(self):
        req = requests.get('http://localhost:5000/id/followed/')
        js = req.json()
        self.assertEqual(js.has_key('ids'), True)
        self.assertEqual(js.has_key('type'), True)
        self.assertEqual(js.get('type'), 'followed')

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
        js = json.dumps({'type':'tags', 'data':[]}) 
        headers = {'Content-Type':'application/json; chaset=utf8'}
        req = requests.put('http://localhost:5000/upload/', data=js, headers=headers)
        self.assertEqual(req.text, json.dumps({'code':200, 'msg':'success'}))

    def test_upload_followed(self):
        js = json.dumps({'type':'followed', 'data':[]}) 
        headers = {'Content-Type':'application/json; charset=utf8'}
        req = requests.put('http://localhost:5000/upload/', data=js, headers=headers)
        self.assertEqual(req.text, json.dumps({'code':200, 'msg':'success'}))

    def test_upload_books(self):
        js = json.dumps({'type':'books', 'data':[]})
        headers = {'Content-Type':'application/json; charset=utf8'}
        req = requests.put('http://localhost:5000/upload/', data=js, headers=headers)
        self.assertEqual(req.text, json.dumps({'code':200, 'msg':'success'}))


def main():
    suite = unittest.TestSuite()
    suite.addTest(ServerTestCase('test_tags_API'))
    suite.addTest(ServerTestCase('test_books_API'))
    suite.addTest(ServerTestCase('test_followed_API'))
    suite.addTest(ServerTestCase('test_upload_API'))


    suite.addTest(ClientTestCase('test_tags'))
    suite.addTest(ClientTestCase('test_books'))
    suite.addTest(ClientTestCase('test_followed'))

    suite.addTest(ClientTestCase('test_upload_404'))
    suite.addTest(ClientTestCase('test_upload_tags'))
    suite.addTest(ClientTestCase('test_upload_books'))
    suite.addTest(ClientTestCase('test_upload_followed'))

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()
