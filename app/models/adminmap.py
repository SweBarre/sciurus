from datetime import datetime

from .. import db
from user import User

class AdminMap(db.Model):
    __bind_key__ = None
    __tablename__ = 'admin_maps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))
    access = db.Column(db.Integer)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    user = db.relationship("User")
    domain = db.relationship("Domain")
