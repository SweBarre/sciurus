virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
npm install

cp spa/config.js.template spa/config.js

* edit the spa/config to point to the correct backend address
sciurus.constant('CONFIG', {
        'apiURL' : 'http://127.0.0.1:5000/api/v1/'
});


grunt

* create config file
python manage.py shell

* change development config to use sqlite
class DevelopmentConfig(BaseConfig):                                            
    SECRET_KEY = 'e4>xRSG15dSMFn*FY^#pR&[^3ZK?TS_Kyz32kaS@Aj#(>oM<L+'           
    DEBUG = True                                                                
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/sciurus.db'    
    SQLALCHEMY_BINDS = {                                                        
            'amavis': 'sqlite:////tmp/amavis.db',            
            'spamassassin': 'sqlite:////tmp/spam.db'         
    } 

* init the sciurus database
python manage.py db init sciurus

* add the first domain
python manage.py domain add example.tld

* add the first super admin
python manage.py user add super@example.tld -s -e

* start the backend 
python manage.py runserver

* start the frontend
cd www-root
python -m SimpleHTTPServer

