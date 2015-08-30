#!/usr/bin/env python
from app import create_app
from app.commands import UserCommand, DbCommand, DomainCommand
from app.models import User
from flask.ext.script import Manager

manager = Manager(create_app)

manager.add_command('user', UserCommand)
manager.add_command('db', DbCommand)
manager.add_command('domain', DomainCommand)

manager.add_option('-c', '--config', dest='config', required=False)

if __name__ == '__main__':
    manager.run()
