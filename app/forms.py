from flask.ext.wtf import Form
from wtforms.fields import TextField
from wtforms.validators import Required

class SignUpForm(Form):
    firstname = TextField('firstname' , validators=[Required()])
    lastname = TextField('lastname' , validators=[Required()])
    email  = TextField('email' , validators=[Required()])
