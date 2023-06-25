from datetime import datetime

from flask import request
from flask_restx import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.utilities.dto import FertilizerDto
from main.services.fertilizer_service import get_fertilizer_data

fertilizer_ns = FertilizerDto.fertilizer_ns
_fertilizer = FertilizerDto.fertilizer


class Fertilizer(Resource):
    @fertilizer_ns.param('date', description='The date to query data for, defaults to today',
                         _in='query', example='2022-01-01')
    @fertilizer_ns.doc("Get Fertilizer data")
    @fertilizer_ns.response(200, 'Successfully fetch fertilizers.')
    @fertilizer_ns.response(401, 'Not Authorized.')
    @fertilizer_ns.response(404, 'Not Found')
    @fertilizer_ns.response(400, 'Bad Request')
    @jwt_required()
    def get(self, farm_id):
        """Get a fertilizer by the farm ID, for a given date. If no date is provided, it defaults to the current date"""
        """
        This endpoint retrieves fertilizer data for a specific farm, for a given  date.
        Only authorized users with a valid JWT token can access this endpoint.

        Parameters:
        - farm_id (int): The ID of the farm to retrieve fertilizer data for.

        Query Parameters:
        - date (str, optional): The date to query data for. Defaults to today's date.

        Returns:
        - 200: If the fertilizer data is successfully fetched.
        - 401: If the user is not authorized (invalid or missing JWT token).
        - 404: If the fertilizer data is not found.
        - 400: If the request is malformed or missing required parameters.
        """
        date = request.args.get('date', str(datetime.now().date()))
        user_id = get_jwt_identity()

        return get_fertilizer_data(farm_id, date, user_id)