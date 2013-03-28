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
        self._tasks_url = 'http://localhost:8080/id/followed/'
        self._url = 'http://www.douban.com/people/%s/contacts'
        self._upload_url = 'http://localhost:8080/upload/'
        logging.basicConfig(filename='followed_error.log', filemod='a+', level=logging.ERROR)

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
            cfg = {}
            cfg['status'] = self._status
            cfg['free_tasks'] = list(self._free_tasks)
            cfg['done_tasks'] = list(self._done_tasks)
            f.write(json.dumps(cfg))

    def __get_followed(self, user):
        page = self._fetch.get(self._url % user)
        followed = user_followed_parser(page)
        return followed

    def __get_tasks(self):
        if self._status == 'free':
            resp = requests.get(self._tasks_url)
            js = resp.json() 
            self._free_tasks = js.get('tasks')    
            self._status = 'running'

    def __do_tasks(self):
        with open('followed.txt', 'a') as f:
            for t in self._free_tasks:
                if t not in self._done_tasks:
                    obj = {'_id':t}
                    obj['followed'] = self.__get_followed(t)
                    f.write(json.dumps(obj) + '\n')
                    self._done_tasks.add(t)

    def __upload_tasks(self):
        tasks = {'type':'followed', 'data':[]}
        with open('followed.txt', 'r') as f:
            for line in f:
                obj = json.loads(line.rstrip('\n'))        
                tasks['data'].append(obj)

        data = json.dumps(tasks)
        headers = {'Content-type':'application/json; charset=utf8'}
        while True:
            resp = requests.put(self._upload_url, data=data, headers=headers)
            js = resp.json()
            if js.get('code') == 200:
                os.remove('user_followed_config.cfg')
                self.__reset()
                break
            
    def run(self):
        while True:
            try:
                self.__get_tasks()
                self.__do_tasks()
                self.__upload_tasks()
            except KeyboardInterrupt:
                break
            except Exception, e:
                logging.error(repr(e))
