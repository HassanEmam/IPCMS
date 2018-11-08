'''


'''
from IPCMS import db

class Section(db.Model):
	__tablename__ ="sections"
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(80), unique=True)
	name = db.Column(db.String(80))
	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
	project= db.relationship('Project', backref='section')
	parent_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
	parent = db.relationship(lambda: Section, remote_side=id, backref='subs')
	
	active = db.Column(db.Boolean)
	__table_args__ = (
		db.UniqueConstraint('code', 'project_id', name='uix_sec1'),
	)
	def __init__(self, code, name, project, parent, active=True):
		self.code = code
		self.name = name
		self.active = active
		self.project_id = project.id
		self.parent = parent
		if parent:
			self.parent_id= parent.id
		
	def json(self):
		return ({"name": self.name , "id": str(self.id) ,
                "parent_id": str(self.parent_id), 
                "level": 0,
                "childs":[ ]})
		
	def __repr__(self):
		return self.name
	
	