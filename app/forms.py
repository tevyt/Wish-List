from flask.ext.wtf import Form
from wtforms.fields import TextField
from wtforms.validators import Required , Email, EqualTo
from app import db
from app.models import User

def unique_email_validator(form , field):
    user = db.session.query(User).filter_by(email=field.data).first()
    if user != None:
        field.errors.append('This email is already in use')
        return False
    return True

class SignUpForm(Form):
    firstname = TextField('firstname' , validators=[Required()])
    lastname = TextField('lastname' , validators=[Required()])
    email  = TextField('email' , validators=[unique_email_validator, Required() , Email()])
    password = TextField('password' , validators=[Required() , EqualTo('confirmation')])
    confirmation = TextField('confirmation' , validators=[Required()])

class LoginForm(Form):
    email  = TextField('email' , validators=[Required() , Email()])
    password = TextField('password' , validators=[Required()])


class ItemForm(Form):
    name = TextField('name' , validators=[Required()])
    thumbnail_url = TextField('thumbnailUrl')
    description = TextField('description', validators=[Required()])
