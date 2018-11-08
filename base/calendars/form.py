"""


"""

from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, TextAreaField, BooleanField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#from project.models import Project

class CycleForm(Form):
    
        
    def get_cycle_types():
        return ['Days', 'Weeks', 'Months']
    
    code = StringField('Code', [validators.Required()])
    name= StringField('Calendar Name', [validators.Required()])
    cycle_type = SelectField(choices=[('day', 'Days'), ('week', 'Weeks'), ('month', 'Months')])
    cycle_value = IntegerField('Cycle Value', [validators.Required()])
    #project = QuerySelectField('Project', query_factory= get_projects, allow_blank=True)
    week_start = SelectField(u'Week Starts On', choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3','Thursday'), ('4','Friday'), ('5','Saturday'), ('6','Sunday')])

    is_active = BooleanField('Active', default=True)
