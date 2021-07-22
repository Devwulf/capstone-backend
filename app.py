from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from api.route.home import home_api
from api.route.policy import policy_api
from auth.routes.auth import auth_api
from auth.services.database import db_session, init_db
from auth.models.models import User, Role

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Authentication
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "super-secret"

app.config["SWAGGER"] = {
    "title": "Capstone API",
}
swagger = Swagger(app)

app.register_blueprint(home_api, url_prefix="/api")
app.register_blueprint(policy_api, url_prefix="/api/policy")
app.register_blueprint(auth_api, url_prefix="/auth")

@app.before_first_request
def initialize_db():
    init_db()

if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)