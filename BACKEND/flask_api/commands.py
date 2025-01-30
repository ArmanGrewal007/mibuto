import click
import random
import requests
from flask.cli import with_appcontext
from flask_api.extensions import user_datastore
from flask_api.models import db, Subjects, Chapters, Quizzes
from flask_security.utils import hash_password
from faker import Faker
from datetime import date, datetime, timedelta

################ Creating admin user ################
@click.command('create-admin')
@click.argument('username')
@click.argument('password')
@click.argument('full_name')
@click.argument('qualification')
@click.argument('dob')
@with_appcontext
def create_admin(username, password, full_name, qualification, dob):
    """
    Create an admin user. 
    """
    try:
        # Create admin role if it doesn't exist
        admin_role = user_datastore.find_role('Admin')
        if not admin_role:
            admin_role = user_datastore.create_role(
                name='Admin',
                description='Administrator role'
            )
            db.session.flush()  # Ensure the role has an ID

        # Create user role if it doesn't exist
        user_role = user_datastore.find_role('User')
        if not user_role:
            user_role = user_datastore.create_role(
                name='User',
                description='Regular user role'
            )
            db.session.flush()  # Ensure the role has an ID

        # Create admin user
        hashed_password = hash_password(password)
        admin_user = user_datastore.create_user(
            username=username,
            password=hashed_password,
            full_name=full_name,
            qualification=qualification,
            dob=date.fromisoformat(dob),
            active=True,
            roles=[admin_role, user_role]  # Assign roles directly during creation
        )
        
        db.session.commit()
        click.echo('Admin created')

    except Exception as e:
        db.session.rollback()
        click.echo(f'Error: {str(e)}')

################ Creating dummy data ################
fake = Faker('en_IN') # Indian locale

################ Creating dummy subjects ################
@click.command('create-subjects')
@click.argument('n', type=int)
@with_appcontext
def create_subjects(n):
    try:
        academic_subjects = [
            'Mathematics', 'Physics', 'Chemistry',
            'Biology', 'Computer Science', 'Literature',
            'History', 'Art', 'Economics'
        ]        
        admin_user = user_datastore.find_role('Admin').users.first()
        if not admin_user:
            click.echo("Error: No admin user found.")
            return
        admin_user_id = admin_user.id
        subjects = []
        for _ in range(n):
            name = f"{fake.random_element(academic_subjects)}-{fake.random_int(min=100, max=400)}"
            description = (
                f"Study of {fake.random_element(['atoms', 'molecules', 'structures'])} and "
                f"{fake.random_element(['forces', 'dynamics', 'systems'])}."
            )
            
            subject = Subjects(
                name=name,
                description=description,
                created_by=admin_user_id
            )
            subjects.append(subject)

        db.session.bulk_save_objects(subjects)
        db.session.commit()
        click.echo(f"{n} dummy subject(s) created.")

    except Exception as e:
        db.session.rollback()
        click.echo(f"Error: {str(e)}")

