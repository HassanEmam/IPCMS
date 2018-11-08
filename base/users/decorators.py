from functools import wraps
from flask import session, request, redirect, url_for, abort, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            session['next'] = request.url
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            session['next'] = request.url
            return redirect(url_for('login', next=request.url))
        elif session.get('is_admin') is None:
            abort(403)
        elif session.get('is_admin')==False:
            flash('You do not have permission to perform this action, please contact your administrator for support', 'alert-danger')
            return redirect(url_for('login_success'))
        return f(*args, **kwargs)
    return decorated_function

def project_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('project_id') is None:
            session['next'] = request.url
            return redirect(url_for('selectproject', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def organisation_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('organisation_id') is None:
            session['next'] = request.url
            return redirect(url_for('login_success', next=request.url))
        return f(*args, **kwargs)
    return decorated_function