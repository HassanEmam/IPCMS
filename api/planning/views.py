from IPCMS import app, db
from flask import jsonify
from base.organisations.models import Organisation
from base.users.models import User
from base.users.decorators import *
from api.view import *
from planning.programme.models import Task

@app.route("/addactivities", methods="POST")
def add_activities():
    params = request.get_json()
    print(params)
