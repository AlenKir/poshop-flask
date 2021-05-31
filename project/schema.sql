DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cost FLOAT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    image TEXT
);

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mark INTEGER NOT NULL,
    text TEXT,
    author TEXT,
    product_id INTEGER
);

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ready INTEGER NOT NULL,
    shipped INTEGER NOT NULL,
    cost FLOAT NOT NULL,
    priority INTEGER
);

DROP TABLE IF EXISTS product_order;

CREATE TABLE product_order (
    product_id INTEGER,
    order_id INTEGER
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT,
    password_hash TEXT
);

DROP TABLE IF EXISTS cart;

CREATE TABLE cart (
    product_id INTEGER,
    user_id INTEGER
);


DROP TABLE IF EXISTS user_order;

CREATE TABLE user_order (
    user_id INTEGER,
    order_id INTEGER
);