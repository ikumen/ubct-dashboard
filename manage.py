"""
python manage.py db init (run once to initialize alembic work directory)
python manage.py db migrate
python manage.py db upgrade
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# Note models needs to be import so migration can detect tables defs
from backend import factory, datastores, models


app = factory.create_config_only_app()
datastores.db.init_app(app)

migrate = Migrate(app, datastores.db, 'alembic')
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()