import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

smtp = smtplib.SMTP()
smtp.connect('localhost')


def send_email(subject, sender, recipients, text_body, html_body):
    msgRoot = MIMEMultipart("alternative")
    msgRoot['Subject'] = Header(subject, "utf-8")
    msgRoot['From'] = sender
    msgRoot['To'] = recipients
    text = MIMEText(open(text_body, 'r').read(), "plain", "utf-8")
    msgRoot.attach(text)
    html = MIMEText(open(html_body, 'r').read(), "html", "utf-8")
    msgRoot.attach(html)
    smtp.sendmail(sender, recipients, msgRoot.as_string())


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Constology] Reset Your Password',
               sender="info@conoccult.com",
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
