from flask.ext.wtf import Form
from wtforms.fields import TextField
from wtforms.validators import Required , Email, EqualTo

class SignUpForm(Form):
    firstname = TextField('firstname' , validators=[Required()])
    lastname = TextField('lastname' , validators=[Required()])
    email  = TextField('email' , validators=[Required() , Email()])
    password = TextField('password' , validators=[Required() , EqualTo('confirmation')])
    confirmation = TextField('confirmation' , validators=[Required()])
