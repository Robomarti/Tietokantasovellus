from db import db
import users
import profiles
from sqlalchemy.sql import text

def get_list():
    sql = "SELECT id, title, cooking_time, recipe, likes, created_at, public, user_id FROM recipes WHERE public=TRUE ORDER BY likes DESC"
    result = db.session.execute(text(sql))
    return result.fetchall()

def send(title, recipe, public, cooking_time):
    user_id = users.logged_user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO recipes (title,cooking_time,recipe,likes,public,user_id) VALUES (:title,:cooking_time,:recipe, 0,:public,:user_id)"
    db.session.execute(text(sql), {"title":title, "cooking_time":cooking_time, "recipe":recipe, "public":public, "user_id":user_id})
    db.session.commit()
    return True

def is_public(id):
	sql = "SELECT public FROM recipes WHERE id=(:id)"
	result = db.session.execute(text(sql), {"id":id})
	public = result.fetchone()[0]
	return public

def recipe_publisher_id(id):
	sql = "SELECT user_id FROM recipes WHERE id=(:id)"
	result = db.session.execute(text(sql), {"id":id})
	user_id = result.fetchone()
	if user_id:
		user_id = user_id[0]
	return user_id

def get_recipe(id):
	sql = "SELECT id, title, cooking_time, recipe, likes, created_at, public, user_id FROM recipes WHERE id=(:id)"
	result = db.session.execute(text(sql), {"id":id})
	return result.fetchone()

def get_likes(recipe_id):
	sql = "SELECT likes FROM recipes WHERE id=(:recipe_id)"
	result = db.session.execute(text(sql), {"recipe_id":recipe_id})
	return int(str(result.fetchone())[1:-2])

def like_recipe(recipe_id):
	likes = get_likes(recipe_id) + 1
	publisher_id = get_publisher_id(recipe_id)
	total_likes = profiles.get_total_likes(publisher_id) + 1

	sql = "BEGIN;" \
	"UPDATE recipes SET likes=(:likes) WHERE id=(:recipe_id);" \
	"UPDATE profiles SET total_likes=(:total_likes) WHERE user_id=(:publisher_id);" \
	"COMMIT;"

	db.session.execute(text(sql), {"likes":likes,"recipe_id":recipe_id, "total_likes":total_likes, "publisher_id":publisher_id})
	db.session.commit()

def delete_recipe(id):
	sql = "DELETE FROM recipes WHERE id=(:id)"
	db.session.execute(text(sql), {"id":id})
	db.session.commit()

def search_recipe(content):
	found_recipes = []
	sql = "SELECT id FROM recipes WHERE title LIKE (:title) OR recipe LIKE (:recipe) ORDER BY likes DESC"
	result = db.session.execute(text(sql), {"title":"%"+content+"%", "recipe":"%"+content+"%"})
	results = result.fetchall()
	for id in results:
		found_recipes.append(get_recipe(id[0]))

	return found_recipes

def search_recipe_by_time(content):
	found_recipes = []
	sql = "SELECT id FROM recipes WHERE CAST(cooking_time as TEXT) LIKE (:cooking_time) ORDER BY likes DESC"
	result = db.session.execute(text(sql), {"cooking_time":"%"+content+"%"})
	results = result.fetchall()
	for id in results:
		found_recipes.append(get_recipe(id[0]))

	return found_recipes

def update(recipe_id, title, recipe, likes, public, cooking_time):
    user_id = users.logged_user_id()
    if user_id == 0:
        return False
    sql = "UPDATE recipes SET " \
    			"title = (:title), " \
			    "cooking_time = (:cooking_time), " \
			    "recipe = (:recipe), " \
			    "likes = (:likes), " \
			    "public = (:public), " \
			    "user_id = (:user_id) " \
			    "WHERE id = (:recipe_id)"
    db.session.execute(text(sql), {"title":title, "cooking_time":cooking_time, "recipe":recipe, "likes":likes, "public":public, "user_id":user_id, "recipe_id":recipe_id})
    db.session.commit()
    return True

def get_recipes_of_user(user_id, public):
	sql = "SELECT id, title, cooking_time, recipe, likes, created_at, public, user_id FROM recipes WHERE public=(:public) AND user_id=(:user_id) ORDER BY likes DESC"
	result = db.session.execute(text(sql), {"user_id":user_id, "public":public})
	return result.fetchall()

def get_publisher_id(recipe_id):
	sql = "SELECT user_id FROM recipes WHERE id=(:id)"
	result = db.session.execute(text(sql), {"id":recipe_id})
	return result.fetchone()[0]

def get_better_format(recipe):
	better_format_recipe = []
	for row in recipe:
		better_format_recipe.append(str(row))
	better_format_recipe[5] = better_format_recipe[5][:-7]
	return better_format_recipe
