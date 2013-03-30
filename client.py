#!/usr/bin/env python
#coding=utf-8
#file Name: client.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Fri 29 Mar 2013 01:03:02 PM CST

import requests
import logging
import json
from fetch import Fetch
def run_time_sign(func):
    print 'calling %s.%s method' % (func.__class__, func.__name__)
    return func

class Client:
    '''client base class'''
    @run_time_sign
    def __init__(self):
        pass

    def __del__(self):
        pass

    def __read_info(self):
        pass

    def __save_info(self):
        pass

    def __get_tasks(self, url):
        pass

    def __do_tasks(self, url):
        pass

    def __upload_tasks(self, url):
        pass


