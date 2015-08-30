from flask.ext.script import Manager
from .. import db
import sys

DbCommand = Manager(usage="Perform database administration tasks [Sciurus, Amavis, Spamassassin]")

@DbCommand.command
def init(database):
    """ Initialize database """
    database=database.lower()
    if database == 'sciurus':
        database = None
    elif database == 'amavis' or database == 'spamassassin':
        pass
    else:
        sys.exit('Unknown database')

    db.create_all(bind=database)

    if database == None:
        #Fill with default data
        from ..models import Setting, Domain
        Setting.install()


    print " * Done"
