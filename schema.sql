CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE notebooks (
    id SERIAL PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    title TEXT,
    notebook_id INTEGER REFERENCES notebooks
);

CREATE TABLE equations (
    id SERIAL PRIMARY KEY,
    content TEXT,
    page_id INTEGER REFERENCES pages,
    order_num INTEGER,
    type VARCHAR(1)
);
