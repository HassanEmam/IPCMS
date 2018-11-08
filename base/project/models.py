'''


'''
from IPCMS import db


class UserProject(db.Model):
	__tablename__ = 'user_project'
	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	role_id = db.Column(db.Integer)
	user = db.relationship("User", backref="parent_assocs")
	project = db.relationship("Project", backref="assoc")
	is_active = db.Column(db.Boolean)
	
	__table_args__ = (
		db.UniqueConstraint('project_id', 'user_id', name='uix_1'),
	)
	def __init__(self, project, user, role, is_active=True):
		self.project_id = project.id
		self.user_id = user.id
		self.role_id = role.id
		self.is_active= is_active



class Project(db.Model):
	__tablename__ ="projects"
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(80), unique=True)
	name = db.Column(db.String(80))
	owner = db.Column(db.Integer, db.ForeignKey('users.id'))
	description = db.Column(db.Text)
	start = db.Column(db.DateTime)
	finish = db.Column(db.DateTime)
	cycle_id = db.Column(db.Integer, db.ForeignKey('reportingcycles.id'))
	cycle= db.relationship('ReportingCycle', backref='project')
	org_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
	organisation= db.relationship('Organisation', backref='project')
	status = db.Column(db.Boolean, default=True)
	users = db.relationship("UserProject")

	__table_args__ = (
		db.UniqueConstraint('code', 'org_id', name='uix_prj1'),
	)

	def __init__(self, code, name, description, owner, start, finish, cycle, organisation, status):
		self.code = code
		self.name = name
		self.owner = owner
		self.description = description
		self.start = start
		self.finish = finish
		self.status = status
		self.org_id= organisation.id
		self.cycle_id= cycle.id
		
	def __repr__(self):
		return self.name
	
	