from db import db
import users
from sqlalchemy.sql import text
from sqlalchemy.sql import text

def get_list():
    sql = "SELECT id, title, cooking_time, recipe, likes, created_at, public, user_id FROM recipes WHERE public=TRUE ORDER BY likes"
    result = db.session.execute(text(sql))
    return result.fetchall()

def send(title, recipe, public, cooking_time):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO recipes (title,cooking_time,recipe,likes,public,user_id) VALUES (:title,:cooking_time,:recipe, 0,:public,:user_id)"
    db.session.execute(text(sql), {"title":title, "cooking_time":cooking_time, "recipe":recipe, "public":public, "user_id":user_id})
    db.session.commit()
    return True

def is_public(id):
	sql = "SELECT public FROM recipes WHERE id=:id"
	result = db.session.execute(text(sql), {"id":id})
	public = result.fetchone()
	return public

def recipe_publisher_id(id):
	sql = "SELECT user_id FROM recipes WHERE id=:id"
	result = db.session.execute(text(sql), {"id":id})
	user_id = result.fetchone()
	return user_id

def get_recipe(id):
	sql = "SELECT id, title, cooking_time, recipe, likes, created_at, public, user_id FROM recipes WHERE id=(:id)"
	result = db.session.execute(text(sql), {"id":id})
	return result.fetchone()
