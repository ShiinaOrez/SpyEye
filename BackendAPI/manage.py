import sys
import importlib
import os
import time
from spy_eye_app import create_app, db
from spy_eye_app.models import User, App, User2App, Oper, Coor
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def createdb():
    db.create_all()

if __name__ == "__main__":
    manager.run()
    app.run(debug=True)
