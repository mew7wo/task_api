#!/usr/bin/env python
#coding=utf-8
#file Name: main.py
#author: mew7wo
#mail: mew7wo@gmail.com
#created Time: Wed 06 Mar 2013 09:24:58 PM CST


import json
from flask import Flask, jsonify
from flask import Response, request

app = Flask(__name__)

@app.route('/id/followed/')
def id_followed():
    pass


@app.route('/id/books/')
def id_books():
    return jsonify(msg='fuck')


@app.route('/id/tags/')
def id_tags(): 
    pass


@app.route('/book/tags/')
def book_tags():
    js = json.dumps({'tags':['abc', 'dsaf']})
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/upload/', method=['PUT'])
def upload():
    pass

def id_books_upload():
    pass

def id_tags_upload():
    pass

def id_followed_upload():
    pass

if __name__ == '__main__':
    app.run(debug=True)
