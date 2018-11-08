'''
Calendar class maintains project calendar
It has properties as 
start date, 
reporting cycle type i.e. days, weeks, months
reporting cycle value number of periods for reports i.e. 1 month, 4 weeks, 30 days, etc.

the class has the following methods
json to convert properties to json format to store in database
save_to_db which saves the properies into the mongodb database
find_by_id this is a classmethod that returns an object for a given ID
generate_reporting_periods add reporting periods to database table for reporting

'''
import uuid
from app.common.database import Database

class Calendar(object):

	def __init__(self, code, name, cycle_type, cycle_value, project_id, _id=None):
		self.code = code
		self.name = name
		self.cycle_type = cycle_type
		self.cycle_value = cycle_value
		self.project_id = project_id
	
	def json(self):
		return {'_id': self._id,
				'code': self.code,
				'name': self.name,
				'cycle_type': self.cycle_type,
				'cycle_value': self.cycle_value,
				'project_id': self.project_id}
				
	def save_to_database(self):
		Database.insert(table= 'wbs', data= self.json())
		
	@classmethod
	def find_by_id(cls, id):
		account = Database.find_one(table= 'controlaccounts', data= {'_id': id})
		return cls(**account)
	
	@classmethod
	def exist(name, code):
		account_code = Database.find_one(table= 'controlaccounts', data= {'code': self.code})
		account_name = Database.find_one(table= 'controlaccounts', data= {'code': self.code})
		if account_code or account_name:
			return True
		else:
			return False