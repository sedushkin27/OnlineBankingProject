from flask import Flask, render_template, session, request, redirect, sessions, url_for
from online_bank import create_user, get_user, create_save_graphs
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '26f39dc632b5b24cbdca563ee5969af42e67b789'


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
    if request.method == 'GET':
        if id is not None:
            create_save_graphs(id)
    return render_template('profile.html', user_nickname=session['user_nickname'], user_name=session['user_name'],
                           user_surname=session['user_surname'], user_age=session['user_age'],
                           user_birthday=session['user_birthday'], user_email=session['user_email'],
                           user_number=session['user_number'], user_gender=session['user_gender'],
                           uset_address=session['user_address'])


@app.route("/Custom/Wallets")
def wallets():
    return render_template('customWallet.html', user_name=session['user_name'], user_money=session['user_money'])


@app.route("/Login", methods=['POST', 'GET'])
def login():
    global id
    id = None
    error = None
    if request.method == "POST":
        info_user = get_user(request.form['email'], request.form['password'])
        if info_user is not None:
            id = info_user[0]
            start_custom(info_user[1], info_user[2], info_user[3], info_user[4], info_user[5], info_user[6],
                         info_user[7], info_user[8], info_user[9], info_user[10])
            return redirect(url_for('custom'))
        else:
            error = "no such user was found"
    return render_template('Login.html', error=error)


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
    return render_template('Registration.html', error=error)


@app.route("/RequestPassword", methods=['POST', 'GET'])
def requestPassword():
    return render_template('RequestPassword.html')


if __name__ == "__main__":
    app.run(debug=True)
