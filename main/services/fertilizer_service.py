
from geoalchemy2.functions import ST_AsText

from main import db
from main.models.farm_model.farm_model import FarmModel
from main.models.fertilizer_model.fertilizer_model import FertilizerModel


def get_fertilizer_data(farm_id: int, date_to_query_data: str, user_id: int):
    """
    Retrieve fertilizer data for a specific farm and date.

    This function retrieves the fertilizer data for a specific farm on a given date.
    The data includes the locations and nitrogen values of the fertilizers applied on the farm.

    Args:
        farm_id (int): The ID of the farm.
        date_to_query_data (str): The date to query the fertilizer data in the format 'YYYY-MM-DD'.
        user_id (int): The ID of the user.

    Returns:
        - If the farm is found and fertilizer data is available for the specified date:
            - Tuple[Dict[str, Any], int]: A tuple containing the fertilizer data and the status code.

    """
    try:

        farm = FarmModel.query.filter_by(id=farm_id, user_id=user_id).all()
        if not farm:
            return {"error": "Farm not found"}, 404

        fertilizer_data = FertilizerModel.query.filter_by(farm_id=farm_id, date=date_to_query_data).all()
        if not fertilizer_data:
            return {"error": "Fertilizer data not found"}, 404

        locations = []
        total_nit = 0.0

        for fertilizer in fertilizer_data:
            location_wkt = db.session.scalar(ST_AsText(fertilizer.location))
            latitude, longitude = map(float, location_wkt[6:-1].split())
            location = {
                "geo": [latitude, longitude],
                "nit": fertilizer.nit
            }
            locations.append(location)
            total_nit += fertilizer.nit

        response = {
            "data": {
                "locations": locations,
                "total": total_nit
            }
        }
        return response, 200

    except Exception as e:
        print(f"{str(e)}")
        return {"error": str(e)}, 400
