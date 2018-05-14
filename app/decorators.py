from functools import wraps
from flask import request
from .models import User

def token_required(func):
    '''checks validity of tokens'''
    @wraps(func)
    def decorated(*args, **kwargs):
        access_token = None
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header:
                access_token = authorization_header.split(' ')[1]
            if access_token:
                username = User.decode_token(access_token)
                user = User.query.filter_by(username=username).first()
                return func(user=user, *args, **kwargs)
            return {'message':"Please login first, your session might have expired"}, 401
        except Exception as e:
            return {'message': 'An error occured', 'error':str(e)},400
    return decorated

def admin_token_required(func):
    '''check users have valid tokens and have admin property'''
    @wraps(func)
    def decorated(*args, **kwargs):
        access_token = None
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header:
                access_token = authorization_header.split(' ')[1]
            if access_token:
                username = User.decode_token(access_token)

                user = User.get(username=username)
                if user.admin == True:
                    return func(user=user, *args, **kwargs)
                return {'message': 'Unauthorized'}, 401
            return {'message':"Please login first, your session might have expired"}, 401
        except Exception as e:
            return {'message': 'An error occured', 'error':str(e)},400
    return decorated

