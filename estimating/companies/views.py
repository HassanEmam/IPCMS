from IPCMS import app, db
from estimating.companies.form import CompanyForm
from estimating.companies.models import Company
from flask import render_template
from base.users.models import User
from base.users.decorators import *
from base.organisations.models import Organisation
from wtforms import validators
from datetime import datetime

@app.route('/newcompany', methods=['POST', 'GET'])
@admin_required
def new_company():
    form = CompanyForm()
    try:

        if request.method == "POST":
            if session.get('organisation_id'):
                user= User.query.filter_by(id= session['user_id']).first()
                org = Organisation.query.filter_by(id= session['organisation_id']).first()
                company = Company (code= form.code.data,
                                    name= form.name.data,
                                    description= form.description.data,
                                    address=form.address.data,
                                    contact_number= form.contact_number.data,
                                    contact_person= form.contact_person.data,
                                    organisation = org)
                db.session.add(company)
                db.session.flush()
                db.session.commit()

                flash('Company has been created successully','alert-success')
                return redirect(url_for('view_companies'))
    except validators.ValidationError as e:
        flash(e, 'alert-danger')
    return render_template('estimating/companies/setup.html', form=form, action='new')




@app.route('/view_companies')
@login_required
def view_companies():
    if session.get('user_id'):
        companies=Company.query.filter_by(org_id= session['organisation_id'], status=True).all()
        return render_template('estimating/companies/view.html', companies=companies, organisation = Organisation.query.filter_by(id=session['organisation_id']).first())

@app.route('/view_company/<id>')
@login_required
def company_details(id):
    company = Company.query.filter_by(id= id).first()
    return render_template('estimating/companies/details.html', company=company)


@app.route('/delete/<id>')
@admin_required
def delete_company(id):
    company = Company.query.filter_by(id=id).first()
    company.status=False
    db.session.add(company)
    db.session.commit()
    return redirect(url_for('view_companies'))

@app.route('/edit_company/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_company(id):
    company = Company.query.filter_by(id= id).first()
    form = CompanyForm(obj= company)

    if request.method == "POST":
        company.code = form.code.data
        company.name = form.name.data
        company.description = form.description.data
        company.contact_person = form.contact_person.data
        company.address = form.address.data
        company.contact_number = form.contact_number.data

        db.session.add(company)
        db.session.flush()
        db.session.commit()
        flash('Company has been updated successfully','alert-success')
        return redirect(url_for('view_companies'))
    return render_template('estimating/companies/setup.html', form = form, company=company, action='edit')

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