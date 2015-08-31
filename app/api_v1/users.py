from flask import request, jsonify, abort
from flask.ext.restful import Resource
from ..models import User
from .. import db
from ..core.security import AccessRights, authorized
from . import api
from ..core import security, get_email_domain

class Users(Resource):
    method_decorators = [security.authenticated]

    def get(self):
        access_needed = AccessRights.USER_READ.value 
        if not security.authorized(access_needed):
            abort(401, "Not Authorized")
        elif security.authorized(access_needed, only_super=True):
            # Super user admin
            users = User.query.all()
        else:
            # Domain user admin
            users = []
            admin_maps = security.current_user.admin_domains.all()
            for admin_map in admin_maps:
                usr = User.query.filter(User.email.like( \
                        "%{0}".format(admin_map.domain.name))).all()
                users.extend(usr)

        ret_list=[]
        for user in users:
            ret_list.append(user.to_dict())
        return jsonify({'users':ret_list})

class SingleUser(Resource):
    method_decorators = [security.authenticated]

    def get(self, email):
        domain = get_email_domain(email)
        if not ( email == security.current_user.email or \
                security.authorized(AccessRights.USER_READ.value, domain=domain)):
            abort(401, "Not Authorized")

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404)
        return jsonify({'user':user.to_dict()})

    def put(self, email):
        json_user = request.get_json()
        domain = get_email_domain(email)
        if not ( email == security.current_user.email or \
                security.authorized(AccessRights.USER_EDIT.value, domain=domain)):
            abort(401, "Not Authorized")

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404, "User not found")

        # check if all user keys exists in json request
        if not (all (k in json_user for k in ( \
                'email',
                'first_name',
                'last_name',
                'enabled',
                'super_admin'))):
            abort(400, "missing user information")
        if not (user.etag == json_user['etag']):
            abort(400, "wrong etag")
        #saving user
        user.first_name = json_user['first_name']
        user.last_name = json_user['last_name']
        user.enabled = json_user['enabled']
        db.session.commit()
        return jsonify({'status':'ok', 'user':user.to_dict()})

class SetPassword(Resource):
    method_decorators = [security.authenticated]
    
    def post(self, email):
        if not ( email == security.current_user.email or \
                security.authorized(AccessRights.USER_EDIT.value, domain=domain)):
            abort(401, "Not Authorized")
        json_request = request.get_json()
        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404)
        if not (all (k in json_request for k in ( \
                'oldPassword',
                'newPassword'))):
            abort(400, 'missing parameters')
        if not user.verify_password(json_request['oldPassword']):
            abort(401, "wrong password provided")
        user.password = json_request['newPassword']
        db.session.commit()
        return jsonify({'status':'ok'})

api.add_resource(Users, '/users')
api.add_resource(SingleUser, '/users/<string:email>')
api.add_resource(SetPassword, '/users/<string:email>/password')
