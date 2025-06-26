from flask import Blueprint, request, jsonify
from models import users_collection
from utils import decode_token
from bson import ObjectId

watchlist_bp = Blueprint('watchlist', __name__)

# 🔐 Helper: get user from token
def get_user_from_token():
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        user_id = decode_token(token.split(' ')[1])
        return user_id
    return None

# ✅ GET /api/watchlist - Get user's watchlist
@watchlist_bp.route('/', methods=['GET'])
def get_watchlist():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = users_collection.find_one({'_id': ObjectId(user_id)})
    return jsonify({'watchlist': user.get('watchlist', [])})

# ✅ POST /api/watchlist - Add a movie to watchlist
@watchlist_bp.route('/', methods=['POST'])
def add_to_watchlist():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    movie = request.json
    users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$addToSet': {'watchlist': movie}}  # Prevent duplicates
    )
    return jsonify({'message': 'Movie added to watchlist'})

# ✅ DELETE /api/watchlist - Remove a movie
@watchlist_bp.route('/', methods=['DELETE'])
def remove_from_watchlist():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    movie_id = request.json.get('id')  # The movie's unique TMDb id

    users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$pull': {'watchlist': {'id': movie_id}}}
    )
    return jsonify({'message': 'Movie removed from watchlist'})
