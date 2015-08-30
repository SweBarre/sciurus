import os
from datetime import datetime
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

CONFIG_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'config.py'
)

if os.path.isfile(CONFIG_FILE):
    from config import configurations

db = SQLAlchemy()

from app.models import User
'''
@login_manager.request_loader
def load_user_from_request(request):
    print request.headers
    token = request.headers.get('X-Auth-Token')
    if token:
        user = User.verify_auth_token(token)
        if user:
            return user
    return None
'''
def not_found(error):
    response = jsonify({'code': 404,'message': 'No interface defined for URL'})
    response.status_code = 404
    return response


def create_config():
    import sys
    while True:
        answer = raw_input(
            'No configuration found, do you want to create it [y/N]'
        )
        if answer.upper() in ['Y', 'YES', 'N', 'NO', '']:
            break
    if answer.upper() in ['N', 'NO', '']:
        sys.exit('No configuration found, quitting!')
    from create_config import create_config_file
    create_config_file()


def create_app(config):
    if config is None:
        config = 'dev'
    if not os.path.isfile(CONFIG_FILE):
        create_config()
    #Create Flask application
    app = Flask(__name__)
    app.config.from_object(configurations[config])

    #set 404 errors to the not_found function
    app.error_handler_spec[None][404] = not_found

    #Init flask extentinons
    db.init_app(app)
    with app.app_context():
        from models import Setting
        try:
            db_version = Setting.db_version()
            if db_version < Setting.DB_VERSION:
                #TODO: Implement settings db upgrade code
                print " * Upgrading the settings database"
        except:
            pass
    
    from .api_v1 import api_v1
    app.register_blueprint(api_v1)

    return app
