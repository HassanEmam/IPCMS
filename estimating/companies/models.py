'''


'''
from IPCMS import db


class Company(db.Model):
	__tablename__ ="companies"
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(80), unique=True)
	name = db.Column(db.String(80))
	description = db.Column(db.Text)
	address = db.Column(db.Text)
	contact_number = db.Column(db.Text)
	contact_person = db.Column(db.Text)
	org_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
	organisation= db.relationship('Organisation', backref='company')
	status = db.Column(db.Boolean, default=True)

	__table_args__ = (
		db.UniqueConstraint('code', 'org_id', name='uix_prj1'),
	)

	def __init__(self, code, name, description, address, contact_number, contact_person, organisation, status=True):
		self.code = code
		self.name = name
		self.description = description
		self.address = address
		self.constact_person = contact_person
		self.contact_number = contact_number
		self.org_id = organisation.id

	def __repr__(self):
		return self.name
	
	