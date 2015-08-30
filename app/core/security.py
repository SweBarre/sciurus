import os
import hashlib
import getpass
import base64
from enum import Enum
from flask import request, abort
from functools import wraps

current_user = None

class AccessRights(Enum):
    DOMAIN_FULL = 0x800
    DOMAIN_EDIT = 0x400
    DOMAIN_READ = 0x200
    USER_FULL = 0x100
    USER_EDIT = 0x80
    USER_READ = 0x40
    AMAVIS_FULL = 0x20
    AMAVIS_EDIT = 0x10
    AMAVIS_READ = 0x8
    QUARANTINE_FULL = 0x4
    QUARANTINE_EDIT = 0x2
    QUARANTINE_READ = 0x1

def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global current_user
        token = request.headers.get('X-Auth-Token')
        if token:
            from ..models import User
            user = User.verify_auth_token(token)
            if user:
                current_user = user
            else:
                abort(401, 'Access denied!!!!')
        else:
            abort(401, 'Access denied!')
        return func(*args, **kwargs)
    return wrapper

def _checkAuth(access, checking):
    #check if the autherize bit is set.
    if access & checking:
        return True

    #check if access is _READ and check is _EDIT or _FULL
    if AccessRights(access).name.endswith('_READ'):
        check_tmp = checking >> 1
        if access & check_tmp:
            return True
        check_tmp = check_tmp >> 1
        if access & check_tmp:
            return True

    # check ig access is _EDIT and if check is _FULL
    if AccessRights(access).name.endswith('_EDIT'):
        checking = checking >> 1
        if access & checking:
            return True

    # not autherized
    return False


def authorized(access,
               user=None,
               domain=None,
               only_super=False):
    if user==None:
        user = current_user
    #check if user has super admin for specific access
    if _checkAuth(access, user.super_admin):
        return True
    if only_super:
        return False
    #the access is for all domains.
    if domain==None:
    	admin_maps = user.admin_domains.all()
    	for admin_map in admin_maps:
        	if _checkAuth(access, admin_map.access):
            	    return True
    	return False
    else:
        # just check to see if user has access in a particular domain
        from ..models import Domain
        domain = Domain.query.filter_by(name=domain).first()
        if not domain:
            abort(404, 'Domain not found')
        print domain.name
        admin_map = user.admin_domains.filter_by(domain_id=domain.id).first()
        if not admin_map:
            return False
        return _checkAuth(access, admin_map.access)

    return False


def create_admin_list(access):
    if not access:
        return False
    return_list = []
    for accessRight in AccessRights:
        if access & accessRight.value:
            return_list.append(accessRight.name)
    return return_list


def generate_password_hash(password, salt=None):
    if salt == None:
        # Generate a 5 byte random salt
        salt = os.urandom(5)
    # Hash our password + salt
    sha = hashlib.sha512()
    sha.update(password)
    sha.update(salt)
    ssha512 = base64.b64encode('{}{}'.format(sha.digest(), salt))
    # Print it out with a prefix for Dovecot

    return "{{SSHA512}}{}".format(ssha512)

def check_password_hash(password_hash, password):
    #get the salt from the passward hash
    striped = password_hash.replace('{SSHA512}','')
    decoded = base64.b64decode(striped)
    salt = decoded[64::]

    if password_hash == generate_password_hash(password, salt=salt):
        return True
    else:
        return False
