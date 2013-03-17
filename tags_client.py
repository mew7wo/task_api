#!/usr/bin/env python
#coding=utf-8
#file Name: tags_client.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Wed 13 Mar 2013 06:01:27 PM CST


import requests
import os
import json
import logging
from fetch import Fetch

class TagsTask():
    def __init__(self):
        logging.basicConfig(filename='error.log', filemode='a+', level=logging.ERROR)
        self.__read_info()
        self._fetcher = Fetch()
        self._url = 'https://api.douban.com/v2/book/user/%s/tags?count=100'
        self._task_url = 'http://localhost:5000/id/tags/'
        self._upload_url = 'http://localhost:5000/upload/'

    def run(self):
        while True:
            try:
                self.__get_tasks()
                self.__do_tasks()
                self.__upload_tasks()
            except KeyboardInterrupt:
                break
            except Exception, e:
                logging.error(str(e))

    def __read_info(self):
        self.__reset()
        if os.path.exists('config.cfg')
            with open('config.cfg', 'r') as f:
                js = json.loads(f.read())
                self._status = js.get('status')
                self._free_task = js.get('free_task')
                self._done_task = js.get('done_task')

    def __save_info(self):
        with open('config.cfg', 'w') as f:
            js = {}
            js['status'] = self._status
            js['free_task'] = self._free_task
            js['done_task'] = self._done_task
            f.write(json.dumps(js))

    def __reset(self):
        self._free_task = set()
        self._done_task = set()
        self._status = 'free'

    def __get_tags(self, user):
        js = self._fetcher.get(self._url % user, sleeptime=2.3)
        obj = json.loads(js)
        return {'_id':user, 'tags':obj['tags']}

    def __get_tasks(self):
        if self._status == 'free':
            self.__reset() 
            req = requests.get(self._task_url)
            js = req.json()
            for t in js.get('ids'):
                self._free_task.add(t)
            self._status = 'running'

    def __do_tasks(self):
        with open('tags.txt', 'a') as f:
            for t in self._free_task:
                if t not in self._done_task:
                    tags = self.__get_tags(t)
                    f.write(json.dumps(tags) + '\n')
                    self._done_task.add(t)
                    
    def __upload_task(self):
        tasks = {'type':'tags', 'data':[]} 
        with open('tags.txt', 'r') as f:
            for line in f:
                tasks['data'].append(json.loads(line.rstrip('\n')))

        data = json.dumps(tasks)
        headers = {'Content-type':'application/json;charset=utf8'}
        while True:
            resp = requests.put(self._upload_url, data=data, headers=headers)
            js = resp.json
            if js.get('code') == 200:
                self._status = 'free'
                os.remove('tags.txt')
                break

def main():
    t = TagsTask()
    t.run()

if __name__ == '__main__':
    main()

