from .. import db
from datetime import datetime
from hashlib import sha1

from sqlalchemy.ext.declarative import declared_attr

class SciurusMixin(object):
    """ Base model for the Sciurus app """
    
    #attributes that should be hidden in self.to_dict
    __no_dict__ = []

    # Attributes that should be excluded from etag 
    __no_etag__ = []

    id =  db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    modified_at = db.Column(db.DateTime(), default=datetime.utcnow)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        """ returns columns as a dictionary """
        return_dict = {}
        columns = self.__table__.columns.keys()
        for key in columns:
            value = getattr(self, key)
            if isinstance(value, datetime):
                value = value.isoformat()
            if key in self.__no_dict__:
                continue
            return_dict[key] = value
        return_dict['etag'] = self.etag
        return return_dict

    @property
    def etag(self):
        columns = self.__table__.columns.keys()
        string = ""
        for key in columns:
            if key in self.__no_etag__:
                continue
            value = getattr(self, key)
            if isinstance(value, datetime):
                value = value.isoformat()
            string += str(value)
        return_hash = sha1()
        return_hash.update(string)
        return return_hash.hexdigest()

    @etag.setter
    def etag(self):
        raise AttributeError('etag is not settable!!')

