import bcrypt
import jwt
import os
from datetime import datetime, timedelta

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify password
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Generate JWT
def generate_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm='HS256')
    return token

# Verify JWT
def decode_token(token):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
