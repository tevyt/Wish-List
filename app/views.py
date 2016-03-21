from app import app

@app.route('/' , methods=['GET'])
def root():
    return 'TODO'

@app.route('/signup', methods=['POST'])
def sign_up():
    return 'TODO'

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
