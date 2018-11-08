from flask_wtf import Form
from wtforms import validators, StringField, BooleanField, TextAreaField, SubmitField

class MessageForm(Form):
    to = StringField('To', validators=[validators.Required()])
    subject = StringField('Subject', validators=[validators.Required()])
    message = TextAreaField('Message', validators=[validators.Required()])
    submit = SubmitField('Send')
