from datetime import datetime
from json import dumps
from base import SciurusMixin

from .. import db

class Domain(SciurusMixin, db.Model):
    __bind_key__ = None
    __tablename__ = 'domains'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    admin_maps = db.relationship('AdminMap', backref='domain_admin', lazy='dynamic')
    enabled = db.Column(db.Boolean, default=False)
