'''


'''
from IPCMS import db

class Permission(db.Model):
	__tablename__ ="permissions"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	is_active = db.Column(db.Boolean)

	def __init__(self, name, is_active=True):
		self.name = name
		self.is_active= is_active
		
	def __repr__(self):
		return self.name
	
	