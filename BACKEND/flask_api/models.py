import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# Many-to-many relationship table for Users <-> Roles
users_roles = db.Table('users_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)

class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))          
    qualification = db.Column(db.String(255))      
    dob = db.Column(db.Date())                     
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    roles = db.relationship('Roles', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))
    # scores = db.relationship('Score', backref='user', lazy=True)  

# class Subjects(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')

# class Chapters(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')

# class Quizzes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200))
#     chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
#     date_of_quiz = db.Column(db.DateTime)
#     time_duration = db.Column(db.String(5))  # HH:MM format
#     remarks = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
#     scores = db.relationship('Score', backref='quiz', lazy=True)

# class Questions(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
#     question_statement = db.Column(db.Text, nullable=False)
#     option1 = db.Column(db.String(255))
#     option2 = db.Column(db.String(255))
#     option3 = db.Column(db.String(255))
#     option4 = db.Column(db.String(255))
#     correct_option = db.Column(db.Integer, nullable=False)  # Stores 1-4

# class Scores(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
#     score = db.Column(db.Integer, nullable=False)
#     total_questions = db.Column(db.Integer, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
