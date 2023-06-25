from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.utilities.dto import FarmDto
from main.services.farm_service import get_farm

farm_ns = FarmDto.farm_ns
_farm = FarmDto.farm


class Farm(Resource):
    @farm_ns.doc("Fetch Farm data")
    @farm_ns.response(200, 'Successfully fetch fertilizers.')
    @farm_ns.response(401, 'Unauthorized.')
    @farm_ns.response(404, 'Not Found')
    @farm_ns.response(400, 'Bad Request')
    @jwt_required()
    def get(self):
        """Get Farm data"""
        """
        This endpoint retrieves Farm data for the authenticated user.
        Only authorized users with a valid JWT token can access this endpoint.

        Returns:
        - 200: Successful response with a list of farms.
        - 401: If the user is not authorized (invalid or missing JWT token).
        - 404: If the Farm data is not found.
        - 400: If the request is malformed or missing required parameters.
        """
        user_id = get_jwt_identity()

        return get_farm(user_id)
