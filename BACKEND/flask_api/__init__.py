import socket
from flask import Flask
from flask_api.config import Config
from flask_api.extensions import db, migrate, init_extensions, user_datastore
from flask_api.routes import main
from flask_cors import CORS
import os

def get_local_ips():
    """Get all non-loopback IPv4 addresses and localhost"""
    ips = ['localhost']
    try:
        # Get IP from active connection
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))  # Google's public DNS
            ips.append(s.getsockname()[0])
    except Exception:
        pass
    
    # Get all interface IPs
    try:
        hostname = socket.gethostname()
        ips.extend(
            ip for ip in socket.gethostbyname_ex(hostname)[2] 
            if not ip.startswith('127.')
        )
    except socket.gaierror:
        pass
    return list(set(ips))  # Remove duplicates

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_extensions(app)
    
    # Dynamic CORS configuration
    frontend_port = os.getenv('FRONTEND_PORT', '8080')
    allowed_origins = [f"http://{ip}:{frontend_port}"  for ip in get_local_ips()]
    # Allow localhost with any port in development
    if app.config.get('FLASK_ENV') == 'development':
        allowed_origins.append(r'http://localhost:*')
    CORS(app, resources={
        r"/*": {
            "origins": allowed_origins,
            "supports_credentials": True
        }
    })
    
    app.register_blueprint(main)
    # Register CLI command
    from .commands import create_admin
    app.cli.add_command(create_admin)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)