import numpy as np
import matplotlib.pyplot as plt
import hashlib
import sqlite3
from random import randint
from datetime import datetime, timedelta
import os


def hesh_password(password):
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()


def open():
    global conn, cursor
    conn = sqlite3.connect('db/online_bank.db')
    cursor = conn.cursor()
    query_1 = ''' CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY NOT NULL,
        nickname TEXT NOT NULL,
        name TEXT DEFAULT 'unspecified', 
        surname TEXT DEFAULT 'unspecified',
        password TEXT NOT NULL,
        email CHAR(30) NOT NULL,
        phoneNumber CHAR(30) NOT NULL,
        gender TEXT NOT NULL,
        age INTEGER NOT NULL,
        birthday DATE NOT NULL,
        address TEXT DEFAULT 'unspecified',
        money INTEGER NOT NULL
    ) '''
    query_2 = ''' CREATE TABLE IF NOT EXISTS credit_cards(
        id INTEGER PRIMARY KEY NOT NULL,
        number_card TEXT NOT NULL,
        time_limit_expires DATE NOT NULL,
        cvv2 INTEGER NOT NULL,
        money INTEGER NOT NULL
    ) '''
    query_3 = ''' CREATE TABLE IF NOT EXISTS user_story(
        id INTEGER PRIMARY KEY NOT NULL,
        id_user INTEGER NOT NULL, 
        date DATE NOT NULL,
        money INTEGER NOT NULL,
        FOREIGN KEY (id_user) REFERENCES users(id)
    ) '''
    cursor.execute(query_1)
    cursor.execute(query_2)
    cursor.execute(query_3)


def close():
    conn.commit()
    cursor.close()
    conn.close()


def create_test_card():
    time_limit_expires = datetime.now() + timedelta(days=15*365)
    number_card = randint(100000000000000, 999999999999999)
    cvv2 = randint(100, 999)
    cursor.execute(f''' INSERT INTO credit_cards (number_card, time_limit_expires, cvv2, money) VALUES(?,?,?,?)''',
                   (number_card, time_limit_expires.date(), cvv2, 100))


def create_user(nickname, name, surname, password, email, phoneNumber, gender, age, birthday):
    open()
    cursor.execute(f''' INSERT INTO users (nickname, name, surname, password, email, 
        phoneNumber, gender, age, birthday, money) 
        VALUES(?,?,?,?,?,?,?,?,?,?)
        ''', (nickname, name, surname, hesh_password(password), email, phoneNumber, gender, age, birthday, 0))
    create_test_card()
    close()


def create_save_graphs(id_user):
    x = []
    y = []
    story = get_story(id_user)
    for i in story:
        x.append(i[0])
        y.append(i[1])
    plt.bar(x, y)
    plt.savefig('static/image/graphs_story.png')


def add_story(id_user, money):
    result = None
    for i in cursor.execute(f'''SELECT id, id_user, date FROM user_story 
                        WHERE date = ? AND id_user = ?''', (datetime.now().date(), id_user)):
        result = i
    if result is not None:
        cursor.execute(f'''UPDATE user_story SET money = ? 
                        WHERE date = ? AND id_user = ?''', (money, datetime.now().date(), id_user))
    else:
        cursor.execute(f'''INSERT INTO user_story (id_user, date, money) 
                        VALUES(?,?,?)''', (id_user, datetime.now().date(), money))


def get_story(id_user):
    result = None
    open()
    cursor.execute(f'''SELECT date, money FROM user_story WHERE id_user = ?''', id_user)
    result = cursor.fetchall()
    close()
    return result


def get_user(email, password):
    result = None
    open()
    for i in cursor.execute('''SELECT id, nickname, name, surname, email, phoneNumber, gender, age, address, birthday, 
            money FROM users WHERE email = ? AND password = ?''', (email, hesh_password(password))):
        result = i
    if result is not None:
        add_story(result[0], result[10])
    close()
    return result


def card_transfer(number_card, cvv2, money, id):
    open()
    user_money = None
    user_money = cursor.execute('''SELECT money FROM users WHERE money >= ? AND id = ?''', (money, id))
    if user_money is not None:
        result = user_money - money
        cursor.execute('''UPDATE users SET money = ? WHERE id = ?''', (result, id))
        result = user_money + money
        cursor.execute('''UPDATE credit_cards SET money = ? 
                                WHERE number_card = ? AND cvv2 = ?''', (result, number_card, cvv2))
        close()
        return True
    close()
    return False


def wire_transfer(number_card, cvv2, money, id):
    open()
    card_money = None
    card_money = cursor.execute('''SELECT money FROM credit_cards 
                                  WHERE money >= ? AND number_card = ? AND cvv2 = ?''', (money, number_card, cvv2))
    if card_money is not None:
        result = card_money - money
        cursor.execute('''UPDATE credit_cards SET money = ? 
                        WHERE number_card = ? AND cvv2 = ?''',  (result, number_card, cvv2))
        result = card_money + money
        cursor.execute('''UPDATE users SET money = ? WHERE id = ?''', (result, id))
        close()
        return True
    close()
    return False
