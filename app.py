from flask import Flask, render_template, session, request, redirect, sessions, url_for # Importing necessary modules for creating a Flask web application
from online_bank import create_user, get_user, get_user_credit_card, create_save_graphs, email_verification, delete_user_story_card, update_password, update_user, add_card # Importing functions from online_bank module
from datetime import datetime # Importing datetime module for handling date and time
from email_management import send_email # Importing send_email function from email_management module

app = Flask(__name__) # Creating a Flask web application
app.config['SECRET_KEY'] = '26f39dc632b5b24cbdca563ee5969af42e67b789' # Setting a secret key for the application

email_user = None # Initializing email_user variable

# Function to start a custom session for the user
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

# Function to end a custom session for the user
def end_custom():
    session.clear() # Clearing all session variables

# Route for the home page
@app.route("/")
def index():
    return render_template('home.html') # Rendering home.html template

# Route for the About Us page
@app.route("/AboutUs")
def aboutUs():
    return render_template('aboutUs.html') # Rendering aboutUs.html template

# Route for the Support page
@app.route("/Support")
def support():
    return render_template('support.html') # Rendering support.html template

# Route for the Custom page
@app.route("/Custom")
def custom():
    return render_template('customMain.html', user_name=session['user_name'], user_surname=session['user_surname'],
                           user_email=session['user_email'], user_number=session['user_number'],
                           user_gender=session['user_gender']) # Rendering customMain.html template with user details

# Route for the Profile page
@app.route("/Custom/Profile", methods=['POST', 'GET'])
def profile():
    global id_user # Declaring id_user as a global variable
    if id_user is not None: # Checking if the user is logged in
        create_save_graphs(id_user) # Creating and saving graphs for the user
    return render_template('profile.html', user_nickname=session['user_nickname'], user_name=session['user_name'],
                           user_surname=session['user_surname'], user_age=session['user_age'],
                           user_birthday=session['user_birthday'], user_email=session['user_email'],
                           user_number=session['user_number'], user_gender=session['user_gender'],
                           user_address=session['user_address']) # Rendering profile.html template with user details

# Route for updating the user profile
@app.route("/Custom/Profile/Update", methods=['POsT', 'GET'])
def update_profile():
    if request.method == "POST": # Checking if the request method is POST
        info_user = update_user(id_user, request.form['nickname'], request.form['name'], request.form['surname'],
                                request.form['email'], request.form['number'], request.form['address']) # Updating user information
        if info_user is not None:
            start_custom(info_user[1], info_user[2], info_user[3], info_user[4], info_user[5], info_user[6],
                         info_user[7], info_user[8], info_user[9], info_user[10]) # Starting a new custom session with updated user information
    return render_template('update_profile.html', user_nickname=session['user_nickname'], user_name=session['user_name'],
                           user_surname=session['user_surname'], user_age=session['user_age'],
                           user_birthday=session['user_birthday'], user_email=session['user_email'],
                           user_number=session['user_number'], user_gender=session['user_gender'],
                           user_address=session['user_address']) # Rendering update_profile.html template

# Route for the Wallets page
@app.route("/Custom/Wallets", methods=['POST', 'GET'])
def wallets():
    global id_user # Declaring id_user as a global variable
    if id_user is not None: # Checking if the user is logged in
        c_list = get_user_credit_card(id_user) # Getting the list of credit cards for the user
        return render_template('customWallet.html', user_nickname=session['user_nickname'], user_money=session['user_money'],
                               c_list=c_list) # Rendering customWallet.html template with user details and credit card list
    return render_template('customWallet.html', user_nickname=session['user_nickname'], user_money=session['user_money']) # If the user is not logged in, rendering the template with only user details

# Route for adding a new credit card
@app.route("/Custom/Wallets/AddCard", methods=['POST', 'GET'])
def addCard():
    global id_user # Declaring id_user as a global variable
    if request.method == "POST": # Checking if the request method is POST
        if id_user is not None: # Checking if the user is logged in
            expiration = datetime.strptime(request.form['expiration'], '%Y-%m-%d') # Parsing the expiration date from the form
            add_card(id_user, request.form['name'], request.form['surname'], request.form['number_card'],
                     request.form['cvv2'], expiration.date()) # Adding a new credit card for the user
    return render_template('addСreditСard.html') # Rendering addСreditСard.html template

