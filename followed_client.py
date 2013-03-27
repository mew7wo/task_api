#!/usr/bin/env python
#coding=utf-8
#file Name: followed_client.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Mon 25 Mar 2013 04:15:15 PM CST



import os
import json
import request
from followed import Followed
from fetch import Fetch
from paser import user_followed_parser


class FollowedTask:
    ''' get douban user followed'''
    def __init__(self):
        self.__reset()
        self.__read_info()
        self._fetch = Fetch(username='1398882026@qq.com', pw='liumengchao')
        self._tasks_url = ''
        self._url = ''
        self._upload_url = ''

    def __del__(self):
        self.__save_info()

    def __reset(self):
        self._status = 'free'
        self._free_tasks = set()
        self._done_tasks = set()

    def __read_info(self):
        if os.path.exist('user_followed_config.cfg'):
            with open('user_followed_config.cfg', 'r') as f:
                cfg = json.loads(f.read())
                self._status = cfg.get('status')
                self._free_tasks = set(cfg.get('free_tasks'))
                self._done_tasks = set(cfg.get('done_tasks'))

    def __save_info(self):
        with open('user_followed_config.cfg', 'w') as f:
            cfg = {'status':self._status}
            cfg['free_tasks'] = list(self._free_tasks)
            cfg['done_tasks'] = list(self._done_tasks)
            f.write(json.dumps(cfg))

    def __get_followed(self):

    def __get_tasks(self):
        if self._status == 'free':
            resp = requests.get(self._tasks_url)
            js = resp.json() 
            self._free_task = js.get('tasks')    
            self._status = 'running'

    def __do_tasks(self):
        with open('followed.txt', 'a') as f:
            for t in self._free_tasks:
                if t not in self._done_tasks:
                    obj = {'_id':t}
                    obj['followed'] = self.__get_followed()
                    f.write(json.dumps(obj) + '\n')

    def __upload_tasks(self):

    def run(self):
