'''


'''
from IPCMS import db


class Resource(db.Model):
    __tablename__ = "rsrc_types"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    type_id = db.Column(db.Integer, db.ForeignKey('rsrc_types.id'))
    type = db.relationship('RSRCType', backref='resources')
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    organisation = db.relationship('Organisation', backref='rsrctypes')
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, code, name, type, organisation, is_active=True):
        self.code = code
        self.name = name
        if type:
            self.type_id = type.id
        if organisation:
            self.organisation_id = organisation.id
        self.is_active = is_active

    def __repr__(self):
        return self.name

