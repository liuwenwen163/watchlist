import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith("win")
if WIN:
    # win系统下是三个/，并且是/
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 通过实例化Flask类，创建一个程序对象
app = Flask(__name__)
# 告诉SQLAlchemy数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'


# 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
# 实例化用户认证的扩展类
login_manager = LoginManager(app)
login_manager.login_message = '请先进行登录！'  # 未登录用户尝试修改时，进行保护


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户ID作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用ID作为User模型的主键查询对应的用户
    return user  # 返回用户对象


login_manager.login_view = 'login'  # 将用户重定向到登录界面，指定登录视图端点


@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    # 返回字典 {'user': user}
    return dict(user=user)


from watchlist import views, errors, commands

