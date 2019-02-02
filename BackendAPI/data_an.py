from spy_eye_app import db
from spy_eye_app.models import User, App, User2App, Oper, Coor


def user_count():
    num = len(db.session().query(User).all())
    print("[UserCount]:", num)


def app_count():
    num = len(db.session().query(App).all())
    print("[AppCount]: ", num)


def operation_count():
    num = len(db.session().query(Oper).all())
    print("[OperCount]:", num)


def max_operation_q():
    q = 0
    records = db.session().query(User2App).all()
    for record in records:
        for oper in record.operations:
            size = 0
            for coor in oper.coordinates:
                size = size + 1
            if q < size:
                q = size
    print("[MAX_Q]:    ", q)


def run():
    user_count()
    app_count()
    operation_count()
    max_operation_q()

#    last_user_info()
#    last_user_apps_operations_info()