from models import User
from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource, Namespace, fields

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required


auth_ns = Namespace('auth', description='A namespace for our authentication.')


signup_modal=auth_ns.model(
    'SignUp',
    {
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

login_modal=auth_ns.model(
    'LogIn',
    {
        "username":fields.String(),
        "password":fields.String()
    }
)


@auth_ns.route('/signup')
class SignUp(Resource):
    
    @auth_ns.expect(signup_modal)
    def post(self):
        data = request.get_json()
        username=data.get('username')
        db_user=User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message":f"User with username {username} already exists."})
        
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )
        
        new_user.save()
        
        return make_response(jsonify({"message":"User is created successfully."}),201)
    
    
@auth_ns.route('/login')
class LogIn(Resource):
    
    @auth_ns.expect(login_modal)
    def post(self): 
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        db_user=User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
            
            return jsonify({
                "access token": access_token,
                "refresh_token" : refresh_token
            })