from flask_sqlalchemy import SQLAlchemy

# from .farm_model.farm import Farm
# from ..models.fertilizer_model.fertilizer import Fertilizer
from main import db
from main.models.farm_model.farm_model import FarmModel
from main.models.fertilizer_model.fertilizer_model import FertilizerModel
from main.models.user_model.user import User


def seed_database():

    import os
    from datetime import datetime

    # Define the folder path where the files are located
    folder_path = 'data'

    # Read files from the folder
    for file_name in os.listdir(folder_path):
        print(f"file_name>>>>{file_name}")
        if file_name.endswith('.txt'):
            # Parse the farm ID and date from the file name
            parts = file_name[:-4].split('-')
            farm_id = '-'.join(parts[:5])
            date_str = '-'.join(parts[5:])
            date = datetime.strptime(date_str, '%Y-%m-%d').date()


            # Read the file contents
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Parse the file contents
            fertilizers_data = file_content.split('\n')
            for fertilizer_data in fertilizers_data:
                if fertilizer_data:
                    location_str, nit_str = fertilizer_data.split('\t')
                    latitude, longitude = map(float, location_str.split(','))
                    nit = float(nit_str)

                    user = User.query.get(1)
                    if not user:
                        user = User(id=1, username='user@example.com',
                                    first_name='first', last_name='last', password='123456789')
                        db.session.add(user)

                    # Create Farm if it doesn't exist
                    farm = FarmModel.query.filter_by(id=farm_id).first()
                    if not farm:
                        farm = FarmModel(id=farm_id, name=f'Farm {farm_id}',
                                         user_id=1)  # Assuming user_id=1 for simplicity
                        db.session.add(farm)

                    # Create Fertilizer entry
                    fertilizer = FertilizerModel(location=f'POINT({longitude} {latitude})', date=date, nit=nit,
                                                 farm_id=farm_id)
                    db.session.add(fertilizer)

    # Commit the changes to the database
    db.session.commit()


# seed_database()
