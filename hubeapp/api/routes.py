from flask import Blueprint, jsonify, request, make_response
from hubeapp import app
from hubeapp.models.models import User, db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

mod = Blueprint('api', __name__)

@mod.route('/user', methods=['GET'])
def get_all_user():
    all_user = User.query.all()
    output = []
    for user in all_user:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['active'] = user.active
        output.append(user_data)
    return jsonify({'Users': output })

@mod.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False, active=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Message': 'New user has been created!'})

@mod.route('/user/<public_id>', methods=['GET'])
def get_single_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"Messages": "No user found!"})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    user_data['active'] = user.active

    return jsonify({"User": user_data})

@mod.route('/user/<public_id>', methods=['PUT'])
def update_user_to_admin(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'Message': 'No user found!'})
    user.admin = True
    db.session.commit()
    return jsonify({'Message': 'User has been updated to admin.'})

@mod.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'Message': 'No user found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'Message': 'User has been deleted.'})

@mod.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.JWT.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@mod.route('/item', methods=["GET"])
def all_item():
    return "{'Message': 'You are on the API'}"