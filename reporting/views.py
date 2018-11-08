from IPCMS import app
from flask import render_template
from base.users.decorators import *
import json

@app.route('/report3', methods=['POST', 'GET'])

def report3():
    
    return render_template('reports/dashboard.html')
    
    
# @app.route('/report2', methods=['POST', 'GET'])
#
# def report2():
#
#     return render_template('reports/dashboard2.html')
#
# @app.route('/report', methods=['POST', 'GET'])
# @login_required
# @project_required
# def report():
#     if session.get('project_id'):
#         wwps = WWP.query.filter_by(project_id= session['project_id']).all()
#         data=[]
#         for wwp in wwps:
#             jsonWWP = wwp.to_json()
#             WWPtasks = WWPDetail.query.filter_by(wwp_id=wwp.id).all()
#             jsonTasks =[]
#             for task in WWPtasks:
#                 jsonTasks.append(task.to_json())
#             jsonWWP["tasks"] = []
#             jsonWWP["tasks"] = jsonTasks
#
#             data.append(jsonWWP)
#         data = json.dumps(data )
#     return render_template('reports/dashboard3.html',data=data)
#
# @app.route('/reportdata')
# def get_data():
#     if session.get('project_id'):
#         wwps = WWP.query.filter_by(project_id= session['project_id']).all()
#         data=[]
#         for wwp in wwps:
#             jsonWWP = wwp.to_json()
#             WWPtasks = WWPDetail.query.filter_by(wwp_id=wwp.id).all()
#             jsonTasks =[]
#             for task in WWPtasks:
#                 jsonTasks.append(task.to_json())
#                 print(jsonTasks, jsonWWP)
#             jsonWWP["tasks"] = []
#             jsonWWP["tasks"] = jsonTasks
#
#             data.append(jsonWWP)
#         data = json.dumps(data )
#         return(data)