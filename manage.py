import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from main.models.farm_model.farm_model import FarmModel
from main.models.user_model.user import User
from main.models.fertilizer_model.fertilizer_model import FertilizerModel
from seed_database import seed_database

import os

from main import create_app, blueprint, db

app = create_app(os.getenv('ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def migrate_if_needed():
    migration_files = os.listdir('migrations')
    if not migration_files:
        print('Running initial migration...')
        migrate_init()
    else:
        print('Migration files found. Skipping migration initialization.')


def migrate_init():
    with app.app_context():
        db.create_all()
        db.session.commit()
        print('Database initialized.')


@manager.command
def run():
    app.run(host='0.0.0.0', port=3000)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def seed():
    seed_database()


if __name__ == '__main__':
    manager.run()
