-- Change the default delimiter so we can use ';' inside our procedures
DELIMITER $$

-- ====================================================================
-- FUNCTION: fn_IsValidSession
-- ====================================================================
-- Purpose: Checks if a session token is valid and not expired.
-- Returns: The user_id (INT) if valid, or NULL if not found or expired.
-- Usage:   SELECT fn_IsValidSession('some_session_token');
-- ====================================================================

CREATE FUNCTION `fn_IsValidSession`(
    p_session_token VARCHAR(255)
)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    -- Declare a variable to hold the user_id
    DECLARE v_user_id INT;

    -- Initialize it to NULL (this will be returned if no match is found)
    SET v_user_id = NULL;

    -- Try to find a matching, unexpired session
    SELECT user_id
    INTO v_user_id
    FROM user_sessions
    WHERE session_token = p_session_token AND expires_at > NOW()
    LIMIT 1; -- Ensure we only get one result

    -- Return the result
    RETURN v_user_id;

END$$


-- ====================================================================
-- PROCEDURE: sp_GetFoodDetails
-- ====================================================================
-- Purpose: Gets all related data for a single food item.
--          This procedure returns THREE separate result sets.
-- Usage:   CALL sp_GetFoodDetails(123);
-- ====================================================================

CREATE PROCEDURE `sp_GetFoodDetails`(
    IN p_food_id INT
)
BEGIN
    -- 1. Get the main food details
    SELECT *
    FROM foods
    WHERE id = p_food_id;

    -- 2. Get the list of ingredients for that food
    SELECT ingredient_name
    FROM ingredients
    WHERE food_id = p_food_id;

    -- 3. Get the list of dietary restrictions for that food
    -- (We join with the restrictions table to get the name)
    SELECT r.id, r.restriction
    FROM dietary_restrictions r
    JOIN diet_restrict_ass dra ON r.id = dra.restriction_id
    WHERE dra.food_id = p_food_id;

END$$


-- ====================================================================
-- PROCEDURE: sp_AddNewFood
-- ====================================================================
-- Purpose: A transactional procedure to add a new food item and all its
--          related data (ingredients, restrictions) at once.
--          We assume p_ingredient_list is comma-separated (e.g., "Flour,Sugar,Eggs")
--          and p_restriction_list is comma-separated IDs (e.g., "1,5,7").
-- Usage:   CALL sp_AddNewFood(1, 'New Cookie', 'MyBrand', ..., 'Flour,Sugar', '1,3', @new_id, @msg);
--          SELECT @new_id, @msg;
-- ====================================================================

CREATE PROCEDURE `sp_AddNewFood`(
    -- IN parameters for the 'foods' table
    IN p_user_id INT,
    IN p_name VARCHAR(255),
    IN p_brand VARCHAR(100),
    IN p_publication_status ENUM('draft', 'published'),
    IN p_sugars FLOAT,
    IN p_protein FLOAT,
    IN p_carbs FLOAT,
    IN p_dietary_fiber FLOAT,
    IN p_cal FLOAT,
    IN p_cholesterol FLOAT,
    IN p_sodium FLOAT,
    IN p_trans_fats FLOAT,
    IN p_total_fats FLOAT,
    IN p_sat_fats FLOAT,
    IN p_serving_amt FLOAT,
    IN p_serving_unit VARCHAR(50),
    IN p_category_id INT,
    IN p_cuisine_id INT,

    -- IN parameters for the related data (comma-separated lists)
    IN p_ingredient_list TEXT,
    IN p_restriction_list TEXT,

    -- OUT parameters to return the result
    OUT p_new_food_id INT,
    OUT p_message VARCHAR(255)
)
BEGIN
    -- Variable to hold the new food ID after we insert it
    DECLARE v_food_id INT;

    -- Variables for looping through the comma-separated lists
    DECLARE v_ingredient_name VARCHAR(255);
    DECLARE v_restriction_id_str VARCHAR(10);
    DECLARE v_ingredient_pos INT;
    DECLARE v_restriction_pos INT;
    DECLARE v_temp_ingredient_list TEXT;
    DECLARE v_temp_restriction_list TEXT;

    -- Declare an exit handler for any SQL error.
    -- This will roll back the transaction.
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_new_food_id = NULL;
        SET p_message = 'An error occurred. Transaction rolled back.';
    END;

    -- Start the transaction
    START TRANSACTION;

    -- 1. Insert the main food item
    INSERT INTO foods (
        name, brand, publication_status, sugars, protein, carbs,
        dietary_fiber, cal, cholesterol, sodium, trans_fats,
        total_fats, sat_fats, serving_amt, serving_unit,
        user_id, category_id, cuisine_id
    ) VALUES (
        p_name, p_brand, p_publication_status, p_sugars, p_protein, p_carbs,
        p_dietary_fiber, p_cal, p_cholesterol, p_sodium, p_trans_fats,
        p_total_fats, p_sat_fats, p_serving_amt, p_serving_unit,
        p_user_id, p_category_id, p_cuisine_id
    );

    -- Get the ID of the food we just inserted
    SET v_food_id = LAST_INSERT_ID();
    SET p_new_food_id = v_food_id; -- Set OUT param

    -- 2. Loop and insert ingredients
    -- Add a comma to the end to make the loop logic simpler
    SET v_temp_ingredient_list = CONCAT(p_ingredient_list, ',');

    WHILE LENGTH(v_temp_ingredient_list) > 0 DO
        -- Find the next comma
        SET v_ingredient_pos = LOCATE(',', v_temp_ingredient_list);
        -- Get the part before the comma
        SET v_ingredient_name = TRIM(SUBSTRING(v_temp_ingredient_list, 1, v_ingredient_pos - 1));

        -- If the name is not empty, insert it
        IF LENGTH(v_ingredient_name) > 0 THEN
            INSERT INTO ingredients (food_id, ingredient_name)
            VALUES (v_food_id, v_ingredient_name);
        END IF;

        -- Remove the part we just processed from the list
        SET v_temp_ingredient_list = SUBSTRING(v_temp_ingredient_list, v_ingredient_pos + 1);
    END WHILE;


    -- 3. Loop and insert dietary restrictions
    -- Add a comma to the end
    SET v_temp_restriction_list = CONCAT(p_restriction_list, ',');

    WHILE LENGTH(v_temp_restriction_list) > 0 DO
        -- Find the next comma
        SET v_restriction_pos = LOCATE(',', v_temp_restriction_list);
        -- Get the ID (as a string)
        SET v_restriction_id_str = TRIM(SUBSTRING(v_temp_restriction_list, 1, v_restriction_pos - 1));

        -- If the ID is not empty, convert to INT and insert
        IF LENGTH(v_restriction_id_str) > 0 THEN
            INSERT INTO diet_restrict_ass (food_id, restriction_id)
            VALUES (v_food_id, CAST(v_restriction_id_str AS UNSIGNED));
        END IF;

        -- Remove the part we just processed
        SET v_temp_restriction_list = SUBSTRING(v_temp_restriction_list, v_restriction_pos + 1);
    END WHILE;


    -- If we made it this far without an error, commit the transaction
    COMMIT;
    SET p_message = 'Food added successfully.';

END$$

-- ====================================================================
-- TRIGGER: foods_BEFORE_INSERT
-- ====================================================================
-- Purpose: This trigger fires before any new row is inserted into the
--          `foods` table. Its primary job is to act as a safety net
--          by ensuring that the `publication_status` is always set to
--          'private' by default. This prevents foods from being
--          accidentally public if the application layer fails to specify
--          a status.
-- ====================================================================
CREATE DEFINER = CURRENT_USER TRIGGER `mydatabase`.`foods_BEFORE_INSERT` 
BEFORE INSERT ON `foods` FOR EACH ROW
BEGIN
    SET NEW.publication_status = 'private';
END$$

-- Don't forget to reset the delimiter back to normal!
DELIMITER ;