DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS users;

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