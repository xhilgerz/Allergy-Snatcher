

CREATE DEFINER = CURRENT_USER TRIGGER `mydatabase`.`foods_BEFORE_INSERT` 
BEFORE INSERT ON `foods` FOR EACH ROW
BEGIN
    SET NEW.publication_status = 'private';
END