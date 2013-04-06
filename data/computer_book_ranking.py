#!/usr/bin/env python
#coding=utf-8
#file Name: computer_book_ranking.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Fri 05 Apr 2013 10:33:56 PM CST


import json
from pymongo import Connection

db = Connection().doubanbook

def cs_tags():
    tags = set()
    cur = db.computer_tags.find()
    for r in cur:
        tags.add(r['tag'])

    return tags

def filter_user(tags):
    users = set()
    cur = db.user_tags.find()
    for r in cur:
        for t in r['tags']:
            if t['title'] in tags:
                users.add(r['_id'])
                break
    return users

def rank_user(users):
    ranked_user = {}
    for u in users:
        ranked_user[u] = 0

    for u in users:
        user_row = db.user_followed.find_one({'_id':u})
        if user_row != None:
            for f in user_row['followed']:
                if f in users:
                    ranked_user[f] = ranked_user[f] + 1

    return ranked_user

def filter_book(users, tags):
    src_books = set()
    for u in users:
        row = db.user_books.find_one({'_id':u})
        if row != None:
            for b in row['books']:
                src_books.add(b['_id']) 

    books = set()
    for b in src_books:
        row = db.book.find_one({'_id':b})
        if row != None:
            for t in row['tags']:
                if t['title'] in tags:
                    books.add(b)
                    break

    return books

def rank_book(ranked_user, books):
    ranked_book = {}
    for u in ranked_user:
        row = db.user_books.find_one({'_id':u})
        if row != None:
            for b in row['books']:
                if b['_id'] in books:
                    ranked_book.setdefault(b['_id'], 0)
                    ranked_book[b['_id']] = ranked_book[b['_id']] + ranked_user[u]
            
    return ranked_book 

def export_book(ranked_book):
    with open('computer_rank_book.txt', 'w') as f:
        for b in ranked_book:
            row = db.book.find_one({'_id':b})
            if row != None:
                row['weight'] = ranked_book[b]
                f.write('%s\n' % json.dumps(row))

        
def main():
    tags = cs_tags()
    users = filter_user(tags)
    ranked_user = rank_user(users)
    books = filter_book(users, tags)
    ranked_book = rank_book(ranked_user, books)
    export_book(ranked_book)

if __name__ == '__main__':
    main()
