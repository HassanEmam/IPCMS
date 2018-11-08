from IPCMS import app, db
from flask import render_template, redirect, session, request, url_for, flash
from base.users.form import RegisterForm, LoginForm, RoleForm, UserProjectForm
from base.users.models import User, Role, UserLog
# from users.token import generate_confirmation_token, confirm_token
# from users.email import *
from base.users.decorators import login_required, admin_required, organisation_required, project_required
from base.organisations.models import Organisation
from base.project.models import Project, UserProject
import bcrypt, datetime
from sqlalchemy import exc
from base.users.form import ResetPasswordRequestForm, ResetPasswordForm
from base.users.email import send_password_reset_email


'''
This section handles user registeration and login
'''

@app.route('/confirmemail/<token>')
@login_required
def confirm_account(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'alert-danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'alert-success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'alert-success')
    return redirect(url_for('login_success'))



@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = User.query.filter_by(
            username=form.username.data,
            ).first()
        if request.headers.getlist("X-Forwarded-For"):
           ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
           ip = request.remote_addr
        print('ip', ip)
        if author:
            if bcrypt.checkpw(form.password.data.encode('utf-8'), author.password.encode('utf-8')) :
                session['username'] = form.username.data
                log = UserLog(user_id= str(author.id), ipaddr= str(ip), success=True)
                db.session.add(log)

                db.session.commit()
                session['user_id'] = author.id
                org = Organisation.query.filter_by(id=author.organisation_id).first()
                if org:
                    session['is_admin'] = author.is_admin

                    session['organisation_id'] = org.id
                    session['organisation'] =org.name
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('login_success'))
            else:
                log = UserLog(user_id= str(author.id), ipaddr= ip, success=False)
                db.session.add(log)
                db.session.commit()
                flash("Invalid login credentials",'alert-danger')

                return redirect(url_for('login'))
        else:


            flash("Invalid login credentials",'alert-danger')
            return redirect(url_for('login'))
    return render_template('users/login.html', form=form, error=error)



@app.route('/register', methods=('GET', 'POST'))
@organisation_required
@admin_required
def register():
    form = RegisterForm()
    org = Organisation.query.filter_by(id= session['organisation_id']).first()

    if form.validate_on_submit():
        try:
            salt = bcrypt.gensalt()

            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
            user= User(firstname= form.firstname.data,
                        lastname= form.lastname.data,
                        email= form.email.data,
                        username= form.username.data,
                        password= hashed_password,
                        organisation= org,
                        is_admin= form.is_admin.data,
                        is_active= form.is_active.data)

            # token = generate_confirmation_token(user.email)
            # confirm_url = url_for('confirm_account', token=token, _external=True)
            # html = render_template('users/activate.html', confirm_url=confirm_url)
            # subject = "Please confirm your email"

            db.session.add(user)
            db.session.commit()
            # send_email(user.email, subject, html)
            #flash('A confirmation email has been sent via email.', 'alert-success')
            flash('User Registered Successfully ', 'alert-success')
            return redirect(url_for('newuserprojectassignment'))
        except exc.IntegrityError:
            flash('The user details conflict with existing user', 'alert-danger')
            db.session.rollback()
            return redirect(url_for('view_users'))
    return render_template('users/register.html', form=form, action='new')



@app.route('/edituser/<id>', methods=('GET', 'POST'))
@organisation_required
@login_required
def edit_user(id):
    if session.get('is_admin') or id==str(session['user_id']):
        user = User.query.filter_by(id=id).first()
        form = RegisterForm(obj= user)
        org = Organisation.query.filter_by(id= session['organisation_id']).first()
        if request.method=='POST':
            try:

                salt = bcrypt.gensalt()

                user.firstname= form.firstname.data
                user.lastname= form.lastname.data
                user.email= form.email.data
                user.organisation= org
                user.is_admin= form.is_admin.data
                user.is_active = form.is_active.data
                db.session.flush()
                db.session.commit()
                flash('User Details Successfully Updated', 'alert-success')
                return redirect(url_for('login_success'))

            except :
                flash('Unexpected error have occurred while saving your data. Contact system admin', 'alert-danger')
                db.session.rollback()
                return redirect(url_for('view_users'))
        return render_template('users/register.html', form = form, user=user, action='edit')
    else:
        flash ("You don't have enough permissions to perform changes to user details", 'alert-danger')
        return redirect(url_for('login_success'))


