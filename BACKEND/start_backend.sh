#! /usr/bin/env zsh

source venv/bin/activate
# export FLASK_APP=app.py
# export FLASK_ENV=development
rm -rf instance/main.db # Remove the previous database
flask db migrate -m "Another migration" # Create a new migration
flask create-admin arman arman fullname "Master's Degree" "1990-01-01" # Create an admin user
flask create-subjects 10 
flask create-chapters 50
flask create-quizzes 100
flask run --host=0.0.0.0 --port=5001 # Run the application