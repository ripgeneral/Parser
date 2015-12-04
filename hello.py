# -*- coding: utf-8 -*-
#!flask/bin/python

from flask import render_template,redirect,url_for,request
from flask import Flask
# from pymongo import MongoClient
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

# app.config['MONGO_HOST'] = '172.16.0.154'
# app.config['MONGO_PORT'] = 27017
# app.config['MONGO_DBNAME'] = 'test'
app.config.update(
    MONGO_HOST = '172.16.0.154',
    MONGO_PORT = 27017,
    MONGO_DBNAME = 'test',
    MONGO_AUTO_START_REQUEST = False
)

mongo = PyMongo(app,config_prefix='MONGO')

# client = MongoClient('172.16.0.154',27017)
# db = client.test

@app.route('/')
def hello():
    return render_template('hello.html')

# @app.route('/new',methods=['POST'])
# def new():
#     item_doc= {
#         'name':request.form['name'],
#         'desc':request.form['desc']
#     }
#     db.test.insert_one(item_doc)
#
#     return redirect(url_for('list'))

# @app.route('/list')
# def list():
#      # _items = db.test.find()
#      # items = [item for item in _items]
#      return render_template('list.html',items = items )

@app.route('/view')
def view():
    try:
        # _items = db.test.find().sort("id",pymongo.DESCENDING)
        _items = mongo.db.test.find().sort("id", -1 )
        # .sort("id",pymongo.DESCENDING)
        # return _items
        items  = [item for item in _items]
        return render_template('view.html',items = items)
    except Exception as e:
        return 'Error: '+str(e)

@app.route('/projects/')
def projects():
    return 'The project pages'

@app.route('/about/')
def about():
    return 'The about pages'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
