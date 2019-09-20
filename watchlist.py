# encoding: utf-8
from flask import Flask, render_template, request, url_for, redirect, flash
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
app.config['SECRET_KEY'] = 'dev'

# # 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":    # 判断是否使 POST 请求
        # 获取表单数据
        title = request.form.get("title")
        year = request.form.get("year")
        # 验证数据，如果数据为空或者长度不符合要求，就报错
        if not title or not year or len(year)>4 or len(title)>60:
            flash("Invalid input.")
            return redirect(url_for("index"))
        # 保存表单到数据库
        movie = Movie(title=title, year=year)   # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash("Item created successfully!")  # 显示成功创建提示
        return redirect(url_for("index"))  # 重定向回主页
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid Input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item Updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item Deleted.")
    return redirect(url_for('index'))


@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    # 返回模板和状态码
    return render_template('404.html',), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


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


