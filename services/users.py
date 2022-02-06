import os
from services.db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["username"] = username
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def register(name, password):
    print(1)
    password_hash = generate_password_hash(password)
    print(2)
    try:
        print(3)
        sql = """INSERT INTO users (username, password) VALUES (:username, :password)"""
        print(4)
        db.session.execute(sql, {"username":name, "password":password_hash})
        print(5)
        db.session.commit()
    except:
        return False
    print(6)
    return login(name, password)
