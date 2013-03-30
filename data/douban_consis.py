#!/usr/bin/env python
#coding=utf-8
#file Name: douban_consis.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Fri 29 Mar 2013 09:12:23 PM CST


from pymongo import Connection
db = Connection().doubanbook

def consis_user_status():
    cur = db.user_status.find()
    for r in cur:
        db.user_status.save({'_id':r['_id'], 'followed':'free', 'books':'free', 'tags':'free'})

def consis_tags():
    cur = db.user_tags.find()
    for r in cur:
        db.user_status.update({'_id':r['_id']}, {'$set':{'tags':'done'}})

def consis_books():
    cur = db.user_books.find()
    for r in cur:
        db.user_status.update({'_id':r['_id']}, {'$set':{'books':'done'}})

def consis_followed():
    cur = db.user_followed.find()
    for r in cur:
        db.user_status.update({'_id':r['_id']}, {'$set':{'followed':'done'}})

def main():
    consis_user_status()
    consis_tags()
    consis_books()
    consis_followed()


if __name__ == '__main__':
    main()
