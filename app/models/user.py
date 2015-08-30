from datetime import datetime
from hashlib import sha1
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask import current_app, abort
from sqlalchemy import or_
from base import SciurusMixin
from ..core import security

from .. import db


class User(SciurusMixin, db.Model):
    __bind_key__ = None
    __tablename__ = 'users'
    __no_dict__ = ['password_hash']
    __no_etag__ = ['password_hash', 'last_login']
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(254), nullable=True)
    last_name = db.Column(db.String(254), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    enabled = db.Column(db.Boolean, default=False)
    admin_domains = db.relationship('AdminMap', backref='admin', lazy='dynamic')
    last_login = db.Column(db.DateTime())
    super_admin = db.Column(db.Integer, default=0)

    @property
    def password(self):
        raise AttributeError('Passwords are not readable!!')

    @password.setter
    def password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def verify_password(self, password):
        return security.check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=False):
        if not expiration:
            expiration = current_app.config['X_AUTH_TOKEN_TIMEOUT']
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            abort(401, "Token signature expired")
        except BadSignature:
            abort(401, "Bad token signature!")
        except:
            abort(500)
        user = User.query.get(data.get('id'))
        return user

    def to_dict(self):
        return_dict = super(User, self).to_dict()
        #create the list for the domains where user is admin
        admin_maps = self.admin_domains.all()
        if not admin_maps:
            return_dict['admin'] = False
            return_dict['is_admin'] = False
        else:
            domains_list=[]
            return_dict['is_admin'] = True
            for admin_map in admin_maps:
                domain_dict={}
                domain_dict['name'] = admin_map.domain.name
                domain_dict['access'] = security.create_admin_list(admin_map.access)
                domains_list.append(domain_dict)
            return_dict['admin'] = domains_list
        # Create the super_admin list
        return_dict['super_admin'] = security.create_admin_list(self.super_admin)
        if return_dict['super_admin']:
            return_dict['is_admin'] = True
        return return_dict
