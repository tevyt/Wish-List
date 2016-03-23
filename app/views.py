from app import app
from flask import render_template , jsonify, request

@app.route('/' , methods=['GET'])
def root():
    return app.send_static_file('main.html')

@app.route('/signup', methods=['POST'])
def sign_up():
    new_user = request.get_json()


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
