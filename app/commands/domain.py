from flask.ext.script import Manager
from .. import db
from ..models import Domain

DomainCommand = Manager(usage="Perform domain administration tasks")

@DomainCommand.command
def add(domain, enabled=False):
    """ Add a new domain """

    tmpD = Domain.query.filter_by(name=domain).first()
    if tmpD:
        print('Domain already exists')
    else:
        new_domain = Domain(name=domain, enabled=enabled)
        db.session.add(new_domain)
        db.session.commit()
        print('Domain {0} has been created'.format(domain))

@DomainCommand.command
def show(domain):
    """ Show domain settings for <domain>, if <domain>=all then show all"""
    print "Domain\t\tAdmins"
    if domain == "all":
        tmpD = Domain.query.all()
    else:
        tmpD = Domain.query.filter_by(name=domain)
    for dom in tmpD:
        admins = []
        for admin in dom.admin_maps.all():
            admins.append(admin.user.email)
        print "{0}\t\t{1}".format(dom.name, ", ".join(admins))

@DomainCommand.command
def delete(domain):
    """ deletes domain """
    print("#TODO: Implement code :)")
    pass
