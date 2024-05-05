from flask import Flask, render_template, session, request, redirect, sessions, url_for
from online_bank import create_user, get_user, get_user_credit_card, create_save_graphs, email_verification, delete_user_story_card, update_password, update_user, add_card
from datetime import datetime
from email_management import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = '26f39dc632b5b24cbdca563ee5969af42e67b789'

email_user = None


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


def end_custom():
    session.clear()


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/AboutUs")
def aboutUs():
    return render_template('aboutUs.html')


@app.route("/Support")
def support():
    return render_template('support.html')


@app.route("/Custom")
def custom():
    return render_template('customMain.html', user_name=session['user_name'], user_surname=session['user_surname'],
                           user_email=session['user_email'], user_number=session['user_number'],
                           user_gender=session['user_gender'])


@app.route("/Custom/Profile", methods=['POST', 'GET'])
def profile():
    if id_user is not None:
        create_save_graphs(id_user)
    return render_template('profile.html', user_nickname=session['user_nickname'], user_name=session['user_name'],
                           user_surname=session['user_surname'], user_age=session['user_age'],
                           user_birthday=session['user_birthday'], user_email=session['user_email'],
                           user_number=session['user_number'], user_gender=session['user_gender'],
                           user_address=session['user_address'])


@app.route("/Custom/Profile/Update", methods=['POsT', 'GET'])
def update_profile():
    if request.method == "POST":
        info_user = update_user(id_user, request.form['nickname'], request.form['name'], request.form['surname'],
                                request.form['email'], request.form['number'], request.form['address'])
        if info_user is not None:
            start_custom(info_user[1], info_user[2], info_user[3], info_user[4], info_user[5], info_user[6],
                         info_user[7], info_user[8], info_user[9], info_user[10])
    return render_template('update_profile.html', user_nickname=session['user_nickname'], user_name=session['user_name'],
                           user_surname=session['user_surname'], user_age=session['user_age'],
                           user_birthday=session['user_birthday'], user_email=session['user_email'],
                           user_number=session['user_number'], user_gender=session['user_gender'],
                           user_address=session['user_address'])


@app.route("/Custom/Wallets", methods=['POST', 'GET'])
def wallets():
    global id_user
    if id_user is not None:
        c_list = get_user_credit_card(id_user)
        c_list = "123"
        return render_template('customWallet.html', user_nickname=session['user_nickname'], user_money=session['user_money'],
                               c_list=c_list)
    return render_template('customWallet.html', user_nickname=session['user_nickname'], user_money=session['user_money'])


@app.route("/Custom/Wallets/AddCard", methods=['POST', 'GET'])
def addCard():
    global id_user
    if request.method == "POST":
        print(id_user)
        if id_user is not None:
            expiration = datetime.strptime(request.form['expiration'], '%Y-%m-%d')
            print(expiration)
            add_card(id_user, request.form['name'], request.form['surname'], request.form['number_card'],
                     request.form['cvv2'], expiration.date())
    return render_template('addСreditСard.html', )


@app.route("/Login", methods=['POST', 'GET'])
def login():
    global id_user
    id_user = None
    error = None
    if request.method == "POST":
        info_user = get_user(request.form['email'], request.form['password'])
        if info_user is not None:
            id_user = info_user[0]
            start_custom(info_user[1], info_user[2], info_user[3], info_user[4], info_user[5], info_user[6],
                         info_user[7], info_user[8], info_user[9], info_user[10])
            return redirect(url_for('custom'))
        else:
            error = "no such user was found"
    return render_template('login.html', error=error)


@app.route("/Registration", methods=['POST', 'GET'])
def registration():
    error = None
    if request.method == "POST":
        if request.form['password1'] != request.form['password2']:
            error = "Passwords don't match"
        else:
            birth_day = datetime.strptime(request.form['birth-day'], '%Y-%m-%d')
            age = datetime.now().year - birth_day.year
            if age >= 18:
                create_user(request.form['usernickname'], request.form['username'], request.form['surname'],
                            request.form['password1'], request.form['email'], request.form['number'],
                            request.form['gender'], age, birth_day.date())
                return redirect(url_for('login'))
            else:
                error = "You're under 18"
    return render_template('registration.html', error=error)


@app.route("/RequestPassword", methods=['POST', 'GET'])
def requestPassword():
    global email_user
    if request.method == "POST":
        email_user = request.form['email']
        if email_user is not None:
            if email_verification(email_user):
                send_email(email_user, '''a request has been received to change your password. 
                If it's you, please click on the link: ''')
    return render_template('requestPassword.html')


@app.route("/UpdatePassword", methods=['POST', 'GET'])
def updatePassword():
    global email_user
    if request.method == "POST":
        if email_user is not None:
            if request.form['password_1'] == request.form['password_2']:
                update_password(email_user, request.form['password_1'])
                return redirect(url_for('login'))
    return render_template('password_update.html')


@app.route("/RequestDeletion", methods=['POST', 'GET'])
def requestDeletion():
    global email_user
    if request.method == "POST":
        email_user = request.form['email']
        if email_user is not None:
            if email_verification(email_user):
                send_email(email_user, '''a request to delete your account has been received. 
                If this is you, please follow the link: ''')
    return render_template('requestDeletion.html')


@app.route("/Deletion", methods=['POST', 'GET'])
def deletion():
    global email_user
    if request.method == "POST":
        if email_user is not None:
            delete_user_story_card(email_user)
            return redirect(url_for('login'))
    return render_template('deletion.html')


if __name__ == "__main__":
    app.run(debug=True)
