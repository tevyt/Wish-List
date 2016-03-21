from flask import Flask
import os
import sys 
import logging

app = Flask(__name__)

#See Error Logs
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.config['SECRET_KEY'] = 'mnIcdwVxqc80HQ0nYOtS'

from app import views


