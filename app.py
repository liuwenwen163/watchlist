# encoding: utf-8
from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello Totoro</h1><img src='http://helloflask.com/totoro.gif'>"
