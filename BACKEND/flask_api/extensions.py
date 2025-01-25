from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate
from flask_api.models import db, Users, Roles
from flask_jwt_extended import JWTManager

migrate = Migrate()
user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = None
jwt = JWTManager()

# Call the function to create roles
def create_roles(app):
    global user_datastore
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
        # Create roles if they don't exist
        if not user_datastore.find_role('User'):
            user_datastore.create_role(name='User', description='Regular user role')
        if not user_datastore.find_role('Admin'):
            user_datastore.create_role(name='Admin', description='Administrator role')
        db.session.commit()

def init_extensions(app):
    global user_datastore, security
    db.init_app(app)
    migrate.init_app(app, db)
    security = Security(app, user_datastore)
    jwt.init_app(app)
    create_roles(app)