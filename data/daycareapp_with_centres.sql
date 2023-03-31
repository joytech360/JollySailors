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
  `version_num` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,
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
  `name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
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
  `message` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
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
  `name` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `email` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `phone_no` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `date_joined` date DEFAULT NULL,
  `street` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `city` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `province` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `postal_code` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `country` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `lat` decimal(10,6) DEFAULT NULL,
  `lng` decimal(10,6) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `opening_time` time DEFAULT NULL,
  `closing_time` time DEFAULT NULL,
  `about` varchar(1028) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `profile_pic` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_daycare_email` (`email`),
  KEY `ix_daycare_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=184 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daycare`
--

LOCK TABLES `daycare` WRITE;
/*!40000 ALTER TABLE `daycare` DISABLE KEYS */;
INSERT INTO `daycare` VALUES (1,'Cathedral Area Cooperative Daycare',NULL,'306-522-7533',NULL,'2051 Cameron Street',' Regina',' SK','S4T',NULL,50.446169,-104.625118,NULL,NULL,NULL,'Centre',NULL),(2,'Stepping Stones, Robinson',NULL,'306-352-3755',NULL,'1501 Robinson Street',' Regina',' SK','S4T',NULL,50.454680,-104.623722,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(3,'The Dragon\'s Den Child Care',NULL,'306-791-8682',NULL,'2401 Retallack Street',' Regina',' SK','S4T',NULL,50.440415,-104.621851,NULL,NULL,NULL,'Centre',NULL),(4,'Samreen Khan',NULL,'306-580-4948',NULL,'1409 Rae Street',' Regina',' SK','S4T',NULL,50.456545,-104.620759,NULL,NULL,NULL,'Home',NULL),(5,'Crystal Benjamin',NULL,'306-698-3226',NULL,'2345 Toronto Street',' Regina',' SK','S4P',NULL,50.441537,-104.599429,NULL,NULL,NULL,'Home',NULL),(6,'MacKenzie Infant Care Centre (Registered Balfour Students only)',NULL,'306-569-1308',NULL,'1308 College Avenue',' Regina',' SK','S4P',NULL,50.441074,-104.599586,NULL,NULL,NULL,'Centre, Teen parent infant centre, Accepts infants 6 weeks - 18 months',NULL),(7,'Little Memories Child Care Co-op',NULL,'306-522-0393',NULL,'3128 Dewdney Avenue',' Regina',' SK','S4T',NULL,50.455392,-104.626120,NULL,NULL,NULL,'Centre',NULL),(8,'Mackenzie Infant Care Centre-Balfour Site II (Registered Balfour Students only)',NULL,'306-569-1308',NULL,'1245 College Avenue',' Regina',' SK','S4P',NULL,50.440074,-104.599087,NULL,NULL,NULL,'Centre, Teen parent infant centre, Accepts infants 6 weeks - 18 months',NULL),(9,'Wise Owl School Age Care',NULL,'306-522-5291',NULL,'3525 13th Avenue',' Regina',' SK','S4T',NULL,50.444789,-104.631881,NULL,NULL,NULL,'Centre',NULL),(10,'Gemma Lopez',NULL,'306-450-3605',NULL,'1247 Retallack Street',' Regina',' SK','S4T',NULL,50.458863,-104.622179,NULL,NULL,NULL,'Group family child care home',NULL),(11,'Stepping Stones, Elphinstone',NULL,'306-352-2533',NULL,'1561 Elphinstone Street',' Regina',' SK','S4T',NULL,50.453971,-104.630699,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months, Extended hours',NULL),(12,'Scott Infant and Toddler Centre',NULL,'306-525-2344',NULL,'3355 6th Avenue',' Regina',' SK','S4T',NULL,50.459405,-104.630798,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months, Teen parent infant centre',NULL),(13,'Prairie Lily Early Learning Centre - Sacred Heart',NULL,'306-949-0090',NULL,'1325 Argyle Street',' Regina',' SK','S4T',NULL,50.457559,-104.631677,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(14,'Belinda Wrobel',NULL,'306-525-6632',NULL,'2735 Winnipeg Street',' Regina',' SK','S4P',NULL,50.435558,-104.594860,NULL,NULL,NULL,'Home',NULL),(15,'Turtle Park Co-operative Day Care Centre',NULL,'306-584-9344',NULL,'3100 – 20th Avenue',' Regina',' SK','S4S',NULL,50.432969,-104.626220,NULL,NULL,NULL,'Centre',NULL),(16,'Jodi Anderson',NULL,'306-352-2892',NULL,'2600 Coronation Street',' Regina',' SK','S4S',NULL,50.437583,-104.636574,NULL,NULL,NULL,'Home',NULL),(17,'Emily Camposano',NULL,'306-241-6333',NULL,'2100 Pasqua Street',' Regina',' SK','S4T',NULL,50.445337,-104.641251,NULL,NULL,NULL,'Group family child care home',NULL),(18,'Shazia Qasim',NULL,'306-520-8722',NULL,'2101 Edward Street',' Regina',' SK','S4T',NULL,50.445361,-104.642008,NULL,NULL,NULL,'Group family child care home',NULL),(19,'Abida Sultana',NULL,'306-209-9200',NULL,'3635 Normandy Avenue',' Regina',' SK','S4S',NULL,50.433711,-104.633734,NULL,NULL,NULL,'Home',NULL),(20,'Seven Stones Child Care',NULL,'306-525-3960',NULL,'1101 Princess Street',' Regina',' SK','S4T',NULL,50.460752,-104.634938,NULL,NULL,NULL,'Centre',NULL),(21,'Meherun Nesha',NULL,'306-757-9867',NULL,'715 Robinson Street',' Regina',' SK','S4T',NULL,50.467387,-104.623668,NULL,NULL,NULL,'Home',NULL),(22,'Child Care Centre Co-operative',NULL,'306-757-2919',NULL,'105 College Avenue East',' Regina',' SK','S4N',NULL,50.440656,-104.581064,NULL,NULL,NULL,'Centre',NULL),(23,'Circle Project Infant Centre',NULL,'306-949-4911',NULL,'4401 Dewdney Avenue',' Regina',' SK','S4T',NULL,50.454919,-104.644096,NULL,NULL,NULL,'Accepts infants 6 weeks - 18 months, Centre',NULL),(24,'Shaista Shaheen',NULL,'306-584-9469',NULL,'670 Garnet Street',' Regina',' SK','S4T',NULL,50.468300,-104.627233,NULL,NULL,NULL,'Home, Group family child care home',NULL),(25,'Stepping Stones – Broad',NULL,'306-791-3315',NULL,'545 Broad Street',' Regina',' SK','S4R',NULL,50.470245,-104.606100,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(26,'Circle Project Children\'s Centre',NULL,'306-569-3988',NULL,'1115 Pasqua Street',' Regina',' SK','S4T',NULL,50.461266,-104.640743,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(27,'Regina Eastview Day Care',NULL,'306-525-5543',NULL,'128 – 6th Avenue East',' Regina',' SK','S4N',NULL,50.460016,-104.582554,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(28,'Orr Centre Daycare Inc.',NULL,'306-559-1001',NULL,'358 Century Crescent',' Regina',' SK','S4T',NULL,50.453591,-104.647824,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(29,'Sandcastles Coventry Road',NULL,'306-545-9001',NULL,'9 Coventry Road',' Regina',' SK','S4T',NULL,50.458945,-104.644528,NULL,NULL,NULL,'Centre',NULL),(30,'Dianne Barnes',NULL,'306-352-1575',NULL,'713 Argyle Street',' Regina',' SK','S4T',NULL,50.467406,-104.632289,NULL,NULL,NULL,'Home',NULL),(31,'Ambreen Majeed',NULL,'306-352-0994',NULL,'475 Ottawa Street',' Regina',' SK','S4R',NULL,50.471005,-104.600302,NULL,NULL,NULL,'Group family child care home',NULL),(32,'Adult Campus Child Care Centre',NULL,'306-757-8140',NULL,'4210 4th Avenue',' Regina',' SK','S4T',NULL,50.463612,-104.641759,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(33,'YWCA Deanna\'s Den',NULL,'306-359-4425',NULL,'1855 2nd Avenue North',' Regina',' SK','S4R',NULL,50.472157,-104.607507,NULL,NULL,NULL,'Accepts infants 6 weeks - 18 months',NULL),(34,'YWCA Sally\'s Place',NULL,'306-359-4425',NULL,'1855 2nd Avenue North',' Regina',' SK','S4R',NULL,50.472157,-104.607507,NULL,NULL,NULL,'Centre',NULL),(35,'Nazneen Kashif',NULL,'306-450-6550',NULL,'3207 Westgate Avenue',' Regina',' SK','S4S',NULL,50.425257,-104.626457,NULL,NULL,NULL,'Home',NULL),(36,'Pamela Fuchs',NULL,'306-757-6056',NULL,'2775 Francis Street',' Regina',' SK','S4N',NULL,50.434745,-104.578988,NULL,NULL,NULL,'Group family child care home, Home',NULL),(37,'Bo-Peep Co-operative Day Care',NULL,'306-545-3498',NULL,'4834 Dewdney Avenue',' Regina',' SK','S4T',NULL,50.455503,-104.650733,NULL,NULL,NULL,'Centre',NULL),(38,'Dawn Marie',NULL,'306-584-1397',NULL,'41 Calder Crescent',' Regina',' SK','S4S',NULL,50.422846,-104.610425,NULL,NULL,NULL,'Home, Group family child care home',NULL),(39,'Julie Geiger',NULL,'306-924-5908',NULL,'2815 Harvey Street',' Regina',' SK','S4N',NULL,50.433570,-104.577546,NULL,NULL,NULL,'Home',NULL),(40,'Brenda Vogt',NULL,'306-352-8878',NULL,'468 Froom Crescent',' Regina',' SK','S4N',NULL,50.443291,-104.571095,NULL,NULL,NULL,'Home',NULL),(41,'Ehrlo Early Learning Centre Imperial',NULL,'306-751-4502',NULL,'200 Broad Street',' Regina',' SK','S4R',NULL,50.476555,-104.607405,NULL,NULL,NULL,'Centre',NULL),(42,'Sandcastles Kings Road',NULL,'306-584-9660',NULL,'3615 Kings Road',' Regina',' SK','S4S',NULL,50.422298,-104.626173,NULL,NULL,NULL,'Accepts infants 6 weeks - 18 months',NULL),(43,'YMCA South Child Care Centre McVeety',NULL,'306-584-8123',NULL,'38 Turgeon Crescent',' Regina',' SK','S4S',NULL,50.420443,-104.605221,NULL,NULL,NULL,'Centre',NULL),(44,'Rizwana Shahid',NULL,'639-571-3435',NULL,'175 Scarth Street',' Regina',' SK','S4R',NULL,50.475688,-104.610461,NULL,NULL,NULL,'Home',NULL),(45,'Gator Park Child Care Centre',NULL,'306-584-2999',NULL,'2941 Lakeview Avenue',' Regina',' SK','S4S',NULL,50.421235,-104.626082,NULL,NULL,NULL,'Centre',NULL),(46,'Centre éducatif à la petite enfance de l\'École du Parc',NULL,'306-533-2432',NULL,'621 Douglas Avenue East',' Regina',' SK','S4N',NULL,50.433015,-104.576575,NULL,NULL,NULL,'Francophone, Accepts infants 6 weeks - 18 months',NULL),(47,'Ayesha Tariq',NULL,'306-216-2204',NULL,'2305 Greer Court',' Regina',' SK','S4N',NULL,50.444467,-104.568796,NULL,NULL,NULL,'Home',NULL),(48,'Valerie Pretty',NULL,'306-205-1559',NULL,'159 Halifax Street',' Regina',' SK','S4R',NULL,50.475915,-104.603205,NULL,NULL,NULL,'Home',NULL),(49,'Kids First Day Care Centre (Registered High School Students only)',NULL,'306-523-3318',NULL,'1069 – 14th Avenue East',' Regina',' SK','S4N',NULL,50.443256,-104.568371,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(50,'Hope\'s Home John Paul II',NULL,'306-205-8412',NULL,'2200 25th Avenue',' Regina',' SK','S4S',NULL,50.419218,-104.612922,NULL,NULL,NULL,'Centre',NULL),(51,'Saplings Early Learning Child Care Centre - Hamilton',NULL,'306-206-0267',NULL,'125 Hamilton Street',' Regina',' SK','S4R',NULL,50.476616,-104.608332,NULL,NULL,NULL,'Accepts infants 6 weeks - Kindergarten',NULL),(52,'Bright Beginnings Early Childhood Centre',NULL,'306-543-7373',NULL,'3775 Regency Crescent',' Regina',' SK','S4R',NULL,50.472731,-104.634967,NULL,NULL,NULL,'Centre',NULL),(53,'God’s Little Blessings Child Care',NULL,'306-543-1301',NULL,'5130 – 4th Avenue',' Regina',' SK','S4T',NULL,50.463163,-104.655044,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(54,'Saima Waheed',NULL,'306-501-7186',NULL,'1349 Forget Street',' Regina',' SK','S4T',NULL,50.457423,-104.649296,NULL,NULL,NULL,'Group family child care home',NULL),(55,'Solid Futures Learning Centre Co-operative',NULL,'306-543-7874',NULL,'4705 – 1st Avenue',' Regina',' SK','S4T',NULL,50.467087,-104.648640,NULL,NULL,NULL,'Centre',NULL),(56,'La maison educative Gard\'Amis',NULL,'306-525-9449',NULL,'2 Turgeon Crescent',' Regina',' SK','S4S',NULL,50.418591,-104.605119,NULL,NULL,NULL,'Francophone, Accepts infants 6 weeks - 18 months',NULL),(57,'Sheila Pretty',NULL,'306-757-0111',NULL,'1546 Rupert Street',' Regina',' SK','S4N',NULL,50.454282,-104.566702,NULL,NULL,NULL,'Home',NULL),(58,'Lubna Aamir',NULL,'306-550-4577',NULL,'468 Edward Street',' Regina',' SK','S4R',NULL,50.471232,-104.642736,NULL,NULL,NULL,'Home',NULL),(59,'YMCA Albert Street Childcare Centre',NULL,'306-757-9622',NULL,'3801 Albert Street',' Regina',' SK','S4S',NULL,50.418507,-104.616890,NULL,NULL,NULL,'Centre',NULL),(60,'Maria Cecilia Melanson',NULL,'306-541-3548',NULL,'3048 25th Avenue',' Regina',' SK','S4S',NULL,50.418959,-104.625259,NULL,NULL,NULL,'Group family child care home, Extended hours',NULL),(61,'Centre Educatif Gard\'Amis',NULL,'306-525-9448',NULL,'1601 Cowan Crescent',' Regina',' SK','S4S',NULL,50.417945,-104.602988,NULL,NULL,NULL,'Centre, Francophone',NULL),(62,'Farzana Siddiqui',NULL,'306-585-1966',NULL,'1433 Uhrich Avenue',' Regina',' SK','S4S',NULL,50.412512,-104.602851,NULL,NULL,NULL,'Home, Group family child care home, 24 hours',NULL),(63,'Kaylee Stevenson',NULL,'306-717-6797',NULL,'3516 King Street',' Regina',' SK','S4S',NULL,50.421970,-104.638473,NULL,NULL,NULL,'Home',NULL),(64,'Sharlene Nomura',NULL,'306-757-8251',NULL,'1541 Regent Street',' Regina',' SK','S4N',NULL,50.454371,-104.564700,NULL,NULL,NULL,'Home',NULL),(65,'Montessori School of Regina, Inc. (South Location)',NULL,'306-522-1500',NULL,'3515 Pasqua Street',' Regina',' SK','S4S',NULL,50.423438,-104.640374,NULL,NULL,NULL,'Centre',NULL),(66,'Saima Babir',NULL,'306-580-6303',NULL,'2 Sheppard Street',' Regina',' SK','S4R',NULL,50.479512,-104.623827,NULL,NULL,NULL,'Group family child care home',NULL),(67,'Dai Vu',NULL,'306-999-1992',NULL,'1628 Oxford Street',' Regina',' SK','S4N',NULL,50.452899,-104.560948,NULL,NULL,NULL,'Home',NULL),(68,'Toni-Lynn Vanin',NULL,'306-737-1063',NULL,'1352 Grosvenor Street',' Regina',' SK','S4N',NULL,50.457132,-104.562441,NULL,NULL,NULL,'Home, 24 hours',NULL),(69,'pamināwasowin',NULL,'306-790-5950,',NULL,'1 First Nations Way',' Regina',' SK','S4S',NULL,50.419200,-104.580830,NULL,NULL,NULL,'Centre',NULL),(70,'Awasis Childcare Co-operative',NULL,'306-585-5322',NULL,'3737 Wascana Parkway',' Regina',' SK','S4S',NULL,50.418782,-104.592093,NULL,NULL,NULL,'Centre',NULL),(71,'Wascana Day Care Co-operative',NULL,'306-585-5311',NULL,'3737 Wascana Parkway',' Regina',' SK','S4S',NULL,50.418782,-104.592093,NULL,NULL,NULL,'Centre',NULL),(72,'Shazia Tahir',NULL,'306-807-1904',NULL,'94 Munroe Place',' Regina',' SK','S4S',NULL,50.414477,-104.601098,NULL,NULL,NULL,'Group family child care home',NULL),(73,'Lorna Kelln',NULL,'306-525-3381',NULL,'17 Halleran Crescent',' Regina',' SK','S4R',NULL,50.479556,-104.633693,NULL,NULL,NULL,'Home, Extended hours',NULL),(74,'Farzana Naznin',NULL,'306-205-8723',NULL,'94 McMurchy Avenue',' Regina',' SK','S4R',NULL,50.482319,-104.625958,NULL,NULL,NULL,'Group family child care home',NULL),(75,'Ducky Day Care Centre Co-operative',NULL,'306-543-1765',NULL,'97 McMurchy Avenue',' Regina',' SK','S4R',NULL,50.481799,-104.626086,NULL,NULL,NULL,'Centre',NULL),(76,'Chris Isaac',NULL,'306-924-2074',NULL,'5315 McKinley Avenue',' Regina',' SK','S4T',NULL,50.468588,-104.656684,NULL,NULL,NULL,'Home',NULL),(77,'Ehrlo Early Learning Centre, Gladys McDonald',NULL,'306-751-4500',NULL,'335 Garnet Street North',' Regina',' SK','S4R',NULL,50.481313,-104.626335,NULL,NULL,NULL,'Centre',NULL),(78,'Glencairn Child Care Co-op',NULL,'306-789-9677',NULL,'88B Cavendish Street',' Regina',' SK','S4N',NULL,50.453830,-104.558278,NULL,NULL,NULL,'Centre',NULL),(79,'Michel Graham',NULL,'306-533-8237',NULL,'1223 8th Avenue North',' Regina',' SK','S4R',NULL,50.483359,-104.598754,NULL,NULL,NULL,'Home, Group family child care home',NULL),(80,'Denise Bailas',NULL,'306-545-0790',NULL,'1106 – 8th Avenue North',' Regina',' SK','S4R',NULL,50.478874,-104.606515,NULL,NULL,NULL,'Home, Group family child care home',NULL),(81,'Montessori School of Regina, Inc. (East Location)',NULL,'306-751-0093',NULL,'101 Mayfield Road',' Regina',' SK','S4V',NULL,50.429582,-104.562412,NULL,NULL,NULL,'Centre',NULL),(82,'Uzma Saifullah',NULL,'306-580-0850',NULL,'4300 Acadia Drive',' Regina',' SK','S4S',NULL,50.411635,-104.603654,NULL,NULL,NULL,'Home',NULL),(83,'YMCA South Child Care Centre Massey',NULL,'306-584-8823',NULL,'131 Massey Road',' Regina',' SK','S4S',NULL,50.411382,-104.608325,NULL,NULL,NULL,'Centre',NULL),(84,'Beverly Wason',NULL,'306-569-0445',NULL,'46 Stapleford Crescent',' Regina',' SK','S4R',NULL,50.478706,-104.647435,NULL,NULL,NULL,'Home',NULL),(85,'Nataliya Fedechko',NULL,'306-552-8550',NULL,'74 Sommerfeld Drive',' Regina',' SK','S4V',NULL,50.427504,-104.563025,NULL,NULL,NULL,'Home, Group family child care home',NULL),(86,'Kayla Nelson',NULL,'306-550-3233',NULL,'4231 Castle Road',' Regina',' SK','S4S',NULL,50.410801,-104.600182,NULL,NULL,NULL,'Home',NULL),(87,'Ehrlo Early Learning Centre, Wilfrid Walker',NULL,'306-751-4506',NULL,'2102 Wagman Drive East',' Regina',' SK','S4V',NULL,50.440252,-104.553060,NULL,NULL,NULL,'Centre',NULL),(88,'Gardiner Park Child Care Association',NULL,'306-789-7333',NULL,'380 Gardiner Park Court',' Regina',' SK','S4V',NULL,50.435578,-104.554620,NULL,NULL,NULL,'Centre',NULL),(89,'Cindy Emery',NULL,'306-789-9175',NULL,'2206 Dewdney Avenue East',' Regina',' SK','S4N',NULL,50.455300,-104.552295,NULL,NULL,NULL,'Home, Extended hours',NULL),(90,'Elfie Nkongolo',NULL,'306-559-4094',NULL,'4127 Pasqua Street',' Regina',' SK','S4S',NULL,50.412947,-104.640636,NULL,NULL,NULL,'Group family child care home',NULL),(91,'Sabrina Sabourin',NULL,'306-737-7032',NULL,'2211 Wagman Drive East',' Regina',' SK','S4V',NULL,50.438392,-104.551769,NULL,NULL,NULL,'Group family child care home',NULL),(92,'Purti Soni',NULL,'306-550-1338',NULL,'23 Sunset Drive',' Regina',' SK','S4S',NULL,50.408576,-104.622632,NULL,NULL,NULL,'Group family child care home',NULL),(93,'Frehiwet Asfaha',NULL,'306-219-2119',NULL,'2220 7th Avenue East',' Regina',' SK','S4N',NULL,50.458521,-104.551684,NULL,NULL,NULL,'Group family child care home',NULL),(94,'Laxmi Ramanathan',NULL,'306-515-2310',NULL,'69 Krauss Street',' Regina',' SK','S4T',NULL,50.463892,-104.670852,NULL,NULL,NULL,'Group family child care home',NULL),(95,'Nazia Mir',NULL,'306-205-1070',NULL,'115 Scrivener Crescent',' Regina',' SK','S4N',NULL,50.459198,-104.551229,NULL,NULL,NULL,'Home, Group family child care home',NULL),(96,'Bilal Syed',NULL,'306-737-7756',NULL,'8 Dolphin Bay',' Regina',' SK','S4S',NULL,50.407400,-104.609306,NULL,NULL,NULL,'Group family child care home',NULL),(97,'Melanie Martin',NULL,'306-546-2554',NULL,'126 Salemka Crescent',' Regina',' SK','S4R',NULL,50.487548,-104.631243,NULL,NULL,NULL,'Home',NULL),(98,'Rafiqun Nisa',NULL,'306-205-4869',NULL,'4663 Curtiss Avenue',' Regina',' SK','S4W',NULL,50.413417,-104.647974,NULL,NULL,NULL,'Home',NULL),(99,'Jahanzeb Naz Jamil',NULL,'306-999-1999',NULL,'4667 Curtiss Avenue',' Regina',' SK','S4W',NULL,50.413474,-104.648178,NULL,NULL,NULL,'Home',NULL),(100,'Maurvi Bhatt',NULL,'306-351-3091',NULL,'4812 Wright Road',' Regina',' SK','S4W',NULL,50.413625,-104.650813,NULL,NULL,NULL,'Group family child care home',NULL),(101,'Samantha Irvine',NULL,'306-529-9396',NULL,'34 Hodges Crescent',' Regina',' SK','S4N',NULL,50.452758,-104.546638,NULL,NULL,NULL,'Home',NULL),(102,'Majbeen Khawar',NULL,'639-571-4489',NULL,'4820 Wright Road',' Regina',' SK','S4W',NULL,50.413464,-104.651129,NULL,NULL,NULL,'Home, Group family child care home',NULL),(103,'Lee Ann Tymo',NULL,'306-535-7585',NULL,'7 Woodsworth Crescent',' Regina',' SK','S4T',NULL,50.473819,-104.666251,NULL,NULL,NULL,'Home',NULL),(104,'Geraldine Natacha Ramsamy-Louise',NULL,'306-501-7080',NULL,'5081 Snowbirds Crescent',' Regina',' SK','S4W',NULL,50.414317,-104.654143,NULL,NULL,NULL,'Francophone, Group family child care home',NULL),(105,'Harbour Landing Village Child Care Centre',NULL,'306-559-5545',NULL,'4000 James Hill Road',' Regina',' SK','S4W',NULL,50.414444,-104.660051,NULL,NULL,NULL,'Centre',NULL),(106,'Umme Abiha',NULL,'306-201-7259',NULL,'2406 Crowe Street East',' Regina',' SK','S4V',NULL,50.434580,-104.548605,NULL,NULL,NULL,'Accepts infants 6 weeks - 18 months',NULL),(107,'Amanda McCall',NULL,'306-531-7062',NULL,'71 Sibbald Crescent',' Regina',' SK','S4T',NULL,50.466130,-104.675014,NULL,NULL,NULL,'Extended hours, Home',NULL),(108,'Cynthia Kalina',NULL,'306-209-4489',NULL,'99 Lockwood Road',' Regina',' SK','S4S',NULL,50.405409,-104.625773,NULL,NULL,NULL,'Group family child care home',NULL),(109,'Viktoriia Akulova',NULL,'306-450-9012',NULL,'150 Bentley Drive',' Regina',' SK','S4N',NULL,50.454649,-104.545167,NULL,NULL,NULL,'Group family child care home',NULL),(110,'Arpna Kumari',NULL,'306-550-5236',NULL,'903 Broad Street North',' Regina',' SK','S4R',NULL,50.491470,-104.605900,NULL,NULL,NULL,'Group family child care home',NULL),(111,'Khady Bodian',NULL,'306-585-1929',NULL,'3328 Grant Road',' Regina',' SK','S4S',NULL,50.408396,-104.597357,NULL,NULL,NULL,'Home, Group family child care home, Francophone',NULL),(112,'Hardeep Lehal',NULL,'306-999-1799',NULL,'67 Bothwell Crescent',' Regina',' SK','S4R',NULL,50.491819,-104.599397,NULL,NULL,NULL,'Group family child care home',NULL),(113,'Sonamben Desai',NULL,'306-560-0192',NULL,'3712 Gordon Road',' Regina',' SK','S4S',NULL,50.405739,-104.634479,NULL,NULL,NULL,'Group family child care home',NULL),(114,'Play & Discover Early Learning Centre Inc.',NULL,'306-775-7916',NULL,'4500 Wascana Parkway',' Box 556',' Regina','SK',NULL,50.407965,-104.581254,NULL,NULL,NULL,'Centre',NULL),(115,'Musarrat Afza',NULL,'306-206-0863',NULL,'5110 Canuck Crescent',' Regina',' SK','S4W',NULL,50.416657,-104.653632,NULL,NULL,NULL,'Group family child care home',NULL),(116,'Sauvine Deugouelieu Ngueptchouang',NULL,'306-450-6514',NULL,'2926 Partridge Crescent',' Regina',' SK','S4R',NULL,50.492452,-104.623871,NULL,NULL,NULL,'Group family child care home',NULL),(117,'Bright Beginnings Early Childhood Centre-Argyle',NULL,'306-543-3220',NULL,'280 Sangster Blvd.',' Regina',' SK','S4R',NULL,50.490996,-104.631950,NULL,NULL,NULL,'Centre',NULL),(118,'Kidzone Child Care',NULL,'306-586-5505',NULL,'93 Lincoln Drive',' Regina',' SK','S4S',NULL,50.402433,-104.631882,NULL,NULL,NULL,'Centre',NULL),(119,'Prairie Lily Early Learning Centre, Ruth M. Buck',NULL,'306-949-6684',NULL,'6330 – 7th Avenue North',' Regina',' SK','S4T',NULL,50.476403,-104.670969,NULL,NULL,NULL,'Centre',NULL),(120,'Thi (Hien) Dinh',NULL,'306-999-1990',NULL,'1247 James Crescent',' Regina',' SK','S4N',NULL,50.460173,-104.542501,NULL,NULL,NULL,'Group family child care home',NULL),(121,'Jessie Knibbs',NULL,'306-531-2972',NULL,'137 Dalgliesh Drive',' Regina',' SK','S4R',NULL,50.485584,-104.655000,NULL,NULL,NULL,'Group family child care home',NULL),(122,'Nicole Funke',NULL,'306-539-6197',NULL,'179-A Wells Street',' Regina',' SK','S4R',NULL,50.489067,-104.646410,NULL,NULL,NULL,'Group family child care home',NULL),(123,'Sarabjit Kaur',NULL,'306-737-7083',NULL,'2 Bannister Bay',' Regina',' SK','S4R',NULL,50.487088,-104.652971,NULL,NULL,NULL,'Group family child care home',NULL),(124,'Jade Kampman',NULL,'306-551-1464',NULL,'2330 Hanover Crescent',' Regina',' SK','S4V',NULL,50.424231,-104.549671,NULL,NULL,NULL,'Home',NULL),(125,'Iffat Tahira',NULL,'306-737-3249',NULL,'3007 Phaneuf Crescent',' Regina',' SK','S4V',NULL,50.440042,-104.539973,NULL,NULL,NULL,'Group family child care home',NULL),(126,'Anastasie Mbuyi-Tshiasuma',NULL,'306-586-8459',NULL,'95 Plainsview Drive',' Regina',' SK','S4S',NULL,50.399645,-104.619388,NULL,NULL,NULL,'Francophone, Group family child care home, Home',NULL),(127,'Whitmore Park Child Care Co-op',NULL,'306-586-7532',NULL,'15 Birchwood Road',' Regina',' SK','S4S',NULL,50.400463,-104.604139,NULL,NULL,NULL,'Centre',NULL),(128,'Crystal Gordon',NULL,'306-515-1924',NULL,'5641 Cederholm Avenue',' Regina',' SK','S4W',NULL,50.413080,-104.662150,NULL,NULL,NULL,'Home',NULL),(129,'Saima Adeel',NULL,'613-709-5403',NULL,'1179 Ferguson Crescent',' Regina',' SK','S4N',NULL,50.460256,-104.540905,NULL,NULL,NULL,'Group family child care home',NULL),(130,'Anna Siudut',NULL,'306-351-1377',NULL,'6131 7th Avenue North',' Regina',' SK','S4T',NULL,50.478753,-104.669290,NULL,NULL,NULL,'Home',NULL),(131,'Jennifer Evanochko',NULL,'306-529-2646',NULL,'1155 Ferguson Crescent',' Regina',' SK','S4N',NULL,50.460367,-104.539769,NULL,NULL,NULL,'Home',NULL),(132,'Dianelis Mesa Tejera',NULL,'306-990-0550',NULL,'2343 Riverbend Crescent',' Regina',' SK','S4V',NULL,50.441071,-104.537990,NULL,NULL,NULL,'Home',NULL),(133,'Ehrlo Early Learning Centre, Ruth Pawson',NULL,'306-751-4504',NULL,'40 Weekes Crescent',' Regina',' SK','S4R',NULL,50.495523,-104.604946,NULL,NULL,NULL,'Centre',NULL),(134,'Prairie Lily Early Learning Centre, Normanview',NULL,'306-949-6684',NULL,'78 Dempsey Avenue',' Regina',' SK','S4T',NULL,50.476160,-104.673728,NULL,NULL,NULL,'Centre',NULL),(135,'Nadia Tahir',NULL,'306-580-8311',NULL,'3106 Dewdney Avenue East',' Regina',' SK','S4N',NULL,50.455340,-104.538384,NULL,NULL,NULL,'Group family child care home',NULL),(136,'Aqeel Siddiqui',NULL,'306-206-0744',NULL,'146 Fuhrmann Crescent',' Regina',' SK','S4R',NULL,50.486284,-104.658087,NULL,NULL,NULL,'Group family child care home',NULL),(137,'Ehrlo Early Learning Centre, W.F. Ready',NULL,'306-751-2722',NULL,'2710 Helmsing Street',' Regina',' SK','S4V',NULL,50.437251,-104.539776,NULL,NULL,NULL,'Centre',NULL),(138,'Shumaila Saeed',NULL,'647-648-5256',NULL,'2601 Narcisse Drive',' Regina',' SK','S4X',NULL,50.495207,-104.620833,NULL,NULL,NULL,'Group family child care home',NULL),(139,'Shazia Mumtaz',NULL,'306-775-1786',NULL,'1114 Jurasin Street North',' Regina',' SK','S4X',NULL,50.495492,-104.627143,NULL,NULL,NULL,'24 hours, Group family child care home',NULL),(140,'Archana Geethakumari',NULL,'306-515-3876',NULL,'8 French Crescent',' Regina',' SK','S4R',NULL,50.492304,-104.647895,NULL,NULL,NULL,'Group family child care home',NULL),(141,'Mariya Elias',NULL,'306-581-7938',NULL,'432 Dalgliesh Drive',' Regina',' SK','S4R',NULL,50.491021,-104.652488,NULL,NULL,NULL,'Home',NULL),(142,'YMCA Harbour Landing Child Care Centre',NULL,'306-585-3160',NULL,'4417 James Hill Road',' Regina',' SK','S4W',NULL,50.407655,-104.659077,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(143,'Shannon Grumbly',NULL,'306-347-8231',NULL,'178 Rodenbush Drive',' Regina',' SK','S4R',NULL,50.498072,-104.601989,NULL,NULL,NULL,'Home',NULL),(144,'Chelsea Gottfried',NULL,'306-541-3190',NULL,'3159 Zech Place',' Regina',' SK','S4V',NULL,50.428514,-104.539815,NULL,NULL,NULL,'Home',NULL),(145,'Seema Rani',NULL,'306-519-1159',NULL,'3162 Mazurak Crescent',' Regina',' SK','S4X',NULL,50.498548,-104.626338,NULL,NULL,NULL,'Home',NULL),(146,'Natalya Tatchuk',NULL,'306-537-3883',NULL,'935 Dutkowski Crescent',' Regina',' SK','S4N',NULL,50.463319,-104.536080,NULL,NULL,NULL,'Group family child care home',NULL),(147,'Fatema Khirun Nesa',NULL,'306-450-4978',NULL,'3126 Mazurak Crescent',' Regina',' SK','S4X',NULL,50.498643,-104.625278,NULL,NULL,NULL,'Accepts infants 6 weeks - 18 months',NULL),(148,'Syeda Mustafa',NULL,'306-580-4940',NULL,'5421 Gordon Road',' Regina',' SK','S4W',NULL,50.405054,-104.658543,NULL,NULL,NULL,'Home',NULL),(149,'Oleksii Akulov',NULL,'306-450-8330',NULL,'3011 Hayden Park Road',' Regina',' SK','S4V',NULL,50.432123,-104.534545,NULL,NULL,NULL,'Home',NULL),(150,'Samina Mansoor',NULL,'639-997-6490',NULL,'2455 Broderick Bay',' Regina',' SK','S4V',NULL,50.440326,-104.531535,NULL,NULL,NULL,'Group family child care home',NULL),(151,'Hina Nadeem',NULL,'306-737-1939',NULL,'4530 Delhaye Way',' Regina',' SK','S4W',NULL,50.406236,-104.663435,NULL,NULL,NULL,'Group family child care home',NULL),(152,'Prairie Grown Early Learning Centre Inc',NULL,'306-775-5050',NULL,'3125 Woodham Drive',' Regina',' SK','S4V',NULL,50.428434,-104.536802,NULL,NULL,NULL,'Centre',NULL),(153,'Shabnam Rizwan',NULL,'306-205-3999',NULL,'314 Dalgliesh Drive',' Regina',' SK','S4R',NULL,50.490986,-104.660038,NULL,NULL,NULL,'Group family child care home',NULL),(154,'Janyne Foster',NULL,'306-550-1449',NULL,'3611 Hammstrom Way East',' Regina',' SK','S4N',NULL,50.458973,-104.531443,NULL,NULL,NULL,'Home, Group family child care home',NULL),(155,'Ayesha Nadeem',NULL,'306-546-2624',NULL,'4650 Padwick Crescent',' Regina',' SK','S4W',NULL,50.400034,-104.648168,NULL,NULL,NULL,'Group family child care home',NULL),(156,'Bishnu Poudel',NULL,'306-450-7236',NULL,'5388 Aerial Crescent',' Regina',' SK','S4W',NULL,50.402698,-104.656322,NULL,NULL,NULL,'Group family child care home',NULL),(157,'Nicole LaRose',NULL,'306-789-9610',NULL,'1335 Chatwin Crescent',' Regina',' SK','S4N',NULL,50.457085,-104.528225,NULL,NULL,NULL,'Group family child care home',NULL),(158,'Rink Avenue Daycare Co-operative',NULL,'306-545-7055',NULL,'587 Rink Avenue',' Regina',' SK','S4X',NULL,50.487479,-104.675069,NULL,NULL,NULL,'Centre',NULL),(159,'Memuna Aggrey',NULL,'306-761-0989',NULL,'3722 Cormorant Drive',' Regina',' SK','S4N',NULL,50.465697,-104.528275,NULL,NULL,NULL,'Home',NULL),(160,'Deanna Morin',NULL,'306-545-9521',NULL,'348 Prairie View Drive',' Regina',' SK','S4Y',NULL,50.474076,-104.691067,NULL,NULL,NULL,'Home',NULL),(161,'Mobina Zahid',NULL,'306-949-9435',NULL,'2406 Jameson Crescent',' Regina',' SK','S4V',NULL,50.439145,-104.524691,NULL,NULL,NULL,'Group family child care home',NULL),(162,'Galina Horovitc',NULL,'306-205-8462',NULL,'6339 Leger Bay',' Regina',' SK','S4X',NULL,50.490800,-104.673211,NULL,NULL,NULL,'Group family child care home',NULL),(163,'Maricel Fabian',NULL,'306-717-8851',NULL,'5622 Beacon Place',' Regina',' SK','S4W',NULL,50.398883,-104.661779,NULL,NULL,NULL,'Home',NULL),(164,'Dhivya Rajkumar',NULL,'306-201-8045',NULL,'5612 Gilbert Crescent',' Regina',' SK','S4W',NULL,50.397934,-104.660987,NULL,NULL,NULL,'Accepts infants 6 weeks - 18 months',NULL),(165,'Xiuhua Zhou',NULL,'306-596-9988',NULL,'6146 Wascana Court',' Regina',' SK','S4V',NULL,50.414951,-104.533150,NULL,NULL,NULL,'Group family child care home',NULL),(166,'Galina Tsozik',NULL,'306-543-2303',NULL,'1354 Hahn Crescent',' Regina',' SK','S4X',NULL,50.500134,-104.657005,NULL,NULL,NULL,'Home, Group family child care home',NULL),(167,'YMCA North West Child Care Centre',NULL,'306-757-9622',NULL,'5939 Rochdale Blvd.',' Regina',' SK','S4X',NULL,50.494875,-104.667891,NULL,NULL,NULL,'Centre, Accepts infants 6 weeks - 18 months',NULL),(168,'YMCA Rochdale Child Care Centre',NULL,'306-757-9622',NULL,'5939 Rochdale Blvd.',' Regina',' SK','S4X',NULL,50.494875,-104.667891,NULL,NULL,NULL,'Centre',NULL),(169,'Sonia Fagan',NULL,'306-533-0413',NULL,'1014 Mawson Bay',' Regina',' SK','S4X',NULL,50.493132,-104.677088,NULL,NULL,NULL,'Home',NULL),(170,'Cristina Cruz',NULL,'306-209-1738',NULL,'3347 Green Bank Road',' Regina',' SK','S4V',NULL,50.422583,-104.519662,NULL,NULL,NULL,'Home, Group family child care home, 24 hours',NULL),(171,'Alia Imran',NULL,'306-510-3751',NULL,'3146 Green Bank Road',' Regina',' SK','S4V',NULL,50.426507,-104.523926,NULL,NULL,NULL,'Home',NULL),(172,'Rowena Betoro',NULL,'306-201-9843',NULL,'3142 Green Bank Road',' Regina',' SK','S4V',NULL,50.426637,-104.523878,NULL,NULL,NULL,'Home',NULL),(173,'Milian Lamichhane',NULL,'306-351-5515',NULL,'7070 Wascana Cove Drive',' Regina',' SK','S4V',NULL,50.417333,-104.528231,NULL,NULL,NULL,'Group family child care home',NULL),(174,'Maria Rahim',NULL,'306-541-3176',NULL,'3259 Valley Green Way',' Regina',' SK','S4V',NULL,50.426673,-104.522622,NULL,NULL,NULL,'Group family child care home',NULL),(175,'Shagufta Iftikhar',NULL,'306-584-9810',NULL,'3637 Green Cedar Court',' Regina',' SK','S4V',NULL,50.422376,-104.523232,NULL,NULL,NULL,'Home, Group family child care home',NULL),(176,'Galina Krumer',NULL,'306-529-3390',NULL,'1587 Lakeridge Drive',' Regina',' SK','S4X',NULL,50.503797,-104.658948,NULL,NULL,NULL,'Home, Group family child care home',NULL),(177,'Krystal Langford',NULL,'639-915-0503',NULL,'6935 Farrell Bay',' Regina',' SK','S4X',NULL,50.496211,-104.680136,NULL,NULL,NULL,'Home, Group family child care home',NULL),(178,'Raldaline Barabar',NULL,'306-519-4838',NULL,'4241 E Green Olive Way',' Regina',' SK','S4V',NULL,50.418768,-104.520237,NULL,NULL,NULL,'Home, Group family child care home',NULL),(179,'First Years Learning Centre Inc. - Greens',NULL,'306-359-7170',NULL,'5133 E Green Brooks Way',' Regina',' SK','S4V',NULL,50.424239,-104.510444,NULL,NULL,NULL,'Centre',NULL),(180,'Ravi Atwal',NULL,'306-450-2671',NULL,'3346 Chuka Boulevard',' Regina',' SK','S4V',NULL,50.425250,-104.512832,NULL,NULL,NULL,'Home',NULL),(181,'Park Play Early Learning Centre',NULL,'306-910-1414',NULL,'7451 Mapleford Blvd.',' Regina',' SK','S4Y',NULL,50.500788,-104.688184,NULL,NULL,NULL,'Centre',NULL),(182,'Khola Sajjad Syeda',NULL,'306-581-8586',NULL,'5404 Green Apple Drive',' Regina',' SK','S4V',NULL,50.421279,-104.505115,NULL,NULL,NULL,'Group family child care home',NULL),(183,'Hope\'s Home Rosewood',NULL,'306-522-1516',NULL,'7695 Mapleford Boulevard',' Regina',' SK','S4Y',NULL,50.500780,-104.691039,NULL,NULL,NULL,'Centre',NULL);
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
  `name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `email` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `phone_no` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `join_date` date DEFAULT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `street` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `city` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `province` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `postal_code` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `country` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
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

-- Dump completed on 2023-03-31 11:25:38
