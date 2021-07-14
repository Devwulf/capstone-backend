from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from database import db_session
from models import User
import uuid

auth_api = Blueprint("auth", __name__)

@auth_api.route("/register", methods=["GET", "POST"])
def signup_user():  
 data = request.get_json()  

 hashed_password = generate_password_hash(data["password"], method="sha256")
 
 new_user = User(id=str(uuid.uuid4()), username=data["username"], password=hashed_password, admin=False) 
 db_session.add(new_user)  
 db_session.commit()    

 return jsonify({"message": "registered successfully"})   


@auth_api.route("/login", methods=["GET", "POST"])  
def login_user(): 
 
  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
     return make_response("could not verify", 401, {"WWW.Authentication": "Basic realm: "login required""})    

  user = Users.query.filter_by(name=auth.username).first()   
     
  if check_password_hash(user.password, auth.password):  
     token = jwt.encode({"public_id": user.public_id, "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config["SECRET_KEY"])  
     return jsonify({"token" : token.decode("UTF-8")}) 

  return make_response("could not verify",  401, {"WWW.Authentication": "Basic realm: "login required""})
