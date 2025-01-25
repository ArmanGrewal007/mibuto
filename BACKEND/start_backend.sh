#! /usr/bin/env zsh

source venv/bin/activate
rm -rf instance/main.db # Remove the previous database
flask db migrate -m "Another migration" # Create a new migration
flask create-admin arman arman@example.com arman # Create an admin user
export FLASK_APP=app.py
flask run # Run the application