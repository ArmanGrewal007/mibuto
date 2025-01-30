from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_api.models import db, Quizzes, Users
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from datetime import datetime

quiz = Blueprint('quiz', __name__)

########################## Create Quiz ##########################
@quiz.route('/create-quiz', methods=['POST'])
@jwt_required()
def create_quiz():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'chapter_id', 'time_duration']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), HTTPStatus.BAD_REQUEST
        
        # Create new quiz
        new_quiz = Quizzes(
            title=data['title'],
            chapter_id=data['chapter_id'],
            time_duration=data['time_duration'],
            date_of_quiz=datetime.fromisoformat(data.get('date_of_quiz', datetime.utcnow().isoformat())),
            remarks=data.get('remarks')
        )
        
        db.session.add(new_quiz)
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz created successfully',
            'data': new_quiz.to_dict()
        }), HTTPStatus.CREATED
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error. Chapter might not exist.'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Read Quiz ##########################
@quiz.route('/get-quiz', methods=['GET'])
def get_quiz():
    try:
        quiz_id = request.args.get('id')
        
        if quiz_id:
            # Get specific quiz
            quiz_data = Quizzes.query.get(quiz_id)
            if not quiz_data:
                return jsonify({'error': 'Quiz not found'}), HTTPStatus.NOT_FOUND
            return jsonify({
                'status': 'success',
                'data': quiz_data.to_dict()
              }), HTTPStatus.OK
        else:
            # Get all quizzes with optional filters
            chapter_id = request.args.get('chapter_id')
            query = Quizzes.query
            
            if chapter_id:
                query = query.filter_by(chapter_id=chapter_id)
            
            quizzes = query.all()
            return jsonify({
                'status': 'success', 
                'data':[quiz.to_dict() for quiz in quizzes]
                }), HTTPStatus.OK
            
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Update Quiz ##########################
@quiz.route('/update-quiz', methods=['PATCH'])
@jwt_required()
def update_quiz():
    try:
        data = request.get_json()
        quiz_id = data.get('id')
        
        if not quiz_id:
            return jsonify({'error': 'Quiz ID is required'}), HTTPStatus.BAD_REQUEST
            
        quiz_to_update = Quizzes.query.get(quiz_id)
        if not quiz_to_update:
            return jsonify({'error': 'Quiz not found'}), HTTPStatus.NOT_FOUND
            
        # Update fields if provided
        if 'title' in data:
            quiz_to_update.title = data['title']
        if 'chapter_id' in data:
            quiz_to_update.chapter_id = data['chapter_id']
        if 'time_duration' in data:
            quiz_to_update.time_duration = data['time_duration']
        if 'date_of_quiz' in data:
            quiz_to_update.date_of_quiz = datetime.fromisoformat(data['date_of_quiz'])
        if 'remarks' in data:
            quiz_to_update.remarks = data['remarks']
            
        db.session.commit()
        return jsonify({
            'message': 'Quiz updated successfully',
            'data': quiz_to_update.to_dict()
        }), HTTPStatus.OK
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error. Chapter might not exist.'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

########################## Delete Quiz ##########################
@quiz.route('/delete-quiz', methods=['DELETE'])
@jwt_required()
def delete_quiz():
    try:
        quiz_id = request.args.get('id')
        
        if not quiz_id:
            return jsonify({'error': 'Quiz ID is required'}), HTTPStatus.BAD_REQUEST
            
        quiz_to_delete = Quizzes.query.get(quiz_id)
        if not quiz_to_delete:
            return jsonify({'error': 'Quiz not found'}), HTTPStatus.NOT_FOUND
            
        db.session.delete(quiz_to_delete)
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz deleted successfully',
            'id': quiz_id
        }), HTTPStatus.OK
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR