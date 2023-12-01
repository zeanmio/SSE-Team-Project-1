CREATE TABLE userdata (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    country VARCHAR(50),
    city VARCHAR(50),
    exploration_date DATE
);

INSERT INTO userdata (username, country, city, exploration_date) VALUES ('exampleuser', 'examplecountry', 'examplecity', '2023-01-01');

SELECT * FROM userdata;