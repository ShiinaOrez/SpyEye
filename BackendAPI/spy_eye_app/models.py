import time
from . import db
from flask import current_app
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    apps = db.relationship('App', backref='user', lazy='dynamic')

class App(db.Model):
    __tablename__ = 'apps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    operations = db.relationship('Oper', backref='app', lazy='dynamic')

class Oper(db.Model):
    __tablename__ = 'operations'
    id = db.Column(db.Integer, primary_key=True)
    coordinates = db.relationship('Coor', backref='oper', lazy='dynamic')

class Coor(db.Model):
    __tablename__ = "coordinates"
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    time = db.Column(TIMESTAMP)
