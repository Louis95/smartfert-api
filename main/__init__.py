import os

from flask_jwt_extended import JWTManager

from .config import config_by_name, db, flask_bcrypt, key
from flask.app import Flask
from flask_restx import Api
from flask import Blueprint
from flask_marshmallow import Marshmallow

from .controllers.user_controller.user import user_ns, Users, UserLogin
from .controllers.fertilizer_controller.fertilizer import fertilizer_ns, Fertilizer
from .controllers.farm_controller.farm import farm_ns, Farm

ma = Marshmallow()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


blueprint = Blueprint('api', __name__)
authorizations = {
    'Bearer Token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='SmartFert 3000',
    version='1.0',
    description='API for interview Test',
    authorizations=authorizations,
    security='Bearer Token'
)


api.add_namespace(user_ns, path='/')
user_ns.add_resource(Users, 'register')
user_ns.add_resource(UserLogin, 'login/')

api.add_namespace(fertilizer_ns, path='/fertilizer')
fertilizer_ns.add_resource(Fertilizer, '/<string:farm_id>')

api.add_namespace(farm_ns, path='/')
farm_ns.add_resource(Farm, 'farm/')


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    app.config['JWT_SECRET_KEY'] = key
    jwt = JWTManager(app)
    app.config['RESTPLUS_MASK_SWAGGER'] = False

    return app
