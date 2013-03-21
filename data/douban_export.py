#!/usr/bin/env python
#coding=utf-8
#file Name: douban_export.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Thu 21 Mar 2013 09:56:02 PM CST



import json
from pymongo import Connection

def export_user_status(db, filename):
    with open(filename, 'w') as f:
        cur = db.user_status.find()
        for r in cur:
            f.write(json.dumps(r).encode('utf-8') + '\n')


def export_user_followed(db, filename):
    with open(filename, 'w') as f:
        cur = db.user_followed.find()
        for r in cur:
            f.write(json.dumps(r).encode('utf-8')+'\n')

def main():
    db = Connection(host='localhost', port=27017).doubanbook
    export_user_status(db, 'user_status.dat')
    export_user_followed(db, 'user_followed.dat')


if __name__ == '__main__':
    main()