@app.route('/viewusers', methods=('GET', 'POST'))
@organisation_required
@admin_required
def view_users():
    users = User.query.filter_by(organisation_id= session.get('organisation_id'), is_active=True).all()
    return render_template('users/viewusers.html', users=users)
    return 'users list'

@app.route('/viewuser/<id>', methods=('GET', 'POST'))
@login_required
def view_user(id):
    if session.get('is_admin') or id==str(session['user_id']):
        user = User.query.filter_by(id= id, organisation_id= session.get('organisation_id'), is_active=True).first()
        assignments= UserProject.query.filter_by(user_id=user.id, is_active=True).all()
        assigns=[]
        for ass in assignments:
            role= Role.query.filter_by(id= ass.role_id).first()
            assigns.append([ass.project, role])

        return render_template('users/viewuser.html', user=user, assignments= assigns)
    else:
        flash('You are not authorised to access user details')
        return redirect(url_for('login_success'))



@app.route('/deleteuser/<id>')
@admin_required
def delete_user(id):
    try:
        user = User.query.filter_by(id= id).first()
        user.is_active = False

        db.session.add(user)
        db.session.commit()
    except:
        flash('Unexpected error have occurred while saving your data. Contact system admin', 'alert-danger')
        db.session.rollback()
        return redirect(url_for('view_users'))
    return redirect(url_for('view_users'))



@app.route('/logout')
def logout():
    if session.get('project_id'):
        session.pop('project_id')
    if session.get('project'):
        session.pop('project')
    if session.get('username'):
        session.pop('username')
    if session.get('user_id'):
        session.pop('user_id')
    if session.get('organisation_id'):
        session.pop('organisation_id')
        session.pop('organisation')
    if session.get('is_admin'):
        session.pop('is_admin')
    return redirect(url_for('login'))



@app.route('/')
@app.route('/login_success')
@login_required
def login_success():
    # if session.get('is_admin')==True:
    #     projects= Project.query.filter_by(org_id= session['organisation_id']).all()
    #     return render_template('/project/projectselection.html', projects= projects)
    # elif session.get('user_id'):
    #     assprojects = UserProject.query.filter_by(user_id=session['user_id'])
    #     projects=[]
    #     for prj in assprojects:
    #         projects.append(prj.project)
    #     return render_template('/project/projectselection.html', projects= projects)
    id = str(session.get('user_id'))
    return render_template('/userdashboard.html', id=id)

@app.route('/admindb')
@admin_required
def admindb():
    # if session.get('is_admin')==True:
    #     projects= Project.query.filter_by(org_id= session['organisation_id']).all()
    #     return render_template('/project/projectselection.html', projects= projects)
    # elif session.get('user_id'):
    #     assprojects = UserProject.query.filter_by(user_id=session['user_id'])
    #     projects=[]
    #     for prj in assprojects:
    #         projects.append(prj.project)
    #     return render_template('/project/projectselection.html', projects= projects)
    id = str(session.get('user_id'))
    return render_template('/admindashboard.html', id=id)

@app.route('/about')
def about():
    return render_template('/users/about.html')

@app.route('/selectproject')
@login_required
def selectproject():
    if session.get('is_admin')==True:
        projects= Project.query.filter_by(org_id= session['organisation_id']).all()
        return render_template('/project/projectselection.html', projects= projects)
    elif session.get('user_id'):
        assprojects = UserProject.query.filter_by(user_id=session['user_id'])
        projects=[]
        for prj in assprojects:
            projects.append(prj.project)
        return render_template('/project/projectselection.html', projects= projects)

@app.route('/allprojects')
@admin_required
def all_projects():

    if session.get('organisation_id'):
        projects = Project.query.filter_by(org_id=session['organisation_id'])
        return render_template('/project/projectselection.html', projects= projects)
    return render_template('/project/view.html')

'''
This section controls the routes for Role
it has functions to create, edit, delete and view Roles
'''


