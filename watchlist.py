# encoding: utf-8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

WIN = sys.platform.startswith("win")
if WIN:
    # win系统下是三个/，并且是/
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
# 告诉SQLAlchemy数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# # 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    # 返回模板和状态码
    return render_template('404.html',), 404

@app.context_processor
def inject_user():
    user = User.query.first()
    # 返回字典 {'user': user}
    return dict(user=user)

# 创建数据库模型
class User(db.Model):   # 表名user，自动生成小写处理
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):  # 表名movie
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# 添加一些虚拟数据，引入click，需要在命令行敲击命令进行创建
@app.cli.command()
def forge():
    '''Generate fake data,在命令行同级目录下，输入 flask forge 进行调用'''
    db.create_all()

    name = 'Sen Dou'
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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo("Done.")


