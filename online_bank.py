import numpy as np
import smtplib
import matplotlib
import matplotlib.pyplot as plt
import hashlib
import sqlite3
from random import randint
from datetime import datetime, timedelta
import os

matplotlib.use('Agg')


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
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        number_card TEXT NOT NULL,
        time_limit_expires DATE NOT NULL,
        cvv2 INTEGER NOT NULL,
        money INTEGER NOT NULL
    ) '''
    query_3 = '''CREATE TABLE IF NOT EXISTS user_credit_card(
        id INTEGER PRIMARY KEY NOT NULL,
        id_user INTEGER NOT NULL,
        number_card TEXT NOT NULL,
        cvv2 INTEGER NOT NULL,
        FOREIGN KEY (id_user) REFERENCES users(id)
    )'''
    query_4 = ''' CREATE TABLE IF NOT EXISTS user_story(
        id INTEGER PRIMARY KEY NOT NULL,
        id_user INTEGER NOT NULL, 
        date DATE NOT NULL,
        money INTEGER NOT NULL,
        FOREIGN KEY (id_user) REFERENCES users(id)
    ) '''
    query_5 = ''' CREATE TABLE IF NOT EXISTS user_story_transfers(
        id INTEGER PRIMARY KEY NOT NULL,
        id_user INTEGER NOT NULL,
        date DATE NOT NULL,
        from_where TEXT NOT NULL,
        to_where TEXT NOT NULL,
        how_much_money INTEGER NOT NULL,
        FOREIGN KEY (id_user) REFERENCES users(id)
    )'''
    cursor.execute(query_1)
    cursor.execute(query_2)
    cursor.execute(query_3)
    cursor.execute(query_4)
    cursor.execute(query_5)


def close():
    conn.commit()
    cursor.close()
    conn.close()


def create_test_card(name, surname):
    time_limit_expires = datetime.now() + timedelta(days=15*365)
    number_card = randint(100000000000000, 999999999999999)
    cvv2 = randint(100, 999)
    cursor.execute(''' INSERT INTO credit_cards (name, surname, number_card, time_limit_expires, cvv2, money) 
                    VALUES(?,?,?,?,?,?)''', (name, surname, number_card, time_limit_expires.date(), cvv2, 100))


def create_user(nickname, name, surname, password, email, phoneNumber, gender, age, birthday):
    open()
    check = None
    for i in cursor.execute('''SELECT id FROM users WHERE nickname = ? OR email = ? OR phoneNumber = ? 
                        OR (name = ? AND surname = ?)''', (nickname, email, phoneNumber, name, surname)):
        check = i
    if check is None:
        cursor.execute(''' INSERT INTO users (nickname, name, surname, password, email, 
            phoneNumber, gender, age, birthday, money) 
            VALUES(?,?,?,?,?,?,?,?,?,?)
            ''', (nickname, name, surname, hesh_password(password), email, phoneNumber, gender, age, birthday, 0))
        conn.commit()
        create_test_card(name, surname)
    close()


def create_save_graphs(id_user):
    x = []
    y = []
    story = get_story(id_user)
    for i in story:
        x.append(i[0])
        y.append(i[1])
    plt.bar(x, y, color='blue')
    plt.savefig('static/image/graphs_story.png')


def delete_user_story_card(email):
    open()
    result = None
    for i in cursor.execute('''SELECT id, name, surname FROM users WHERE email = ?''', (email, )):
        result = i
    cursor.execute('''DELETE FROM users WHERE id = ?''', str(result[0]))
    cursor.execute('''DELETE FROM user_story WHERE id_user = ?''', str(result[0]))
    cursor.execute('''DELETE FROM user_story_transfers WHERE id_user = ?''', str(result[0]))
    cursor.execute('''DELETE FROM credit_cards WHERE name = ? AND surname = ?''', (result[1], result[2]))
    cursor.execute('''DELETE FROM user_credit_card WHERE id_user''', str(result[0]))
    close()


def add_story(id_user, money):
    result = None
    for i in cursor.execute('''SELECT id, id_user, date FROM user_story 
                        WHERE date = ? AND id_user = ?''', (datetime.now().date(), id_user)):
        result = i
    if result is not None:
        cursor.execute('''UPDATE user_story SET money = ? 
                        WHERE date = ? AND id_user = ?''', (money, datetime.now().date(), id_user))
    else:
        cursor.execute('''INSERT INTO user_story (id_user, date, money) 
                        VALUES(?,?,?)''', (id_user, datetime.now().date(), money))


def get_story(id_user):
    result = None
    open()
    cursor.execute('''SELECT date, money FROM user_story WHERE id_user = ?''', str(id_user))
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


def get_story_transfer(id_user):
    open()
    cursor.execute('''SELECT date, from_where, to_where, how_much_money FROM user_story_transfers WHERE id_user = ?''',
                   str(id_user))
    story_transfer = cursor.fetchall()
    close()
    return story_transfer


def get_user_credit_card(id_user):
    credits_card = None
    open()
    for i in cursor.execute('''SELECT number_card FROM user_credit_card WHERE id_user = ? ''', (id_user, )):
        credits_card = i
    close()
    return credits_card


def email_verification(email):
    result = None
    open()
    for i in cursor.execute('''SELECT id FROM users WHERE email = ?''', (email, )):
        result = i
    close()
    print(result)
    if result is not None:
        return True
    return False


def add_card(id_user, name, surname, number, cvv2, date):
    card = None
    open()
    for i in cursor.execute('''SELECT id FROM credit_cards WHERE name = ? AND surname = ? AND number_card = ? 
                            AND cvv2 = ? AND time_limit_expires = ? ''', (name, surname, number, cvv2, date)):
        card = i
    if card is not None:
        cursor.execute('''INSERT INTO user_credit_card (id_user, number_card, cvv2) VALUES(?,?,?)''',
                       (id_user, number, cvv2))
    close()


def card_transfer(number_card, money, id_user):
    open()
    user_money = None
    user_card = None
    user_card = cursor.execute('''SELECT number_card, cvv2, FROM user_credit_card WHERE id_user = ? 
                                        AND number_card = ?''', (id_user, number_card)).fetchone()
    if user_card is not None:
        user_money = cursor.execute('''SELECT money FROM users WHERE money >= ? AND id = ?''',
                                    (money, id_user)).fetchone()
        if user_money is not None:
            result = user_money[0] - money
            cursor.execute('''UPDATE users SET money = ? WHERE id = ?''', (result, id_user))
            result = user_money[0] + money
            cursor.execute('''UPDATE credit_cards SET money = ? 
                                    WHERE number_card = ? AND cvv2 = ?''', (result, number_card, user_card[1]))
            cursor.execute('''INSERT INTO user_story_transfers (id_user, date, from_where, to_where, how_much_money) 
                                    VALUES(?,?,?,?,?)''', (id_user, datetime.now().date(), 'Bank',
                                                           f'Credit card: {number_card}', money))
            close()
            return True
    close()
    return False


def wire_transfer(number_card, money, id_user):
    open()
    card_money = None
    user_card = None
    user_card = cursor.execute('''SELECT number_card, cvv2, FROM user_credit_card WHERE id_user = ? 
                                    AND number_card = ?''', (id_user, number_card)).fetchone()
    if user_card is not None:
        card_money = cursor.execute('''SELECT money FROM credit_cards 
                                      WHERE money >= ? AND number_card = ? AND cvv2 = ?''',
                                    (money, number_card, user_card[1])).fetchone()
        if card_money is not None:
            result = card_money[0] - money
            cursor.execute('''UPDATE credit_cards SET money = ? 
                            WHERE number_card = ? AND cvv2 = ?''',  (result, number_card, user_card[1]))
            result = card_money[0] + money
            cursor.execute('''UPDATE users SET money = ? WHERE id = ?''', (result, id_user))
            cursor.execute('''INSERT INTO user_story_transfers (id_user, date, from_where, to_where, how_much_money) 
                                            VALUES(?,?,?,?,?)''', (id_user, datetime.now().date(), f'Credit card: {number_card}',
                                                                   'Bank', money))
            close()
            return True
    close()
    return False


def update_password(email, password):
    open()
    cursor.execute('''UPDATE users SET password = ? WHERE email = ?''', (hesh_password(password), email))
    close()


def update_user(id_user, nickname, name, surname, email, phoneNumber, address):
    result = None
    open()
    cursor.execute('''UPDATE users SET nickname = ?, name = ?, surname = ?, email = ?, phoneNumber = ?, address = ?
                    WHERE id = ?''', (nickname, name, surname, email,phoneNumber, address, id_user))
    for i in cursor.execute('''SELECT id, nickname, name, surname, email, phoneNumber, gender, age, address, birthday, 
            money FROM users WHERE email = ?''', (email, )):
        result = i
    close()
    return result
