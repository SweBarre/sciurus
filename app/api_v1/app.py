from flask import request, jsonify, abort
from flask.ext.restful import Resource
from ..core.security import AccessRights
from . import api
from ..core import security

class App(Resource):
    method_decorators = [security.authenticated]

    def get(self):
        """ returns the application settings """
        return_dict = {}

        # create the access rights list.
        tmp_list=[]
        for right in AccessRights:
            if not right.name=="ALL":
                tmp_list.append(right.name)
        return_dict['accessRights'] = tmp_list

        return jsonify(return_dict)


api.add_resource(App, '/app')
