from app import app
from flask import render_template, request, redirect, session, abort
import recipes, users, profiles, comments, messages
import secrets

@app.route("/")
def index():
	session["csrf_token"] = secrets.token_hex(16)
	list = recipes.get_list()
	better_list = []
	for recipe in list:
		better_list.append(recipes.get_better_format(recipe))
	user = users.get_username(users.logged_user_id())
	return render_template("index.html", count=len(better_list), recipes=better_list, user=user)

@app.route("/new_recipe")
def new():
	token = session["csrf_token"]
	return render_template("new_recipe.html", token=token)

@app.route("/publish_recipe", methods=["POST"])
def send():
	if session["csrf_token"] != request.form["csrf_token"]:
		abort(403)
	title = request.form["title"]
	recipe = request.form["recipe"]
	public = request.form.get("public")
	if not public:
		public = False
	cooking_time = request.form.get("cooking_time")
	if not cooking_time:
		cooking_time = 1
	
	recipes.send(title, recipe, public, cooking_time)
	return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		if not session["csrf_token"]:
			session["csrf_token"] = secrets.token_hex(16)
		return render_template("login.html")

	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(username, password):
			return redirect("/")
		else:
			return render_template("error.html", error="Wrong username or password")

@app.route("/logout")
def logout():
	if users.logged_user_id() != 0:
		users.logout()
	return redirect("/")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
	if request.method == "GET":
		if not session["csrf_token"]:
			session["csrf_token"] = secrets.token_hex(16)
		token = session["csrf_token"]
		return render_template("sign_up.html", token=token)

	if request.method == "POST":
		if session["csrf_token"] != request.form["csrf_token"]:
			abort(403)
		username = request.form["username"]
		if len(username) < 1:
			return render_template("error.html", error="The username field is mandatory")
		if users.exists(username):
			return render_template("error.html", error="The username already exists")
		password1 = request.form["password1"]
		if len(password1) < 1:
			return render_template("error.html", error="The password field is mandatory")
		password2 = request.form["password2"]
		if password1 != password2:
			return render_template("error.html", error="The passwords do not match")
		user_id = users.sign_up(username, password1)
		if user_id:
			profiles.create_profile(user_id)
			return redirect("/")
		else:
			return render_template("error.html", error="Sign up failed, please try again later")

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
	if recipes.is_public(recipe_id) or recipes.recipe_publisher_id(recipe_id) == users.logged_user_id():
		token = session["csrf_token"]
		recipe = recipes.get_recipe(recipe_id)
		recipe_publisher_name = users.get_username(recipe[7])
		better_format_recipe = recipes.get_better_format(recipe)
		is_admin = users.is_admin()
		recipe_comments = comments.get_comments_by_recipe_id(recipe_id)
		return render_template("recipe.html", recipe=better_format_recipe, 
						 recipe_publisher_name=recipe_publisher_name, is_admin=is_admin,
						 recipe_comments=recipe_comments, token=token)
	return render_template("error.html", error="You have no permissions to see this recipe")

@app.route("/delete_recipe/<int:id>", methods=["POST"])
def delete_recipe(id):
	if session["csrf_token"] != request.form["csrf_token"]:
		abort(403)
	if recipes.recipe_publisher_id(id) == users.logged_user_id() or users.is_admin():
		recipes.delete_recipe(id)
		return redirect("/")
	return render_template("error.html", error="You do not have permission to delete this recipe.")

@app.route("/edit_recipe/<int:id>", methods=["POST"])
def edit_recipe(id):
	if session["csrf_token"] != request.form["csrf_token"]:
		abort(403)
	if recipes.recipe_publisher_id(id) == users.logged_user_id() or users.is_admin():
		recipe = recipes.get_recipe(id)
		return render_template("edit_recipe.html", recipe=recipe)
	return render_template("error.html", error="You do not have permission to edit this recipe.")

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
	if session["csrf_token"] != request.form["csrf_token"]:
		abort(403)
	title = request.form["title"]
	cooking_time = request.form.get("cooking_time")
	recipe = request.form["recipe"]
	likes = request.form["likes"]
	public = request.form.get("public")
	recipe_id = request.form.get("recipe_id")

	if not public:
		public = False
	if not cooking_time:
		cooking_time = 1
	
	recipes.update(recipe_id, title, recipe, likes, public, cooking_time)
	return redirect(f"/recipe/{recipe_id}")

