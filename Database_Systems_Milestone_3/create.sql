-- =====================================================
-- Allergy Snatcher Full Unified Schema (Complete Init)
-- =====================================================

CREATE DATABASE IF NOT EXISTS mydatabase
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mydatabase;

-- =====================================================
-- USER / AUTHENTICATION TABLES
-- =====================================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role ENUM('admin','moderator','user','disabled') DEFAULT 'user',
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX (username),
    INDEX (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS passwords (
    user_id INT NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS oauth_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    provider VARCHAR(50) NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    access_token VARCHAR(2048),
    refresh_token VARCHAR(2048),
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (provider, provider_user_id),
    UNIQUE (provider, user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX (provider),
    INDEX (provider_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at DATETIME NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token_expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX (session_token),
    INDEX (refresh_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- FOOD LOOKUP TABLES
-- =====================================================

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS cuisines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cuisine VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS dietary_restrictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restriction VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- CORE FOOD TABLES
-- =====================================================

CREATE TABLE IF NOT EXISTS foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    publication_status ENUM('public', 'private', 'unlisting') DEFAULT 'private',
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
    serving_unit ENUM('g', 'mg', 'oz', 'lb', 'tsp', 'tbsp', 'cup', 'item') DEFAULT 'g',
    user_id INT,
    category_id INT,
    cuisine_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (cuisine_id) REFERENCES cuisines(id) ON DELETE SET NULL,
    UNIQUE KEY unique_food_name_brand (name, brand),
    INDEX (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food_id INT NOT NULL,
    ingredient_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS diet_restrict_assoc (
    food_id INT NOT NULL,
    restriction_id INT NOT NULL,
    PRIMARY KEY (food_id, restriction_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (restriction_id) REFERENCES dietary_restrictions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- END OF SCHEMA
-- =====================================================

