from flask_wtf import Form
from wtforms import validators, StringField, BooleanField

class PermissionForm(Form):

    name= StringField('Permission Name', [validators.Required()])
    is_active = BooleanField('Active')