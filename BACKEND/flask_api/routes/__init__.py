from flask import Blueprint, jsonify
from .user_routes import user
from .admin_routes import admin
from .subject_routes import subject
from .chapter_routes import chapter

main = Blueprint('main', __name__)

# Register individual blueprints
blueprints = [user, admin, subject, chapter]

for blueprint in blueprints:
    main.register_blueprint(blueprint)

@main.route('/', methods=['GET'])
def home():
    return jsonify(message="Welcome to the API"), 200