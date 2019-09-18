# encoding: utf-8
# 向数据库添加记录信息
from watchlist import app,User,Movie,db
import click
# # 数据的添加
# user=User(name='Grey Li')
# m1=Movie(title='Mongo',year='1999')
# m2=Movie(title='JackChen',year='1986')
# db.session.add(user)
# db.session.add(m1)
# db.session.add(m2)
# db.session.commit()

# # 数据的修改更新
# movie = Movie.query.get(2)
# movie.title = "XLL-E"
# movie.year = "2012"
# db.session.commit()

# # 添加一些虚拟数据
# @app.cli.command()
# def forge():
#     '''Generate fake data'''
#     db.create_all()
#
#     name = 'Arias Li'
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
#     ]
#
#     user = User(name=name)
#     db.session.add(user)
#     for m in movies:
#         movie = Movie(title=['title'], year=m['year'])
#         db.session.add(movie)
#
#     db.session.commit()
#     click.echo('Done.')



