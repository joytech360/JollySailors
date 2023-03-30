-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: daycareapp
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('adeb6a3c7536');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `child`
--

DROP TABLE IF EXISTS `child`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `child` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  KEY `ix_child_name` (`name`),
  CONSTRAINT `child_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child`
--

LOCK TABLES `child` WRITE;
/*!40000 ALTER TABLE `child` DISABLE KEYS */;
/*!40000 ALTER TABLE `child` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `child_request`
--

DROP TABLE IF EXISTS `child_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `child_request` (
  `id` int NOT NULL AUTO_INCREMENT,
  `daycare_id` int DEFAULT NULL,
  `child_id` int DEFAULT NULL,
  `date_requested` date DEFAULT NULL,
  `message` varchar(512) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `child_id` (`child_id`),
  KEY `daycare_id` (`daycare_id`),
  CONSTRAINT `child_request_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `child` (`id`),
  CONSTRAINT `child_request_ibfk_2` FOREIGN KEY (`daycare_id`) REFERENCES `daycare` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child_request`
--

LOCK TABLES `child_request` WRITE;
/*!40000 ALTER TABLE `child_request` DISABLE KEYS */;
/*!40000 ALTER TABLE `child_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daycare`
--

DROP TABLE IF EXISTS `daycare`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daycare` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb3_bin DEFAULT NULL,
  `email` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `phone_no` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `date_joined` date DEFAULT NULL,
  `street` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `city` varchar(32) COLLATE utf8mb3_bin DEFAULT NULL,
  `province` varchar(8) COLLATE utf8mb3_bin DEFAULT NULL,
  `postal_code` varchar(16) COLLATE utf8mb3_bin DEFAULT NULL,
  `country` varchar(32) COLLATE utf8mb3_bin DEFAULT NULL,
  `lat` decimal(10,6) DEFAULT NULL,
  `lng` decimal(10,6) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `opening_time` time DEFAULT NULL,
  `closing_time` time DEFAULT NULL,
  `about` varchar(1028) COLLATE utf8mb3_bin DEFAULT NULL,
  `profile_pic` varchar(128) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_daycare_email` (`email`),
  KEY `ix_daycare_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daycare`
--

LOCK TABLES `daycare` WRITE;
/*!40000 ALTER TABLE `daycare` DISABLE KEYS */;
/*!40000 ALTER TABLE `daycare` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daycare_staff`
--

DROP TABLE IF EXISTS `daycare_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daycare_staff` (
  `user_id` int DEFAULT NULL,
  `daycare_id` int DEFAULT NULL,
  KEY `daycare_id` (`daycare_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `daycare_staff_ibfk_1` FOREIGN KEY (`daycare_id`) REFERENCES `daycare` (`id`),
  CONSTRAINT `daycare_staff_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daycare_staff`
--

LOCK TABLES `daycare_staff` WRITE;
/*!40000 ALTER TABLE `daycare_staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `daycare_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daycare_student`
--

DROP TABLE IF EXISTS `daycare_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daycare_student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `daycare_id` int DEFAULT NULL,
  `child_id` int DEFAULT NULL,
  `date_joined` date DEFAULT NULL,
  `date_left` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `child_id` (`child_id`),
  KEY `daycare_id` (`daycare_id`),
  CONSTRAINT `daycare_student_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `child` (`id`),
  CONSTRAINT `daycare_student_ibfk_2` FOREIGN KEY (`daycare_id`) REFERENCES `daycare` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daycare_student`
--

LOCK TABLES `daycare_student` WRITE;
/*!40000 ALTER TABLE `daycare_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `daycare_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `email` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `phone_no` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `join_date` date DEFAULT NULL,
  `password_hash` varchar(128) COLLATE utf8mb3_bin DEFAULT NULL,
  `street` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `city` varchar(32) COLLATE utf8mb3_bin DEFAULT NULL,
  `province` varchar(8) COLLATE utf8mb3_bin DEFAULT NULL,
  `postal_code` varchar(16) COLLATE utf8mb3_bin DEFAULT NULL,
  `country` varchar(32) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  KEY `ix_user_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-30  0:12:34
