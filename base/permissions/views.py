from IPCMS import app, db
from base.permissions.form import PermissionForm
from base.permissions.models import Permission
from flask import render_template
from base.users.decorators import *


@app.route('/newpermission', methods=['GET', 'POST'])
def new_permission():
    form = PermissionForm()
    
    if request.method == "POST" and form.validate():
        permission = Permission (name= form.name.data, 
                            is_active= True)
        db.session.add(permission)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('view_permissions'))
    return render_template('permissions/setup.html', form=form, action='new')
    
@app.route('/editpermission/<id>', methods=['GET', 'POST'])
@login_required
def edit_permission(id):
    permission = Permission.query.filter_by(id= id).first()
    form = PermissionForm(obj= permission)
    
    if request.method == "POST" and form.validate():
        permission.name = form.name.data
        permission.is_active = form.is_active.data
        
        db.session.add(permission)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('view_permissions'))
    return render_template('permissions/setup.html', form = form, permission=permission, action='edit')

@app.route('/viewpermissions')
def view_permissions():
    permissions = Permission.query.filter_by(is_active=True).all()
    return render_template('permissions/view.html', permissions=permissions)