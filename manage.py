from website import create_app, db
from flask_migrate import Migrate
from flask_script import Manager

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

@manager.command
def db_migrate(message):
    """Run migration scripts"""
    from flask_migrate import upgrade, migrate, init
    with app.app_context():
        init()
        migrate(message=message)
        upgrade()

@manager.command
def db_upgrade():
    """Apply migrations"""
    from flask_migrate import upgrade
    with app.app_context():
        upgrade()

if __name__ == '__main__':
    manager.run()
