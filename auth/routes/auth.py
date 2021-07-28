from http import HTTPStatus
from flask import Blueprint, request, current_app, jsonify, make_response
from flasgger import swag_from
from flask_cors.decorator import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from auth.services.database import db_session
from auth.models.models import User
import uuid
import jwt
import datetime

auth_api = Blueprint("auth", __name__)

@auth_api.route("/register", methods=["POST"])
@cross_origin()
def signup_user():  
    data = request.get_json()
    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"message": "username already exists"})

    hashed_password = generate_password_hash(data["password"], method="sha256")
 
    new_user = User(id=str(uuid.uuid4()), username=data["username"], password=hashed_password)
    db_session.add(new_user)
    db_session.commit()
    return jsonify({"message": "registered successfully"})

@auth_api.route("/login", methods=["POST"])
@cross_origin()
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response("could not verify", 401, {"WWW.Authentication": "Basic realm: 'login required'"})    

    user = User.query.filter_by(username=auth.username).first()   
    if not user or not user.username or not user.password:
        return make_response("could not verify", 401, {"WWW.Authentication": "Basic realm: 'login required'"})    

    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({"id": user.id, "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config["SECRET_KEY"], algorithm="HS256")  
        return jsonify({"token" : token}) 

    return make_response("could not verify", 401, {"WWW.Authentication": "Basic realm: 'login required'"})

@auth_api.route("/token", methods=["GET"])
@cross_origin()
def check_valid_token():
    token = None 

    if "x-access-tokens" in request.headers:  
        token = request.headers["x-access-tokens"] 
    
    if not token:  
        return make_response("a valid token is missing", 400, {"WWW.Authentication": "Basic realm: 'login required'"}) 

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except:
        return jsonify({"message": "invalid token"})

    return jsonify({"message": "valid token"})
