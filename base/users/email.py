# users/email.py

from flask_mail  import Message
from flask import render_template
from IPCMS import app, mail

app.config.from_object('settings')
app.config["MAIL_SERVER"] = "mail.emamology.com"
app.config["MAIL_PORT"] = 26
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = 'info@emamology.com'
app.config["MAIL_PASSWORD"] = 'Hassan81'

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Emamology] Reset Your Password',
               sender="Emamology <hassan@emamology.com>",
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))