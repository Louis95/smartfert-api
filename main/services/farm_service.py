from main.models.farm_model.farm_model import FarmModel


def get_farm(user_id):
    """
    Get farms for a specific user.

    This function retrieves the farms associated with a specific user identified by their user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        - If farms are found for the user:
            - dict: A dictionary containing the farm data for the user.
            - status_code (int): 200 - Success.
        - If no farms are found for the user:
            - dict: A dictionary indicating the error.
                - 'error' (str): The error message indicating no farms were found for the user.
            - status_code (int): 404 - Not Found.
    """
    user_farms = FarmModel.query.filter_by(user_id=user_id).all()

    if not user_farms:
        return {"error": "No Farm found"}, 404

    farms = []
    for farm in user_farms:
        farms.append({
            'id': farm.id,
            'name': farm.name
        })

    return {'data': farms}, 200
