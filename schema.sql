DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS messages;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
	is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title TEXT,
	recipe TEXT,
	likes INTEGER,
    created_at TIMESTAMP,
	public BOOLEAN DEFAULT TRUE,
	user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
	content TEXT,
	likes INTEGER,
    created_at TIMESTAMP,
	user_id INTEGER REFERENCES users,
	recipe_id INTEGER REFERENCES recipes
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
	description TEXT,
	likes INTEGER,
	user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
	content TEXT,
	sent_at TIMESTAMP,
	sent_from_id INTEGER REFERENCES users,
	sent_to_id INTEGER REFERENCES users
);