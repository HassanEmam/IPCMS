from colp import app, db
from flask import render_template, redirect, session, request, url_for, flash
from base.users import RegisterForm, LoginForm, RoleForm
from base.users import User, Role
from base.users.decorators import login_required, admin_required
from base.organisations.models import Organisation
from base.project import Project
import bcrypt

'''
This section handles user registeration and login
'''
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    session['organisation_id'] = "None"
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = User.query.filter_by(
            username=form.username.data,
            ).first()
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                #
                session['user_id'] = author.id
                org = Organisation.query.filter_by(admin_id=author.id).first()
                if org:
                    session['is_admin'] = author.is_admin
                    session['organisation_id'] = org.id
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('login_success'))
            else:
                error = "Incorrect password"
        else:
            error = "User not found"
    return render_template('users/login.html', form=form, error=error)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
        
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)  
        user= User(form.firstname.data,
                    form.lastname.data, 
                    form.email.data, 
                    form.username.data, 
                    hashed_password,
                    True)
        
        db.session.add(user)
        db.session.commit()
        flash('User Registered')
        return redirect(url_for('login_success'))
    return render_template('users/register.html', form=form)

@app.route('/logout')
def logout():
    if session.get('project_id'):
        session.pop('project_id')
    if session.get('username'):
        session.pop('username')
    if session.get('user_id'):
        session.pop('user_id')
    if session.get('organisation_id'):
        session.pop('organisation_id')
    if session.get('is_admin'):
        session.pop('is_admin')
    return redirect(url_for('login'))



@app.route('/')
@app.route('/login_success')
@login_required
def login_success():
    if session.get('organisation_id'):
        projects = Project.query.filter_by(org_id= session['organisation_id'])
        return render_template('/project/projectselection.html', projects= projects)
    

'''
This section controls the routes for Role
it has functions to create, edit, delete and view Roles
'''


@app.route('/newrole', methods=('GET', 'POST'))
def add_role():
    form = RoleForm()
    if form.validate_on_submit():
          
        role= Role(form.description.data,
                    form.is_read.data, 
                    form.is_create.data, 
                    form.is_edit.data,
                    form.is_delete.data)
        
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('view_roles'))
    return render_template('users/roleform.html', form=form, action='new')
    
@app.route('/viewroles')
def view_roles():
    roles = Role.query.filter_by(is_active =True).all()
    return render_template('users/view_roles.html', roles=roles)

    
@app.route('/editrole/<id>', methods=('GET', 'POST'))
@admin_required
def edit_role(id):
    role = Role.query.filter_by(id= id).first()
    form = RoleForm(obj= role)
    
    if request.method == "POST" and form.validate():
        role.description = form.description.data
        role.is_read = form.is_read.data
        role.is_create = form.is_create.data
        role.is_edit = form.is_edit.data
        role.is_delete = form.is_delete.data
        
        db.session.add(role)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('view_roles'))
    return render_template('users/roleform.html', form = form, role=role, action='edit')
    
@app.route('/deleterole/<id>')
def delete_role(id):
    role = Role.query.filter_by(id= id).first()
    role.is_active = False
        
    db.session.add(role)
    db.session.commit()
    return redirect(url_for('view_roles'))
    
