from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
import sys 
import logging

app = Flask(__name__)

#See Error Logs
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://travis:wishlist@localhost/wishlist"
db = SQLAlchemy(app)
from app import views
from app.models import User


