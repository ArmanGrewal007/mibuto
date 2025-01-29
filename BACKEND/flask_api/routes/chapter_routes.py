from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_api.models import db, Chapters, Users
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from datetime import datetime

chapter = Blueprint('chapter', __name__)

########################## Create Chapter ##########################
@chapter.route('/create-chapter', methods=['POST'])
@jwt_required()
def create_chapter():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'subject_id']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields. Required: name, subject_id'
            }), HTTPStatus.BAD_REQUEST
        
        # Create new chapter
        new_chapter = Chapters(
            name=data['name'],
            description=data.get('description', ''),  # Optional field
            subject_id=data['subject_id']
        )
        
        db.session.add(new_chapter)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Chapter created successfully',
            'data': new_chapter.to_dict()
        }), HTTPStatus.CREATED
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Chapter name already exists'
        }), HTTPStatus.CONFLICT
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Read Chapter ##########################
@chapter.route('/get-chapter', methods=['GET'])
def get_chapter():
    try:
        chapter_id = request.args.get('chapter_id')
        subject_id = request.args.get('subject_id')
        
        if chapter_id:
            # Get specific chapter
            chapter = Chapters.query.get(chapter_id)
            if not chapter:
                return jsonify({
                    'status': 'error',
                    'message': 'Chapter not found'
                }), HTTPStatus.NOT_FOUND
            return jsonify({
                'status': 'success',
                'data': chapter.to_dict()
            }), HTTPStatus.OK
            
        elif subject_id:
            # Get all chapters for a subject
            chapters = Chapters.query.filter_by(subject_id=subject_id).all()
            return jsonify({
                'status': 'success',
                'data': [chapter.to_dict() for chapter in chapters]
            }), HTTPStatus.OK
            
        else:
            # Get all chapters
            chapters = Chapters.query.all()
            return jsonify({
                'status': 'success',
                'data': [chapter.to_dict() for chapter in chapters]
            }), HTTPStatus.OK
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Update Chapter ##########################
@chapter.route('/update-chapter/<int:chapter_id>', methods=['PATCH'])
@jwt_required()
def update_chapter(chapter_id):
    try:
        chapter = Chapters.query.get(chapter_id)
        if not chapter:
            return jsonify({
                'status': 'error',
                'message': 'Chapter not found'
            }), HTTPStatus.NOT_FOUND
        
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            chapter.name = data['name']
        if 'description' in data:
            chapter.description = data['description']
        if 'subject_id' in data:
            chapter.subject_id = data['subject_id']
            
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Chapter updated successfully',
            'data': chapter.to_dict()
        }), HTTPStatus.OK
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Chapter name already exists'
        }), HTTPStatus.CONFLICT
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Delete Chapter ##########################
@chapter.route('/delete-chapter/<int:chapter_id>', methods=['DELETE'])
@jwt_required()
def delete_chapter(chapter_id):
    try:
        chapter = Chapters.query.get(chapter_id)
        if not chapter:
            return jsonify({
                'status': 'error',
                'message': 'Chapter not found'
            }), HTTPStatus.NOT_FOUND
            
        db.session.delete(chapter)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Chapter deleted successfully'
        }), HTTPStatus.OK
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR