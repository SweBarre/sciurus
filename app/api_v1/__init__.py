from flask import Blueprint, abort
from flask.ext.restful import Api
from flask.ext.cors import CORS

api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1)
api = Api(api_v1, prefix="/api/v1")

#override api unautherized function
def unauth(resp):
    return resp
api.unauthorized = unauth
'''
def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous():
            abort(401, 'Access denied!!!!')
        return func(*args, **kwargs)
    return wrapper
'''
from . import login
from . import users
from . import app
