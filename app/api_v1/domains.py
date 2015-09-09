from flask import request, jsonify, abort
from flask.ext.restful import Resource
from ..models import Domain
from .. import db
from ..core.security import AccessRights, authorized
from . import api
from ..core import security, get_email_domain

class Domains(Resource):
    method_decorators = [security.authenticated]

    def get(self):
        access_needed = AccessRights.DOMAIN_READ.value 
        if not security.authorized(access_needed):
            abort(401, "Not Authorized")
        elif security.authorized(access_needed, only_super=True):
            # Super user admin
            domains = Domain.query.all()
        else:
            # Domain user admin
            domains = []
            admin_maps = security.current_user.admin_domains.all()
            for admin_map in admin_maps:
                dom = Domain.query.filter_by(name=admin_map.domain.name).first()
                domains.extend(dom)

        ret_list=[]
        for domain in domains:
            ret_list.append(domain.to_dict())
        return jsonify({'domains':ret_list})

api.add_resource(Domains, '/domains')
