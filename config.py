import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'project.db')
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 15

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = '1'
    MAIL_USERNAME = 'ZDSecSolKS@gmail.com'
    MAIL_PASSWORD = 'ZDSecSol2019'
    ADMINS = ['ZDSecSolKS@gmail.com']

    #SESSION_COOKIE_SECURE = True
    #SESSION_COOKIE_HTTPONLY = True

