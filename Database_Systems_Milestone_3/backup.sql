-- MySQL dump 10.13  Distrib 8.0.43, for Linux (aarch64)
--
-- Host: localhost    Database: mydatabase
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (21,'-Grain Snacks'),(5,'Beverage'),(2,'Beverage (Grounds)'),(15,'Bread'),(8,'Breakfast Cereal'),(16,'Canned Goods'),(3,'Condiment'),(6,'Crackers'),(14,'Dairy'),(17,'Dessert'),(4,'Fast Food'),(10,'Frozen Dessert'),(20,'Pasta Alternative'),(19,'Prepared Meal'),(1,'Shelf-Stable Meal'),(13,'Snack'),(11,'Snack Bar'),(7,'Snack Mix'),(9,'Soda');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuisines`
--

DROP TABLE IF EXISTS `cuisines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuisines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cuisine` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cuisine` (`cuisine`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuisines`
--

LOCK TABLES `cuisines` WRITE;
/*!40000 ALTER TABLE `cuisines` DISABLE KEYS */;
INSERT INTO `cuisines` VALUES (3,'American'),(16,'Atlantean'),(8,'Cyberpunk'),(11,'Dwarven'),(4,'Elven'),(15,'Fusion'),(7,'Gothic'),(6,'Intergalactic'),(17,'Mediterranean'),(1,'Military'),(2,'Monster'),(9,'Pirate'),(5,'Robotic'),(14,'Sci-Fi'),(13,'Space-faring'),(10,'Volcanic');
/*!40000 ALTER TABLE `cuisines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `diet_restrict_assoc`
--

DROP TABLE IF EXISTS `diet_restrict_assoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diet_restrict_assoc` (
  `food_id` int NOT NULL,
  `restriction_id` int NOT NULL,
  PRIMARY KEY (`food_id`,`restriction_id`),
  KEY `restriction_id` (`restriction_id`),
  CONSTRAINT `diet_restrict_assoc_ibfk_1` FOREIGN KEY (`food_id`) REFERENCES `foods` (`id`) ON DELETE CASCADE,
  CONSTRAINT `diet_restrict_assoc_ibfk_2` FOREIGN KEY (`restriction_id`) REFERENCES `dietary_restrictions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diet_restrict_assoc`
--

LOCK TABLES `diet_restrict_assoc` WRITE;
/*!40000 ALTER TABLE `diet_restrict_assoc` DISABLE KEYS */;
INSERT INTO `diet_restrict_assoc` VALUES (1,1),(10,1),(14,1),(1,2),(4,2),(21,2),(2,3),(17,3),(18,3),(2,4),(5,4),(6,4),(19,4),(2,5),(5,5),(19,5),(20,5),(2,6),(4,8),(7,12),(9,13),(11,15),(13,17),(15,19),(16,20),(18,23),(20,27);
/*!40000 ALTER TABLE `diet_restrict_assoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dietary_restrictions`
--

DROP TABLE IF EXISTS `dietary_restrictions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dietary_restrictions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `restriction` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `restriction` (`restriction`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dietary_restrictions`
--

LOCK TABLES `dietary_restrictions` WRITE;
/*!40000 ALTER TABLE `dietary_restrictions` DISABLE KEYS */;
INSERT INTO `dietary_restrictions` VALUES (13,'Caffeinated'),(8,'Contains Beef'),(1,'Contains Dairy'),(2,'Contains Gluten'),(12,'Contains Nuts'),(6,'Dairy-Free'),(20,'Extremely Spicy'),(5,'Gluten-Free'),(19,'High-Fiber'),(15,'High-Protein'),(23,'Low-Calorie'),(27,'Low-Carb'),(16,'Non-Alcoholic'),(17,'Spicy'),(3,'Sugar-Free'),(4,'Vegan');
/*!40000 ALTER TABLE `dietary_restrictions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foods`
--

DROP TABLE IF EXISTS `foods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foods` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `brand` varchar(100) DEFAULT NULL,
  `publication_status` enum('public','private','unlisting') DEFAULT 'private',
  `dietary_fiber` float DEFAULT NULL,
  `sugars` float DEFAULT NULL,
  `protein` float DEFAULT NULL,
  `carbs` float DEFAULT NULL,
  `cal` float DEFAULT NULL,
  `cholesterol` float DEFAULT NULL,
  `sodium` float DEFAULT NULL,
  `trans_fats` float DEFAULT NULL,
  `total_fats` float DEFAULT NULL,
  `sat_fats` float DEFAULT NULL,
  `serving_amt` float DEFAULT NULL,
  `serving_unit` enum('g','mg','oz','lb','tsp','tbsp','cup','item') DEFAULT 'g',
  `user_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `cuisine_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_food_name_brand` (`name`,`brand`),
  KEY `user_id` (`user_id`),
  KEY `category_id` (`category_id`),
  KEY `cuisine_id` (`cuisine_id`),
  KEY `name` (`name`),
  CONSTRAINT `foods_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `foods_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL,
  CONSTRAINT `foods_ibfk_3` FOREIGN KEY (`cuisine_id`) REFERENCES `cuisines` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foods`
--

LOCK TABLES `foods` WRITE;
/*!40000 ALTER TABLE `foods` DISABLE KEYS */;
INSERT INTO `foods` VALUES (1,'MRE - Chili Mac','US Gov\'t Surplus','public',6,8,18,45,NULL,55,1100,1,20,8,227,'g',1,1,1,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(2,'Shadow-Bean Coffee','Umbral Roasters','public',0,0,0,0,NULL,0,0,0,0,0,2,'tbsp',1,2,NULL,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(3,'Slime-Mold Jelly','Ooze Organics','public',0,12,0,13,NULL,0,10,0,0,0,1,'tbsp',1,3,2,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(4,'Steamed Hams','Krusty Burger','public',2,7,22,40,NULL,80,980,1.5,25,10,1,'item',1,4,3,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(5,'Glimmerwing Nectar','Feywild Botanicals','public',0,8,0,8,NULL,0,5,0,0,0,8,'oz',1,5,4,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(6,'Ancient Grain Crackers','Pharaoh\'s Fields','public',3,0,3,18,NULL,0,190,0,7,0.5,6,'item',1,6,NULL,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(7,'Mecha-Munch Nuts & Bolts Mix','Roboto Snacks','public',4,2,9,10,NULL,0,180,0,22,3.5,40,'g',1,7,5,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(8,'Cosmic Crunch Cereal','Galaxy Foods','public',4,12,3,35,NULL,0,150,0,5,1,1.5,'cup',1,8,6,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(9,'Vampire\'s Kiss Soda','Nocturne Beverages','public',0,38,0,38,NULL,0,30,0,0,0,1,'item',1,9,7,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(10,'Arctic Ice Cream (Mint Shard)','Polar Pantry','public',1,18,3,20,NULL,45,50,0.5,14,9,0.66,'cup',1,10,NULL,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(11,'Cyber-Coated Energy Bar','NeoCorp Dynamics','public',5,10,20,25,NULL,10,100,0,12,4,60,'g',1,11,8,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(13,'Magma Crisps','Vulcan Snacks','public',1,0,2,25,NULL,0,450,0,15,2,28,'g',1,13,10,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(14,'Sky-Berry Yogurt','Nimbus Dairy','public',1,18,6,22,NULL,25,80,0,8,5,150,'g',1,14,NULL,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(15,'Dwarven Rock-Bread','Ironforge Bakery','public',15,1,10,50,NULL,0,300,0,2,0.5,1,'item',1,15,11,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(16,'Dragon\'s Breath Chili (Canned)','Wyvern Kitchen','public',8,6,20,25,NULL,50,950,1,18,7,1,'cup',1,16,3,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(17,'Zero-G Gelatin Bites','AstroEats','public',0,0,2,0,NULL,0,40,0,0,0,1,'item',1,17,13,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(18,'Cryo-Stasis Popsicle','Future Freeze','public',0,0,0,3,NULL,0,5,0,0,0,1,'item',1,10,14,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(19,'Quantum Quinoa Salad','Particle Provisions','public',5,3,7,30,NULL,0,250,0,10,1,1,'cup',1,19,15,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(20,'Deep Sea Kelp Noodles','Atlantean Harvest','public',3,0,2,10,NULL,0,600,0,1,0,1,'cup',1,20,16,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(21,'Sealed Magic Crackers','King\'s Guard Foods','public',4.5,2,5,20,NULL,0,60,0,4,1,30,'g',2,21,17,'2025-11-13 01:18:35','2025-11-13 01:18:35');
/*!40000 ALTER TABLE `foods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `food_id` int NOT NULL,
  `ingredient_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `food_id` (`food_id`),
  CONSTRAINT `ingredients_ibfk_1` FOREIGN KEY (`food_id`) REFERENCES `foods` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (1,1,'Cooked Pasta'),(2,1,'Beef Crumbles'),(3,1,'Tomato Sauce'),(4,1,'Kidney Beans'),(5,1,'Cheese Sauce'),(6,1,'Modified Food Starch'),(7,2,'100% Void-Roasted Arabica Beans'),(8,3,'Cultured Slime Gelatin'),(9,3,'Fruit Pectin'),(10,3,'Sugar'),(11,3,'Citric Acid'),(12,4,'100% Beef Patty'),(13,4,'Bun'),(14,4,'Lettuce'),(15,4,'Special Sauce'),(16,5,'Dewdrops'),(17,5,'Liquefied Moonlight'),(18,5,'Crushed Pixie Petals'),(19,6,'Spelt Flour'),(20,6,'Amaranth'),(21,6,'Quinoa'),(22,6,'Sunflower Oil'),(23,6,'Sea Salt'),(24,7,'Titanium-Salted Peanuts'),(25,7,'Cashew \"Gears\"'),(26,7,'Almond \"Sprockets\"'),(27,7,'Lubricant (Oil)'),(28,8,'Puffed Quasars'),(29,8,'Dried Nebula Berries'),(30,8,'Crystallized Stardust'),(31,9,'Carbonated Water'),(32,9,'Cane Sugar'),(33,9,'Citric Acid'),(34,9,'Natural Pomegranate Flavor'),(35,9,'Red #40'),(36,10,'Cream'),(37,10,'Milk'),(38,10,'Sugar'),(39,10,'Peppermint Extract'),(40,10,'Dark Chocolate Shards'),(41,11,'Protein Isolate'),(42,11,'Nano-Oats'),(43,11,'Synthetic Honey'),(44,11,'Chromium Drizzle'),(49,13,'Obsidian Flakes'),(50,13,'Sulfur Salt'),(51,13,'Lava Essence (Flavoring)'),(52,14,'Cultured Milk'),(53,14,'Cloudberries'),(54,14,'Cane Sugar'),(55,14,'Live Cultures'),(56,15,'Stoneground Wheat'),(57,15,'Basalt Flour'),(58,15,'Salt'),(59,15,'Yeast'),(60,16,'Ground Beef'),(61,16,'Kidney Beans'),(62,16,'Tomato Puree'),(63,16,'Ghost Peppers'),(64,16,'Onion'),(65,16,'Spices'),(66,17,'Water'),(67,17,'Gelatin'),(68,17,'Aspartame'),(69,17,'Artificial Flavor'),(70,17,'Potassium Sorbate'),(71,18,'Water'),(72,18,'Blue Raspberry Flavoring'),(73,18,'Citric Acid'),(74,18,'Stabilizers'),(75,18,'Sucralose'),(76,19,'Entangled Quinoa'),(77,19,'Diced Bell Peppers'),(78,19,'Cucumber'),(79,19,'Lemon-Vinaigrette'),(80,20,'Bioluminescent Kelp'),(81,20,'Sea Salt'),(82,20,'Filtered Trench Water'),(83,21,'Sprouted Wheat Flour'),(84,21,'Quinoa Seeds'),(85,21,'Sea Salt'),(86,21,'Olive Oil');
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth_accounts`
--

DROP TABLE IF EXISTS `oauth_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth_accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `provider` varchar(50) NOT NULL,
  `provider_user_id` varchar(255) NOT NULL,
  `access_token` varchar(2048) DEFAULT NULL,
  `refresh_token` varchar(2048) DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_provider_user_id` (`provider`,`provider_user_id`),
  UNIQUE KEY `uq_provider_user` (`provider`,`user_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_oauth_accounts_provider` (`provider`),
  KEY `ix_oauth_accounts_provider_user_id` (`provider_user_id`),
  CONSTRAINT `oauth_accounts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth_accounts`
--

LOCK TABLES `oauth_accounts` WRITE;
/*!40000 ALTER TABLE `oauth_accounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passwords`
--

DROP TABLE IF EXISTS `passwords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passwords` (
  `user_id` int NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `passwords_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passwords`
--

LOCK TABLES `passwords` WRITE;
/*!40000 ALTER TABLE `passwords` DISABLE KEYS */;
/*!40000 ALTER TABLE `passwords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_sessions`
--

DROP TABLE IF EXISTS `user_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `session_token` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `refresh_token` varchar(255) NOT NULL,
  `refresh_token_expires_at` datetime NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_sessions_refresh_token` (`refresh_token`),
  UNIQUE KEY `ix_user_sessions_session_token` (`session_token`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_sessions`
--

LOCK TABLES `user_sessions` WRITE;
/*!40000 ALTER TABLE `user_sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `role` enum('admin','moderator','user','disabled') DEFAULT 'user',
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `username_2` (`username`),
  KEY `email_2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'System','system@local.host','admin','System',NULL,'2025-11-13 01:18:35','2025-11-13 01:18:35'),(2,'demo_admin','demo_admin@example.com','admin','Demo','Admin','2025-11-13 01:18:35','2025-11-13 01:18:35');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'mydatabase'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-13  1:34:47
