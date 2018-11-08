'''


'''
from IPCMS import db
from datetime import datetime


#from users.models import User

class Message(db.Model):
    __tablename__ ="messages"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender= db.relationship('User', foreign_keys=[sender_id])
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient = db.relationship('User', foreign_keys=[recipient_id])
    body = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read = db.Column(db.Boolean)
    is_active= db.Column(db.Boolean)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


