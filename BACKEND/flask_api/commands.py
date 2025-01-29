import click
import random
import requests
from flask.cli import with_appcontext
from flask_api.extensions import user_datastore
from flask_api.models import db, Subjects
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