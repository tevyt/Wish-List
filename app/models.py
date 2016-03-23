from . import db
from hashlib import sha224

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(70))
    password = db.Column(db.String(70))

    def __init__(self, firstname , lastname , email , password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email 
        self.password = sha224(password).hexdigest()
    
    def __repr__(self):
        return {'id' : self.id , 'firstname': self.firstname , 'lastname': self.lastname , 'email': self.email}
