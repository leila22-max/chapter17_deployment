from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail
from flask_moment import Moment

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_object(Config)

# Objects
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
moment = Moment (app)

# Email Logs
if not app.debug:
    auth = None
    if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
        auth = (app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:                                                                                                                                                          
        secure = ()
        mail_handler = SMTPHandler( 
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr= 'no-reply@' +  app.config ['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], subject='Tinker FullStack Aplication Error...',
        credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

#Save logs to an existing folder called logs

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler= RotatingFileHandler(
    'logs/tinker_app.log',
    maxBytes=10240,
    backupCount=10)   
file_handler.setFormatter(
    logging.Formatter('%(asctime)s %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Tinker Full-Stack App')
    

from app import routes, models,errors

