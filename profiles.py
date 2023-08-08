from db import db
from sqlalchemy.sql import text

def create_profile(user_id):
    if user_id == 0:
        return False
    sql = "INSERT INTO profiles (bio, total_likes, user_id) VALUES (:bio,0,:user_id)"
    db.session.execute(text(sql), {"bio":"", "user_id":user_id})
    db.session.commit()
    return True

def get_profile_by_user_id(user_id):
	sql = "SELECT id, bio, total_likes, user_id FROM profiles WHERE user_id=(:user_id)"
	result = db.session.execute(text(sql), {"user_id":user_id})
	return result.fetchone()