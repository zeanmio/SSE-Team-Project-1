CREATE TABLE users (
    userid SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);
SELECT * FROM users;


CREATE TABLE userdata (
    id SERIAL PRIMARY KEY,
    userid INT NOT NULL,
    country VARCHAR(50),
    city VARCHAR(50),
    exploration_date DATE,
    attraction_type VARCHAR(50),
    food_type VARCHAR(50),
    FOREIGN KEY (userid) REFERENCES users(userid)
);
SELECT * FROM userdata;


CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    userid INT NOT NULL,
    feedback TEXT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(userid)
);
SELECT * FROM feedback;


CREATE TABLE attractions (
    id SERIAL PRIMARY KEY,
    userid INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(userid)
);
SELECT * FROM attractions;


CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    userid INT NOT NULL,
    title VARCHAR(255),
    FOREIGN KEY (userid) REFERENCES users(userid)
);
SELECT * FROM events;


SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';