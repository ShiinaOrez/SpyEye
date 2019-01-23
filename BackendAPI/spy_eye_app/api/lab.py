import time
from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import User, App, User2App, Oper, Coor

def change(x):
    db.session.add(x)
    db.session.commit()

@api.route("/post/", methods=["POST"], endpoint='PostData')
def post_data():
    uid = request.get_json().get('userID')
    appName = request.get_json().get('appName')
    dataList = request.get_json().get('dataList')

    usr = User.query.filter_by(id=uid).first()
    if usr is None:
        usr = User()
        change(usr)

    app = App.query.filter_by(name=appName).first()
    if app is None:
        app = App(name=appName)
        change(app)

    record = User2App.query.filter_by(app_id=app.id, user_id=uid).first()
    if record is None:
        record = User2App(app_id=app.id, user_id=uid)
        change(record)

    oper = Oper()
    change(oper)
    oper.record_id = record.id
    for data in dataList:
        coordinates = Coor(oper_id=oper.id, x=data["x"], y=data["y"], statu=data["statu"], time=data["time"])
        change(coordinates)
    return jsonify({"operationID": oper.id})
