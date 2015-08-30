from flask.ext.script import Manager
from .. import db
from ..models import User, Domain, AdminMap
from ..core import get_email_domain, security
import sys

UserCommand = Manager(usage="Perform user administration tasks")

@UserCommand.command
def add(email, enabled=False, admin=False, super_admin=False, first_name=None , last_name=None):
    """ Register a new user """

    # check if the domain exists
    tmpDomain = Domain.query.filter_by(name=get_email_domain(email)).first()
    if not tmpDomain:
        print("Target domain [{0}] doesn't exist".format(get_email_domain(email)))
        return
    
    tmpU = User.query.filter_by(email=email).first()
    admin_access = 0
    for accessRight in security.AccessRights:
        admin_access = admin_access | accessRight.value
    if tmpU:
        print('User {email} already exists'.format(email=email))
    else:
        from getpass import getpass
        password = getpass()
        password2 = getpass(prompt='Confirm: ')
        if password != password2:
            import sys
            sys.exit('Error: Passwords dont match')
        user = User(
                email=email, 
                password=password, 
                enabled=enabled,
                first_name=first_name,
                last_name=last_name)

        if super_admin:
            user.super_admin = admin_access
            print('User {email} has been added as super-admin'.format(email=email))
        db.session.add(user)
        db.session.commit()
        if admin:
            adminmap = AdminMap(user_id=user.id,
                                domain_id=tmpDomain.id,
                                access=admin_access
                                )
            db.session.add(adminmap)
            db.session.commit()
            print('User {email} has been added as admin for {domain}'.format(
                email=email,
                domain=tmpDomain.name))
        print('User {email} has been created'.format(email=email))

@UserCommand.command
def delete(email):
    """ deletes a user """
    print("#TODO: Implement code :)")
    pass
