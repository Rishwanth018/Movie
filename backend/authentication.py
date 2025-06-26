from flask import Blueprint, request, jsonify
from models import users_collection
from utils import hash_password, check_password, generate_token

auth_bp = Blueprint('auth', __name__)

# ✅ User Signup Route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'User already exists'}), 400

    hashed_pw = hash_password(password)
    users_collection.insert_one({
        'email': email,
        'password': hashed_pw,
        'watchlist': []
    })

    return jsonify({'message': 'Signup successful'}), 201

# ✅ User Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email})
    if not user or not check_password(password, user['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = generate_token(user['_id'])
    return jsonify({'token': token}), 200
