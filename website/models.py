from . import database
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(150), unique=True)
    hashed_password = database.Column(database.String(150))
    is_admin = database.Column(database.Boolean, default=False)
    characters = database.relationship('Character')
    messages = database.relationship('Chat')

class Chat(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.String(300))
    date =  database.Column(database.DateTime(timezone=True), default=func.now())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    
class Character(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(150), unique=True)
    hp = database.Column(database.Integer)
    attack_damage = database.Column(database.Integer)
    level = database.Column(database.Integer, default=1)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    
class Monster(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(150), unique=True)
    hp = database.Column(database.Integer)
    attack_damage = database.Column(database.Integer)
    
class GameMap(database.Model):
    id = database.Column(database.Integer, primary_key=True)