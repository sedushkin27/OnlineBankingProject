from flask import Flask, render_template, session, request, redirect, sessions, url_for
from db_bank import create_user, get_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '26f39dc632b5b24cbdca563ee5969af42e67b789'


def start_custom(name, surname, email, number, gender, money):
    session['username'] = name
    session['usersurname'] = surname
    session['useremail'] = email
    session['usernumber'] = number
    session['usergender'] = gender
    session['usermoney'] = money


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
    return render_template('customMain.html', username=session['username'], usersurname=session['usersurname'],
                           useremail=session['useremail'], usernumber=session['usernumber'],
                           usergender=session['usergender'])


@app.route("/Custom/Wallets")
def wallets():
    return render_template('customWallet.html', username=session['username'], usersurname=session['usersurname'],
                           useremail=session['useremail'], usernumber=session['usernumber'],
                           usergender=session['usergender'])


@app.route("/Login", methods=['POST', 'GET'])
def login():
    info_user = None
    if request.method == "POST":
        info_user = get_user(request.form['email'], request.form['password'])
        if info_user != None:
            start_custom(info_user[0], info_user[1], info_user[2], info_user[3], info_user[4], info_user[5])
            return redirect(url_for('custom'))
        else:
            print("NO")
    return render_template('Login.html')


@app.route("/Registration", methods=['POST', 'GET'])
def registration():
    error = None
    if request.method == "POST":
        if request.form['password1'] != request.form['password2']:
            error = "passwords don't match"
        else:
            create_user(request.form['username'], request.form['surname'], request.form['password1'],
                        request.form['email'], request.form['number'], 'male')
            return redirect(url_for('login'))
    return render_template('Registration.html', error=error)


@app.route("/RequestPassword", methods=['POST', 'GET'])
def requestPassword():
    return render_template('RequestPassword.html')


if __name__ == "__main__":
    app.run(debug=True)