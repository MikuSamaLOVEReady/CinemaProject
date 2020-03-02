from flask import Flask # Flask是一个calss
from flask_sqlalchemy import SQLAlchemy #也是引入的一个calss
from flask_admin import Admin
from flask_login import LoginManager
import logging

from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config') #从config.py 中适配

app.debug = True
handler = logging.FileHandler('flask.log', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
#handler.setLevel(logging.ERROR)
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)


db = SQLAlchemy(app)  # 实例化db对象后



bootstrap = Bootstrap(app)
admin = Admin(app,template_mode='bootstrap3')



from app import views,models
#,models