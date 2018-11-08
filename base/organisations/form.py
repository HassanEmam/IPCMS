from wtforms import validators, StringField, TextAreaField, BooleanField
from base.users.models import User
from base.users.form import RegisterForm

class OrganisationForm(RegisterForm):
    
    def get_users():
        return User.query
    
    code = StringField('Code', [validators.Required()])
    name= StringField('Organisation Name', [validators.Required()])
    description = TextAreaField ('Description', [validators.Required()])
    is_active = BooleanField('Active', default=True)
