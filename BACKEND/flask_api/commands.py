import click
import random
import requests
from flask.cli import with_appcontext
from flask_api.extensions import user_datastore
from flask_api.models import db
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
        click.echo('Admin created successfully')

    except Exception as e:
        db.session.rollback()
        click.echo(f'Error: {str(e)}')

################ Creating dummy data ################
fake = Faker('en_IN') # Indian locale