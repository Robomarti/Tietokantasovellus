from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import database
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		
		user = User.query.filter_by(username=username).first()
		if user:
			if check_password_hash(user.hashed_password, password):
				flash('Logged in successfully', category='info')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Username or password is not correct', category='error')
		else:
			flash('Username or password is not correct', category='error')
    
	return render_template('login.html', user=current_user)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		username = request.form.get('username')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		
		user = User.query.filter_by(username=username).first()
		if user:
			flash('Username already exists', category='error')
		elif len(username) < 4:
			flash('Username must be at least 5 characters', category='error')
		elif len(password1) < 4:
			flash('Password must be at least 5 characters', category='error')
		elif password1 != password2:
			flash('Passwords must be the same', category='error')
		else:
			new_user = User(username=username, hashed_password=generate_password_hash(password1, method='sha256'))
			database.session.add(new_user)
			database.session.commit()
			login_user(new_user, remember=True)
			flash('Created the account', category='info')
			return redirect(url_for('views.home'))

	return render_template('sign_up.html', user=current_user)

