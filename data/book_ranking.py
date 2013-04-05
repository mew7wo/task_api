#!/usr/bin/env python
#coding=utf-8
#file Name: book_ranking.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Thu 04 Apr 2013 09:55:19 AM CST


from pymongo import Connection

db = Connection().doubanbook

def cmp(a, b):
    return b[1] - a[1]

def user_weight():
    users = {}
    with open('user_tags_filter.txt', 'r') as f:
        for line in f:
            users.setdefault(line.rstrip('\n'), 0)

    with open('user_ranking.txt', 'r') as f:
        for line in f:
            it = line.rstrip('\n').split(' ')
            if users.has_key(it[0]):
                users[it[0]] = int(it[1])

    return users

def book_union(users):
    books = {}
    for u in users:
        b = db.user_books.find_one({'_id':u})
        for i in b.get('books'):
            books.setdefault(i['_id'], 0)
            books[i['_id']] = books[i['_id']] + users[u]
    its = books.items()
    its.sort(cmp)

    return its

def main():
    users = user_weight()
    book_ranking = book_union(users)
    with open('book_ranking.txt', 'w') as f:
        for b in book_ranking:
            f.write('%s %d\n' % b) 

if __name__ == '__main__':
    main()
