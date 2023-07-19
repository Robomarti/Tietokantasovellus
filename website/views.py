from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Character
from . import database
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	if request.method == 'POST':
		name = request.form.get('character_name')
	
		if len(name) < 1:
			flash('Character name is too short', category='error')
		else:
			new_character = Character(username=name, hp=10, attack_damage=1, level=1, user_id=current_user.id)
			database.session.add(new_character)
			database.session.commit()
			flash('Character created!', category='info')

	return render_template('home.html', user=current_user)

@views.route('/delete-character', methods=['POST'])
def delete_character():
	data = json.loads(request.data)
	character_id = data['character_id']
	character = Character.query.get(character_id)
	if character and character.user_id == current_user.id:
		database.session.delete(character)
		database.session.commit()
	return jsonify({})