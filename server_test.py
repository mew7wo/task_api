#!/usr/bin/env python
#coding=utf-8
#file Name: server_test.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Mon 11 Mar 2013 04:49:19 PM CST


import unittest
from main import *


class APITestCase(unittest.TestCase):
    ''' test api path 
        test return json format
        test charset'''
    def testTagsAPI(self):
        with app.test_request_context('/id/tags/', method='GET'):
            self.assertEqual(request.path, '/id/tags/')

    ''' test books api path
        test return json format
        test charset '''
    def testBooksAPI(self):
        with app.test_request_context('/id/books/', method='GET'):
            self.assertEqual(request.path, '/id/books/')

    ''' test followed api path
        test return json format
        test charset '''
    def testFollowedAPI(self):
        with app.test_request_context('/id/followed/', method='GET'):
            self.assertEqual(request.path, '/id/followed/')
            
    ''' test upload api path '''
    def testUploadAPI(self):  
        with app.test_request_context('/upload/', method='PUT'):
            self.assertEqual(request.path, '/upload/')

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(APITestCase('testTagsAPI'))
    suite.addTest(APITestCase('testBooksAPI'))
    suite.addTest(APITestCase('testFollowedAPI'))
    suite.addTest(APITestCase('testUploadAPI'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