@app.route('/addrole', methods=('GET', 'POST'))
@admin_required
def add_role():
    try:
        form = RoleForm()
        if form.validate_on_submit():
            organisation = Organisation.query.filter_by(id= session['organisation_id']).first()
            role= Role(form.name.data,
                        organisation,
                        form.manager.data,
                        form.is_active.data)

            db.session.add(role)
            db.session.commit()
            flash('Role created successfully','alert-success')
            return redirect(url_for('view_roles'))
    except exc.IntegrityError:
        flash('The role name ' + form.name.data + ' already exists','alert-danger')
        db.session.rollback()
        return redirect(url_for('view_roles'))
    return render_template('users/roleform.html', form=form, action='new')

@app.route('/viewroles')
@login_required
def view_roles():
    roles = Role.query.filter_by(is_active =True, organisation_id= session.get('organisation_id')).all()
    return render_template('users/view_roles.html', roles=roles, organisation_name= Organisation.query.filter_by(id=session.get('organisation_id')).first())


@app.route('/editrole/<id>', methods=('GET', 'POST'))
@admin_required
def edit_role(id):
    role = Role.query.filter_by(id= id).first()
    form = RoleForm(obj= role)

    if request.method == "POST" and form.validate():
        try:

            role.name = form.name.data
            role.manager = form.manager.data
            role.is_active = form.is_active.data

            db.session.add(role)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('view_roles'))
        except:
            flash('Unexpected error have occurred while saving your data. Contact system admin', 'alert-danger')
            db.session.rollback()
            return redirect(url_for('view_roles'))
    return render_template('users/roleform.html', form = form, role=role, action='edit')

@app.route('/deleterole/<id>')
@admin_required
def delete_role(id):
    try:
        role = Role.query.filter_by(id= id).first()
        role.is_active = False

        db.session.add(role)
        db.session.commit()
        return redirect(url_for('view_roles'))
    except:
        flash('Unexpected error have occurred while saving your data. Contact system admin', 'alert-danger')
        db.session.rollback()
        return redirect(url_for('view_roles'))

@app.route('/assignusers', methods=['GET', 'POST'])
@project_required
@admin_required
def newuserprojectassignment():
    form = UserProjectForm()
    if request.method == "POST":
        prj= Project.query.filter_by(id= session.get('project_id')).first()
        user = form.user.data
        role = form.role.data
        user_id = user.id
        usrassignment = UserProject.query.filter_by(project_id=prj.id, user_id=user.id).first()
        print(user.id)
        if not usrassignment:
            assignment = UserProject(project= prj,
                                    user= user,
                                    role= role)
            try:
                db.session.add(assignment)
                db.session.commit()
                flash('User has been assigned successfully to the Project','alert-success')
                return redirect(url_for('view_user', id= user_id))
            except exc.IntegrityError as e:
                db.session.rollback()
                return "User already assigned to this project"
        else:
            flash ('User already assigned to activity', 'alert-danger')
            return redirect(url_for('newuserprojectassignment'))
    return render_template('/users/projectassignment.html', form=form, action='new')

@app.route('/deleteusrprojassignment', methods=['GET'])
def delusrprjassignment():
    try:
        project_id = request.args.get('prj_id')
        user_id = request.args.get('user_id')

        userassig = UserProject.query.filter_by(project_id=project_id, user_id=user_id).first()
        userassig.is_active = False

        db.session.add(userassig)
        db.session.commit()
        flash('Assignment has been deleted successully')
        return redirect(url_for('view_user', id=user_id))
    except:
        flash('Unexpected error have occurred while saving your data. Contact system admin', 'alert-danger')
        db.session.rollback()
        return redirect(url_for('view_user', id=user_id))

@app.route('/editusrprojassignment', methods=['GET', 'POST'])
def editusrprjassignment():
    project_id = request.args.get('prj_id')
    user_id = request.args.get('user_id')

    userassig = UserProject.query.filter_by(project_id=project_id, user_id=user_id).first()
    form = UserProjectForm(obj=userassig)

    if userassig:
        if request.method == "POST":
            try:

                role= Role.query.filter_by(id = userassig.role_id)
                role = form.role.data
                print (role)
                userassig.role_id = role.id
                db.session.add(userassig)
                db.session.commit()
                flash('Assignment has been amended successully','alert-success')
            except:
                flash('Unexpected error have occurred while saving your data. Contact system admin', 'alert-danger')
                db.session.rollback()
                return redirect(url_for('view_user', id=user_id))
            return redirect(url_for('view_user', id=user_id))
    else:
        flash('Unexpected error has occured', 'alert-danger')
    return render_template('/users/projectassignment.html', form=form, action='edit', prj_id=project_id, user_id = user_id)