# Route for user login
@app.route("/Login", methods=['POST', 'GET'])
def login():
    global id_user # Declaring id_user as a global variable
    id_user = None # Initializing id_user
    error = None # Initializing error
    if request.method == "POST": # Checking if the request method is POST
        info_user = get_user(request.form['email'], request.form['password']) # Getting user information from the email and password
        if info_user is not None: # Checking if the user exists
            id_user = info_user[0] # Setting id_user to the user id
            start_custom(info_user[1], info_user[2], info_user[3], info_user[4], info_user[5], info_user[6],
                         info_user[7], info_user[8], info_user[9], info_user[10]) # Starting a new custom session with user information
            return redirect(url_for('custom')) # Redirecting to the Custom page
        else:
            error = "no such user was found" # Setting error if the user is not found
    return render_template('login.html', error=error) # Rendering login.html template with error

# Route for user registration
@app.route("/Registration", methods=['POST', 'GET'])
def registration():
    error = None # Initializing error
    if request.method == "POST": # Checking if the request method is POST
        if request.form['password1'] != request.form['password2']: # Checking if the passwords match
            error = "Passwords don't match" # Setting error if the passwords don't match
        else:
            birth_day = datetime.strptime(request.form['birth-day'], '%Y-%m-%d') # Parsing the birth day from the form
            age = datetime.now().year - birth_day.year # Calculating the user age
            if age >= 18: # Checking if the user is at least 18 years old
                create_user(request.form['usernickname'], request.form['username'], request.form['surname'],
                            request.form['password1'], request.form['email'], request.form['number'],
                            request.form['gender'], age, birth_day.date()) # Creating a new user
                return redirect(url_for('login')) # Redirecting to the Login page
            else:
                error = "You're under 18" # Setting error if the user is not at least 18 years old
    return render_template('registration.html', error=error) # Rendering registration.html template with error

# Route for requesting password change
@app.route("/RequestPassword", methods=['POST', 'GET'])
def requestPassword():
    global email_user # Declaring email_user as a global variable
    if request.method == "POST": # Checking if the request method is POST
        email_user = request.form['email'] # Setting email_user to the email from the form
        if email_user is not None: # Checking if the email is provided
            if email_verification(email_user): # Checking if the email is verified
                send_email(email_user, '''a request has been received to change your password. 
                If it's you, please click on the link: ''') # Sending an email to change the password
    return render_template('requestPassword.html') # Rendering requestPassword.html template

# Route for updating the password
@app.route("/UpdatePassword", methods=['POST', 'GET'])
def updatePassword():
    global email_user # Declaring email_user as a global variable
    if request.method == "POST": # Checking if the request method is POST
        if email_user is not None: # Checking if the email is provided
            if request.form['password_1'] == request.form['password_2']: # Checking if the new passwords match
                update_password(email_user, request.form['password_1']) # Updating the password
                return redirect(url_for('login')) # Redirecting to the Login page
    return render_template('password_update.html') # Rendering password_update.html template

# Route for requesting account deletion
@app.route("/RequestDeletion", methods=['POST', 'GET'])
def requestDeletion():
    global email_user # Declaring email_user as a global variable
    if request.method == "POST": # Checking if the request method is POST
        email_user = request.form['email'] # Setting email_user to the email from the form
        if email_user is not None: # Checking if the email is provided
            if email_verification(email_user): # Checking if the email is verified
                send_email(email_user, '''a request to delete your account has been received. 
                If this is you, please follow the link: ''') # Sending an email to delete the account
    return render_template('requestDeletion.html') # Rendering requestDeletion.html template

# Route for account deletion
@app.route("/Deletion", methods=['POST', 'GET'])
def deletion():
    global email_user # Declaring email_user as a global variable
    if request.method == "POST": # Checking if the request method is POST
        if email_user is not None: # Checking if the email is provided
            delete_user_story_card(email_user) # Deleting the user's stories and cards
            return redirect(url_for('login')) # Redirecting to the Login page
    return render_template('deletion.html') # Rendering deletion.html template

if __name__ == "__main__":
    app.run(debug=True) # Running the Flask application in debug mode
