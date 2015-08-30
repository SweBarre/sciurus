from flask import request, jsonify, abort
from flask.ext.restful import Resource
from ..models import User
from . import api
from ..core.security import authenticated

class Login(Resource):
    def post(self):
        json_request = request.get_json()
        if not "email" in json_request or not "password" in json_request:
             # Throw a bad request
             abort(400)
        user = User.query.filter_by(email=json_request['email']).first()
        if user is None or not user.verify_password(json_request['password']):
            abort(401) #Unathorized
        return jsonify({ 'token': user.generate_auth_token(),
                         'user': user.to_dict()})

class CheckLogin(Resource):
    method_decorators = [authenticated]

    def get(self):
        return jsonify({'status':'OK'})

api.add_resource(Login, '/login')
api.add_resource(CheckLogin, '/login/check')
