-- =====================================================
-- Allergy Snatcher Database Cleanup Script
-- Safely drops all tables in dependency order
-- =====================================================

-- Optional: switch to the right database
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;

-- -----------------------------------------------------
-- Disable foreign key checks (required for clean drops)
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS = 0;

-- ---------- CHILD TABLES (depend on others) ----------
DROP TABLE IF EXISTS diet_restrict_assoc;
DROP TABLE IF EXISTS ingredients;

-- ---------- PARENT TABLES ----------
DROP TABLE IF EXISTS foods;
DROP TABLE IF EXISTS dietary_restrictions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS cuisines;
DROP TABLE IF EXISTS users;

-- -----------------------------------------------------
-- Re-enable foreign key checks
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS = 1;

-- Optional: confirm result
SHOW TABLES;
