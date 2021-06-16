from flask import Flask
from flasgger import Swagger
from api.route.home import home_api
from api.route.policy import policy_api

def createApp():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'Capstone API',
    }
    swagger = Swagger(app)

    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(policy_api, url_prefix="/api/policy")

    return app

if __name__ == '__main__':
    app = createApp()
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)