
-- User Tables
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role ENUM('admin','user') NOT NULL DEFAULT 'user',
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (username),
    UNIQUE (email),
    INDEX (username),
    INDEX (email)
);

CREATE TABLE passwords (
    user_id INT NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE oauth_accounts (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    provider VARCHAR(50) NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    access_token VARCHAR(2048),
    refresh_token VARCHAR(2048),
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (provider, provider_user_id),
    UNIQUE (provider, user_id),
    FOREIGN KEY(user_id) REFERENCES users (id),
    INDEX (provider),
    INDEX (provider_user_id)
);

CREATE TABLE user_sessions (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL,
    expires_at DATETIME NOT NULL,
    refresh_token VARCHAR(255) NOT NULL,
    refresh_token_expires_at DATETIME NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (session_token),
    UNIQUE (refresh_token),
    FOREIGN KEY(user_id) REFERENCES users (id),
    INDEX (session_token),
    INDEX (refresh_token)
);

-- Food Lookup Tables
CREATE TABLE categories (
    id INT NOT NULL AUTO_INCREMENT,
    category VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (category)
);

CREATE TABLE cuisines (
    id INT NOT NULL AUTO_INCREMENT,
    cuisine VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (cuisine)
);

CREATE TABLE dietary_restrictions (
    id INT NOT NULL AUTO_INCREMENT,
    restriction VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (restriction)
);

-- Core Food Tables
CREATE TABLE foods (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    publication_status ENUM('public', 'private', 'unlisting') NOT NULL DEFAULT 'private',
    dietary_fiber FLOAT,
    sugars FLOAT,
    protein FLOAT,
    carbs FLOAT,
    cal FLOAT,
    cholesterol FLOAT,
    sodium FLOAT,
    trans_fats FLOAT,
    total_fats FLOAT,
    sat_fats FLOAT,
    serving_amt FLOAT,
    serving_unit VARCHAR(50),
    user_id INT,
    category_id INT NOT NULL,
    cuisine_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id),
    FOREIGN KEY(category_id) REFERENCES categories (id),
    FOREIGN KEY(cuisine_id) REFERENCES cuisines (id),
    INDEX (name)
);

CREATE TABLE ingredients (
    id INT NOT NULL AUTO_INCREMENT,
    food_id INT NOT NULL,
    ingredient_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(food_id) REFERENCES foods (id)
);

CREATE TABLE diet_restrict_assoc (
    food_id INT NOT NULL,
    restriction_id INT NOT NULL,
    PRIMARY KEY (food_id, restriction_id),
    FOREIGN KEY(food_id) REFERENCES foods (id),
    FOREIGN KEY(restriction_id) REFERENCES dietary_restrictions (id)
);
