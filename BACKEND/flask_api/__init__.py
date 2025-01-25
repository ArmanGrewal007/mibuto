import inspect
from flask import Flask
from flask_api.config import Config
from flask_api.extensions import db, migrate, init_extensions, user_datastore
from flask_api.routes import main
from flask_cors import CORS 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_extensions(app) 
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
    app.register_blueprint(main) 
    # Register CLI command
    from .commands import create_admin
    app.cli.add_command(create_admin)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)