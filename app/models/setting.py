from datetime import datetime
from base import SciurusMixin

from .. import db


class Setting(SciurusMixin, db.Model):
    #bind to the default SQLALCHEMY_DATABASE_URI
    __bind_key__ = None
#    __tablename__ = 'settings'
    DB_VERSION = 1

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=False, unique=True, index=True)
    value = db.Column(db.String(64), nullable=False)
    
    @staticmethod
    def db_version():
        db_version = Setting.query.filter_by(key='db_version').first()
        if db_version:
            return int(db_version.value)
        else:
            return 0
    
    @staticmethod
    def install():
        param = Setting(key='db_version', value=str(Setting.DB_VERSION))
        db.session.add(param)
        db.session.commit() 
