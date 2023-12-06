CREATE TABLE userdata (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    country VARCHAR(50),
    city VARCHAR(50),
    exploration_date DATE,
    attraction_type VARCHAR(50)
);
INSERT INTO userdata (username, country, city, exploration_date, attraction_type) VALUES ('exampleuser', 'examplecountry', 'examplecity', '2023-01-01', 'exampletype');
SELECT * FROM userdata;


CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    feedback TEXT NOT NULL
);
INSERT INTO feedback (username, feedback) VALUES ('exampleuser', 'examplefeedback');
SELECT * FROM feedback;


CREATE TABLE attractions (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    rate INT,
    wikidata VARCHAR(255)
);
INSERT INTO attractions (id, name, latitude, longitude, rate, wikidata) VALUES ('exampleid', 'examplename', 0.0, 0.0, 0, 'examplewikidata');
SELECT * FROM attractions;

CREATE TABLE user_favourites (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    latitude FLOAT,
    longitude FLOAT
);
