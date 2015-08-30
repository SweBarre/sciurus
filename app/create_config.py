#!/usr/bin/env python
import os
import sys

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.py')
CONFIG_FILE_TEMPLATE = """class BaseConfig(object):
    # Application Settins
    DEBUG = False
    TESTING = False
    #X_AUTH_TOKEN_TIMEOUT = 600

class ProductionConfig(BaseConfig):
    SECRET_KEY = '{{secret_key_prod}}'
    SQLALCHEMY_DATABASE_URI = '{{db_uri_production}}'
    SQLALCHEMY_BINDS = {
            'amavis': '{{db_uri_production_amavis}}',
            'spamassassin': '{{db_uri_production_spamassassin}}'
    }
                        

class DevelopmentConfig(BaseConfig):
    SECRET_KEY = '{{secret_key_dev}}'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = '{{db_uri_development}}'
    SQLALCHEMY_BINDS = {
        'amavis': '{{db_uri_development_amavis}}',
        'spamassassin': '{{db_uri_development_spamassassin}}'
    }


class TestConfig(BaseConfig):
    SECRET_KEY = '{{secret_key_test}}'
    TESTING = True
    # In memory DB
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_BINDS = {
        'amavis': 'sqlite://',
        'spamassassin': 'sqlite://'
    }

configurations = { 'prod': ProductionConfig,
                   'test' : TestConfig,
                    'dev' : DevelopmentConfig 
                 }
"""

config ={}

def create_settings_db(config):
    
    def create_connection_string(database):
        from getpass import getpass
        print " {0} settings:".format(database)
        server = "localhost"
        user = database.lower()
        database = database.lower()
        
        input_var = raw_input("   server [{0}] : ".format(server))
        if input_var != "":
            server = input_var
        
        input_var = raw_input("   database [{0}] : ".format(database))
        if input_var != "":
            database = input_var

        input_var = raw_input("   user [{0}] : ".format(user))
        if input_var != "":
            user = input_var

        password = getpass("   password : ")

        print ""
        return 'mysql://{user}:{password}@{server}/{database}'.format(
                user=user,
                password=password,
                database=database,
                server=server )

    print "MySQL settings for {0} configuration".format(config)
    print "-" * (len(config) + 33)

    return_dict = {}
    return_dict['db_uri_{0}'.format(config.lower())] = create_connection_string('Sciurus')
    return_dict['db_uri_{0}_amavis'.format(config.lower())] = create_connection_string('Amavis')
    return_dict['db_uri_{0}_spamassassin'.format(config.lower())] = create_connection_string('Spamassassin')

    return return_dict


def generate_key():
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.letters + string.digits + '#$%&()*+,-./:;<=>?@[]^_') for _ in xrange(50))

def create_config_file():
    import sys
    print("\nCreating Configuration file")
    print("---------------------------")
    print(" * Creating secret keys:")
    print("    - Production")
    config['secret_key_prod'] = generate_key()
    print("    - Development")
    config['secret_key_dev'] = generate_key()
    print("    - Test")
    config['secret_key_test'] = generate_key()
    
    config.update(create_settings_db('Production'))
    config.update(create_settings_db('Development'))
    #get database info
    #config['db_uri_prod'] = create_settings_db('Production')
    #config['db_uri_dev'] = create_settings_db('Development')


    cfgContent = CONFIG_FILE_TEMPLATE
    for cfg_item in config.keys():
        cfgContent = cfgContent.replace("{{"+cfg_item+"}}",config[cfg_item])
    
    print(" * Saving file")
    f = open(CONFIG_FILE, "w")
    f.write(cfgContent)
    f.close()
    print(" * Securing file")
    os.chmod(CONFIG_FILE, 0640)
    print(" * Done!")
    sys.exit()

    

if __name__ == '__main__':
    create_config_file()
