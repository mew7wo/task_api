#!/usr/bin/env python
#coding=utf-8
#file Name: server.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Wed 06 Mar 2013 09:24:58 PM CST


import json
from flask import Flask, jsonify
from flask import Response, request
from flask.ext.pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'doubanbook'
mongo = PyMongo(app)

@app.route('/test/', methods=['GET'])
def test_page():
    return prepare_resp({'code':200, 'msg':'test...'})

@app.route('/id/followed/', methods=['GET'])
def id_followed():
    cur = mongo.db.user_status.find({'followed':'free'}).limit(100)
    users = []
    for r in cur:
        mongo.db.user_status.update(r, {'$set':{'followed':'running'}})
        users.append(r['_id'])

    tasks = {}
    tasks['type'] = 'followed'
    tasks['tasks'] = users

    return prepare_resp(tasks)
    
@app.route('/id/books/', methods=['GET'])
def id_books():
    cur = mongo.db.user_status.find({'followed':'done', 'tags':'done', 'books':'free'}).limit(10)
    users = []
    for r in cur:
        mongo.db.user_status.update(r, {'$set':{'books':'running'}})
        users.append(r['_id'])

    tasks = {}
    tasks['type'] = 'books'
    tasks['tasks'] = users

    return prepare_resp(tasks)

@app.route('/id/tags/', methods=['GET'])
def id_tags(): 
    cur = mongo.db.user_status.find({'followed':'done', 'tags':'free'}).limit(100)
    users = []
    for r in cur:
        mongo.db.user_status.update(r, {'$set':{'tags':'running'}})
        users.append(r['_id'])

    tasks = {}
    tasks['type'] = 'tags'
    tasks['tasks'] = users

    return prepare_resp(tasks)


def prepare_resp(resp):
    js = json.dumps(resp)
    return Response(js, status=200, mimetype='application/json;charset=utf8')
    

@app.route('/upload/', methods=['PUT'])
def upload():
    js = request.json
    data_type = js.get('type')
    if data_type == 'books':
        return id_books_upload(js['data'])
    elif data_type == 'tags':
        return id_tags_upload(js['data'])
    elif data_type == 'followed':
        return id_followed_upload(js['data'])
    else:
        return id_404_upload()


def id_books_upload(ary):
    for user in ary:
        books = []
        for r in user['books']:
            obj = {}
            obj['_id'] = r['book_id']
            obj['status'] = r['status']
            obj['updated'] = r['updated']
            books.append(obj) 
            
            book = r['book']
            book['_id'] = book['id']
            del book['id']

            tags = []
            for t in book['tags']:
                t['title'] = t['title'].lower()
                t['name'] = t['name'].lower()
                tags.append(t)

            book['tags'] = tags
            mongo.db.book.save(book) 

        mongo.db.user_books.insert({'_id':user['_id'], 'books':books}) 
        mongo.db.user_status.update({'_id':user['_id']}, {'$set':{'books':'done'}})

    return prepare_resp({'code':200, 'msg':'success'})

def id_tags_upload(ary):
    for r in ary:
        tags = []
        for t in r['tags']:
            t['title'] = t['title'].lower()
            t['name'] = t['name'].lower()
            tags.append(t)
        mongo.db.user_tags.insert({'_id':r['_id'], 'tags':tags})
        mongo.db.user_status.update({'_id':r['_id']}, {'$set':{'tags':'done'}})

    return prepare_resp({'code':200, 'msg':'success'}) 

def id_followed_upload(ary):
    for r in ary:
        mongo.db.user_followed.insert({'_id':r['_id'], 'followed':r['followed']})
        mongo.db.user_status.update({'_id':r['_id']}, {'$set':{'followed':'done'}})

    return prepare_resp({'code':200, 'msg':'success'})

def id_404_upload():
    return prepare_resp({'code':404, 'msg':'not found'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9090, debug=True)

