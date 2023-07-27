from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = "SELECT title, likes FROM recipes WHERE public=TRUE ORDER BY likes"
    result = db.session.execute(text(sql))
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO recipes (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(text(sql), {"content":content, "user_id":user_id})
    db.session.commit()
    return True