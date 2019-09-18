# encoding: utf-8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys

# 定义虚拟数据
name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

# WIN = sys.platform.startswith("win")
# if WIN:
#     prefix = 'sqlite///'
# else:
#     prefix = 'sqlite////'
#
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
# # 在扩展类实例化前加载配置
# db = SQLAlchemy(app)


@app.route('/')
def index():
    # user = User.query.first()
    # movies = Movie.query.all()
    return render_template('index.html', name=name, movies=movies)

# # 创建数据库模型
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#
# class Movie(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(60))
#     year = db.Column(db.String(4))