@app.route("/like_recipe/<int:recipe_id>", methods=["POST"])
def like_recipe(recipe_id):
	if session["csrf_token"] != request.form["csrf_token"]:
		abort(403)
	if recipes.recipe_publisher_id(recipe_id) != users.logged_user_id():
		recipes.like_recipe(recipe_id)
		return redirect(f"/recipe/{recipe_id}")
	else:
		return render_template("error.html", error="You can not like your own recipe.")

@app.route("/recipe_result")
def recipe_result():
	recipe_query = request.args["recipe_query"]
	if recipe_query.isdigit():
		found_recipes = recipes.search_recipe_by_time(recipe_query)
	else:
		found_recipes = recipes.search_recipe(recipe_query)
	return render_template("result.html", found_recipes=found_recipes)

@app.route("/user_result")
def user_result():
	username_query = request.args["username_query"]
	found_users = users.search_user(username_query)
	return render_template("user_result.html", found_users=found_users)

@app.route("/profile/<int:user_id>")
def profile(user_id):
	token = session["csrf_token"]
	profile_owner = users.get_username(user_id)
	public_recipes = recipes.get_recipes_of_user(user_id, True)

	if user_id == users.logged_user_id():
		private_recipes = recipes.get_recipes_of_user(user_id, False)
	else:
		private_recipes = []
	found_profile = profiles.get_profile_by_user_id(user_id)
	public_count = len(public_recipes)
	private_count = len(private_recipes)

	return render_template("profile.html", profile_owner=profile_owner, found_recipes=public_recipes,
			found_profile=found_profile, private_recipes=private_recipes, public_count=public_count,
			private_count=private_count, token=token)

@app.route("/send_a_message/<int:receiver_id>", methods=["GET", "POST"])
def send_a_message(receiver_id):
	if request.method == "GET":
		token = session["csrf_token"]
		sender = users.logged_user_id()
		return render_template("new_message.html", receiver=receiver_id, sender=sender, token=token)

	if request.method == "POST":
		if session["csrf_token"] != request.form["csrf_token"]:
			abort(403)
		sender = request.form["sender"]
		message = request.form["message"]
		if messages.new_message(sender, receiver_id, message):
			profile_id = profiles.get_profile_by_user_id(receiver_id)
			return redirect(f"/profile/{profile_id[0]}")
		return render_template("error.html", error="Sending the message failed")

@app.route("/show_messages/<int:user_id>", methods=["GET"])
def show_messages(user_id):
	if request.method == "GET":
		sent_messages = messages.get_messages_by_user(user_id)
		received_messages = messages.get_messages_of_user(user_id)
		all_messages = messages.get_all_messages(user_id)
		return render_template("messages.html", sent_messages=sent_messages, received_messages=received_messages, all_messages=all_messages, get_username=users.get_username)

@app.route("/edit_bio/<int:profile_id>", methods=["GET", "POST"])	
def edit_bio(profile_id):
	if request.method == "GET":
		token = session["csrf_token"]
		current_bio = profiles.get_bio(profile_id)
		if profiles.get_profiles_users_id(profile_id) == users.logged_user_id() or users.is_admin():
			return render_template("edit_bio.html", profile_id=profile_id, current_bio=current_bio, token=token)
		return render_template("error.html", error=f"You do not have permission to edit this biography.")

	if request.method == "POST":
		if session["csrf_token"] != request.form["csrf_token"]:
			abort(403)
		new_bio = request.form["bio"]
		profiles.update_bio(profile_id, new_bio)
		return redirect(f"/profile/{profile_id}")

@app.route("/add_comment/<int:recipe_id>", methods=["GET", "POST"])	
def add_comment(recipe_id):
	if request.method == "GET":
		token = session["csrf_token"]
		return render_template("add_comment.html", recipe_id=recipe_id,token=token)

	if request.method == "POST":
		if session["csrf_token"] != request.form["csrf_token"]:
			abort(403)
		content = request.form["content"]
		success = comments.post_comment(recipe_id, content)
		if success:
			return redirect(f"/recipe/{recipe_id}")
		else:
			return render_template("error.html", error="Adding your comment failed.")

@app.route("/like_comment/<int:comment_id>", methods=["POST"])
def like_comment(comment_id):
	if session["csrf_token"] != request.form["csrf_token"]:
		abort(403)
	recipe_id = request.form.get("recipe_id")
	if comments.get_publisher_id(comment_id) != users.logged_user_id():
		comments.like_comment(comment_id)
		return redirect(f"/recipe/{recipe_id}")
	else:
		return render_template("error.html", error="You can not like your own comment.")