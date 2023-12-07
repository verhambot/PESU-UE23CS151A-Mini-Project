-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: zomapes
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `zomamenu`
--

DROP TABLE IF EXISTS `zomamenu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zomamenu` (
  `Sl_No` int NOT NULL,
  `Food` varchar(512) DEFAULT NULL,
  `Price` int DEFAULT NULL,
  PRIMARY KEY (`Sl_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zomamenu`
--

LOCK TABLES `zomamenu` WRITE;
/*!40000 ALTER TABLE `zomamenu` DISABLE KEYS */;
INSERT INTO `zomamenu` VALUES (1,'Fried Rice',60),(2,'Chicken Biryani',90),(3,'Veg Noodles',70),(4,'Chicken Noodles',90),(5,'Paneer Parotta',60),(6,'Veg Parotta',70),(7,'Aloo Parotta',60),(8,'Curd Rice',50),(9,'Roti Curry',60),(10,'Masala Dosa',60),(11,'Idly 2pcs',40),(12,'Vada',25),(13,'Mangalore Buns',50),(14,'Poori',60),(15,'Oreo Milkshake',80),(16,'KitKat Milkshake',80),(17,'Cold Coffee',80),(18,'Coffee',15),(19,'Cake',30),(20,'Water Bottle',20);
/*!40000 ALTER TABLE `zomamenu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-07 12:16:13
