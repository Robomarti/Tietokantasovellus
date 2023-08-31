from db import db
import users, profiles
from sqlalchemy.sql import text

def get_comments_by_recipe_id(recipe_id):
	sql = "SELECT C.id, C.content, C.likes, C.created_at, C.user_id, C.recipe_id, " \
	"U.username FROM comments C, users U WHERE C.recipe_id = (:recipe_id) AND U.id = C.user_id ORDER BY likes DESC;"
	result = db.session.execute(text(sql), {"recipe_id":recipe_id})
	return result.fetchall()

def post_comment(recipe_id, content):
	user_id = users.logged_user_id()
	if user_id == 0:
		return False
	sql = "INSERT INTO comments (content, likes, user_id, recipe_id) VALUES (:content, 0, :user_id, :recipe_id)"
	db.session.execute(text(sql), {"content":content, "user_id":user_id, "recipe_id":recipe_id})
	db.session.commit()
	return True

def get_publisher_id(comment_id):
	sql = "SELECT user_id FROM comments WHERE id=(:comment_id)"
	result = db.session.execute(text(sql), {"comment_id":comment_id})
	return result.fetchone()[0]

def like_comment(comment_id):
	likes = get_likes(comment_id) + 1
	publisher_id = get_publisher_id(comment_id)
	total_likes = profiles.get_total_likes(publisher_id) + 1

	sql = "BEGIN;" \
	"UPDATE comments SET likes=(:likes) WHERE id=(:comment_id);" \
	"UPDATE profiles SET total_likes=(:total_likes) WHERE user_id=(:publisher_id);" \
	"COMMIT;"

	db.session.execute(text(sql), {"likes":likes,"comment_id":comment_id, "total_likes":total_likes, "publisher_id":publisher_id})
	db.session.commit()

def get_likes(comment_id):
	sql = "SELECT likes FROM comments WHERE id=(:comment_id)"
	result = db.session.execute(text(sql), {"comment_id":comment_id})
	return int(str(result.fetchone())[1:-2])
