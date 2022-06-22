import jwt
from flask_bcrypt import generate_password_hash, check_password_hash
from flask import Blueprint, request
from .model import User
from app.db import db
from app.commom import loginRequired

user_blueprint = Blueprint('user_blueprint', __name__)

#1. User Registration => POST
@user_blueprint.route('/register', methods= ['POST'])
def register():
    payload = request.json
    user_password = generate_password_hash(payload['password'])
    user = User(email = payload['email'], password = user_password)
    db.session.add(user)
    db.session.commit()
    return {'status':'Registered Successfully'}

#2. User Login => POST
@user_blueprint.route('/login', methods = ['POST'])
def login():
    payload = request.json
    user = User.query.filter_by(email= payload['email']).first()
    if user:
        hash_password = check_password_hash(user.password, payload['password'])
        if hash_password:
            jwt_encode = jwt.encode({'id':user.id, 'name':user.username, 'add':user.add}, "MPM" , algorithm="HS256")
            return {'token': jwt_encode}, 200
        else:
            return {'Message': 'Invalid email/password'},401
    else:
        return {'Message': 'Invalid email/password'},401

#User Dashboard => GET 
@user_blueprint.route('/dashboard', methods=['GET'])
@loginRequired
def dashboard(id):
    print(id)
    return "Dashboard"

#User Order => GET
@user_blueprint.route('/order', methods=['GET'])
def order():
    try:
        decode = jwt.decode(request.headers['Authorization'], "MPM", algorithms=["HS256"])
        if decode:
            return {"Message": 'Authorized user of id '+ str(decode['id'])}, 200
        else:
            return {"Message": "Unauthorized user"}, 401
    except:
        return {"Message": "Unauthorized user"}, 401


