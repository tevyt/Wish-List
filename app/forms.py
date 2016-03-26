from flask.ext.wtf import Form
from wtforms.fields import TextField
from wtforms.validators import Required , Email, EqualTo

class SignUpForm(Form):
    firstname = TextField('firstname' , validators=[Required()])
    lastname = TextField('lastname' , validators=[Required()])
    email  = TextField('email' , validators=[Required() , Email()])
    password = TextField('password' , validators=[Required() , EqualTo('confirmation')])
    confirmation = TextField('confirmation' , validators=[Required()])

class LoginForm(Form):
    email  = TextField('email' , validators=[Required() , Email()])
    password = TextField('password' , validators=[Required()])


class ItemForm(Form):
    name = TextField('name' , validators=[Required()])
    thumbnail_url = TextField('thumbnailUrl' , validators=[Required()])
    description = TextField('description')
