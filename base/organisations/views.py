from IPCMS import app, db
from base.organisations.form import OrganisationForm
from base.organisations.models import Organisation
from flask import render_template, redirect, url_for, request, session
import bcrypt
from base.users.models import User
from base.users.decorators import login_required, admin_required

'''
This code controls the creation, editing, viewing and deleting of organisations
'''


@app.route('/neworganisation', methods=['POST', 'GET'])
def add_organisation():
    form = OrganisationForm()
    
    if request.method == "POST" and form.validate():
        organisation = Organisation (code= form.code.data, 
                                    name= form.name.data, 
                                    description= form.description.data,
                                    is_active= form.is_active.data)
        db.session.add(organisation)
        db.session.flush()
        

        if organisation:
            org_id = organisation.id
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
            admin= User(firstname= form.firstname.data,
                    lastname= form.lastname.data, 
                    email= form.email.data, 
                    username= form.username.data, 
                    password= hashed_password,
                    organisation= organisation,
                    is_admin= True)
            print(org_id)
            db.session.add(admin)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('view_organisations'))
        
    return render_template('organisations/organisationform.html', form=form, action='new')


@app.route('/vieworganisations')
def view_organisations():
    organisations = Organisation.query.filter_by(id=session.get('organisation_id'), is_active=True).all()
    return render_template('organisations/view.html', organisations=organisations)

@app.route('/editorganisation/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_organisation(id):
    organisation = Organisation.query.filter_by(id= id).first()
    form = OrganisationForm(obj= organisation)
    
    if request.method == "POST" and form.validate():
        organisation.code = form.code.data
        organisation.is_active = form.is_active.data
        organisation.name = form.name.data
        organisation.description = form.description.data

        db.session.add(organisation)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('view_organisations'))
    return render_template('organisations/organisationform.html', form = form, organisation=organisation, action='edit')

@app.route('/deleteorganisation/<id>')
def delete_organisations(id):
    organisation = Organisation.query.filter_by(id= id).first()
    organisation.is_active = False
        
    db.session.add(organisation)
    db.session.commit()
    return redirect(url_for('view_organisations'))