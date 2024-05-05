# Importing necessary modules for creating a Flask web application
from flask import Flask, render_template, session, request, redirect, sessions, url_for # Importing necessary modules for creating a Flask web application
from online_bank import create_user, get_user, get_user_credit_card, create_save_graphs, email_verification, delete_user_story_card, update_password, update_user, add_card # Importing functions from online_bank module
from datetime import datetime # Importing datetime module for handling date and time
from email_management import send_email # Importing send_email function from email_management module

# Creating a Flask web application
app = Flask(__name__)

# Setting a secret key for the application
app.config['SECRET_KEY'] = '26f39dc632b5b24cbdca563ee5969af42e67b789'

# Initializing email_user variable
email_user = None

# Helper function to start a custom session for the user
def start_custom(nickname, name, surname, email, number, gender, age, address, birthday, money):
    session['user_nickname'] = nickname
    session['user_name'] = name
    session['user_surname'] = surname
    session['user_email'] = email
    session['user_number'] = number
    session['user_gender'] = gender
    session['user_age'] = age
    session['user_address'] = address
    session['user_birthday'] = birthday
    session['user_money'] = money

# Helper function to end a custom session for the user
def end_custom():
    session.clear() # Clearing all session variables

# Route for the home page
@app.route("/")
def index():
    return render_template('home.html') # Rendering home.html template

# ... (other route functions)

# Main
if __name__ == "__main__":
    app.run(debug=True) # Running the Flask application in debug mode
