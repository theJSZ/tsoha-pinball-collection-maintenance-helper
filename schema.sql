CREATE TABLE collections (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE machines (id SERIAL PRIMARY KEY, name TEXT, collection_id INTEGER REFERENCES collections ON DELETE CASCADE);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, email TEXT, password TEXT);
CREATE TABLE issues (id SERIAL PRIMARY KEY, machine_id REFERENCES machines, user_id REFERENCES users, created_at TIMESTAMP, content TEXT, closed_by INTEGER REFERENCES users, severity INTEGER);
CREATE TABLE comments (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, issue_id INTEGER REFERENCES issues, created_at TIMESTAMP, content TEXT);
CREATE TABLE rights (user_id INTEGER REFERENCES users, collection_id INTEGER REFERENCES collections, is_admin BOOLEAN);