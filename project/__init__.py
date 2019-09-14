from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from logging.handlers import RotatingFileHandler

import os
import logging


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

if not os.path.exists('logs'):
    os.mkdir('logs')
log_handler = RotatingFileHandler('logs/zendesk.log', maxBytes=20480, backupCount=8)
log_file_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
log_handler.setFormatter(log_file_format)
log_handler.setLevel(logging.INFO)

app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Starting up Zendesk Security Challenger Solution')

from project import routes, models, errors
