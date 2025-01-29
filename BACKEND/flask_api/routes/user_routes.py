
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_api.models import db
from flask_api.extensions import user_datastore
from flask_security.utils import hash_password, verify_password


user = Blueprint('user', __name__)

######################### SignUp Logic #########################
@user.route('/user-signup', methods=['POST'])
def user_signup():
    data = request.json

    # Validate that required fields are present
    required_fields = ['username', 'password', 'full_name', 'qualification', 'dob']
    for field in required_fields:
        if not data.get(field):
            return jsonify(message=f"Missing required field: {field}"), 400

    # Check if user already exists (by username)
    if user_datastore.find_user(username=data['username']):
        return jsonify(message="Username is already taken"), 400

    # Create user
    try:
        hashed_password = hash_password(data['password'])
        user = user_datastore.create_user(
            username=data['username'], 
            password=hashed_password,
            full_name=data['full_name'],
            qualification=data['qualification'],
            dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
            active=True
        )
        user_datastore.add_role_to_user(user, 'User')
        db.session.commit()
        return jsonify(message="User registered successfully"), 201

    except Exception as e:
        db.session.rollback()
        return jsonify(message="An error occurred while registering the user", error=str(e)), 500

########################## Login Logic ##########################
def process_login(username, password, require_admin=False):
    """
    Handles the common login logic for users and admins.
    """
    # Find the user by username
    user = user_datastore.find_user(username=username)
    if not user:
        return jsonify(message="Invalid username or password"), 401

    # Check if the user is active
    if not user.active:
        return jsonify(message="Account is inactive"), 403

    # Verify the password
    if not verify_password(password, user.password):
        return jsonify(message="Invalid username or password"), 401

    # Check for admin role if required
    if require_admin and 'Admin' not in [role.name for role in user.roles]:
        return jsonify(message="Unauthorized access"), 403

    # Generate a token
    token = None
    if require_admin:
        token = create_access_token(identity=f"{username}-{user.id}")

    # Return user data and token
    return jsonify(
        message="Login successful",
        user={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "qualification": user.qualification,
            "dob": user.dob.isoformat() if user.dob else None,
            "roles": [role.name for role in user.roles]
        },
        token=token
    ), 200

@user.route('/user-login', methods=['POST'])
def user_login():
    data = request.json

    # Validate that required fields are present
    if not data.get('username') or not data.get('password'):
        return jsonify(message="Missing required fields (username or password)"), 400

    # Call the helper function for user login
    return process_login(username=data['username'], password=data['password'])

@user.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json

    # Validate that required fields are present
    if not data.get('username') or not data.get('password'):
        return jsonify(message="Missing required fields (username or password)"), 400

    # Call the helper function for admin login
    return process_login(username=data['username'], password=data['password'], require_admin=True)