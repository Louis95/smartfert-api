from typing import List

from flask_restx import Namespace, fields


class UserDto:
    user_ns = Namespace('users', description='user related operations')
    user = user_ns.model('UserModel', {
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
        'password': fields.String(required=True, discriminator="The user password"),
        'username': fields.String(required=True, discriminator="The user email address")
    })
    user_auth = user_ns.model('UserAuth', {
        'username': fields.String(required=True, description='The email address used for authentication'),
        'password': fields.String(required=True, description='The password used for authentication'),

    })


class FarmDto:
    farm_ns = Namespace('Farm', description='farm related operations')
    farm = farm_ns.model('FarmModel', {
        'name': fields.String(required=True, description="farm name"),
        'user_id': fields.Integer(required=True, description="user id"),
        'fertilizers': fields.String(List, required=True, description="fertilizers used")
    })


class FertilizerDto:
    fertilizer_ns = Namespace('fertilizers', description='fertilizer related operations')
    fertilizer = fertilizer_ns.model('FertilizerModel', {
        'geo': fields.String(required=True, description="The geo coordinates for the location"),
        'nit': fields.Float(required=True, description="The amount of Nitrogen applied on the location")
    })
