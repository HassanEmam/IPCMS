from IPCMS import app, db
from estimating.companies.models import Company
from estimating.subcontractors.models import Subcontractor
from flask import jsonify
from base.users.models import User
from base.users.decorators import *
from api.view import *


# @app.route('/api/new_company', methods=['POST', 'GET'])
# @admin_required
# def api_new_company():
#     try:
#         if request.method == "POST":
#             if session.get('organisation_id'):
#                 org = Organisation.query.filter_by(id=session['organisation_id']).first()
#             else:
#                 org = Organisation.query.filter_by(id='1').first()
#             company = Company(code=request.form.code.data,
#                               name=request.form.name.data,
#                               description=request.form.description.data,
#                               address=request.form.address.data,
#                               contact_number=request.form.contact_number.data,
#                               contact_person=request.form.contact_person.data,
#                               organisation=org)
#             db.session.add(company)
#             db.session.flush()
#             db.session.commit()
#
#             flash('Company has been created successully','alert-success')
#             return redirect(url_for('view_companies'))
#     except validators.ValidationError as e:
#         flash(e, 'alert-danger')
#     return render_template('estimating/companies/setup.html', form=form, action='new')


@app.route('/api/view_subcontractors')
@token_required
def api_view_subcontractors(current_user):
    subcontractors = []
    result =[]
    if session.get('organisation_id'):
        subcontractors = Subcontractor.query.filter_by(org_id=session['organisation_id'], status=True).all()
    else:
        subcontractors = Subcontractor.query.filter_by(status=True).all()
    for s in subcontractors:
        ser = dict()
        ser['code'] = s.code
        ser['name'] = s.name
        ser['description'] = s.description
        ser['address'] = s.address
        ser['contact_person'] = s.contact_person
        ser['contact_number'] = s.contact_number
        result.append(ser)
    return jsonify({"subcontractors": result})

@app.route('/api/view_companies')
@token_required
def api_view_companies(current_user):
    companies = None
    result = []
    if session.get('organisation_id'):
        companies= Company.query.filter_by(org_id=session['organisation_id'], status=True).all()
    else:
        companies = Company.query.filter_by(org_id='1', status=True).all()
    for c in companies:
        cmp = dict()
        cmp['code'] = c.code
        cmp['name'] = c.name
        cmp['description'] = c.description
        cmp['address'] = c.address
        cmp['contact_person'] = c.contact_person
        cmp['contact_number'] = c.contact_number
        result.append(cmp)
    return jsonify({"companies": result})

# @app.route('/view_company/<id>')
# @login_required
# def company_details(id):
#     company = Company.query.filter_by(id= id).first()
#     return render_template('estimating/companies/details.html', company=company)
#
#
# @app.route('/delete/<id>')
# @admin_required
# def delete_company(id):
#     company = Company.query.filter_by(id=id).first()
#     company.status=False
#     db.session.add(company)
#     db.session.commit()
#     return redirect(url_for('view_companies'))
#
# @app.route('/edit_company/<id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_company(id):
#     company = Company.query.filter_by(id= id).first()
#     form = CompanyForm(obj= company)
#
#     if request.method == "POST":
#         company.code = form.code.data
#         company.name = form.name.data
#         company.description = form.description.data
#         company.contact_person = form.contact_person.data
#         company.address = form.address.data
#         company.contact_number = form.contact_number.data
#
#         db.session.add(company)
#         db.session.flush()
#         db.session.commit()
#         flash('Company has been updated successfully','alert-success')
#         return redirect(url_for('view_companies'))
#     return render_template('estimating/companies/setup.html', form = form, company=company, action='edit')

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