################ Creating dummy chapters ################
@click.command('create-chapters')
@click.argument('n', type=int)
@with_appcontext
def create_chapters(n):
    try:
        subjects = Subjects.query.all()
        if not subjects:
            click.echo("Error: No subjects found. Create subjects first.")
            return

        chapter_components = {
            'prefixes': [
                'Introduction to', 'Fundamentals of', 'Advanced',
                'Principles of', 'Applications of', 'Modern',
                'Basic', 'Theoretical', 'Experimental',
                'Comparative', 'History of', 'Digital'
            ],
            'topics': [
                'Thermodynamics', 'Organic Chemistry', 'Linear Algebra',
                'Cell Biology', 'Algorithms', 'World Literature',
                'Microeconomics', 'Renaissance Art', 'Quantum Mechanics',
                'Genetics', 'Data Structures', 'Ancient Civilizations',
                'Electromagnetism', 'Biochemistry', 'Probability Theory'
            ],
            'suffixes': [
                'I', 'II', 'III', 'IV',
                'Concepts', 'Systems', 'Analysis',
                'Theory', 'Practice', 'Methods',
                'and Applications', 'in Modern Science', 'in Technology'
            ]
        }

        chapters = []
        used_names = set()  # Track names in current batch
        existing_names = {c.name for c in Chapters.query.all()}  # Existing DB names

        for _ in range(n):
            retry_count = 0
            while True:
                # Build chapter name
                name = ' '.join([
                    fake.random_element(chapter_components['prefixes']),
                    fake.random_element(chapter_components['topics']),
                    fake.random_element(chapter_components['suffixes'])
                ]).replace('  ', ' ').strip()

                # Check uniqueness in both DB and current batch
                if name not in existing_names and name not in used_names:
                    break

                # Append random number if duplicate
                name += f" {fake.random_int(1, 1000)}"
                retry_count += 1
                if retry_count > 5:  # Prevent infinite loop
                    break

            used_names.add(name)
            existing_names.add(name)

            # Create description
            description = (
                f"Comprehensive study of {name.split(' ', 2)[-1].lower()} "
                f"covering {fake.random_element(['key concepts', 'practical applications','theoretical foundations', 'historical context'])}. "
                f"Topics include {fake.random_element(['research methods', 'case studies', 'experimental approaches', 'analytical techniques'])} "
                f"in {fake.random_element(['physical sciences', 'biological systems', 'mathematical frameworks', 'computational methods'])}."
            )

            subject = fake.random_element(subjects)
            
            chapters.append(Chapters(
                name=name,
                description=description,
                subject_id=subject.id,
            ))

        # Use individual inserts with ignore for SQLite
        try:
            db.session.bulk_save_objects(chapters)
            db.session.commit()
        except Exception:
            db.session.rollback()
            # Fallback to individual inserts
            for chapter in chapters:
                try:
                    db.session.add(chapter)
                    db.session.commit()
                except Exception:
                    db.session.rollback()
                    continue

        click.echo(f"{len(chapters)} dummy chapter(s) created. {(n - len(chapters))} duplicates skipped.")

    except Exception as e:
        db.session.rollback()
        click.echo(f"Error: {str(e)}")


################ Creating dummy quizzes ################
@click.command('create-quizzes')
@click.argument('n', type=int)
@with_appcontext
def create_quizzes(n):
    try:
        chapters = Chapters.query.all()
        if not chapters:
            click.echo("Error: No chapters found. Create chapters first.")
            return

        quiz_titles = {
            'prefixes': [
                'Basic', 'Advanced', 'Comprehensive', 'Final', 'Midterm',
                'Introductory', 'Mastery', 'Fundamental', 'Applied'
            ],
            'topics': [
                'Assessment', 'Test', 'Quiz', 'Examination', 'Evaluation',
                'Challenge', 'Review', 'Practice Test'
            ]
        }

        quizzes = []
        used_titles = set()
        existing_titles = {q.title for q in Quizzes.query.all()}

        for _ in range(n):
            retry_count = 0
            while True:
                title = f"{fake.random_element(quiz_titles['prefixes'])} {fake.random_element(quiz_titles['topics'])}"
                if title not in existing_titles and title not in used_titles:
                    break
                title += f" {fake.random_int(1, 1000)}"
                retry_count += 1
                if retry_count > 5:
                    break

            used_titles.add(title)
            existing_titles.add(title)

            chapter = fake.random_element(chapters)
            date_of_quiz = datetime.utcnow() + timedelta(days=fake.random_int(-30, 30))
            time_duration = fake.random_int(600, 3600)  # 10 min to 1 hour
            remarks = fake.sentence() if fake.boolean() else None

            quizzes.append(Quizzes(
                title=title,
                chapter_id=chapter.id,
                date_of_quiz=date_of_quiz,
                time_duration=time_duration,
                remarks=remarks
            ))

        try:
            db.session.bulk_save_objects(quizzes)
            db.session.commit()
        except Exception:
            db.session.rollback()
            for quiz in quizzes:
                try:
                    db.session.add(quiz)
                    db.session.commit()
                except Exception:
                    db.session.rollback()
                    continue

        click.echo(f"{len(quizzes)} dummy quiz(zes) created. {(n - len(quizzes))} duplicates skipped.")

    except Exception as e:
        db.session.rollback()
        click.echo(f"Error: {str(e)}")
