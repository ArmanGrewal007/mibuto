import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# Many-to-many relationship table for Users <-> Roles
users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    qualification = db.Column(db.String(255), nullable=True)
    dob = db.Column(db.Date(), nullable=True)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    roles = db.relationship('Roles', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))
    scores = db.relationship('Scores', backref='user', lazy=True)

class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chapters = db.relationship('Chapters', backref='subject', lazy=True, cascade='all, delete-orphan')
    def to_dict(self):
      return {
          "id": self.id,
          "name": self.name,
          "description": self.description,
          "created_by": self.created_by,
          "created_at": self.created_at,
          "chapters": [chapter.to_dict() for chapter in self.chapters]
      }

class Chapters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quizzes = db.relationship('Quizzes', backref='chapter', lazy=True, cascade='all, delete-orphan')
    def to_dict(self):
      return {
          "id": self.id,
          "name": self.name,
          "description": self.description,
          "subject_id": self.subject_id,
          "created_at": self.created_at,
          "quizzes": [quiz.to_dict() for quiz in self.quizzes]
      }

class Quizzes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, default=datetime.utcnow)
    time_duration = db.Column(db.Integer, nullable=False)  # Duration in seconds
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('Questions', backref='quiz', lazy=True, cascade='all, delete-orphan')
    scores = db.relationship('Scores', backref='quiz', lazy=True)
    def to_dict(self):
      return {
          "id": self.id,
          "title": self.title,
          "chapter_id": self.chapter_id,
          "date_of_quiz": self.date_of_quiz,
          "time_duration": self.time_duration,
          "remarks": self.remarks,
          "created_at": self.created_at,
          "questions": [question.to_dict() for question in self.questions]
      }

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    def to_dict(self):
      return {
          "id": self.id,
          "quiz_id": self.quiz_id,
          "question_statement": self.question_statement,
          "option1": self.option1,
          "option2": self.option2,
          "option3": self.option3,
          "option4": self.option4,
          "correct_option": self.correct_option
      }
