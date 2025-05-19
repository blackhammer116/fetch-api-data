CREATE DATABASE news_db;

USE news_db;

CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    description TEXT,
    url TEXT,
    published_at DATETIME
);
