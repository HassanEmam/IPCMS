'''
Calendar class maintains project calendar
It has properties as 
start date, 
reporting cycle type i.e. days, weeks, months
reporting cycle value number of periods for reports i.e. 1 month, 4 weeks, 30 days, etc.


'''
from IPCMS import db
from datetime import datetime

class ReportingCycle(db.Model):
	__tablename__ = 'reportingcycles'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(80))
	name = db.Column(db.String(80))
	cycle_type = db.Column(db.Text)
	cycle_value = db.Column(db.Integer)
	week_start = db.Column(db.Text)
	#project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
	#project = db.relationship('Project', backref='ReportingCalendar')
	organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
	organisation= db.relationship('Organisation', backref='cycles')
	is_active = db.Column(db.Boolean)
	
	__table_args__ = (
		db.UniqueConstraint('code', 'organisation_id', name='uix_rc1'),
	)
	
	def __init__(self, code, name, cycle_type, cycle_value, week_start, organisation, is_active = True):
		self.code = code
		self.name = name
		self.cycle_type = cycle_type
		self.cycle_value = cycle_value
		#self.project_id = project.id
		self.week_start = week_start
		self.organisation_id = organisation.id
		self.is_active = is_active

	def __repr__(self):
		return self.name
		
class ReportingDate(db.Model):
	__tablename__ = 'reportingdates'
	id = db.Column(db.Integer, primary_key=True)
	rdate = db.Column(db.DateTime)
	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
	project = db.relationship('Project', backref='ReportingDate')
	is_active = db.Column(db.Boolean)
	status = db.Column(db.Boolean)
	
	def __init__(self, project, rdate, is_active=True, status=False):
		self.project_id= project.id
		self.rdate = rdate
		self.is_active = is_active
		self.status = status
	
	def __repr__(self):
		dd = datetime.strptime(str(self.rdate), '%Y-%m-%d %H:%M:%S').strftime("%d-%b-%Y")
		return str(dd)