from IPCMS import app, db
from base.project.form import ProjectSetupForm
from base.project.models import Project
from flask import render_template
from base.users.models import User
from base.users.decorators import *
from base.organisations.models import Organisation
from base.calendars.models import ReportingDate
from wtforms import validators
from datetime import datetime

@app.route('/newproject', methods=['POST', 'GET'])
@admin_required
def newproject():
    form = ProjectSetupForm()
    try:

        if request.method == "POST":
            print(form.validate(), request.form.get('start'))
            if session.get('organisation_id'):
                user= User.query.filter_by(id= session['user_id']).first()
                org = Organisation.query.filter_by(id= session['organisation_id']).first()
                start = datetime.strptime(request.form.get('start'), '%d/%m/%Y')
                finish = datetime.strptime(request.form.get('finish'), '%d/%m/%Y')
                print(start,finish)
                project = Project (code= form.code.data,
                                    name= form.name.data,
                                    owner= user.id,
                                    description= form.description.data,
                                    start= start,
                                    finish= finish,
                                    cycle= form.cycle.data,
                                    organisation = org,
                                    status= form.status.data)
                db.session.add(project)
                db.session.flush()
                db.session.commit()
                dates = daterange(project.start, project.finish, project.cycle.cycle_type, project.cycle.cycle_value)
                for d in dates:
                    rd = ReportingDate(project, d)
                    db.session.add(rd)
                db.session.commit()
                flash('Project has been created successully','alert-success')
                return redirect(url_for('view_projects'))
    except validators.ValidationError as e:
        flash(e, 'alert-danger')
    return render_template('project/setup.html', form=form, action='new')


@app.route('/admin', methods =['GET', 'POST'])
@admin_required
def admin():
    return render_template('project/admin.html')

@app.route('/view_projects')
@login_required
def view_projects():
    if session.get('user_id'):
        #assprojects = UserProject.query.filter_by(user_id=session['user_id'])
        projects=Project.query.filter_by(org_id= session['organisation_id'], status=True).all()
        # for prj in assprojects:
        #     projects.append(prj.project)
    #projects = Project.query.filter_by(status=True, org_id=session['organisation_id']).all()
        return render_template('project/view.html', projects=projects, organisation = Organisation.query.filter_by(id=session['organisation_id']).first())

@app.route('/viewproject/<id>')
@login_required
def project_details(id):
    session['project_id'] = id
    project = Project.query.filter_by(id= id).first()
    return render_template('project/details.html', project=project)


@app.route('/viewproject/', methods=['POST', 'GET'])
@login_required
def project_detail():
    project_id= request.form['submit']
    session['project_id']= project_id
    project = Project.query.filter_by(id= project_id).first()
    session['project'] = project.name
    if session.get('next'):
        next = session.get('next')
        session.pop('next')
        return redirect (next)
    return render_template('project/details.html', project=project)

@app.route('/delete/<id>')
@admin_required
def delete_project(id):
    project = Project.query.filter_by(id=id).first()
    project.status=False
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('view_projects'))

@app.route('/editproject/<project_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(project_id):
    project = Project.query.filter_by(id= project_id).first()
    form = ProjectSetupForm(obj= project)

    if request.method == "POST":
        start = datetime.strptime(request.form.get('start'), '%d/%m/%Y')
        finish = datetime.strptime(request.form.get('finish'), '%d/%m/%Y')
        project.code = form.code.data
        project.start = start
        project.finish = finish
        project.status = form.status.data
        project.name = form.name.data
        project.description = form.description.data
        project.cycle= form.cycle.data

        db.session.add(project)
        db.session.flush()
        db.session.commit()
        flash('Project updated successfully','alert-success')
        return redirect(url_for('view_projects'))
    return render_template('project/setup.html', form = form, project=project, action='edit')

@app.route('/view_deleted_projects')
@admin_required
def view_deleted_projects():
    if session.get('user_id'):
        projects=Project.query.filter_by(org_id= session['organisation_id'], status=False).all()
        return render_template('project/viewdeleted.html', projects=projects, organisation = Organisation.query.filter_by(id=session['organisation_id']).first())

@app.route('/restore_deleted_project/<id>')
@admin_required
def restore_project(id):
    project = Project.query.filter_by(id= id).first()
    project.status= True
    db.session.add(project)
    db.session.flush()
    db.session.commit()
    flash('Project recovered successfully','alert-success')
    return redirect(url_for('admindb'))