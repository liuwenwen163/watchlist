# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie



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