def sub(roles, id):
    ul =',"childs":['
    for role in roles:
        if role.manager_id == id:
            ul +='{ "name":"' + role.name +'", "id":"' + str(role.id) +'","manager_id":"' + str(role.manager_id) + '"'

            ul += sub(roles, role.id)
            ul += "}"
    ul += "]"
    return ul


@app.route('/rolesorder')
@admin_required
def roles_ordered():
    roles = Role.query.filter_by(organisation_id= session.get('organisation_id')).all()
    ul="["
    for role in roles:
        if role.manager == None:
            ul += '{ "name":"' + role.name +'", "id":"' + str(role.id) +'","manager_id":"' + str(role.manager_id) + '"'
            id= role.id
            ul += sub(roles, id)
            ul += "},"
    ul =ul[:-1]
    ul +="]"
    return ul





# def sub(roles, id):
#     ul ="<ul>"
#     for role in roles:
#         if role.manager_id == id:
#             ul +="<li id='" + str(role.id) + "'>"
#             ul += role.name
#             ul += sub(roles, role.id)
#             ul += "</li>"
#     ul += "</ul>"
#     return ul

# @app.route('/rolesorder')
# def roles_ordered():
#     roles = Role.query.filter_by(organisation_id= session.get('organisation_id')).all()
#     print(str(roles))
#     ul="<ul>"
#     for role in roles:
#         if role.manager == None:
#             ul +="<li id='"+ str(role.id) +"'>" + role.name
#             id= role.id
#             ul += sub(roles, id)
#             ul += "</li>"
#     ul +="</ul>"
#     return render_template('users/view_roles.1.html', roles= ul)
@app.route('/view_delete_users', methods=['GET', 'POST'])
@admin_required
def view_deleted_users():
    users= User.query.filter_by(organisation_id=session.get('organisation_id'),
                                is_active=False)
    return render_template('/users/viewdeleted.html', users=users)

@app.route('/restore_deleted_user/<id>')
@admin_required
def restore_user(id):
    if session.get('is_admin') or id==str(session['user_id']):
        try:
            user = User.query.filter_by(id=id).first()
            user.is_active = True
            db.session.flush()
            db.session.commit()
            flash('User Successfully Recovered', 'alert-success')
            return redirect(url_for('admindb'))

        except :
            flash('Unexpected error have occurred while saving your data. Contact system admin', 'alert-danger')
            db.session.rollback()
            return redirect(url_for('view_users'))
    else:
        flash ("You don't have enough permissions to perform changes to user details", 'alert-danger')
        return redirect(url_for('login_success'))

@app.route('/view_delete_roles', methods=['GET', 'POST'])
@admin_required
def view_deleted_roles():
    roles = Role.query.filter_by(is_active =False, organisation_id= session.get('organisation_id')).all()
    return render_template('users/viewdeletedroles.html', roles=roles, organisation_name= Organisation.query.filter_by(id=session.get('organisation_id')).first())

@app.route('/restore_deleted_role/<id>')
@admin_required
def restore_role(id):
    if session.get('is_admin') or id==str(session['user_id']):
        try:
            role = Role.query.filter_by(id=id).first()
            role.is_active = True
            db.session.flush()
            db.session.commit()
            flash('Role Data Successfully Recovered', 'alert-success')
            return redirect(url_for('admindb'))

        except :
            flash('Unexpected error have occurred while saving your data. Contact system admin', 'alert-danger')
            db.session.rollback()
            return redirect(url_for('view_users'))
    else:
        flash ("You don't have enough permissions to perform changes to user details", 'alert-danger')
        return redirect(url_for('login_success'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if session.get('user_id'):
        return redirect(url_for('login_success'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'alert-success')
        return redirect(url_for('login'))
    return render_template('/users/reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if session.get('user_id'):
        return redirect(url_for('login_success'))
    user = User.verify_reset_password_token(token)
    print(user)
    if not user:
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset.', 'alert-success')
        return redirect(url_for('login'))
    return render_template('/users/reset_password.html', form=form)