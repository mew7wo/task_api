#!/usr/bin/env python
#coding=utf-8
#file Name: tags_client.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Wed 13 Mar 2013 06:01:27 PM CST


import requests
import json
from fetch import Fetch

class TagsTask():
    def __init__(self):
        self.__reset()
        self._fetcher = Fetch()
        self._url = 'https://api.douban.com/v2/book/user/%s/tags?count=100'

    def run(self):
        pass

    def stop(self):
        pass

    def __reset(self):
        self._free_task = set()
        self._done_task = set()
        self._status = 'free'

    def __get_tags(self, user):
        js = self._fetcher.get(self._url % user)
        obj = json.loads(js)
        return {'_id':user, 'tags':obj['tags']}

    def __get_tasks(self):
        self.__reset() 
        req = requests.get('http://localhost:5000/id/tags/')
        js = req.json()
        for t in js.get('ids'):
            self._free_task.add(t)

    def __do_tasks(self):
        with open('tags.txt', 'a+') as f:
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
            resp = requests.put('http://localhost:5000/upload/', data=data, headers=headers)
            js = resp.json
            if js.get('code') == 200:
                break

def main():
    free_tasks, done_tasks = read_info()
    while True:
        try:
            
        except KeyboardInterrupt:
            save_info()
            break
        except Exception, e:
            print str(e)

    save_info()

if __name__ == '__main__':
    main()

