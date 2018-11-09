from flask_wtf import Form
from wtforms import validators, StringField, TextAreaField, BooleanField, DateField
#from wtforms.fields.html5 import DateField
from flask import session
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class SubcontractorForm(Form):
    code = StringField('Code', [validators.Required()])
    name= StringField('Subcontractor Name', [validators.Required()])
    description = TextAreaField ('Description', [validators.Required()])
    address = TextAreaField('Adress', [validators.Required()])
    contact_person = StringField('Contact Person', [validators.Required()])
    contact_number = StringField('Contact Number', [validators.Required()])
    status = BooleanField('Active', default=True)

