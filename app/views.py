from app import app
from flask import render_template , jsonify, request
from forms import SignUpForm, LoginForm 
from werkzeug.datastructures import MultiDict
from app import db
from app.models import User, AuthToken
from hashlib import sha224
import json
from requests import get
from bs4 import BeautifulSoup
from urlparse import urljoin

@app.route('/' , methods=['GET'])
def root():
    return app.send_static_file('main.html')

@app.route('/signup', methods=['POST'])
def sign_up():
    data = MultiDict(mapping = request.json)
    inputs = SignUpForm(data , csrf_enabled=False)
    if not inputs.validate():
        bad_request_error(inputs.errors)
    else:
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        password = data['password']
        user = User(firstname , lastname , email , password)
        db.session.add(user)
        db.session.commit()
        response = jsonify(user.__repr__())
        response.status_code = 201
        return response


@app.route('/login' , methods=['POST'])
def login():
    data = MultiDict(mapping = request.json)
    inputs = LoginForm(data , csrf_enabled=False)
    if not inputs.validate():
        return bad_request_error(inputs.errors)
    else:
        data = request.get_json()
        error = {'error': 'Invalid login credentials'}
        user = db.session.query(User).filter_by(email=data['email']).first()
        if not user:
            return bad_request_error(error)
        
        hashed_password = sha224(data['password']).hexdigest()

        if user.password != hashed_password:
            return bad_request_error(error)

        token = AuthToken(user.id)
        db.session.add(token)
        db.session.commit()
        user_json = user.__repr__()
        user_json['token'] = token.token
        
        return jsonify(user_json)


@app.route('/wishlist/<user_id>' , methods=['PUT'])
def add_item(user_id):
    return 'TODO'

@app.route('/wishlist/<user_id>' , methods=['GET'])
def view_wishlist(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    items = map(lambda x: x.__repr__() , user.items)
    result = {'items': items , 'firstname': user.firstname , 'lastname': user.lastname}
    return json.dumps(result)

@app.route('/wishlist/<user_id>/<item_id>' , methods=['GET'])
def view_item(user_id , item_id):
    return 'TODO'

@app.route('/wishlist/<user_id>/<item_id>' , methods=['DELETE'])
def delete_item(user_id , item_id):
    return 'TODO'

@app.route('/wishlist', methods=['GET'])
def wish_list_index():
     users = db.session.query(User).all()
     user_list = map(lambda x: x.__repr__() , users)
     return json.dumps(user_list)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    r = get(data['url'])
    data = r.text
    soup = BeautifulSoup(data)


    images = []

    #Images from Amazon
    spans = []
    result_set = soup.find_all('span' , {'class': 'a-button-text'})
    for span in result_set:
        if span.find('img'):
            images.append(span.find('img').get('src'))
    return json.dumps(map(lambda x: {'url' : x} ,images))



@app.errorhandler(404)
def no_such_resource(e):
    response = jsonify(e)
    response.status_code = 404
    return response

def bad_request_error(errors):
    response = jsonify(errors)
    response.status_code = 400
    return response
