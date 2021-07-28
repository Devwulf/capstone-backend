from flask import request, jsonify, current_app
from functools import wraps
from auth.models.models import User
import jwt

# Creates a decorator that automatically checks tokens from a given
# request, and runs the decorated function if that token is valid
def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):
        token = None 

        if "x-access-tokens" in request.headers:  
          token = request.headers["x-access-tokens"] 

        if not token:  
            return jsonify({"message": "a valid token is missing"})   

        try:  
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["id"]).first()  
        except:  
            return jsonify({"message": "token is invalid"})  

        return f(current_user, *args,  **kwargs)

    return decorator 