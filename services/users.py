import os
from services.db import db
from flask import abort, session, request
from werkzeug.security import check_password_hash, generate_password_hash

def get_all():
    try:
        sql = "SELECT username FROM users"
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False

def get_id(username):
    try:
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        return result.fetchone()[0]
    except:
        return False

def get_name(user_id):
    try:
        sql = "SELECT username FROM users WHERE id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        return result.fetchone()[0]
    except:
        return False

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = username
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def register(username, password):
    password_hash = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (username, password) VALUES (:username, :password)"""
        db.session.execute(sql, {"username":username, "password":password_hash})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)