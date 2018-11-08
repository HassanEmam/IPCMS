from colp import app, db

from base.project import Project
from base.users import User
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from base.organisations.models import Organisation
import jwt
import datetime, bcrypt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token =None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id = data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/getprojects', methods=['GET'])
@token_required
def api_get_projects(current_user):
    if not current_user.is_admin:
        return jsonify({"message": 'Cannot perform that function!'})
    projects = Project.query.all()
    result =[]
    for project in projects:
        entity ={"id":project.id, "projectname": project.name}
        result.append(entity)
    return jsonify(result)

@app.route('/api/users', methods=['GET'])
@token_required
def api_users(current_user):
    if not current_user.is_admin:
        return jsonify({"message": 'Cannot perform that function!'})
    users = User.query.all()
    output=[]
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['firstname'] = user.firstname
        user_data['lastname'] = user.lastname
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.is_admin
        output.append(user_data)
    return jsonify({"users": output})

@app.route('/api/user/<id>', methods=['GET'])
@token_required
def api_get_user(current_user, id):
    if not current_user.is_admin:
        return jsonify({"message": 'Cannot perform that function!'})
    user = User.query.filter_by(id = id).first()
    if not user:
        return jsonify({"message": "User not found"})
    user_detail = {"first name" : user.firstname,
                    "last name": user.lastname,
                    "email": user.email,
                    "admin": user.is_admin}
    return jsonify({'user':user_detail})

@app.route('/api/user/<id>', methods=['PUT'])
@token_required
def api_update_user(current_user, id):
    if not current_user.is_admin:
        return jsonify({"message": 'Cannot perform that function!'})
    user = User.query.filter_by(id = id).first()
    if not user:
        return jsonify({"message": "User not found"})

    return ''

@app.route('/api/user/<id>', methods=['DELETE'])
@token_required
def api_delete_user(current_user, id):
    if not current_user.is_admin:
        return jsonify({"message": 'Cannot perform that function!'})
    user = User.query.filter_by(id = id).first()
    if not user:
        return jsonify({"message": "User not found"})
    return ''

@app.route('/api/user', methods=['POST'])
@token_required
def api_add_user(current_user):
    if not current_user.is_admin:
        return jsonify({"message": 'Cannot perform that function!'})
    data = request.get_json()
    org = Organisation.query.filter_by(id= current_user.organisation_id).first()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user= User(firstname= data['firstname.data'],
                lastname= data['lastname.data'],
                email= data['email.data'],
                username= data['username.data'],
                password= hashed_password,
                organisation= org,
                is_admin= data['is_admin.data'],
                is_active= data['is_active.data'])
    db.session.add(user)
    db.session.commit()
    return {"message": "User has been created successfully"}

@app.route('/api/login', methods=['POST'])
def api_login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_respone('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(username = auth.username).first()
    if not user:
        return make_respone('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if bcrypt.hashpw(auth.password, user.password) == user.password:
        token = jwt.encode({'id':user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')}), 201, {'Access-Control-Allow-Origin': '*'}
    return make_respone('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
