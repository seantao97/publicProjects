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
-- Table structure for table `storyv1`
--

DROP TABLE IF EXISTS `storyv1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storyv1` (
  `storyID` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `text` text NOT NULL,
  `user` varchar(50) DEFAULT NULL,
  `dateWritten` datetime NOT NULL,
  `dateConcluded` datetime DEFAULT NULL,
  `concluded` varchar(5) DEFAULT NULL,
  `likes` int(11) DEFAULT NULL,
  `spam` int(11) DEFAULT NULL,
  `userComment` text,
  `yes` int(11) DEFAULT NULL,
  `no` int(11) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`storyID`),
  UNIQUE KEY `storyID_UNIQUE` (`storyID`),
  KEY `user_storyFK_idx` (`user`),
  CONSTRAINT `user_storyFK` FOREIGN KEY (`user`) REFERENCES `usersv1` (`username`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storyv1`
--

LOCK TABLES `storyv1` WRITE;
/*!40000 ALTER TABLE `storyv1` DISABLE KEYS */;
INSERT INTO `storyv1` VALUES (13,'story13 title','some text','seantao','2016-07-22 22:43:01','2016-07-22 22:43:01','s',2,1,'story13 ending',0,0,NULL),(14,'story14 title','lol more text 14','seantao','2016-07-18 19:27:24',NULL,'s',2,1,'story14 ending',1,0,NULL),(15,'story15title','more text 15','seantao','2016-07-19 03:36:48',NULL,'s',1,0,'story 15 ending',0,1,NULL);
/*!40000 ALTER TABLE `storyv1` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-24  2:47:03
