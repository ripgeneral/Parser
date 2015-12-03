#!flask/bin/python

from flask import render_template,redirect,url_for,request
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('172.16.0.154',27017)
db = client.test

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/new',methods=['POST'])
def new():
    item_doc= {
        'name':request.form['name'],
        'desc':request.form['desc']
    }
    db.test.insert_one(item_doc)

    return redirect(url_for('list'))

@app.route('/list')
def list():
     _items = db.test.find()
     items = [item for item in _items]
     return render_template('list.html',items = items )

@app.route('/view')
def view():
    _items = db.test.find()
    items  = [item for item in _items]
    return render_template('view.html',items = items)

@app.route('/projects/')
def projects():
    return 'The project pages'

@app.route('/about/')
def about():
    return 'The about pages'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
