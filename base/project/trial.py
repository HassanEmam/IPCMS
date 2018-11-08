from colp import db

class UseProj(db.Model):
    __tablename__ = 'use_proj'
    left_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    right_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer)
    user = db.relationship("Use", backref="parent_assocs")

class Proj(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship("UseProj", backref="parent")

class Use(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)