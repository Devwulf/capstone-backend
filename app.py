from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from api.route.policy import policy_api
from auth.routes.auth import auth_api
from services.database import init_db, init_model_db, init_auth
import pytest
import logging

class CustomApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        with self.app_context():
            init_db()
            init_model_db()
            init_auth()
        super(CustomApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

def create_app(test_config=None):
    app = CustomApp(__name__)
    cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    # Setup file logging
    logging.basicConfig(filename="./logs/record.log", level=logging.DEBUG, format=f"[%(asctime)s] %(levelname)s (%(threadName)s) - %(message)s")

    # Authentication
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "this-key-does-not-exist"

    app.config["SWAGGER"] = {
        "title": "Capstone API",
    }
    swagger = Swagger(app)

    if test_config is not None:
        app.config.update(test_config)

    app.register_blueprint(policy_api, url_prefix="/api/policy")
    app.register_blueprint(auth_api, url_prefix="/auth")

    return app

# For testing
@pytest.fixture
def test_client():
    app = create_app({"TESTING": True})

    with app.test_client() as client:
        with app.app_context():
            init_db()
            init_model_db()
            init_auth()
        yield client

app = create_app()
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)