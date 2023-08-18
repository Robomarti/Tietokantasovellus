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

def get_profiles_users_id(profile_id):
	sql = "SELECT user_id FROM profiles WHERE id=(:id)"
	result = db.session.execute(text(sql), {"id":profile_id})
	return result.fetchone()[0]

def get_total_likes(publisher_id):
	sql = "SELECT total_likes FROM profiles WHERE user_id=(:publisher_id)"
	result = db.session.execute(text(sql), {"publisher_id":publisher_id})
	return int(str(result.fetchone())[1:-2])

def get_bio(profile_id):
	sql = "SELECT bio FROM profiles WHERE id=(:profile_id)"
	result = db.session.execute(text(sql), {"profile_id":profile_id})
	return result.fetchone()[0]

def update_bio(profile_id, biography):
	sql = "UPDATE profiles SET bio=(:bio) WHERE id=(:profile_id);"
	db.session.execute(text(sql), {"bio": biography, "profile_id":profile_id})
	db.session.commit()
