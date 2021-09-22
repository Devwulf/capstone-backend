from http import HTTPStatus
from flask import Blueprint, request, current_app, jsonify, make_response
from flasgger import swag_from
from flask_cors.decorator import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from services.database import db_session
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
        current_app.logger.warning("Signup: Username '%s' already exists in the database.", data["username"])
        return jsonify({"message": "username already exists"})

    hashed_password = generate_password_hash(data["password"], method="sha256")
 
    new_user = User(id=str(uuid.uuid4()), username=data["username"], password=hashed_password)
    db_session.add(new_user)
    db_session.commit()

    current_app.logger.info("Signup: The user '%s' has registered successfully.", data["username"])
    return jsonify({"message": "registered successfully"})

@auth_api.route("/login", methods=["POST"])
@cross_origin()
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        current_app.logger.warning("Login: The authorization header is invalid or could not be found.")
        return make_response("could not verify", 401, {"WWW.Authentication": "Basic realm: 'login required'"})    

    user = User.query.filter_by(username=auth.username).first()   
    if not user or not user.username or not user.password:
        current_app.logger.warning("Login: Could not find the user '%s'.", auth.username)
        return make_response("could not verify", 401, {"WWW.Authentication": "Basic realm: 'login required'"})    

    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({"id": user.id, "exp" : datetime.datetime.utcnow() + datetime.timedelta(days=1)}, current_app.config["SECRET_KEY"], algorithm="HS256")
        current_app.logger.info("Login: The user '%s' has logged in successfully.", auth.username)
        return jsonify({"token" : token}) 

    current_app.logger.warning("Login: The user '%s' has inputted the wrong password.", auth.username)
    return make_response("could not verify", 401, {"WWW.Authentication": "Basic realm: 'login required'"})

@auth_api.route("/token", methods=["GET"])
@cross_origin()
def check_valid_token():
    token = None 

    if "x-access-tokens" in request.headers:  
        token = request.headers["x-access-tokens"] 
    
    if not token:
        current_app.logger.warning("CheckToken: Token could not be found from header.")
        return make_response("a valid token is missing", 400, {"WWW.Authentication": "Basic realm: 'login required'"}) 

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except:
        current_app.logger.warning("CheckToken: Token '%s' is invalid.", token)
        return jsonify({"message": "invalid token"})

    current_app.logger.info("CheckToken: Token '%s' is valid.", token)
    return jsonify({"message": "valid token"})
