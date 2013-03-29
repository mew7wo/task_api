#!/usr/bin/env python
#coding=utf-8
#file Name: extend_tags.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Thu 28 Mar 2013 10:46:42 PM CST


from pymongo import Connection

def cmp(a, b):
    return b[1] - a[1]

db = Connection().doubanbook

com_tags = set()
book_id = set()
new_tags = {}
tag_cur = db.computer_tags.find()
for t in tag_cur:
    com_tags.add(t['tag'])

book_cur = db.book.find()

for t in book_cur:
    for tag in t['tags']:
        if tag['title'] in com_tags:
            book_id.add(t['_id'])
            for x in t['tags']:
                new_tags.setdefault(x['title'], 0)
                new_tags[x['title']] = new_tags[x['title']] + 1
            break

with open('computer_book_id.txt', 'w') as f:
    for i in book_id:
        f.write('%s\n' % i)


with open('new_computer_tags.txt', 'w') as f:
    tag_and_count = new_tags.items()
    tag_and_count.sort(cmp)
    for i in tag_and_count:
        f.write('%s %d\n' % (i[0].encode('utf-8'), i[1]))
