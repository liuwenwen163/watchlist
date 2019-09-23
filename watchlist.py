# encoding: utf-8
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import sys
import click

WIN = sys.platform.startswith("win")
if WIN:
    # win系统下是三个/，并且是/
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


# 通过实例化Flask类，创建一个程序对象
app = Flask(__name__)
# 告诉SQLAlchemy数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'

# # 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app

# 实例化用户认证的扩展类
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 将用户重定向到登录界面，指定登录视图端点
login_manager.login_message = '请先进行登录！'  # 未登录用户尝试修改时，进行保护


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":  # 判断是否使 POST 请求
        if not current_user.is_authenticated:
            flash('添加信息前请先进行登录。')
            return redirect(url_for('index'))
        # 获取表单数据
        title = request.form.get("title")
        year = request.form.get("year")
        # 验证数据，如果数据为空或者长度不符合要求，就报错
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash("Invalid input.")
            return redirect(url_for("index"))
        # 保存表单到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash("电影添加成功")  # 显示成功创建提示
        return redirect(url_for("index"))  # 重定向回主页
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('无效输入！')
            return redirect(url_for("login"))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            # 使用Flask-login提供的login_user函数，进行用户登录，传入的参数是用户模型
            login_user(user)
            flash('登录成功！')
            return redirect(url_for("index"))

        flash('用户名或密码错误！')
        return redirect(url_for("login"))

    return render_template("login.html")


# 用户注销
@app.route('/logout')
@login_required  # 视图保护
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


# 更改用户名称
# method写上get是因为访问到这个页面用的是get方法
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    # 访问页面的GET方法，返回设置页面；配置提交的POST页面，进入信息更新的逻辑
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('非法的输入')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('设置已更新')
        return redirect(url_for("index"))

    return render_template("settings.html")


# 编辑电影名称
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid Input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('电影条目已更新')
        return redirect(url_for('index'))

    return render_template("edit.html", movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("电影条目已删除")
    return redirect(url_for("index"))


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    # 返回模板和状态码
    return render_template("404.html", ), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.context_processor
def inject_user():
    user = User.query.first()
    # 返回字典 {'user': user}
    return dict(user=user)


# 创建数据库模型
class User(db.Model, UserMixin):  # 表名user，自动生成小写处理
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保存到对应的字段

    def validate_password(self, password):  # 用于验证密码，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class Movie(db.Model):  # 表名movie
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# # 添加一些虚拟数据，引入click，需要在命令行敲击命令进行创建
# @app.cli.command()
# def forge():
#     """Generate fake data,在命令行同级目录下，输入 flask forge 进行调用"""
#     db.create_all()
#
#     name = 'Sen Dou'
#     movies = [
#         {'title': 'My Neighbor Totoro', 'year': '1988'},
#         {'title': 'Dead Poets Society', 'year': '1989'},
#         {'title': 'A Perfect World', 'year': '1993'},
#         {'title': 'Leon', 'year': '1994'},
#         {'title': 'Mahjong', 'year': '1996'},
#         {'title': 'Swallowtail Butterfly', 'year': '1996'},
#         {'title': 'King of Comedy', 'year': '1999'},
#         {'title': 'Devils on the Doorstep', 'year': '1999'},
#         {'title': 'WALL-E', 'year': '2008'},
#         {'title': 'The Pork of Music', 'year': '2012'},
#
#     ]
#
#     user = User(name=name)
#     db.session.add(user)
#     for m in movies:
#         movie = Movie(title=m['title'], year=m['year'])
#         db.session.add(movie)
#
#     db.session.commit()
#     click.echo("Done.")


# 编写命令创建管理员账号
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="The password used to login.")
def admin(username, password):
    """Create admin user"""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name="Admin")
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户ID作为参数
    user = User.query.get(int(user_id))  # 用ID作为User模型的主键查询对应的用户
    return user  # 返回用户对象
