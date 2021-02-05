"""
A cli wrapper for alembic.

Usage: python manage.py db <option>

where <option> can be:
    init      initialize the alembic work directory
    migrate   parse models and create/update schema to reflect model
    upgrade   apply schema updates
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