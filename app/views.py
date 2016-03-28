from app import app
from flask import render_template , jsonify, request
from forms import SignUpForm, LoginForm, ItemForm
from werkzeug.datastructures import MultiDict
from app import db
from app.models import User, AuthToken, Item
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
        return bad_request_error(inputs.errors)
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


@app.route('/wishlist/<user_id>' , methods=['POST'])
def add_item(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    tokens = map(lambda x: x.token , user.tokens)
    check = check_auth_header(request.headers)
    if not check[0]:
        return check[1]
    if not authenticate_user(tokens , request.headers['AuthToken']):
        return unauthorized_message()

    data = MultiDict(mapping=request.json)
    inputs = ItemForm(data , csrf_enabled=False)
    if not inputs.validate():
        return bad_request_error(inputs.errors)
    name = data['name']
    description = data['description']
    thumbnail_url = data['thumbnail_url']
    item = Item(name, description, thumbnail_url, user_id)
    db.session.add(item)
    db.session.commit()
    response = jsonify({'name':item.name , 'description':item.description, 'thumbnail_url':item.thumbnail_url})
    response.status_code = 201
    return response

@app.route('/wishlist/<user_id>' , methods=['GET'])
def view_wishlist(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    items = map(lambda x: x.__repr__() , user.items)
    result = {'items': items , 'firstname': user.firstname , 'lastname': user.lastname}
    return json.dumps(result)

@app.route('/wishlist/<user_id>/<item_id>' , methods=['GET'])
def view_item(user_id , item_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        response = jsonify({'message':'User not found'})
        response.status_code = 404
        return response
    item_ids = map(lambda x: x.id , user.items)
    if not int(item_id) in item_ids:
        response = jsonify({'message': 'No such item'})
        response.status_code = 404
        return response
    index = item_ids.index(int(item_id))
    item = user.items[index]
    return jsonify({'name': item.name, 'description': item.description, 'thumbnailUrl': item.thumbnail_url})


@app.route('/wishlist/<user_id>/<item_id>' , methods=['DELETE'])
def delete_item(user_id , item_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        response = jsonify({'message':'User not found'})
        response.status_code = 404
        return response
    tokens = map(lambda x: x.token , user.tokens)
    check = check_auth_header(request.headers)
    if not check[0]:
        return check[1]
    if not authenticate_user(tokens , request.headers['AuthToken']):
        return unauthorized_message()
    item_ids = map(lambda x: x.id , user.items)
    if not int(item_id) in item_ids:
        response = jsonify({'message': 'No such item'})
        response.status_code = 404
        return response
    db.session.query(Item).filter_by(id=item_id).delete()
    db.session.commit()
    response = jsonify({})
    response.status_code = 204
    return response

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
    result_set = soup.find_all('img')
    for span in result_set:
        if not 'gif' in span.get('src') and not 'png' in span.get('src') and not 'sprite' in span.get('src'):
            images.append(span.get('src'))

    title = soup.find('span' , {'id':'productTitle'}).getText()
    images = map(lambda x: {'url' : x} ,images)
    result = {'images': images ,'title' : title}
    return json.dumps(result)

@app.route('/logout/<user_id>', methods=['DELETE'])
def logout(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        response = jsonify({'message':'User not found'})
        response.status_code = 404
        return response
    tokens = map(lambda x: x.token , user.tokens)
    check = check_auth_header(request.headers)
    if not check[0]:
        return check[1]
    if not authenticate_user(tokens , request.headers['AuthToken']):
        return unauthorized_message()
    db.session.query(AuthToken).filter_by(token=request.headers['AuthToken']).delete()
    db.session.commit()
    response = jsonify({})
    response.status_code = 204
    return response

def authenticate_user(tokens, token ):
    return token in tokens

def check_auth_header(headers):
    error_message = {'message' : 'You need to be logged in to perform this action'}
    if not 'AuthToken' in headers:
        response = jsonify(error_message)
        response.status_code = 401
        return [False, response]
    return [True]

def unauthorized_message():
    response = jsonify({'message' : 'You are not authorized to perform this action'})
    response.status_code = 401
    return response





@app.errorhandler(404)
def no_such_resource(e):
    response = jsonify(e)
    response.status_code = 404
    return response

def bad_request_error(errors):
    response = jsonify(errors)
    response.status_code = 400
    return response
