from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
import sys 
import logging

app = Flask(__name__)

#See Error Logs
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://dlwxmgeohpnlcx:rUM6HI77Lhp6gYSqygwb_cGqj4@ec2-54-235-199-36.compute-1.amazonaws.com:5432/d89u8tpsgnf8c4"
db = SQLAlchemy(app)
from app import views
from app.models import User


