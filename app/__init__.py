from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import config


app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLACHEMY_DATABASE_URI
db = SQLAlchemy(app)

from app import route