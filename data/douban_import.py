#!/usr/bin/env python
#coding=utf-8
#file Name: douban_import.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Thu 21 Mar 2013 10:46:23 PM CST

import json
from pymongo import Connection

def import_user_status(db, filename):
    with open(filename, 'r') as f:
        for line in f:
            user = json.loads(line.rstrip('\n').decode('utf-8'))
            db.user_status.insert(user)

def import_user_followed(db, filename):
    with open(filename, 'r') as f:
        for line in f:
            user = json.loads(line.rstrip('\n').decode('utf-8'))
            db.user_followed.insert(user)

def import_user_tags(db, filename):
    with open(filename, 'r') as f:
        for line in f:
            user = json.loads(line.rstrip('\n').decode('utf-8'))
            db.user_tags.insert(user)

def import_user_books(db, filename):
    pass

def main():
    db = Connection(host='localhost', port=27017).doubanbook
    import_user_status(db, 'user_status.dat')
    import_user_followed(db, 'user_followed.dat')

if __name__ == '__main__':
    main()
