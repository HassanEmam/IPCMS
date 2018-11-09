from IPCMS import app, db
from estimating.subcontractors.form import SubcontractorForm
from estimating.subcontractors.models import Subcontractor
from flask import render_template
from base.users.models import User
from base.users.decorators import *
from base.organisations.models import Organisation
from wtforms import validators
from datetime import datetime

@app.route('/newsubcontractor', methods=['POST', 'GET'])
@admin_required
def new_subcontractor():
    form = SubcontractorForm()
    try:

        if request.method == "POST":
            if session.get('organisation_id'):
                user= User.query.filter_by(id= session['user_id']).first()
                org = Organisation.query.filter_by(id= session['organisation_id']).first()
                subcontractor = Subcontractor (code= form.code.data,
                                    name= form.name.data,
                                    description= form.description.data,
                                    address=form.address.data,
                                    contact_number= form.contact_number.data,
                                    contact_person= form.contact_person.data,
                                    organisation = org,
                                    subcontractor = form.subcontractor.data)
                db.session.add(subcontractor)
                db.session.flush()
                db.session.commit()

                flash('Subcontractor has been created successully','alert-success')
                return redirect(url_for('view_subcontractors'))
    except validators.ValidationError as e:
        flash(e, 'alert-danger')
    return render_template('estimating/subcontractors/setup.html', form=form, action='new')




@app.route('/view_subcontractors')
@login_required
def view_subcontractors():
    if session.get('user_id'):
        subcontractors=Subcontractor.query.filter_by(org_id= session['organisation_id'], status=True).all()
        return render_template('estimating/subcontractors/view.html', subcontractors=subcontractors, organisation = Organisation.query.filter_by(id=session['organisation_id']).first())

@app.route('/view_subcontractor/<id>')
@login_required
def subcontractor_details(id):
    subcontractor = Subcontractor.query.filter_by(id= id).first()
    return render_template('estimating/subcontractors/details.html', subcontractor=subcontractor)


@app.route('/delete/<id>')
@admin_required
def delete_subcontractor(id):
    subcontractor = Subcontractor.query.filter_by(id=id).first()
    subcontractor.status=False
    db.session.add(subcontractor)
    db.session.commit()
    return redirect(url_for('view_subcontractors'))

@app.route('/edit_subcontractor/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subcontractor(id):
    subcontractor = Subcontractor.query.filter_by(id= id).first()
    form = SubcontractorForm(obj= subcontractor)

    if request.method == "POST":
        subcontractor.code = form.code.data
        subcontractor.name = form.name.data
        subcontractor.description = form.description.data
        subcontractor.contact_person = form.contact_person.data
        subcontractor.address = form.address.data
        subcontractor.contact_number = form.contact_number.data
        subcontractor.subcontractor = form.subcontractor.data

        db.session.add(subcontractor)
        db.session.flush()
        db.session.commit()
        flash('Subcontractor has been updated successfully','alert-success')
        return redirect(url_for('view_subcontractors'))
    return render_template('estimating/subcontractors/setup.html', form = form, subcontractor=subcontractor, action='edit')

# @app.route('/view_deleted_projects')
# @admin_required
# def view_deleted_projects():
#     if session.get('user_id'):
#         projects=Project.query.filter_by(org_id= session['organisation_id'], status=False).all()
#         return render_template('project/viewdeleted.html', projects=projects, organisation = Organisation.query.filter_by(id=session['organisation_id']).first())
#
# @app.route('/restore_deleted_project/<id>')
# @admin_required
# def restore_project(id):
#     project = Project.query.filter_by(id= id).first()
#     project.status= True
#     db.session.add(project)
#     db.session.flush()
#     db.session.commit()
#     flash('Project recovered successfully','alert-success')
#     return redirect(url_for('admindb'))