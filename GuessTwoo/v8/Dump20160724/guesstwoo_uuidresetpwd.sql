-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: guesstwoo
-- ------------------------------------------------------
-- Server version	5.7.10-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `uuidresetpwd`
--

DROP TABLE IF EXISTS `uuidresetpwd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uuidresetpwd` (
  `uuid` varchar(36) NOT NULL,
  `email` varchar(50) NOT NULL,
  `newPwd` varchar(100) NOT NULL,
  `dateCreated` datetime NOT NULL,
  `dateExpires` datetime NOT NULL,
  `expired` varchar(1) NOT NULL DEFAULT 'n',
  `used` varchar(1) DEFAULT 'n',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uuidresetpwd`
--

LOCK TABLES `uuidresetpwd` WRITE;
/*!40000 ALTER TABLE `uuidresetpwd` DISABLE KEYS */;
INSERT INTO `uuidresetpwd` VALUES ('62783e6e-a001-43e1-ab35-fdbf6fffca62','seantao97@gmail.com','$2a$10$/Jb7iifEpjdRO/3siG0jaeHg1GOpFLYNmH8g9rON6U8oCrqbu1uvW','2016-07-19 03:37:36','2016-07-20 03:37:36','n','n'),('b94af297-b5fd-410e-a8f3-44fa7af348e8','seantao97@gmail.com','$2a$10$YdXHfIpXzCD6vbBUn2d/UuYP01DKmRKAlBEsOq2gIcW4iwBeq4rFy','2016-07-19 03:59:28','2016-07-20 03:59:28','y','y'),('dac34656-e3db-4088-a800-0bee5af16e07','seantao97@gmail.com','$2a$10$QVf7MdUyraeboocwNTqb.ODVKqkGSWLmdyAA3Y9vnvMkv7p4DFbyO','2016-07-19 03:59:24','2016-07-20 03:59:24','y','y');
/*!40000 ALTER TABLE `uuidresetpwd` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-24  2:47:01
