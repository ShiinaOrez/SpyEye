import time
from . import db
from flask import current_app
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

class App(db.Model):
    __tablename__ = 'apps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class User2App(db.Model):
    __tablename__ = 'user2apps'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    operations = db.relationship('Oper', backref='app', lazy='dynamic')

class Oper(db.Model):
    __tablename__ = 'operations'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('user2apps.id'))
    coordinates = db.relationship('Coor', backref='oper', lazy='dynamic')

class Coor(db.Model):
    __tablename__ = "coordinates"
    id = db.Column(db.Integer, primary_key=True)
    oper_id = db.Column(db.Integer, db.ForeignKey('operations.id'))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    statu = db.Column(db.Integer)
    time = db.Column(db.String(30))
