from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from base.organisations.models import Organisation
from flask import session
from base.users.models import Role, User

class RegisterForm(Form):

    def get_organisations():
        return Organisation.query

    firstname = StringField('First Name', [validators.Required()])
    lastname= StringField('Last Name', [validators.Required()])
    email= EmailField ('Email', [validators.Required()])
    username = StringField('Username', [validators.Required(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Required(),
    validators.EqualTo('confirm', message='Passwords must match'),
    validators.Length(min=4, max=80)])
    confirm = PasswordField('Confirm Password')
    is_admin = BooleanField('Admin')
    is_active = BooleanField('Active', default=True)
    #organisation = QuerySelectField('Organisation', query_factory= get_organisations, allow_blank=True)

class LoginForm(Form):
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

class RoleForm(Form):
    def get_manager():
        return Role.query.filter_by(organisation_id = session.get('organisation_id'))
    print('hello' +str(get_manager))
    name = StringField('Role Name', [validators.Required()])
    manager = QuerySelectField('Manager', query_factory= get_manager, allow_blank=True)
    is_active = BooleanField('Active', default=True)

class UserProjectForm(Form):
    def get_users():
        return User.query.filter_by(organisation_id=session.get('organisation_id'))

    def get_roles():
        return Role.query.filter_by(organisation_id=session.get('organisation_id'))

    user = QuerySelectField('User', query_factory= get_users)
    role = QuerySelectField('Role', query_factory= get_roles)

class ResetPasswordRequestForm(Form):
    email = StringField('Email', validators=[validators.Required(), validators.Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(Form):
    password = PasswordField('Password', validators=[validators.Required()])
    password2 = PasswordField('Repeat Password', validators=[validators.Required(), validators.EqualTo('password')])
    submit = SubmitField('Request Password Reset')
