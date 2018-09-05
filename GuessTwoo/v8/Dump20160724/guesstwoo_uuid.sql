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
-- Table structure for table `uuid`
--

DROP TABLE IF EXISTS `uuid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uuid` (
  `uuid` varchar(36) NOT NULL,
  `dateCreated` datetime NOT NULL,
  `dateExpires` datetime NOT NULL,
  `expired` varchar(1) NOT NULL DEFAULT 'n',
  `used` varchar(1) NOT NULL DEFAULT 'n',
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uuid`
--

LOCK TABLES `uuid` WRITE;
/*!40000 ALTER TABLE `uuid` DISABLE KEYS */;
INSERT INTO `uuid` VALUES ('0b0f656f-3ebc-410e-b304-24f7ad23e890','2016-07-24 01:32:56','2016-07-25 01:32:56','y','y','2','$2a$10$aCw6ccUfruL/0g4tD.ggaeH3ynzXyWJnI4aYIH2A0GVDY1dIPW.va','seantaoalt@gmail.com'),('1712ed63-3609-426d-b900-463f4bebccac','2016-07-18 03:09:22','2016-07-19 03:09:22','y','y','seantao','$2a$10$sShmFP0GvpcvtTV17EIiMuu7yaD2mnREmIlvZg7/KN6KO/sBTeova','seantao97@gmail.com'),('40d4e69f-5303-4ab7-9d4a-30111383d035','2016-07-18 00:39:54','2016-07-19 00:39:54','n','n','seantao','$2a$10$Zq1sspdgqQG0RA50rJpsKeVYQ6DZaEnRJEL4eTbjrpuE0EgFIRqYG','seantao97@gmail.com'),('9fb78b51-c83d-4a2a-8ef3-d626c568487d','2016-07-18 03:02:48','2016-07-19 03:02:48','y','y','seantao','$2a$10$PcQ/RsCVuZxpDR7x5Isevu.JByTm/MM6OPqRcFjwpVKvdrhC1y4n.','seantao97@gmail.com'),('a63f5084-e688-4412-9e1f-4c3a758d6411','2016-07-18 00:37:40','2016-07-19 00:37:40','n','n','seantao','$2a$10$P8jdmaR5oPpYv92pUI.tx.12JO6p9vOfAQl0FSOFrIeMwS4Ua7vui','seantao97@gmail.com'),('e2718928-84d2-4660-a711-d99649281810','2016-07-14 19:34:40','2016-07-15 19:34:40','y','y','seantao','$2a$10$EscxcuCLV3loq7VZ0hKBTezg/oeJxfgAal1T/A8zju8C9xAYm7vae','seantao97@gmail.com'),('ed3e72c3-c2d1-4a5e-affb-e69eaca660e3','2016-07-18 00:40:12','2016-07-19 00:40:12','n','n','seantao','$2a$10$2OWoTyUXTCWgonTYt6fN3.kWVUMCbKp.X3I84aSKtzompLhML7nli','seantao97@gmail.com');
/*!40000 ALTER TABLE `uuid` ENABLE KEYS */;
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
