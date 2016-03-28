from . import db
from hashlib import sha224
from sqlalchemy.orm import relationship
import random
def generate_token():
    return ''.join(random.choice('012345678ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16))

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(70))
    password = db.Column(db.String(70))
    tokens = relationship('AuthToken') 
    items = relationship('Item')

    def __init__(self, firstname , lastname , email , password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email 
        self.password = sha224(password).hexdigest()
    
    def __repr__(self):
        return {'id' : self.id , 'firstname': self.firstname , 'lastname': self.lastname , 'email': self.email}

class AuthToken(db.Model):
    token = db.Column(db.String(16) , primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))

    def __init__(self , user_id):
        tokens = db.session.query(AuthToken).all()
        tokens = map(lambda x: x.token , tokens)
        token = generate_token()
        while token in tokens:
            token = generate_token()
        self.token = token
        self.user_id = user_id

class Item(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.String(2000))
    thumbnail_url = db.Column(db.String(500))
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))

    def __init__(self , name , description , thumbnail_url , user_id):
        self.name = name
        self.description = description
        self.thumbnail_url = thumbnail_url
        self.user_id = user_id

    def __repr__(self):
        return {'id' : self.id , 'name':self.name , 'description': self.description, 'thumbnail':self.thumbnail_url , 'user':self.user_id}
