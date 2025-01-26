#! /usr/bin/env zsh

source venv/bin/activate
rm -rf instance/main.db # Remove the previous database
flask db migrate -m "Another migration" # Create a new migration
flask create-admin arman arman fullname "Master's Degree" "1990-01-01" # Create an admin user
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5001 # Run the application