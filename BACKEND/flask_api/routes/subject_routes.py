from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_api.models import db, Subjects, Users
from http import HTTPStatus

subject = Blueprint('subject', __name__)

########################## Create Subject ##########################
@subject.route('/create-subject', methods=['POST'])
@jwt_required()
def create_subject():
    try:
        # Get current user's ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name'):
            return jsonify({
                'message': 'Subject name is required'
            }), HTTPStatus.BAD_REQUEST
            
        # Check if subject already exists
        existing_subject = Subjects.query.filter_by(name=data['name']).first()
        if existing_subject:
            return jsonify({
                'message': 'Subject with this name already exists'
            }), HTTPStatus.CONFLICT
            
        # Create new subject
        new_subject = Subjects(
            name=data['name'],
            description=data.get('description'),
            created_by=current_user_id
        )
        
        db.session.add(new_subject)
        db.session.commit()
        
        return jsonify({
            'message': 'Subject created successfully',
            'subject': {
                'id': new_subject.id,
                'name': new_subject.name,
                'description': new_subject.description,
                'created_by': new_subject.created_by,
                'created_at': new_subject.created_at
            }
        }), HTTPStatus.CREATED
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error creating subject',
            'error': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Read Subject ##########################
@subject.route('/get-subject', methods=['GET'])
def get_subject():
    try:
        subject_id = request.args.get('id')
        
        if subject_id:
            # Get specific subject
            subject = Subjects.query.get(subject_id)
            if not subject:
                return jsonify({
                    'message': 'Subject not found'
                }), HTTPStatus.NOT_FOUND
                
            return jsonify({
                'subject': {
                    'id': subject.id,
                    'name': subject.name,
                    'description': subject.description,
                    'created_by': subject.created_by,
                    'created_at': subject.created_at
                }
            }), HTTPStatus.OK
            
        else:
            # Get all subjects
            subjects = Subjects.query.all()
            subjects_list = [{
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'created_by': subject.created_by,
                'created_at': subject.created_at
            } for subject in subjects]
            
            return jsonify({
                'subjects': subjects_list
            }), HTTPStatus.OK
            
    except Exception as e:
        return jsonify({
            'message': 'Error fetching subjects',
            'error': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Update Subject ##########################
@subject.route('/update-subject/<int:subject_id>', methods=['PATCH'])
@jwt_required()
def update_subject(subject_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Get subject
        subject = Subjects.query.get(subject_id)
        if not subject:
            return jsonify({
                'message': 'Subject not found'
            }), HTTPStatus.NOT_FOUND
            
        # Check if current user created the subject
        if subject.created_by != current_user_id:
            return jsonify({
                'message': 'Unauthorized to update this subject'
            }), HTTPStatus.FORBIDDEN
            
        # Get request data
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            # Check if new name already exists
            existing_subject = Subjects.query.filter(
                Subjects.name == data['name'],
                Subjects.id != subject_id
            ).first()
            if existing_subject:
                return jsonify({
                    'message': 'Subject with this name already exists'
                }), HTTPStatus.CONFLICT
            subject.name = data['name']
            
        if 'description' in data:
            subject.description = data['description']
            
        db.session.commit()
        
        return jsonify({
            'message': 'Subject updated successfully',
            'subject': {
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'created_by': subject.created_by,
                'created_at': subject.created_at
            }
        }), HTTPStatus.OK
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error updating subject',
            'error': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Delete Subject ##########################
@subject.route('/delete-subject/<int:subject_id>', methods=['DELETE'])
@jwt_required()
def delete_subject(subject_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Get subject
        subject = Subjects.query.get(subject_id)
        if not subject:
            return jsonify({
                'message': 'Subject not found'
            }), HTTPStatus.NOT_FOUND
            
        # Check if current user created the subject
        if subject.created_by != current_user_id:
            return jsonify({
                'message': 'Unauthorized to delete this subject'
            }), HTTPStatus.FORBIDDEN
            
        # Delete subject (will cascade delete related chapters and quizzes)
        db.session.delete(subject)
        db.session.commit()
        
        return jsonify({
            'message': 'Subject deleted successfully'
        }), HTTPStatus.OK
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error deleting subject',
            'error': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR