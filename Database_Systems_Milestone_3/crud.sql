-- ============================
-- CRUD TEST SCRIPT (idempotent)
-- Target DB: mydatabase
-- ============================

USE mydatabase;


SET @demo_food_name = 'Sealed Magic Crackers';
SET @demo_brand = 'King''s Guard Foods';
SET @demo_category = '-Grain Snacks';
SET @demo_cuisine = 'Mediterranean';
SET @demo_user = 'demo_admin';
SET @existing_food_name = 'Grog (Canned)';
SET @existing_food_brand = 'Pirate''s Choice';

-- =====================================================
-- 1️⃣ CREATE TRANSACTION
-- =====================================================
START TRANSACTION;

INSERT IGNORE INTO users (username, email, role, first_name, last_name)
VALUES (@demo_user, 'demo_admin@example.com', 'admin', 'Demo', 'Admin');
SET @demo_user_id = (SELECT id FROM users WHERE username = @demo_user);

INSERT IGNORE INTO categories (category) VALUES (@demo_category);
SET @demo_category_id = (SELECT id FROM categories WHERE category = @demo_category);

INSERT IGNORE INTO cuisines (cuisine) VALUES (@demo_cuisine);
SET @demo_cuisine_id = (SELECT id FROM cuisines WHERE cuisine = @demo_cuisine);

INSERT INTO foods (
    name, brand, publication_status, dietary_fiber, sugars, protein, carbs,
    cholesterol, sodium, trans_fats, total_fats, sat_fats, serving_amt, serving_unit,
    user_id, category_id, cuisine_id
) VALUES (
    @demo_food_name,
    @demo_brand,
    'private',
    3.5,
    2.0,
    5.0,
    20.0,
    0.0,
    75.0,
    0.0,
    6.0,
    1.0,
    30.0,
    'g',
    @demo_user_id,
    @demo_category_id,
    @demo_cuisine_id
) ON DUPLICATE KEY UPDATE
    id = LAST_INSERT_ID(id),
    updated_at = CURRENT_TIMESTAMP;
SET @demo_food_id = LAST_INSERT_ID();

DELETE FROM ingredients WHERE food_id = @demo_food_id;
INSERT INTO ingredients (food_id, ingredient_name) VALUES
    (@demo_food_id, 'Sprouted Wheat Flour'),
    (@demo_food_id, 'Quinoa Seeds'),
    (@demo_food_id, 'Sea Salt'),
    (@demo_food_id, 'Olive Oil');

INSERT IGNORE INTO dietary_restrictions (restriction) VALUES ('Contains Gluten');
SET @restriction_gluten = (SELECT id FROM dietary_restrictions WHERE restriction = 'Contains Gluten');
DELETE FROM diet_restrict_assoc WHERE food_id = @demo_food_id;
INSERT IGNORE INTO diet_restrict_assoc (food_id, restriction_id)
VALUES (@demo_food_id, @restriction_gluten);

COMMIT;

-- =====================================================
-- 2️⃣ READ QUERY
-- =====================================================
SET @demo_food_id = (
    SELECT id FROM foods WHERE name = @demo_food_name AND brand = @demo_brand LIMIT 1
);

SELECT
    f.id,
    f.name,
    f.brand,
    c.category,
    cu.cuisine,
    f.protein,
    f.carbs,
    f.sugars,
    GROUP_CONCAT(DISTINCT dr.restriction ORDER BY dr.restriction SEPARATOR ', ') AS restrictions
FROM foods f
LEFT JOIN categories c ON f.category_id = c.id
LEFT JOIN cuisines cu ON f.cuisine_id = cu.id
LEFT JOIN diet_restrict_assoc dra ON f.id = dra.food_id
LEFT JOIN dietary_restrictions dr ON dra.restriction_id = dr.id
WHERE f.id = @demo_food_id
GROUP BY f.id, f.name, f.brand, c.category, cu.cuisine, f.protein, f.carbs, f.sugars;

-- =====================================================
-- 3️⃣ UPDATE TRANSACTION
-- =====================================================
START TRANSACTION;

SET @demo_food_id = (
    SELECT id FROM foods WHERE name = @demo_food_name AND brand = @demo_brand LIMIT 1
);

UPDATE foods
SET publication_status = 'public',
    sodium = 60.0,
    total_fats = 4.0,
    dietary_fiber = 4.5,
    updated_at = CURRENT_TIMESTAMP
WHERE id = @demo_food_id;

COMMIT;

-- =====================================================
-- 4️⃣ DELETE TRANSACTION (DEMO ITEM CLEANUP)
-- =====================================================
-- START TRANSACTION;
--
-- SET @demo_food_id = (
--     SELECT id FROM foods WHERE name = @demo_food_name AND brand = @demo_brand LIMIT 1
-- );
--
-- DELETE FROM foods WHERE id = @demo_food_id;
--
-- COMMIT;

-- =====================================================
-- 5️⃣ DELETE EXISTING DUMMY-FOODS ITEM
--     Removes "Grog (Canned)" (Pirate's Choice) that ships with init_data.sql.
--     Re-run scripts/reset_db.sh to restore it from dummy-foods.
-- =====================================================
START TRANSACTION;

SET @existing_food_id = (
    SELECT id
    FROM foods
    WHERE name = @existing_food_name
      AND brand = @existing_food_brand
    LIMIT 1
);

DELETE FROM foods WHERE id = @existing_food_id;

COMMIT;
