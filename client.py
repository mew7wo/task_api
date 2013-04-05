#!/usr/bin/env python
#coding=utf-8
#file Name: client.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Fri 29 Mar 2013 01:03:02 PM CST

import requests
import logging
import os
import json
from fetch import Fetch

def run_time_sign(func):
    print 'calling %s.%s method' % (func.__class__, func.__name__)
    return func

class Client:
    '''client base class'''
    @run_time_sign
    def __init__(self):
        self.__reset()
        self.__read_info()

    def __del__(self):
        self.__save_info()

    def __reset(self):
        self._status = 'free'
        self._free_tasks = set()
        self._done_tasks = set()

    def __read_info(self):
        if os.path.exists('%s.cfg' % self.__class__):
            with open('%s.cfg' % self.__class__, 'r') as f:
                config = json.loads(f.read())
                self._status = config.get('status')
                self._free_tasks = set(config.get('free_tasks'))
                self._done_tasks = set(config.get('done_tasks'))

    def __save_info(self):
        with open('%s.cfg' % self.__class__, 'w') as f:
            config = {}
            config['status'] = self._status
            config['free_tasks'] = self._free_tasks
            config['done_tasks'] = self._done_tasks
            f.write(json.dumps(config))

    def __get_tasks(self, url):
        pass

    def __do_tasks(self, url):
        pass

    def __upload_tasks(self, url):
        pass


