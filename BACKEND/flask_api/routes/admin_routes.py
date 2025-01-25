from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_api.models import db
from flask_api.extensions import user_datastore

admin = Blueprint('admin', __name__)

########################## Admin auth ##########################
@admin.route('/admin-dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_user = get_jwt_identity()

    return jsonify(message=f"Welcome to the admin dashboard {current_user}"), 200

@admin.route('/admin-stats', methods=['GET'])
@jwt_required()
def admin_stats():
    return jsonify(message="Admin stats"), 200

######################### Delete User #########################
@admin.route('/user-delete', methods=['DELETE'])
@jwt_required()
# TODO: Need to gracefully delete all relationships with other DBs before deleting the user
def user_delete():
    try:
        # Get current user
        current_user_name = get_jwt_identity()
        current_user = user_datastore.find_user(username=current_user_name)
        
        # Check if user is admin
        if not any(role.name == 'Admin' for role in current_user.roles):
            return jsonify(message="Access denied: Admin privileges required"), 403

        # Parse the input data
        data = request.json

        # Validate that the required field is present
        if not data.get('username_to_delete'):
            return jsonify(message="Missing required field: username_to_delete"), 400

        # Check if the user to delete exists
        user_to_delete = user_datastore.find_user(username=data['username_to_delete'])
        if not user_to_delete:
            return jsonify(message="User to delete not found"), 404

        # Delete the user
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify(message=f"User '{data['username_to_delete']}' deleted successfully"), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(message="An error occurred while deleting the user", error=str(e)), 500
