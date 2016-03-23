from app import app
from flask import render_template , jsonify, request
from forms import SignUpForm    
from werkzeug.datastructures import MultiDict

@app.route('/' , methods=['GET'])
def root():
    return app.send_static_file('main.html')

@app.route('/signup', methods=['POST'])
def sign_up():
    data = MultiDict(mapping = request.json)
    inputs = SignUpForm(data , csrf_enabled=False)
    if not inputs.validate():
        response = jsonify(errors = inputs.errors)
        response.status_code = 400
        return response
    else:
        response = jsonify({'test' : 'test'})
        response.status_code = 201
        return response


@app.route('/login' , methods=['POST'])
def login():
    return 'TODO'

@app.route('/wishlist/<user_id>' , methods=['PUT'])
def add_item(user_id):
    return 'TODO'

@app.route('/wishlist/<user_id>' , methods=['GET'])
def view_wishlist(user_id):
    return 'TODO'

@app.route('/wishlist/<user_id>/<item_id>' , methods=['GET'])
def view_item(user_id , item_id):
    return 'TODO'

@app.route('/wishlist/<user_id>/<item_id>' , methods=['DELETE'])
def delete_item(user_id , item_id):
    return 'TODO'

@app.errorhandler(404)
def no_such_resource(e):
    response = jsonify(e)
    response.status_code = 404
    return response
