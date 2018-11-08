from IPCMS import db, app
from datetime import datetime
import jwt
from time import time

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key =True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(35), unique =True)
    username = db.Column(db.String(80), unique= True)
    password = db.Column(db.String(80))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    organisation= db.relationship('Organisation', backref='users')
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)


    def __init__(self, firstname, lastname, email, username, password, organisation, is_admin=False, is_active=True, confirmed=False, confirmed_on= None):
        self.firstname = firstname
        self.email = email
        self.lastname = lastname
        self.password = password
        self.is_admin = is_admin
        self.username = username
        if organisation:
            self.organisation_id = organisation.id
        self.is_active= is_active
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return self.username

class UserLog(db.Model):
    __tablename__='users_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    success = db.Column(db.Boolean)
    ipaddr = db.Column(db.String(40))

    def __init__(self, user_id, success, ipaddr, date=None):
        self.user_id = user_id
        self.date = datetime.now()
        self.success = success
        self.ipaddr = ipaddr

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self, read=False).count()

    def __repr__(self):
        return 'user:' + str(self.user_id) + ' logged on: ' + str(self.date)


class Role(db.Model):
    __tablename__='roles'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(80))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    organisation = db.relationship('Organisation', backref='roles')
    manager_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    manager = db.relationship(lambda: Role, remote_side=id,backref='subs')
    is_active = db.Column(db.Boolean, default=True)
    __table_args__ = (
		db.UniqueConstraint('name', 'organisation_id', name='uix_rol1'),
	)
    def __init__(self, name, organisation, manager, is_active=True):
        self.name = name
        if organisation is not None:
            self.organisation_id = organisation.id
        if manager is not None:
            self.manager_id = manager.id
        self.is_active = is_active

    def __repr__(self):
        return self.name