CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE notebooks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users
);

CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    notebook_id INTEGER NOT NULL REFERENCES notebooks ON DELETE CASCADE,
    modified DATE
);

CREATE TABLE equations (
    id SERIAL PRIMARY KEY,
    content TEXT,
    page_id INTEGER NOT NULL REFERENCES pages ON DELETE CASCADE,
    order_num INTEGER,
    type VARCHAR(1)
);
