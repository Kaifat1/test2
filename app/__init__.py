from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
import os
from flask_login import LoginManager
#from config import basedir

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.session_protection = 'strong'

bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mydb'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm.init_app(app)
lm.login_view = 'login'