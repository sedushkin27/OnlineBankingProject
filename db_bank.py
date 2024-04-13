import hashlib
import sqlite3
import os

def hesh_password(password):
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()

def open():
    global conn, cursor
    conn = sqlite3.connect('db/bank.db')
    cursor = conn.cursor()
    query_1 = ''' CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        password TEXT NOT NULL,
        email CHAR(30) NOT NULL,
        phoneNumber INTEGER NOT NULL,
        gender TEXT NOT NULL,
        money INTEGER NOT NULL
    ) '''
    cursor.execute(query_1)


def close():
    conn.commit()
    cursor.close()
    conn.close()


def create_user(name, surname, password, email, phoneNumber, gender):
    open()
    cursor.execute(''' INSERT INTO users (name, surname, password, email, phoneNumber, gender, money) 
        VALUES(?,?,?,?,?,?,?)
    ''', (name, surname, hesh_password(password), email, phoneNumber, gender, 0))
    close()


def get_user(email, password):
    result = None
    open()
    for value in cursor.execute('''SELECT name, surname, email, phoneNumber, gender, money FROM users WHERE email = ? 
            AND password = ?''', (email, hesh_password(password))):
        result = value
    close()
    return result