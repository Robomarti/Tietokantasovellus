from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template
from sqlalchemy.sql import text

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def logout():
    del session["user_id"]

def sign_up(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,is_admin) VALUES (:username,:password, FALSE)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except Exception:
        render_template("error.html", message="something went wrong, please try again later.")
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def is_admin():
    sql = "SELECT is_admin FROM users WHERE id=:id"
    result = db.session.execute(text(sql), {"id":user_id()})
    return result.fetchone()

def is_logged_in():
    if session.get("is_admin") == True:
        return True
    return False