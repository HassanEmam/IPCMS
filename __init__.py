from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)
app.config["MAIL_SERVER"] = "mail.emamology.com"
app.config["MAIL_PORT"] = 26
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = 'info@emamology.com'
app.config["MAIL_PASSWORD"] = 'Hassan81'
mail = Mail(app)
CORS(app)

#Migration
migrate= Migrate(app, db)
from base.users import views
from base.project import views
from base.organisations import views
from base.calendars import views
from base.sections import views
from base.permissions import views
from base.calendars import views
from reporting import views
from base.contact import views
from base.messages import views
from estimating.companies import views
from estimating.subcontractors import views
from api import view
from api.estimating import views
from api.planning import views