#!/usr/bin/env python
#coding=utf-8
#file Name: server.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Wed 06 Mar 2013 09:24:58 PM CST


import json
from pymongo import Connection
from flask import Flask, jsonify
from flask import Response, request


app = Flask(__name__)

@app.route('/test/', methods=['GET'])
def test_page():
    return prepare_resp({'code':200, 'msg':'test...'})

@app.route('/id/followed/', methods=['GET'])
def id_followed():
    task = make_task('followed')
    return prepare_resp(task)
    
@app.route('/id/books/', methods=['GET'])
def id_books():
    task = make_task('books')
    return prepare_resp(task)

@app.route('/id/tags/', methods=['GET'])
def id_tags(): 
    task = make_task('tags')
    return prepare_resp(task)

def make_task(task_type):
    db = Connection(host='localhost', port=27017, network_timeout=20).doubanbook
    rs = db.user_status.find({task_type:'free'}).limit(100)
    ids = []
    for cur in rs:
        db.user_status.update(cur, {task_type:'running'})
        ids.append(cur['_id'])

    tk = {}
    tk['ids'] = ids 
    tk['type'] = task_type
    
    return tk


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
    db = Connection(host='localhost', port=27017, network_timeout=10).doubanbook
    for user in ary:
        books = []
        for r in user['books']:
            books.append(r['_id']) 
            db.books.insert(r) 
        db.user_books.insert({'_id':user['_id'], 'books':books}) 
        db.user_status.update({'_id':user['_id']}, {'tags':'done'})

    return prepare_resp({'code':200, 'msg':'success'})

def id_tags_upload(ary):
    db = Connection(host='localhost', port=27017, network_timeout=10).doubanbook
    for r in ary:
        db.user_tags.insert({'_id':r['_id'], 'tags':r['tags']})
        db.user_status.update({'_id':r['_id']}, {'tags':'done'})

    return prepare_resp({'code':200, 'msg':'success'}) 

def id_followed_upload(ary):
    db = Connection(host='localhost', port=27017, network_timeout=10).doubanbook
    for r in ary:
        db.user_followed.insert({'_id':r['_id'], 'tags':r['tags']})
        db.user_status.update({'_id':r['_id']}, {'followed':'done'})

    return prepare_resp({'code':200, 'msg':'success'})

def id_404_upload():
    return prepare_resp({'code':404, 'msg':'not found'})


if __name__ == '__main__':
    app.run(debug=True)

