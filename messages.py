from db import db
from sqlalchemy.sql import text

def new_message(sender, receiver, message):
    if sender == 0 or receiver == 0:
        return False
    sql = "INSERT INTO messages (content, sent_from_id, sent_to_id) VALUES (:message,:sender,:receiver)"
    db.session.execute(text(sql), {"message":message, "sender":sender, "receiver":receiver})
    db.session.commit()
    return True

def get_messages_of_user(user_id):
	sql = "SELECT id, content, sent_at, sent_from_id, sent_to_id, been_read FROM messages WHERE sent_to_id=(:user_id) ORDER BY id DESC"
	result = db.session.execute(text(sql), {"user_id":user_id})
	return result.fetchall()

def get_messages_by_user(user_id):
	sql = "SELECT id, content, sent_at, sent_from_id, sent_to_id, been_read FROM messages WHERE sent_from_id=(:user_id) ORDER BY id DESC"
	result = db.session.execute(text(sql), {"user_id":user_id})
	return result.fetchall()

def get_all_messages(user_id):
	sql = "SELECT id, content, sent_at, sent_from_id, sent_to_id, been_read FROM messages WHERE sent_from_id=(:user_id) OR sent_to_id=(:user_id) ORDER BY id DESC"
	result = db.session.execute(text(sql), {"user_id":user_id})
	return result.fetchall()