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
            return user.id
        else:
            return None

def logout():
    del session["user_id"]

def sign_up(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,is_admin) VALUES (:username,:password, FALSE)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except Exception:
        render_template("error.html", message="Something went wrong, please try again later.")
    return login(username, password)

def logged_user_id():
    return session.get("user_id",0)

def is_admin():
    sql = "SELECT is_admin FROM users WHERE id=:id"
    result = db.session.execute(text(sql), {"id":logged_user_id()})
    return result.fetchone()[0]

def is_logged_in():
    if session.get("is_admin") == True:
        return True
    return False

def exists(username):
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    return result.fetchone()

def get_username(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    user_id = result.fetchone()
    if user_id:
        user_id = user_id[0]
    return user_id

def user_id():
    return session["user_id"]

def search_user(username):
	found_users = []
	sql = "SELECT U.id FROM users U, profiles P WHERE U.username LIKE (:username) ORDER BY P.total_likes DESC"
	result = db.session.execute(text(sql), {"username":"%"+username+"%"})
	results = result.fetchall()
	for user_id in results:
		user_id = user_id[0]
		user_result = (user_id,get_username(user_id))
		if user_result not in found_users:
			found_users.append(user_result)

	return found_users