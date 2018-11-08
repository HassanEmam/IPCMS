from flask_wtf import Form
from wtforms import validators, StringField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField




class SectionForm(Form):
    
    code = StringField('Code', [validators.Required()])
    name= StringField('Section Name', [validators.Required()])
    parent = QuerySelectField('Parent', allow_blank=True)
    active = BooleanField('Active', default=True)
