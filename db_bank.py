import sqlite3

def open():
    global conn, cursor
    conn = sqlite3.connect('db/bank.db')
    cursor = conn.cursor()
    query = ''' CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        password TEXT NOT NULL,
        email CHAR(30) NOT NULL,
        phoneNumber INTEGER NOT NULL,
        gender TEXT NOT NULL,
        money INTEGER NOT NULL
    ) '''
    cursor.execute(query)


def close():
    conn.commit()
    cursor.close()
    conn.close()


def create_user(name, surname, password, email, phoneNumber, gender):
    open()
    cursor.execute(''' INSERT INTO users (name, surname, password, email, phoneNumber, gender, money) 
        VALUES(?,?,?,?,?,?,?)
    ''', (name, surname, password, email, phoneNumber, gender, 0))
    close()


def get_user(email, password):
    result = None
    open()
    for value in cursor.execute('''SELECT name, surname, email, phoneNumber, gender, money FROM users WHERE email = ? 
            AND password = ?''', (email, password)):
        result = value
    close()
    return result