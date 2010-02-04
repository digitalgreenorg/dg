-- MySQL dump 10.11
--
-- Host: localhost    Database: digitalgreen
-- ------------------------------------------------------
-- Server version	5.0.51a-3ubuntu5.4

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
-- Table structure for table `ANIMATOR`
--

DROP TABLE IF EXISTS `ANIMATOR`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `ANIMATOR` (
  `id` int(11) NOT NULL auto_increment,
  `NAME` varchar(100) NOT NULL,
  `AGE` int(11) default NULL,
  `GENDER` varchar(1) NOT NULL,
  `CSP_FLAG` tinyint(1) default NULL,
  `CAMERA_OPERATOR_FLAG` tinyint(1) default NULL,
  `FACILITATOR_FLAG` tinyint(1) default NULL,
  `PHONE_NO` varchar(100) NOT NULL,
  `ADDRESS` varchar(500) NOT NULL,
  `partner_id` int(11) NOT NULL,
  `home_village_id` int(11) NOT NULL,
  `equipmentholder_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `ANIMATOR_partner_id` (`partner_id`),
  KEY `ANIMATOR_home_village_id` (`home_village_id`),
  KEY `ANIMATOR_equipmentholder_id` (`equipmentholder_id`)
) ENGINE=MyISAM AUTO_INCREMENT=80 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `ANIMATOR`
--

LOCK TABLES `ANIMATOR` WRITE;
/*!40000 ALTER TABLE `ANIMATOR` DISABLE KEYS */;
INSERT INTO `ANIMATOR` VALUES (34,'Salim',NULL,'M',NULL,1,NULL,'','',1,25,NULL),(33,'Shyam',38,'M',1,0,0,'','Navatoli, Torpa',1,24,NULL),(58,'Bihar Singh',29,'M',0,1,1,'09938314839','Kendumudhi,Orissa',1,70,NULL),(55,'Kalappa Badiger',30,'M',NULL,NULL,1,'','',2,50,NULL),(35,'Sameer',21,'M',1,0,0,'','',1,27,NULL),(43,'Ramlal Alawa',21,'M',1,1,NULL,'9770022849','Mansingpura',4,33,NULL),(44,'Jyoti',18,'F',1,1,NULL,'9669422105','SPS Neemkhada',4,34,NULL),(39,'Sameer',21,'M',1,0,0,'','',1,29,NULL),(40,'Habil',NULL,'M',0,0,1,'','',1,26,NULL),(41,'Sudeep',NULL,'M',NULL,NULL,1,'','',1,28,NULL),(42,'Asisiyan Gudia',NULL,'M',1,0,NULL,'','',1,31,NULL),(45,'Kalpna Solanki',18,'F',1,1,0,'+919302453156','',4,35,NULL),(46,'Sikdar Lahra',NULL,'M',0,0,1,'917961054','Pandutalab',4,37,NULL),(47,'Mohan Mujalde',NULL,'M',0,0,1,'','Pandutalab',4,37,NULL),(48,'Papu',NULL,'M',0,0,1,'9165368276','Pandutalab',4,37,NULL),(49,'Vandana',NULL,'F',NULL,NULL,NULL,'','',2,43,NULL),(50,'Channabasappa',NULL,'M',NULL,NULL,NULL,'','',2,45,NULL),(51,'Taramati',NULL,'F',NULL,NULL,NULL,'','',2,46,NULL),(52,'Laxmi',NULL,'F',NULL,NULL,NULL,'','',2,47,NULL),(53,'Mahadevi',NULL,'F',NULL,NULL,NULL,'','',2,48,NULL),(54,'Patil',NULL,'M',NULL,NULL,NULL,'','',2,49,NULL),(59,'Koutaki Nayak',26,'F',1,1,1,'','',1,52,NULL),(76,'Bihar Singh',32,'M',0,1,1,'09938314839','Kendumundhi',1,70,NULL),(62,'Ramakant',32,'M',1,0,0,'09178623616','',1,52,NULL),(63,'Hrushikesh Goipai',28,'M',1,1,1,'09338919118','Ektali,Orissa',1,55,NULL),(77,'Paray Pingua',NULL,'M',1,NULL,NULL,'','',1,62,NULL),(79,'Paribal',NULL,'M',1,NULL,NULL,'','',1,80,NULL),(78,'Santosh Naik',NULL,'M',1,1,0,'','',1,70,NULL),(75,'Kuni Rani Sundhi',24,'F',1,0,0,'','Chandusahi',1,69,NULL);
/*!40000 ALTER TABLE `ANIMATOR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ANIMATOR_ASSIGNED_VILLAGE`
--

DROP TABLE IF EXISTS `ANIMATOR_ASSIGNED_VILLAGE`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `ANIMATOR_ASSIGNED_VILLAGE` (
  `id` int(11) NOT NULL auto_increment,
  `animator_id` int(11) NOT NULL,
  `village_id` int(11) NOT NULL,
  `START_DATE` date default NULL,
  PRIMARY KEY  (`id`),
  KEY `ANIMATOR_ASSIGNED_VILLAGE_animator_id` (`animator_id`),
  KEY `ANIMATOR_ASSIGNED_VILLAGE_village_id` (`village_id`)
) ENGINE=MyISAM AUTO_INCREMENT=157 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `ANIMATOR_ASSIGNED_VILLAGE`
--

LOCK TABLES `ANIMATOR_ASSIGNED_VILLAGE` WRITE;
/*!40000 ALTER TABLE `ANIMATOR_ASSIGNED_VILLAGE` DISABLE KEYS */;
INSERT INTO `ANIMATOR_ASSIGNED_VILLAGE` VALUES (37,34,24,NULL),(36,34,25,NULL),(35,34,26,NULL),(126,63,75,NULL),(124,63,73,NULL),(123,63,72,NULL),(122,63,71,NULL),(121,63,62,NULL),(58,62,53,NULL),(108,58,62,NULL),(56,59,52,'2009-11-19'),(38,35,28,NULL),(104,76,62,NULL),(40,40,26,NULL),(41,41,28,NULL),(42,41,27,NULL),(43,41,29,NULL),(44,41,30,NULL),(45,34,30,NULL),(46,39,28,NULL),(47,39,27,NULL),(48,39,29,NULL),(49,47,38,NULL),(50,54,49,NULL),(51,53,48,NULL),(52,51,46,NULL),(53,50,45,NULL),(54,49,43,NULL),(55,52,47,NULL),(125,63,74,NULL),(111,58,74,NULL),(110,58,73,NULL),(109,58,72,NULL),(107,58,60,NULL),(106,58,70,NULL),(105,58,71,NULL),(115,58,67,NULL),(114,58,76,NULL),(113,58,69,NULL),(74,75,69,NULL),(75,75,67,NULL),(112,58,75,NULL),(117,58,55,NULL),(116,58,52,NULL),(103,63,58,NULL),(120,58,79,NULL),(119,58,78,NULL),(118,58,77,NULL),(141,59,69,NULL),(140,59,75,NULL),(139,59,74,NULL),(138,59,73,NULL),(137,59,72,NULL),(136,59,71,NULL),(135,59,62,NULL),(134,63,70,NULL),(133,63,79,NULL),(132,63,78,NULL),(131,63,77,NULL),(130,63,52,NULL),(129,63,67,NULL),(128,63,76,NULL),(127,63,69,NULL),(98,63,55,NULL),(99,63,57,NULL),(100,63,56,NULL),(101,63,59,NULL),(102,63,60,NULL),(142,59,76,NULL),(143,59,67,NULL),(144,59,55,NULL),(145,59,77,NULL),(146,59,78,NULL),(147,59,79,NULL),(148,59,70,NULL),(149,78,74,NULL),(150,78,72,NULL),(151,78,70,NULL),(152,79,80,NULL),(153,79,81,NULL),(154,79,82,NULL),(155,79,83,NULL),(156,79,84,NULL);
/*!40000 ALTER TABLE `ANIMATOR_ASSIGNED_VILLAGE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ANIMATOR_SALARY_PER_MONTH`
--

DROP TABLE IF EXISTS `ANIMATOR_SALARY_PER_MONTH`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `ANIMATOR_SALARY_PER_MONTH` (
  `id` int(11) NOT NULL auto_increment,
  `animator_id` int(11) NOT NULL,
  `DATE` date NOT NULL,
  `TOTAL_SALARY` double default NULL,
  `PAY_DATE` date default NULL,
  PRIMARY KEY  (`id`),
  KEY `ANIMATOR_SALARY_PER_MONTH_animator_id` (`animator_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `ANIMATOR_SALARY_PER_MONTH`
--

LOCK TABLES `ANIMATOR_SALARY_PER_MONTH` WRITE;
/*!40000 ALTER TABLE `ANIMATOR_SALARY_PER_MONTH` DISABLE KEYS */;
/*!40000 ALTER TABLE `ANIMATOR_SALARY_PER_MONTH` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `BLOCK`
--

DROP TABLE IF EXISTS `BLOCK`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `BLOCK` (
  `id` int(11) NOT NULL auto_increment,
  `BLOCK_NAME` varchar(100) NOT NULL,
  `START_DATE` date default NULL,
  `district_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `BLOCK_district_id` (`district_id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `BLOCK`
--

LOCK TABLES `BLOCK` WRITE;
/*!40000 ALTER TABLE `BLOCK` DISABLE KEYS */;
INSERT INTO `BLOCK` VALUES (1,'Samnapur',NULL,1),(2,'Saka',NULL,1),(3,'Mogaon',NULL,2),(4,'Bagli',NULL,3),(5,'Amarpur',NULL,4),(6,'Chaibasa',NULL,4),(7,'Chakradhapur',NULL,4),(8,'Hatgamaria',NULL,4),(9,'Torpa',NULL,5),(10,'Erki',NULL,5),(11,'Murhu',NULL,5),(12,'Karanjia',NULL,6),(13,'Jashipur',NULL,6),(14,'Purulia',NULL,7),(15,'Surshettikoppa',NULL,8),(16,'Kushalnagar',NULL,9),(17,'Kodugu',NULL,9),(18,'Hunsur',NULL,9),(19,'Kanakapura',NULL,10),(25,'ss koppa',NULL,8),(24,'Khunti',NULL,5),(26,'kalgattigi',NULL,8),(27,'Jashipur',NULL,14),(28,'Jashipur',NULL,15);
/*!40000 ALTER TABLE `BLOCK` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DEVELOPMENT_MANAGER`
--

DROP TABLE IF EXISTS `DEVELOPMENT_MANAGER`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `DEVELOPMENT_MANAGER` (
  `id` int(11) NOT NULL auto_increment,
  `NAME` varchar(100) NOT NULL,
  `AGE` int(11) default NULL,
  `GENDER` varchar(1) NOT NULL,
  `HIRE_DATE` date default NULL,
  `PHONE_NO` varchar(100) NOT NULL,
  `ADDRESS` varchar(500) NOT NULL,
  `SPECIALITY` longtext NOT NULL,
  `region_id` int(11) NOT NULL,
  `START_DAY` date default NULL,
  `reviewer_id` int(11) default NULL,
  `equipmentholder_id` int(11) default NULL,
  `SALARY` double default NULL,
  PRIMARY KEY  (`id`),
  KEY `DEVELOPMENT_MANAGER_region_id` (`region_id`),
  KEY `DEVELOPMENT_MANAGER_reviewer_id` (`reviewer_id`),
  KEY `DEVELOPMENT_MANAGER_equipmentholder_id` (`equipmentholder_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `DEVELOPMENT_MANAGER`
--

LOCK TABLES `DEVELOPMENT_MANAGER` WRITE;
/*!40000 ALTER TABLE `DEVELOPMENT_MANAGER` DISABLE KEYS */;
INSERT INTO `DEVELOPMENT_MANAGER` VALUES (2,'Mr. Gulzar',NULL,'M',NULL,'','','',1,NULL,NULL,NULL,NULL),(3,'Mr. Avinash',NULL,'M',NULL,'','','',2,NULL,NULL,NULL,NULL),(4,'Dr. Nadagouda',NULL,'M',NULL,'','','',3,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `DEVELOPMENT_MANAGER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DISTRICT`
--

DROP TABLE IF EXISTS `DISTRICT`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `DISTRICT` (
  `id` int(11) NOT NULL auto_increment,
  `DISTRICT_NAME` varchar(100) NOT NULL,
  `START_DATE` date default NULL,
  `state_id` int(11) NOT NULL,
  `fieldofficer_id` int(11) NOT NULL,
  `FIELDOFFICER_STARTDAY` date default NULL,
  `partner_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `DISTRICT_state_id` (`state_id`),
  KEY `DISTRICT_fieldofficer_id` (`fieldofficer_id`),
  KEY `DISTRICT_partner_id` (`partner_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `DISTRICT`
--

LOCK TABLES `DISTRICT` WRITE;
/*!40000 ALTER TABLE `DISTRICT` DISABLE KEYS */;
INSERT INTO `DISTRICT` VALUES (1,'Dindori ',NULL,1,10,NULL,1),(2,'Mandla ',NULL,1,10,NULL,1),(3,'Dewas',NULL,1,1,NULL,4),(4,'West Singhbum',NULL,2,2,NULL,1),(5,'Khunti ',NULL,2,3,NULL,1),(6,'Karanjia ',NULL,3,4,NULL,1),(7,'Purulia ',NULL,4,4,NULL,1),(8,'Dharwad ',NULL,5,5,NULL,2),(9,'Kushalnagar ',NULL,5,6,NULL,2),(10,'Bangalore Rural',NULL,5,6,NULL,3),(12,'Khunti',NULL,2,3,NULL,1),(14,'Mayurbhanj',NULL,3,4,NULL,1),(15,'Mayurbhanj',NULL,3,4,NULL,1);
/*!40000 ALTER TABLE `DISTRICT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EQUIPMENT_HOLDER`
--

DROP TABLE IF EXISTS `EQUIPMENT_HOLDER`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `EQUIPMENT_HOLDER` (
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `EQUIPMENT_HOLDER`
--

LOCK TABLES `EQUIPMENT_HOLDER` WRITE;
/*!40000 ALTER TABLE `EQUIPMENT_HOLDER` DISABLE KEYS */;
/*!40000 ALTER TABLE `EQUIPMENT_HOLDER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EQUIPMENT_ID`
--

DROP TABLE IF EXISTS `EQUIPMENT_ID`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `EQUIPMENT_ID` (
  `id` int(11) NOT NULL auto_increment,
  `EQUIPMENT_TYPE` varchar(300) NOT NULL,
  `MODEL_NO` varchar(300) NOT NULL,
  `SERIAL_NO` varchar(300) NOT NULL,
  `COST` double default NULL,
  `PROCUREMENT_DATE` date default NULL,
  `WARRANTY_EXPIRATION_DATE` date default NULL,
  `equipmentholder_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `EQUIPMENT_ID_equipmentholder_id` (`equipmentholder_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `EQUIPMENT_ID`
--

LOCK TABLES `EQUIPMENT_ID` WRITE;
/*!40000 ALTER TABLE `EQUIPMENT_ID` DISABLE KEYS */;
/*!40000 ALTER TABLE `EQUIPMENT_ID` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FIELD_OFFICER`
--

DROP TABLE IF EXISTS `FIELD_OFFICER`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `FIELD_OFFICER` (
  `id` int(11) NOT NULL auto_increment,
  `NAME` varchar(100) NOT NULL,
  `AGE` int(11) default NULL,
  `GENDER` varchar(1) NOT NULL,
  `HIRE_DATE` date default NULL,
  `SALARY` double default NULL,
  `PHONE_NO` varchar(100) NOT NULL,
  `ADDRESS` varchar(500) NOT NULL,
  `reviewer_id` int(11) default NULL,
  `equipmentholder_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `FIELD_OFFICER_reviewer_id` (`reviewer_id`),
  KEY `FIELD_OFFICER_equipmentholder_id` (`equipmentholder_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `FIELD_OFFICER`
--

LOCK TABLES `FIELD_OFFICER` WRITE;
/*!40000 ALTER TABLE `FIELD_OFFICER` DISABLE KEYS */;
INSERT INTO `FIELD_OFFICER` VALUES (1,'Kevin Gandhi',22,'M','2009-08-08',NULL,'9650924406','sps',NULL,NULL),(2,'Abhishek',NULL,'M',NULL,NULL,'','',NULL,NULL),(3,'Muthumari',NULL,'F',NULL,NULL,'','',NULL,NULL),(4,'Chandrashekhar',NULL,'M',NULL,NULL,'','',NULL,NULL),(5,'Ramachandra',NULL,'M',NULL,NULL,'','',NULL,NULL),(6,'Archana',NULL,'F',NULL,NULL,'','',NULL,NULL),(10,'Satyam Salil',NULL,'M','2009-10-05',NULL,'','',NULL,NULL);
/*!40000 ALTER TABLE `FIELD_OFFICER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LANGUAGE`
--

DROP TABLE IF EXISTS `LANGUAGE`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `LANGUAGE` (
  `id` int(11) NOT NULL auto_increment,
  `language_name` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=133 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `LANGUAGE`
--

LOCK TABLES `LANGUAGE` WRITE;
/*!40000 ALTER TABLE `LANGUAGE` DISABLE KEYS */;
INSERT INTO `LANGUAGE` VALUES (1,'Hindi'),(2,'English'),(3,'Mundari'),(4,'Sadri'),(19,'Telgu'),(132,'Santhali'),(131,''),(130,''),(129,''),(127,'kannada'),(126,'Bengali'),(125,'Oriya'),(128,'Neemardi'),(123,'Ho');
/*!40000 ALTER TABLE `LANGUAGE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MONTHLY_COST_PER_VILLAGE`
--

DROP TABLE IF EXISTS `MONTHLY_COST_PER_VILLAGE`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `MONTHLY_COST_PER_VILLAGE` (
  `id` int(11) NOT NULL auto_increment,
  `village_id` int(11) NOT NULL,
  `DATE` date NOT NULL,
  `LABOR_COST` double default NULL,
  `EQUIPMENT_COST` double default NULL,
  `TRANSPORTATION_COST` double default NULL,
  `MISCELLANEOUS_COST` double default NULL,
  `TOTAL_COST` double default NULL,
  `PARTNERS_COST` double default NULL,
  `DIGITALGREEN_COST` double default NULL,
  `COMMUNITY_COST` double default NULL,
  PRIMARY KEY  (`id`),
  KEY `MONTHLY_COST_PER_VILLAGE_village_id` (`village_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `MONTHLY_COST_PER_VILLAGE`
--

LOCK TABLES `MONTHLY_COST_PER_VILLAGE` WRITE;
/*!40000 ALTER TABLE `MONTHLY_COST_PER_VILLAGE` DISABLE KEYS */;
/*!40000 ALTER TABLE `MONTHLY_COST_PER_VILLAGE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PARTNERS`
--

DROP TABLE IF EXISTS `PARTNERS`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `PARTNERS` (
  `id` int(11) NOT NULL auto_increment,
  `PARTNER_NAME` varchar(100) NOT NULL,
  `DATE_OF_ASSOCIATION` date default NULL,
  `PHONE_NO` varchar(100) NOT NULL,
  `ADDRESS` varchar(500) NOT NULL,
  `reviewer_id` int(11) default NULL,
  `equipmentholder_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `PARTNERS_reviewer_id` (`reviewer_id`),
  KEY `PARTNERS_equipmentholder_id` (`equipmentholder_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `PARTNERS`
--

LOCK TABLES `PARTNERS` WRITE;
/*!40000 ALTER TABLE `PARTNERS` DISABLE KEYS */;
INSERT INTO `PARTNERS` VALUES (1,'PRADAN',NULL,'','',NULL,NULL),(2,'BAIF',NULL,'','',NULL,NULL),(3,'GREEN Foundation',NULL,'','',NULL,NULL),(4,'SPS',NULL,'','',NULL,NULL);
/*!40000 ALTER TABLE `PARTNERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PERSON`
--

DROP TABLE IF EXISTS `PERSON`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `PERSON` (
  `id` int(11) NOT NULL auto_increment,
  `PERSON_NAME` varchar(100) NOT NULL,
  `FATHER_NAME` varchar(100) NOT NULL,
  `AGE` int(11) default NULL,
  `GENDER` varchar(1) NOT NULL,
  `PHONE_NO` varchar(100) NOT NULL,
  `ADDRESS` varchar(500) NOT NULL,
  `LAND_HOLDINGS` int(11) default NULL,
  `village_id` int(11) NOT NULL,
  `group_id` int(11) default NULL,
  `equipmentholder_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `PERSON_village_id` (`village_id`),
  KEY `PERSON_group_id` (`group_id`),
  KEY `PERSON_equipmentholder_id` (`equipmentholder_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1087 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `PERSON`
--

LOCK TABLES `PERSON` WRITE;
/*!40000 ALTER TABLE `PERSON` DISABLE KEYS */;
INSERT INTO `PERSON` VALUES (109,'Rahil Gudia','',NULL,'F','','',NULL,29,81,NULL),(110,'Salomi Gudia','',NULL,'F','','',NULL,29,81,NULL),(106,'Subatra devi','',NULL,'F','','',NULL,29,81,NULL),(107,'Milo Devi','',NULL,'F','','',NULL,29,81,NULL),(108,'Milo Kumari','',NULL,'F','','',NULL,29,81,NULL),(104,'Sulil','',NULL,'M','','',NULL,26,76,NULL),(105,'Dropathi Devi','',NULL,'F','','',NULL,29,81,NULL),(279,'devemma','',NULL,'F','','',NULL,50,117,NULL),(280,'chenama','',NULL,'F','','',NULL,50,117,NULL),(281,'saraswati','',NULL,'F','','',NULL,50,117,NULL),(282,'Jyosnamayee Nayak','',NULL,'F','','',NULL,52,134,NULL),(283,'Padmasani Nayak','',NULL,'F','','',NULL,52,134,NULL),(284,'Dalimba Nayak','',NULL,'F','','',NULL,52,134,NULL),(285,'Tribeni Nayak','',NULL,'F','','',NULL,52,134,NULL),(946,'Smt. Sulochana Dei','',NULL,'F','','',NULL,68,141,NULL),(945,'Smt. Binodini Dei','',NULL,'F','','',NULL,68,141,NULL),(944,'Smt. Laxmi Dei','',NULL,'F','','',NULL,68,141,NULL),(289,'Droupadri Nayak(A)','',NULL,'F','','',NULL,52,134,NULL),(111,'Bahamani Gudia','',NULL,'F','','',NULL,29,81,NULL),(112,'Gaangi Gudia','',NULL,'F','','',NULL,29,81,NULL),(113,'Juliani Gudia','',NULL,'F','','',NULL,29,81,NULL),(114,'Sibiyani Gudia','',NULL,'F','','',NULL,29,81,NULL),(115,'Magdali Kandulona','',NULL,'F','','',NULL,29,81,NULL),(116,'Magadali Gudia','',NULL,'F','','',NULL,29,81,NULL),(117,'Somari Gudia','',NULL,'F','','',NULL,29,81,NULL),(118,'Munni Gudia','',NULL,'F','','',NULL,29,81,NULL),(119,'Binna Gudia','',NULL,'F','','',NULL,29,81,NULL),(120,'Pyari Devi','',NULL,'F','','',NULL,29,81,NULL),(121,'Ethwari Gudia','',NULL,'F','','',NULL,29,81,NULL),(122,'Hanna Bhengra','',NULL,'F','','',NULL,28,80,NULL),(123,'Barosi Bhengra','',NULL,'F','','',NULL,28,80,NULL),(124,'Jyoti Bhengra','',NULL,'F','','',NULL,28,80,NULL),(125,'Kuwari Bhengra','',NULL,'F','','',NULL,28,80,NULL),(126,'Mukta Bhengra','',NULL,'F','','',NULL,28,80,NULL),(127,'Somari Bhengra','',NULL,'F','','',NULL,28,80,NULL),(128,'Saniyaro Bhengra','',NULL,'F','','',NULL,28,80,NULL),(129,'Agata Bhengra','',NULL,'F','','',NULL,28,80,NULL),(130,'Gaangi Bhengra','',NULL,'F','','',NULL,28,80,NULL),(131,'Chandu Bhengra','',NULL,'F','','',NULL,28,80,NULL),(132,'Sushma Bhengra','',NULL,'F','','',NULL,28,80,NULL),(133,'Ethwari badh','',NULL,'F','','',NULL,28,80,NULL),(134,'Jano Bhengra','',NULL,'F','','',NULL,28,80,NULL),(135,'Birsi Bhengra','',NULL,'F','','',NULL,28,80,NULL),(136,'Birsi Bhengra','',NULL,'F','','',NULL,28,80,NULL),(137,'Shanti Bhengra','',NULL,'F','','',NULL,28,79,NULL),(138,'Sumanti Bhengra','',NULL,'F','','',NULL,28,79,NULL),(139,'Pyaro Bhengra','',NULL,'F','','',NULL,28,79,NULL),(140,'Josphina Bhengra','',NULL,'F','','',NULL,28,79,NULL),(141,'Jhony Topno','',NULL,'F','','',NULL,28,79,NULL),(142,'Birsi Topno','',NULL,'F','','',NULL,28,79,NULL),(143,'Jhariyo Topno','',NULL,'F','','',NULL,28,79,NULL),(144,'Ushki Topno','',NULL,'F','','',NULL,28,79,NULL),(145,'Gaangimuni Topno','',NULL,'F','','',NULL,28,79,NULL),(146,'Dashmi Topno','',NULL,'F','','',NULL,28,79,NULL),(147,'Chami Topno','',NULL,'F','','',NULL,28,79,NULL),(148,'Somari Topna','',NULL,'F','','',NULL,28,79,NULL),(149,'Nandi Bhengra','',NULL,'F','','',NULL,28,79,NULL),(150,'Mukta Bhengra','',NULL,'F','','',NULL,28,79,NULL),(151,'Jhony Bhengra','',NULL,'F','','',NULL,28,79,NULL),(152,'Anju Bhengra','',NULL,'F','','',NULL,28,79,NULL),(153,'Sushila Bhengra','',NULL,'F','','',NULL,28,79,NULL),(154,'Samme Bhengra','',NULL,'F','','',NULL,28,78,NULL),(155,'Dulari Bhengra','',NULL,'F','','',NULL,28,78,NULL),(156,'Sunita Gudia','',NULL,'F','','',NULL,28,78,NULL),(157,'Jagangi Gudia','',NULL,'F','','',NULL,28,78,NULL),(158,'Hanna Gudia','',NULL,'F','','',NULL,28,78,NULL),(159,'Butan Hemrom','',NULL,'F','','',NULL,28,78,NULL),(160,'MuniBhengra','',NULL,'F','','',NULL,28,78,NULL),(161,'Randai Bhengra','',NULL,'F','','',NULL,28,78,NULL),(162,'Budhni Bhengra','',NULL,'F','','',NULL,28,78,NULL),(163,'Somari Bhengra','',NULL,'F','','',NULL,28,78,NULL),(164,'Luisa Bhengra','',NULL,'F','','',NULL,28,78,NULL),(165,'Rahil Bhengra','',NULL,'F','','',NULL,28,78,NULL),(166,'Chandu Bhengra','',NULL,'F','','',NULL,28,78,NULL),(167,'Chirlu Bhengra','',NULL,'F','','',NULL,28,78,NULL),(168,'Pratima Bhengra','',NULL,'F','','',NULL,28,78,NULL),(169,'Gaangi Bhengra','',NULL,'F','','',NULL,28,78,NULL),(170,'Jhingi Bhengra','',NULL,'F','','',NULL,28,78,NULL),(171,'Chami Bhengra','',NULL,'F','','',NULL,28,78,NULL),(172,'Singi Bhengra','',NULL,'F','','',NULL,28,78,NULL),(173,'Radhi Bhengra','',NULL,'F','','',NULL,28,78,NULL),(174,'Lalita Devi','',NULL,'F','','',NULL,27,77,NULL),(175,'Pushpa devi','',NULL,'F','','',NULL,27,77,NULL),(176,'Bimala Devi A','',NULL,'F','','',NULL,27,77,NULL),(177,'Kalavati Devi ','',NULL,'F','','',NULL,27,77,NULL),(178,'Dasmi Devi','',NULL,'F','','',NULL,27,77,NULL),(179,'Malati devi A','',NULL,'F','','',NULL,27,77,NULL),(180,'Kunti Devi A','',NULL,'F','','',NULL,27,77,NULL),(181,'Shanti Devi','',NULL,'F','','',NULL,27,77,NULL),(182,'Bijan Devi','',NULL,'F','','',NULL,27,77,NULL),(183,'Rajmuni Devi','',NULL,'F','','',NULL,27,77,NULL),(184,'Malati devi B','',NULL,'F','','',NULL,27,77,NULL),(185,'Nankur Devi','',NULL,'F','','',NULL,27,77,NULL),(186,'Mankuwar Devi','',NULL,'F','','',NULL,27,77,NULL),(187,'Itwari Devi','',NULL,'F','','',NULL,27,77,NULL),(188,'Bimala Devi B','',NULL,'F','','',NULL,27,77,NULL),(189,'Rita Devi','',NULL,'F','','',NULL,27,77,NULL),(190,'Bolo Devi','',NULL,'F','','',NULL,27,77,NULL),(191,'Urmila Devi','',NULL,'F','','',NULL,27,77,NULL),(192,'Achcheswar Singh','',NULL,'M','','',NULL,30,82,NULL),(193,'Tej Devi','',NULL,'F','','',NULL,25,83,NULL),(194,'Rahil Topno','',NULL,'F','','',NULL,25,83,NULL),(195,'Lakshman','',NULL,'M','','',NULL,38,88,NULL),(196,'Gender Singh','',NULL,'M','','',NULL,38,88,NULL),(197,'Hajari','',NULL,'M','','',NULL,38,88,NULL),(198,'Naval','',NULL,'M','','',NULL,38,88,NULL),(199,'Ramesh','',NULL,'M','','',NULL,38,88,NULL),(200,'Nahar Singh','',NULL,'M','','',NULL,38,88,NULL),(201,'Birmal','',NULL,'M','','',NULL,38,88,NULL),(202,'Amar Singh','',NULL,'M','','',NULL,38,88,NULL),(203,'Kailash','',NULL,'M','','',NULL,38,88,NULL),(204,'Bhim Singh','',NULL,'M','','',NULL,38,88,NULL),(205,'Nan Singh','',NULL,'M','','',NULL,38,88,NULL),(206,'Dema','',NULL,'M','','',NULL,38,88,NULL),(207,'Manohar','',NULL,'M','','',NULL,38,88,NULL),(208,'Jamla','',NULL,'M','','',NULL,38,88,NULL),(209,'Bhayla','',NULL,'M','','',NULL,38,88,NULL),(210,'Rakesh','',NULL,'M','','',NULL,38,88,NULL),(211,'Nagappa Jaygoudar','',NULL,'M','','',NULL,50,116,NULL),(212,'Ramesh kamplikoppa','',NULL,'M','','',NULL,50,116,NULL),(213,'Shankarappa chinchali','',NULL,'M','','',NULL,50,116,NULL),(214,'Basappa goudara','',NULL,'M','','',NULL,50,116,NULL),(215,'Lingareddy naduvinamnai','',NULL,'M','','',NULL,50,116,NULL),(216,'Nagaraj muttagi','',NULL,'M','','',NULL,50,116,NULL),(217,'Nigappa sherewad','',NULL,'M','','',NULL,50,116,NULL),(218,'Chanabasappa shetteppanavar','',NULL,'M','','',NULL,50,116,NULL),(219,'Swamiji','',NULL,'M','','',NULL,50,116,NULL),(220,'Ireppa kabber','',NULL,'M','','',NULL,50,116,NULL),(221,'Parappa ganti','',NULL,'M','','',NULL,50,116,NULL),(222,'Irapaiah neeralagi','',NULL,'M','','',NULL,50,116,NULL),(223,'Fakirappa siddappanavar','',NULL,'M','','',NULL,50,116,NULL),(224,'Kubergouda doddagoudar','',NULL,'M','','',NULL,50,116,NULL),(225,'Honavva','',NULL,'F','','',NULL,50,116,NULL),(226,'Reshma','',NULL,'F','','',NULL,50,116,NULL),(227,'Sharravva','',NULL,'F','','',NULL,50,116,NULL),(228,'Gangamma','',NULL,'F','','',NULL,50,116,NULL),(229,'Kammalavva','',NULL,'F','','',NULL,50,116,NULL),(230,'Sahebi','',NULL,'F','','',NULL,50,116,NULL),(231,'Paravva','',NULL,'F','','',NULL,50,116,NULL),(232,'Rajibi','',NULL,'F','','',NULL,50,116,NULL),(233,'Manjula','',NULL,'F','','',NULL,50,116,NULL),(234,'Yallamma','',NULL,'F','','',NULL,50,116,NULL),(235,'Tayavva','',NULL,'F','','',NULL,50,116,NULL),(236,'Renuka','',NULL,'F','','',NULL,50,116,NULL),(237,'Tippava','',NULL,'F','','',NULL,50,116,NULL),(238,'Manjula ','',NULL,'F','','',NULL,50,116,NULL),(239,'Devakka','',NULL,'F','','',NULL,50,116,NULL),(240,'Savavva','',NULL,'F','','',NULL,50,116,NULL),(241,'Madevi Ganti','',NULL,'F','','',NULL,50,116,NULL),(242,'Iravva hulugur','',NULL,'F','','',NULL,50,115,NULL),(243,'Shantavva','',NULL,'F','','',NULL,50,115,NULL),(244,'Ningavva','',NULL,'F','','',NULL,50,115,NULL),(245,'Devakka','',NULL,'F','','',NULL,50,115,NULL),(246,'Kamalavva','',NULL,'F','','',NULL,50,115,NULL),(247,'Sushilavva','',NULL,'F','','',NULL,50,115,NULL),(248,'Renavva','',NULL,'F','','',NULL,50,115,NULL),(249,'Iravva hulgur','',NULL,'F','','',NULL,50,115,NULL),(250,'Shivakka','',NULL,'F','','',NULL,50,115,NULL),(251,'Sarswati','',NULL,'F','','',NULL,50,115,NULL),(252,'Shekavva','',NULL,'F','','',NULL,50,115,NULL),(253,'Kallavva','',NULL,'F','','',NULL,50,115,NULL),(254,'Devakka','',NULL,'F','','',NULL,50,115,NULL),(255,'Manjula','',NULL,'F','','',NULL,50,115,NULL),(256,'Basavva','',NULL,'F','','',NULL,50,115,NULL),(257,'Nelavva','',NULL,'F','','',NULL,50,115,NULL),(258,'Yellavva ','',NULL,'F','','',NULL,50,115,NULL),(259,'Jayashri','',NULL,'F','','',NULL,50,115,NULL),(260,'Neelamma','',NULL,'F','','',NULL,50,115,NULL),(261,'Gangavva ','',NULL,'F','','',NULL,50,115,NULL),(262,'Gadigavva','',NULL,'F','','',NULL,50,115,NULL),(263,'Neelavva','',NULL,'F','','',NULL,50,115,NULL),(264,'Rudravva Jaygoudra','',NULL,'F','','',NULL,50,115,NULL),(265,'Fakiravva','',NULL,'F','','',NULL,50,115,NULL),(266,'Channavva','',NULL,'F','','',NULL,50,115,NULL),(267,'Madevi','',NULL,'F','','',NULL,50,115,NULL),(268,'Ratnavva','',NULL,'F','','',NULL,50,115,NULL),(269,'Parvatavva','',NULL,'F','','',NULL,50,115,NULL),(270,'Mallavva ','',NULL,'F','','',NULL,50,115,NULL),(271,'Gangavva','',NULL,'F','','',NULL,50,115,NULL),(272,'Hanumavva','',NULL,'F','','',NULL,50,115,NULL),(273,'Shantavva','',NULL,'F','','',NULL,50,115,NULL),(274,'Chanamma','',NULL,'F','','',NULL,50,115,NULL),(275,'Saraswati Aralikatti','',NULL,'F','','',NULL,50,115,NULL),(276,'Basavva','',NULL,'F','','',NULL,50,115,NULL),(277,'Shantavva','',NULL,'F','','',NULL,50,115,NULL),(278,'Akkamma','',NULL,'F','','',NULL,50,115,NULL),(290,'Droupadri Nayak(B)','',NULL,'F','','',NULL,52,134,NULL),(291,'Sabita Nayak(B)','',NULL,'F','','',NULL,52,134,NULL),(292,'Sakuntala Nayak','',NULL,'F','','',NULL,52,134,NULL),(293,'Damayanti Nayak','',NULL,'F','','',NULL,52,134,NULL),(294,'Bhanumati Nayak','',NULL,'F','','',NULL,52,134,NULL),(295,'Jayanti Nayak','',NULL,'F','','',NULL,52,134,NULL),(296,'Droupadri Nayak(C)','',NULL,'F','','',NULL,52,134,NULL),(297,'Nidramani Nayak','',NULL,'F','','',NULL,52,134,NULL),(298,'Mandodari Nayak','',NULL,'F','','',NULL,52,134,NULL),(299,'Sasikala Nayak','',NULL,'F','','',NULL,52,134,NULL),(300,'Kusumanjali Nayak','',NULL,'F','','',NULL,52,134,NULL),(301,'Manjulata Nayak','',NULL,'F','','',NULL,52,134,NULL),(302,'Bhabani Nayak','',NULL,'F','','',NULL,52,134,NULL),(303,'Kautuki Nayak','',NULL,'F','','',NULL,52,134,NULL),(943,'Smt. Bela Pingua','',NULL,'F','','',NULL,68,141,NULL),(942,'Rashasmi Purty','',NULL,'F','','',NULL,68,141,NULL),(941,'Smt. Jambi Buliuli','',NULL,'F','','',NULL,68,141,NULL),(309,'Pramila Nayak','',NULL,'F','','',NULL,52,134,NULL),(310,'Gandhari Nayak','',NULL,'F','','',NULL,52,134,NULL),(311,'Gitanjali Nayak','',NULL,'F','','',NULL,52,134,NULL),(312,'Pramila Nayak(B)','',NULL,'F','','',NULL,52,134,NULL),(933,'Smt. Jayanti Hesah','',NULL,'F','','',NULL,68,141,NULL),(932,'Smt. Balema Hesah','',NULL,'F','','',NULL,68,141,NULL),(931,'Laxmi Chattar ','',NULL,'F','','',NULL,62,132,NULL),(319,'Binati Naik','',NULL,'F','','',NULL,63,133,NULL),(320,'Hemalata Naik','',NULL,'F','','',NULL,63,133,NULL),(321,'Maalati Naik','',NULL,'F','','',NULL,63,133,NULL),(322,'Srimani Naik','',NULL,'F','','',NULL,63,133,NULL),(323,'Keshni Naik','',NULL,'F','','',NULL,63,133,NULL),(324,'Pakana Naik','',NULL,'F','','',NULL,63,133,NULL),(325,'Painta Naik','',NULL,'F','','',NULL,63,133,NULL),(326,'Sita Naik','',NULL,'F','','',NULL,63,133,NULL),(327,'Malli Naik','',NULL,'F','','',NULL,63,133,NULL),(328,'Ratani Naik','',NULL,'F','','',NULL,63,133,NULL),(329,'Somabari Naik','',NULL,'F','','',NULL,63,133,NULL),(330,'Saita Naik','',NULL,'F','','',NULL,63,133,NULL),(331,'Sukumati Naik','',NULL,'F','','',NULL,63,133,NULL),(332,'Khaira Naik','',NULL,'F','','',NULL,63,133,NULL),(333,'Padmini Naik','',NULL,'F','','',NULL,63,133,NULL),(334,'Dhukhini Hembram','',NULL,'F','','',NULL,63,133,NULL),(335,'Bini Hembram','',NULL,'F','','',NULL,63,133,NULL),(336,'Raibari Hembram','',NULL,'F','','',NULL,63,133,NULL),(337,'Suryamani  Hembram','',NULL,'F','','',NULL,63,133,NULL),(338,'Sumi Purty (A)','',NULL,'F','','',NULL,63,133,NULL),(339,'Bali Hembram','',NULL,'F','','',NULL,63,133,NULL),(340,'Mani Purty','',NULL,'F','','',NULL,63,133,NULL),(341,'Jayanti Lohar','',NULL,'F','','',NULL,63,133,NULL),(342,'Gurubari Lohar','',NULL,'F','','',NULL,63,133,NULL),(343,'Laxmi Hembram','',NULL,'F','','',NULL,63,133,NULL),(344,'Khirodi Behera','',NULL,'F','','',NULL,63,133,NULL),(345,'Sumi Purty (b)','',NULL,'F','','',NULL,63,133,NULL),(346,'Pani Hembram','',NULL,'F','','',NULL,63,133,NULL),(347,'Binati Naik','',NULL,'F','','',NULL,63,133,NULL),(348,'Hemalata Naik','',NULL,'F','','',NULL,63,133,NULL),(349,'Maalati Naik','',NULL,'F','','',NULL,63,133,NULL),(350,'Srimani Naik','',NULL,'F','','',NULL,63,133,NULL),(351,'Keshni Naik','',NULL,'F','','',NULL,63,133,NULL),(352,'Pakana Naik','',NULL,'F','','',NULL,63,133,NULL),(353,'Painta Naik','',NULL,'F','','',NULL,63,133,NULL),(354,'Sita Naik','',NULL,'F','','',NULL,63,133,NULL),(355,'Malli Naik','',NULL,'F','','',NULL,63,133,NULL),(356,'Ratani Naik','',NULL,'F','','',NULL,63,133,NULL),(357,'Somabari Naik','',NULL,'F','','',NULL,63,133,NULL),(358,'Saita Naik','',NULL,'F','','',NULL,63,133,NULL),(359,'Sukumati Naik','',NULL,'F','','',NULL,63,133,NULL),(360,'Khaira Naik','',NULL,'F','','',NULL,63,133,NULL),(361,'Padmini Naik','',NULL,'F','','',NULL,63,133,NULL),(362,'Dhukhini Hembram','',NULL,'F','','',NULL,63,133,NULL),(363,'Bini Hembram','',NULL,'F','','',NULL,63,133,NULL),(364,'Raibari Hembram','',NULL,'F','','',NULL,63,133,NULL),(365,'Suryamani  Hembram','',NULL,'F','','',NULL,63,133,NULL),(366,'Sumi Purty (A)','',NULL,'F','','',NULL,63,133,NULL),(367,'Bali Hembram','',NULL,'F','','',NULL,63,133,NULL),(368,'Mani Purty','',NULL,'F','','',NULL,63,133,NULL),(369,'Jayanti Lohar','',NULL,'F','','',NULL,63,133,NULL),(370,'Gurubari Lohar','',NULL,'F','','',NULL,63,133,NULL),(371,'Laxmi Hembram','',NULL,'F','','',NULL,63,133,NULL),(372,'Khirodi Behera','',NULL,'F','','',NULL,63,133,NULL),(373,'Sumi Purty (b)','',NULL,'F','','',NULL,63,133,NULL),(374,'Pani Hembram','',NULL,'F','','',NULL,63,133,NULL),(375,'Binati Naik','',NULL,'F','','',NULL,63,133,NULL),(376,'Hemalata Naik','',NULL,'F','','',NULL,63,133,NULL),(377,'Maalati Naik','',NULL,'F','','',NULL,63,133,NULL),(378,'Srimani Naik','',NULL,'F','','',NULL,63,133,NULL),(379,'Keshni Naik','',NULL,'F','','',NULL,63,133,NULL),(380,'Pakana Naik','',NULL,'F','','',NULL,63,133,NULL),(381,'Painta Naik','',NULL,'F','','',NULL,63,133,NULL),(382,'Sita Naik','',NULL,'F','','',NULL,63,133,NULL),(383,'Malli Naik','',NULL,'F','','',NULL,63,133,NULL),(384,'Ratani Naik','',NULL,'F','','',NULL,63,133,NULL),(385,'Somabari Naik','',NULL,'F','','',NULL,63,133,NULL),(386,'Saita Naik','',NULL,'F','','',NULL,63,133,NULL),(387,'Sukumati Naik','',NULL,'F','','',NULL,63,133,NULL),(388,'Khaira Naik','',NULL,'F','','',NULL,63,133,NULL),(389,'Padmini Naik','',NULL,'F','','',NULL,63,133,NULL),(390,'Dhukhini Hembram','',NULL,'F','','',NULL,63,133,NULL),(391,'Bini Hembram','',NULL,'F','','',NULL,63,133,NULL),(392,'Raibari Hembram','',NULL,'F','','',NULL,63,133,NULL),(393,'Suryamani  Hembram','',NULL,'F','','',NULL,63,133,NULL),(394,'Sumi Purty (A)','',NULL,'F','','',NULL,63,133,NULL),(395,'Bali Hembram','',NULL,'F','','',NULL,63,133,NULL),(396,'Mani Purty','',NULL,'F','','',NULL,63,133,NULL),(397,'Jayanti Lohar','',NULL,'F','','',NULL,63,133,NULL),(398,'Gurubari Lohar','',NULL,'F','','',NULL,63,133,NULL),(399,'Laxmi Hembram','',NULL,'F','','',NULL,63,133,NULL),(400,'Khirodi Behera','',NULL,'F','','',NULL,63,133,NULL),(401,'Sumi Purty (b)','',NULL,'F','','',NULL,63,133,NULL),(402,'Pani Hembram','',NULL,'F','','',NULL,63,133,NULL),(1008,'Suniti Naik ','',NULL,'F','','',NULL,62,132,NULL),(1014,'Sita Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1013,'Jana Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1012,'Jamuna Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1006,'Beni Naik ','',NULL,'F','','',NULL,62,132,NULL),(1007,'Jaumani Naik ','',NULL,'F','','',NULL,62,132,NULL),(1005,'Sadhabani Naik ','',NULL,'F','','',NULL,62,132,NULL),(1004,'Saraswati Naik ','',NULL,'F','','',NULL,62,132,NULL),(1003,'Kainta Naik ','',NULL,'F','','',NULL,62,132,NULL),(1002,'Sumitra Naik ','',NULL,'F','','',NULL,62,132,NULL),(1001,'Sabita Naik ','',NULL,'F','','',NULL,62,132,NULL),(1000,'Rajani Naik ','',NULL,'F','','',NULL,62,132,NULL),(999,'Malli Naik ','',NULL,'F','','',NULL,62,132,NULL),(998,'Pramila Naik ','',NULL,'F','','',NULL,62,132,NULL),(997,'Jaumani Naik ','',NULL,'F','','',NULL,62,132,NULL),(996,'Padmini Naik ','',NULL,'F','','',NULL,62,132,NULL),(995,'Suryamani Chattar ','',NULL,'F','','',NULL,62,132,NULL),(994,'Sukrumani Pingua ','',NULL,'F','','',NULL,62,132,NULL),(993,'Mukta Chattar ','',NULL,'F','','',NULL,62,132,NULL),(1011,'Sangita Chattar ','',NULL,'F','','',NULL,62,131,NULL),(992,'Yatri Chattar ','',NULL,'F','','',NULL,62,132,NULL),(991,'Gurubari Chattar ','',NULL,'F','','',NULL,62,132,NULL),(990,'Sandhari Chattar ','',NULL,'F','','',NULL,62,132,NULL),(438,'Binati Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1010,'Mandakini Naik ','',NULL,'F','','',NULL,62,132,NULL),(988,'Sumtra Sai ','',NULL,'F','','',NULL,62,132,NULL),(989,'Nirash Chattar ','',NULL,'F','','',NULL,62,132,NULL),(1009,'Daimati Naik ','',NULL,'F','','',NULL,62,132,NULL),(987,'Rani Chattar ','',NULL,'F','','',NULL,62,132,NULL),(986,'Chmpabati Pingua ','',NULL,'F','','',NULL,62,132,NULL),(985,'Malati Pingua ','',NULL,'F','','',NULL,62,132,NULL),(984,'Minako Kuldi','',NULL,'F','','',NULL,68,140,NULL),(983,'Parbati Purti','',NULL,'F','','',NULL,68,140,NULL),(981,'Suduni Pingua','',NULL,'F','','',NULL,68,140,NULL),(982,'Malati Nayak','',NULL,'F','','',NULL,68,140,NULL),(980,'Padmabati Nayak','',NULL,'F','','',NULL,68,140,NULL),(979,'Belmatee Pingua','',NULL,'F','','',NULL,68,140,NULL),(978,'Sombari Pingua','',NULL,'F','','',NULL,68,140,NULL),(977,'Mita Pingua','',NULL,'F','','',NULL,68,140,NULL),(976,'Masuree Pingua','',NULL,'F','','',NULL,68,140,NULL),(975,'Namsi Purty','',NULL,'F','','',NULL,68,140,NULL),(974,'Subhadra Pingua','',NULL,'F','','',NULL,68,140,NULL),(973,'Jemamani Purty','',NULL,'F','','',NULL,68,140,NULL),(972,'Indumati Nayak','',NULL,'F','','',NULL,68,140,NULL),(971,'Sabitri Nayak','',NULL,'F','','',NULL,68,140,NULL),(970,'Debasri Nayak','',NULL,'F','','',NULL,68,140,NULL),(969,'Saraswati Nayak','',NULL,'F','','',NULL,68,140,NULL),(968,'Purnami Naik','',NULL,'F','','',NULL,68,140,NULL),(967,'Jayimani Nayak','',NULL,'F','','',NULL,68,140,NULL),(966,'Bimala Nayak','',NULL,'F','','',NULL,68,140,NULL),(965,'Labanya Bewa','',NULL,'F','','',NULL,68,140,NULL),(964,'Sarojeeni Nayak','',NULL,'F','','',NULL,68,140,NULL),(963,'Bhanumati Nayak','',NULL,'F','','',NULL,68,140,NULL),(962,'Gitamani Nayak','',NULL,'F','','',NULL,68,140,NULL),(484,'Malati Tudu','',NULL,'F','','',NULL,60,129,NULL),(485,'Maidi Tudu','',NULL,'F','','',NULL,60,129,NULL),(486,'Duli Tudu(A)','',NULL,'F','','',NULL,60,129,NULL),(487,'Duli Tudu(B)','',NULL,'F','','',NULL,60,129,NULL),(488,'Hiramani Tudu','',NULL,'F','','',NULL,60,129,NULL),(489,'Sebati Tudu','',NULL,'F','','',NULL,60,129,NULL),(490,'Sita Tudu(A)','',NULL,'F','','',NULL,60,129,NULL),(491,'Raude Tudu','',NULL,'F','','',NULL,60,129,NULL),(492,'Sita Tudu(B)','',NULL,'F','','',NULL,60,129,NULL),(493,'Jhanamani Tudu','',NULL,'F','','',NULL,60,129,NULL),(494,'Paya Hansda','',NULL,'F','','',NULL,60,129,NULL),(495,'Jaba Tudu','',NULL,'F','','',NULL,60,129,NULL),(496,'Hiramani Tudu','',NULL,'F','','',NULL,60,129,NULL),(497,'Sukmati Hansda','',NULL,'F','','',NULL,60,129,NULL),(498,'Parbati Tudu','',NULL,'F','','',NULL,60,129,NULL),(499,'Jima Honaga','',NULL,'F','','',NULL,60,129,NULL),(500,'Chhabi Kisku','',NULL,'F','','',NULL,60,129,NULL),(501,'Nangi Tudu','',NULL,'F','','',NULL,60,129,NULL),(502,'Nitima Honaga','',NULL,'F','','',NULL,60,129,NULL),(503,'Rani Tudu','',NULL,'F','','',NULL,60,129,NULL),(504,'Raimat Tudu','',NULL,'F','','',NULL,60,129,NULL),(505,'Phulamani Soren','',NULL,'F','','',NULL,60,129,NULL),(506,'Manki Soren','',NULL,'F','','',NULL,60,129,NULL),(507,'Metal Soren','',NULL,'F','','',NULL,60,129,NULL),(508,'Sakra Tudu','',NULL,'F','','',NULL,60,129,NULL),(509,'Jayanti Honnaga(A)','',NULL,'F','','',NULL,59,128,NULL),(510,'Raimani Honnaga','',NULL,'F','','',NULL,59,128,NULL),(511,'Lalmati Honnaga','',NULL,'F','','',NULL,59,128,NULL),(512,'Harsamani Honnaga','',NULL,'F','','',NULL,59,128,NULL),(513,'Hiramani Honnaga','',NULL,'F','','',NULL,59,128,NULL),(514,'Jayanti Honaga(B)','',NULL,'F','','',NULL,59,128,NULL),(515,'Dusi Honnaga','',NULL,'F','','',NULL,59,128,NULL),(516,'Champabati Honnaga','',NULL,'F','','',NULL,59,128,NULL),(517,'Sulekha Honnaga','',NULL,'F','','',NULL,59,128,NULL),(518,'Kanti Dehuri','',NULL,'F','','',NULL,59,128,NULL),(519,'Budhini Honnaga','',NULL,'F','','',NULL,59,128,NULL),(520,'Panabati Honnga','',NULL,'F','','',NULL,59,128,NULL),(521,'Sumitra Honnaga','',NULL,'F','','',NULL,59,128,NULL),(522,'Chandumani Honnaga','',NULL,'F','','',NULL,59,128,NULL),(523,'Damayanti Honnaga','',NULL,'F','','',NULL,59,128,NULL),(524,'Jemamani Honnga','',NULL,'F','','',NULL,59,128,NULL),(525,'Keshini Honnaga','',NULL,'F','','',NULL,59,128,NULL),(526,'Juneidevi Honnaga','',NULL,'F','','',NULL,59,128,NULL),(527,'Sabitri Honnaga','',NULL,'F','','',NULL,59,128,NULL),(528,'Muni Honnaga','',NULL,'F','','',NULL,59,128,NULL),(529,'Menjri Honnaga','',NULL,'F','','',NULL,59,128,NULL),(530,'Tribeni Dehuri','',NULL,'F','','',NULL,59,128,NULL),(531,'Sakuntala Tudu','',NULL,'F','','',NULL,58,127,NULL),(532,'Manania Tudu','',NULL,'F','','',NULL,58,127,NULL),(533,'Basumati Tudu','',NULL,'F','','',NULL,58,127,NULL),(534,'Sanamani Tudu','',NULL,'F','','',NULL,58,127,NULL),(535,'Gurubari Pingua','',NULL,'F','','',NULL,58,127,NULL),(536,'Padmabati Tudu','',NULL,'F','','',NULL,58,127,NULL),(537,'Dhujamani Tudu','',NULL,'F','','',NULL,58,127,NULL),(538,'Parbati Tudu','',NULL,'F','','',NULL,58,127,NULL),(539,'Baijaynti Hansda','',NULL,'F','','',NULL,58,127,NULL),(540,'Baijaynti Hansda','',NULL,'F','','',NULL,58,127,NULL),(541,'Manita Tudu','',NULL,'F','','',NULL,58,127,NULL),(542,'Pana Murmu','',NULL,'F','','',NULL,58,127,NULL),(543,'Hira mani Hasada','',NULL,'F','','',NULL,58,127,NULL),(544,'Jhingimani Alda','',NULL,'F','','',NULL,58,127,NULL),(545,'Sakra Murmu','',NULL,'F','','',NULL,58,127,NULL),(546,'Ranimani Hembram','',NULL,'F','','',NULL,58,127,NULL),(547,'Champa Hembram','',NULL,'F','','',NULL,58,127,NULL),(548,'Mainabati Tudu','',NULL,'F','','',NULL,58,127,NULL),(549,'Champabati Hansda','',NULL,'F','','',NULL,58,127,NULL),(550,'Bija Soren','',NULL,'F','','',NULL,58,127,NULL),(551,'Rani Soren','',NULL,'F','','',NULL,58,127,NULL),(552,'Nasa Besra','',NULL,'F','','',NULL,58,127,NULL),(553,'Pani Besra','',NULL,'F','','',NULL,58,127,NULL),(554,'Raimani Soren','',NULL,'F','','',NULL,58,127,NULL),(555,'Dulari Hembram','',NULL,'F','','',NULL,58,127,NULL),(556,'Yamunamani Soren','',NULL,'F','','',NULL,58,127,NULL),(557,'Salama Soren','',NULL,'F','','',NULL,58,127,NULL),(558,'Nagimani Soren','',NULL,'F','','',NULL,58,127,NULL),(559,'Chhita Hansda','',NULL,'F','','',NULL,58,127,NULL),(560,'Karmi Hansda','',NULL,'F','','',NULL,58,127,NULL),(561,'Bini Hembram','',NULL,'F','','',NULL,58,127,NULL),(562,'Raibari Hembram','',NULL,'F','','',NULL,58,127,NULL),(563,'Bimala Naik','',NULL,'F','','',NULL,57,126,NULL),(564,'Tulasi Naik','',NULL,'F','','',NULL,57,126,NULL),(565,'Nandini Naik','',NULL,'F','','',NULL,57,126,NULL),(566,'Srimati Naik','',NULL,'F','','',NULL,57,126,NULL),(567,'Padmabati Naik','',NULL,'F','','',NULL,57,126,NULL),(568,'Bilasi Naik','',NULL,'F','','',NULL,57,126,NULL),(569,'Puspalata Naik','',NULL,'F','','',NULL,57,126,NULL),(570,'Daita Naik','',NULL,'F','','',NULL,57,126,NULL),(571,'Beni Naik','',NULL,'F','','',NULL,57,126,NULL),(572,'Ruduni Naik','',NULL,'F','','',NULL,57,126,NULL),(573,'Sasmita Mohakud','',NULL,'F','','',NULL,57,126,NULL),(574,'Pramila Naik','',NULL,'F','','',NULL,57,126,NULL),(575,'Bimala Naik','',NULL,'F','','',NULL,57,126,NULL),(576,'Mandadari Naik','',NULL,'F','','',NULL,57,126,NULL),(577,'Rahaswari Naik','',NULL,'F','','',NULL,57,126,NULL),(578,'Bilasi Naik','',NULL,'F','','',NULL,57,126,NULL),(579,'Sabitri Naik','',NULL,'F','','',NULL,57,126,NULL),(580,'Aira  Naik','',NULL,'F','','',NULL,57,126,NULL),(581,'Nalita Naik','',NULL,'F','','',NULL,57,126,NULL),(582,'Saradi Naik','',NULL,'F','','',NULL,57,126,NULL),(583,'Mangali  Naik','',NULL,'F','','',NULL,57,126,NULL),(584,'Sulekha Naik','',NULL,'F','','',NULL,57,126,NULL),(585,'Adara Naik','',NULL,'F','','',NULL,57,126,NULL),(586,'Pemi Naik','',NULL,'F','','',NULL,57,126,NULL),(587,'Jaleswari Naik','',NULL,'F','','',NULL,57,126,NULL),(588,'Ruduna Naik','',NULL,'F','','',NULL,57,126,NULL),(589,'Sebati Naik','',NULL,'F','','',NULL,57,126,NULL),(590,'Binati Naik','',NULL,'F','','',NULL,57,126,NULL),(591,'Phulamani Marandi','',NULL,'F','','',NULL,56,125,NULL),(592,'Basanti Tudu (A)','',NULL,'F','','',NULL,56,125,NULL),(593,'Dulimani Beshra','',NULL,'F','','',NULL,56,125,NULL),(594,'Basanti Tudu (B)','',NULL,'F','','',NULL,56,125,NULL),(595,'Yamuna Hembram','',NULL,'F','','',NULL,56,125,NULL),(596,'Malaho Tudu','',NULL,'F','','',NULL,56,125,NULL),(597,'Phulamani Soren','',NULL,'F','','',NULL,56,125,NULL),(598,'Jauna Beshara','',NULL,'F','','',NULL,56,125,NULL),(599,'Sumi Tudu','',NULL,'F','','',NULL,56,125,NULL),(600,'Pauri Tudu','',NULL,'F','','',NULL,56,125,NULL),(601,'Samiya Tudu','',NULL,'F','','',NULL,56,125,NULL),(602,'Sahagi Tudu','',NULL,'F','','',NULL,56,125,NULL),(603,'Jamumuna Majhi','',NULL,'F','','',NULL,56,125,NULL),(604,'Subani Besra','',NULL,'F','','',NULL,56,125,NULL),(605,'Lilmani Soren','',NULL,'F','','',NULL,56,125,NULL),(606,'Gouri Tudu','',NULL,'F','','',NULL,56,125,NULL),(607,'Padmabati Tudu','',NULL,'F','','',NULL,56,125,NULL),(608,'Ganga Kisku','',NULL,'F','','',NULL,56,125,NULL),(609,'Maina Tudu','',NULL,'F','','',NULL,56,125,NULL),(610,'Manak Tudu','',NULL,'F','','',NULL,56,125,NULL),(611,'Gangi Tudu','',NULL,'F','','',NULL,56,125,NULL),(612,'Shanti Tudu','',NULL,'F','','',NULL,56,125,NULL),(613,'Manasirani Majhi','',NULL,'F','','',NULL,56,125,NULL),(614,'Dukhini Hembram','',NULL,'F','','',NULL,56,125,NULL),(961,'Kanchana Nayak','',NULL,'F','','',NULL,68,140,NULL),(616,'Kanchan Lohar ','',NULL,'F','','',NULL,55,124,NULL),(960,'Rukmani Bewa','',NULL,'F','','',NULL,68,140,NULL),(959,'Tilattama Nayak','',NULL,'F','','',NULL,68,140,NULL),(619,'Jeetmani Mohanta ','',NULL,'F','','',NULL,55,124,NULL),(958,'Lilabati Dei','',NULL,'F','','',NULL,68,141,NULL),(957,'Dalimba Dei','',NULL,'F','','',NULL,68,141,NULL),(956,'Smt. Ambika Dei','',NULL,'F','','',NULL,68,141,NULL),(955,'Smt. Dukhini Mahakud','',NULL,'F','','',NULL,68,141,NULL),(954,'Smt. Sharala Mahakud','',NULL,'F','','',NULL,68,141,NULL),(953,'Smt. Padmabati Dei','',NULL,'F','','',NULL,68,141,NULL),(952,'Smt. Saraswati Mahakud','',NULL,'F','','',NULL,68,141,NULL),(951,'Smt. Surekha Dei','',NULL,'F','','',NULL,68,141,NULL),(950,'Smt. Sumati Dei','',NULL,'F','','',NULL,68,141,NULL),(949,'Smt. Mithila Dei','',NULL,'F','','',NULL,68,141,NULL),(948,'Smt. Kokila Dei','',NULL,'F','','',NULL,68,141,NULL),(947,'Smt. Kunta Dei','',NULL,'F','','',NULL,68,141,NULL),(940,'Premanjali Pat Pingua','',NULL,'F','','',NULL,68,141,NULL),(939,'Laxmi Buliuli','',NULL,'F','','',NULL,68,141,NULL),(938,'Laxmi Buliuli','',NULL,'F','','',NULL,68,141,NULL),(937,'Jayanti Hesah','',NULL,'F','','',NULL,68,141,NULL),(936,'Mani Purtty','',NULL,'F','','',NULL,68,141,NULL),(935,'Smt. Bahmain Hesah','',NULL,'F','','',NULL,68,141,NULL),(934,'Smt . Naguri Purtty','',NULL,'F','','',NULL,68,141,NULL),(650,'Sunamani Chattar','',NULL,'F','','',NULL,53,122,NULL),(651,'Sarojini Chattar','',NULL,'F','','',NULL,53,122,NULL),(652,'Srimati Chattar','',NULL,'F','','',NULL,53,122,NULL),(653,'Malati Chattar','',NULL,'F','','',NULL,53,122,NULL),(654,'Damayanti Chatar','',NULL,'F','','',NULL,53,122,NULL),(655,'Jannamani Chattar','',NULL,'F','','',NULL,53,122,NULL),(656,'Sita Chattar','',NULL,'F','','',NULL,53,122,NULL),(657,'Gurubari Chatar','',NULL,'F','','',NULL,53,122,NULL),(658,'Sabitree Chattar','',NULL,'F','','',NULL,53,122,NULL),(659,'Nandi Chatar','',NULL,'F','','',NULL,53,122,NULL),(660,'Jhunu Guiya','',NULL,'F','','',NULL,53,122,NULL),(661,'Junee Purty','',NULL,'F','','',NULL,53,122,NULL),(662,'Pyari Chatar','',NULL,'F','','',NULL,53,122,NULL),(663,'Kuni Guiya','',NULL,'F','','',NULL,53,122,NULL),(664,'Binapani Chattar','',NULL,'F','','',NULL,53,122,NULL),(665,'Parbati Guiya','',NULL,'F','','',NULL,53,122,NULL),(666,'Sukumati Chatar','',NULL,'F','','',NULL,53,122,NULL),(667,'Sushama Chatar','',NULL,'F','','',NULL,53,122,NULL),(668,'Sumitra Chatar','',NULL,'F','','',NULL,53,122,NULL),(669,'Menja Chatar','',NULL,'F','','',NULL,53,122,NULL),(670,'Mangulli Chatar','',NULL,'F','','',NULL,53,122,NULL),(671,'Jana Chatar','',NULL,'F','','',NULL,53,122,NULL),(672,'Sukumati Chatar(B)','',NULL,'F','','',NULL,53,122,NULL),(673,'Basanti Chatar','',NULL,'F','','',NULL,53,122,NULL),(674,'Saibanee Chatar','',NULL,'F','','',NULL,53,122,NULL),(675,'Baijayanti Chatar','',NULL,'F','','',NULL,53,122,NULL),(676,'Somabari Chatar','',NULL,'F','','',NULL,53,122,NULL),(677,'Sini Chatar','',NULL,'F','','',NULL,53,122,NULL),(678,'Sakuntalla Bankira','',NULL,'F','','',NULL,53,122,NULL),(679,'Kasturi Chattar','',NULL,'F','','',NULL,53,121,NULL),(680,'Sasmita Chattar','',NULL,'F','','',NULL,53,121,NULL),(681,'Raibari Chattar','',NULL,'F','','',NULL,53,121,NULL),(682,'Suru Chatar','',NULL,'F','','',NULL,53,121,NULL),(683,'Basanti Chattar','',NULL,'F','','',NULL,53,121,NULL),(684,'Sushilla Chattar','',NULL,'F','','',NULL,53,121,NULL),(685,'Lakshmi  Chattar','',NULL,'F','','',NULL,53,121,NULL),(686,'Meena Chattar','',NULL,'F','','',NULL,53,121,NULL),(687,'Tillatamma  Chattar','',NULL,'F','','',NULL,53,121,NULL),(688,'Samabari Chattar','',NULL,'F','','',NULL,53,121,NULL),(689,'Jemamani Chattar','',NULL,'F','','',NULL,53,121,NULL),(690,'Chamanu Chattar','',NULL,'F','','',NULL,53,121,NULL),(691,'Sushama Tiria','',NULL,'F','','',NULL,53,121,NULL),(692,'Basanti Bankira','',NULL,'F','','',NULL,53,121,NULL),(693,'Hachi Chatar','',NULL,'F','','',NULL,53,121,NULL),(694,'Sukanti Bankira','',NULL,'F','','',NULL,53,121,NULL),(695,'Jayanti Chatar','',NULL,'F','','',NULL,53,121,NULL),(696,'Pullamani Bankira','',NULL,'F','','',NULL,53,121,NULL),(697,'Raimani Chatar','',NULL,'F','','',NULL,53,121,NULL),(698,'Dashama Tiria','',NULL,'F','','',NULL,53,121,NULL),(699,'Nillima Chatar','',NULL,'F','','',NULL,53,121,NULL),(700,'Surjyamani Tiria','',NULL,'F','','',NULL,53,121,NULL),(701,'Durapati Bankira','',NULL,'F','','',NULL,53,121,NULL),(702,'Buduni  Bankira','',NULL,'F','','',NULL,53,121,NULL),(703,'Debaki Chatar','',NULL,'F','','',NULL,53,121,NULL),(704,'Srimati Chatar','',NULL,'F','','',NULL,53,121,NULL),(705,'Rebati Nayak','',NULL,'F','','',NULL,52,120,NULL),(706,'Pramila Nayak','',NULL,'F','','',NULL,46,120,NULL),(707,'Purabi Nayak','',NULL,'F','','',NULL,52,120,NULL),(708,'Padmini Nayak','',NULL,'F','','',NULL,52,120,NULL),(709,'Tilattama Nayak','',NULL,'F','','',NULL,52,120,NULL),(710,'Satyabhama Nayak','',NULL,'F','','',NULL,52,120,NULL),(711,'Shakuntala Nayak','',NULL,'F','','',NULL,52,120,NULL),(712,'Jayanti Nayak','',NULL,'F','','',NULL,52,120,NULL),(713,'Netramani Nayak','',NULL,'F','','',NULL,52,120,NULL),(714,'Tapaswini Nayak','',NULL,'F','','',NULL,52,120,NULL),(715,'Bhabani Nayak(B)','',NULL,'F','','',NULL,52,120,NULL),(716,'Binati Nayak','',NULL,'F','','',NULL,52,120,NULL),(717,'Raimani Pingua','',NULL,'F','','',NULL,52,120,NULL),(718,'Gurubari Pingua','',NULL,'F','','',NULL,52,120,NULL),(719,'Chandu Pingua','',NULL,'F','','',NULL,52,120,NULL),(720,'Samabari Pingua(A)','',NULL,'F','','',NULL,52,120,NULL),(721,'Damayanti Nayak','',NULL,'F','','',NULL,52,120,NULL),(722,'Rukmani Patra','',NULL,'F','','',NULL,52,120,NULL),(723,'Jayanti Patra','',NULL,'F','','',NULL,52,120,NULL),(724,'Damayanti Pingua','',NULL,'F','','',NULL,52,120,NULL),(725,'Chami Pingua','',NULL,'F','','',NULL,52,120,NULL),(726,'Gangi Hembram','',NULL,'F','','',NULL,52,120,NULL),(727,'Pramila Tiria','',NULL,'F','','',NULL,52,120,NULL),(728,'Asha Patra','',NULL,'F','','',NULL,52,120,NULL),(729,'Samabari Pingua(B)','',NULL,'F','','',NULL,52,120,NULL),(730,'Sukanti Pingua','',NULL,'F','','',NULL,52,120,NULL),(731,'Laxmi Pingua','',NULL,'F','','',NULL,52,120,NULL),(732,'Charima Pingua','',NULL,'F','','',NULL,52,120,NULL),(733,'Jashoda Nayak','',NULL,'F','','',NULL,52,119,NULL),(734,'Jatani Nayak','',NULL,'F','','',NULL,52,119,NULL),(735,'Pukulli Nayak','',NULL,'F','','',NULL,52,119,NULL),(736,'Babita Nayak','',NULL,'F','','',NULL,52,119,NULL),(737,'Chabirani Nayak','',NULL,'F','','',NULL,52,119,NULL),(738,'Sakuntala Nayak','',NULL,'F','','',NULL,52,119,NULL),(739,'Mahendri Nayak','',NULL,'F','','',NULL,52,119,NULL),(740,'Gitarani Nayak','',NULL,'F','','',NULL,52,119,NULL),(741,'Sumanti Nayak','',NULL,'F','','',NULL,52,119,NULL),(742,'Kasturi Nayak','',NULL,'F','','',NULL,52,119,NULL),(743,'Bhabani Nayak','',NULL,'F','','',NULL,52,119,NULL),(744,'Runurani Nayak','',NULL,'F','','',NULL,52,119,NULL),(745,'Bhoumirani Nayak','',NULL,'F','','',NULL,52,119,NULL),(746,'Manjulata Nayak','',NULL,'F','','',NULL,52,119,NULL),(747,'Ranjeeta Nayak','',NULL,'F','','',NULL,52,119,NULL),(748,'Surekha Nayak','',NULL,'F','','',NULL,52,119,NULL),(749,'Manjubala  Nayak','',NULL,'F','','',NULL,52,119,NULL),(750,'Mahendri Nayak','',NULL,'F','','',NULL,52,119,NULL),(751,'Sujata Nayak','',NULL,'F','','',NULL,52,119,NULL),(752,'Kanakalata  Nayak','',NULL,'F','','',NULL,52,119,NULL),(753,'Mita Nayak','',NULL,'F','','',NULL,52,119,NULL),(754,'Dalimba Nayak','',NULL,'F','','',NULL,52,119,NULL),(755,'Sanjukta Nayak','',NULL,'F','','',NULL,52,119,NULL),(756,'Premalata Nayak','',NULL,'F','','',NULL,52,119,NULL),(757,'Kasturi Nayak','',NULL,'F','','',NULL,52,119,NULL),(758,'Banita Nayak','',NULL,'F','','',NULL,52,119,NULL),(759,'Rajani Nayak','',NULL,'F','','',NULL,52,119,NULL),(760,'Srimati Bewa','',NULL,'F','','',NULL,52,119,NULL),(761,'Kishori Nayak','',NULL,'F','','',NULL,52,119,NULL),(762,'Maitree Nayak','',NULL,'F','','',NULL,52,119,NULL),(763,'Jyosnamayee Nayak','',NULL,'F','','',NULL,52,118,NULL),(764,'Padmasani Nayak','',NULL,'F','','',NULL,52,118,NULL),(765,'Dalimba Nayak','',NULL,'F','','',NULL,52,118,NULL),(766,'Tribeni Nayak','',NULL,'F','','',NULL,52,118,NULL),(767,'Tilottama Nayak','',NULL,'F','','',NULL,52,118,NULL),(768,'Sabita Nayak(A)','',NULL,'F','','',NULL,52,118,NULL),(769,'Gouribati Nayak','',NULL,'F','','',NULL,52,118,NULL),(770,'Droupadri Nayak(A)','',NULL,'F','','',NULL,52,118,NULL),(771,'Droupadri Nayak(B)','',NULL,'F','','',NULL,52,118,NULL),(772,'Sabita Nayak(B)','',NULL,'F','','',NULL,52,118,NULL),(773,'Sakuntala Nayak','',NULL,'F','','',NULL,52,118,NULL),(774,'Damayanti Nayak','',NULL,'F','','',NULL,52,118,NULL),(775,'Bhanumati Nayak','',NULL,'F','','',NULL,52,118,NULL),(776,'Jayanti Nayak','',NULL,'F','','',NULL,52,118,NULL),(777,'Droupadri Nayak(C)','',NULL,'F','','',NULL,52,118,NULL),(778,'Nidramani Nayak','',NULL,'F','','',NULL,52,118,NULL),(779,'Mandodari Nayak','',NULL,'F','','',NULL,52,118,NULL),(780,'Sasikala Nayak','',NULL,'F','','',NULL,52,118,NULL),(781,'Kusumanjali Nayak','',NULL,'F','','',NULL,52,118,NULL),(782,'Manjulata Nayak','',NULL,'F','','',NULL,52,118,NULL),(783,'Bhabani Nayak','',NULL,'F','','',NULL,52,118,NULL),(784,'Kautuki Nayak','',NULL,'F','','',NULL,52,118,NULL),(785,'Sulochana Nayak','',NULL,'F','','',NULL,52,118,NULL),(786,'Bharati Nayak','',NULL,'F','','',NULL,52,118,NULL),(787,'Kanakalata Nayak','',NULL,'F','','',NULL,52,118,NULL),(788,'Tusarkanti Nayak','',NULL,'F','','',NULL,52,118,NULL),(789,'Debaki Nayak','',NULL,'F','','',NULL,52,118,NULL),(790,'Pramila Nayak','',NULL,'F','','',NULL,52,118,NULL),(791,'Gandhari Nayak','',NULL,'F','','',NULL,52,118,NULL),(792,'Gitanjali Nayak','',NULL,'F','','',NULL,52,118,NULL),(793,'Pramila Naik(B)','',NULL,'F','','',NULL,52,118,NULL),(794,'Pyari Sundhi','',NULL,'F','','',NULL,69,143,NULL),(795,'Hemamalini Sundhi','',NULL,'F','','',NULL,69,143,NULL),(796,'Sini Soye','',NULL,'F','','',NULL,69,143,NULL),(797,'Subani soye','',NULL,'F','','',NULL,69,143,NULL),(798,'Rina Soye','',NULL,'F','','',NULL,69,143,NULL),(799,'Barsa Hesa','',NULL,'F','','',NULL,69,143,NULL),(800,'Menjari Hesa','',NULL,'F','','',NULL,69,143,NULL),(801,'Jambi Kandayang','',NULL,'F','','',NULL,69,143,NULL),(802,'Dasama Kandayang','',NULL,'F','','',NULL,69,143,NULL),(803,'Kirati Soya','',NULL,'F','','',NULL,69,143,NULL),(804,'Rajani Soya','',NULL,'F','','',NULL,69,143,NULL),(805,'Kuni Rani Sundhi','',NULL,'F','','',NULL,69,143,NULL),(806,'Dasama Soya','',NULL,'F','','',NULL,69,143,NULL),(807,'Chireng Hesa','',NULL,'F','','',NULL,69,143,NULL),(808,'Anami Kendayang','',NULL,'F','','',NULL,69,143,NULL),(809,'Surmi Soya','',NULL,'F','','',NULL,69,143,NULL),(810,'Kudugi Kendayang','',NULL,'F','','',NULL,69,143,NULL),(811,'Juguni Hesa','',NULL,'F','','',NULL,69,143,NULL),(812,'Jatri Mahakud','',NULL,'F','','',NULL,69,143,NULL),(813,'Purnami sundhi','',NULL,'F','','',NULL,69,143,NULL),(814,'Surjamani Sundhi','',NULL,'F','','',NULL,69,143,NULL),(815,'Sujuki Soye','',NULL,'F','','',NULL,69,143,NULL),(816,'Srimati Tiu','',NULL,'F','','',NULL,69,143,NULL),(817,'Jangamani Honnaga','',NULL,'F','','',NULL,69,142,NULL),(818,'Assai Honnaga','',NULL,'F','','',NULL,69,142,NULL),(819,'Gangi Honnaga','',NULL,'F','','',NULL,69,142,NULL),(820,'Sumitra Honnaga','',NULL,'F','','',NULL,69,142,NULL),(821,'Mechcha Honnaga','',NULL,'F','','',NULL,69,142,NULL),(822,'Basanti Honnaga','',NULL,'F','','',NULL,69,142,NULL),(823,'Jana Honnaga','',NULL,'F','','',NULL,69,142,NULL),(824,'Budhuni Honnaga','',NULL,'F','','',NULL,69,142,NULL),(825,'Diugi Honnaga','',NULL,'F','','',NULL,69,142,NULL),(826,'Hauri Honnaga','',NULL,'F','','',NULL,69,142,NULL),(827,'Jahari Honnaga','',NULL,'F','','',NULL,69,142,NULL),(828,'Munguli Honnaga','',NULL,'F','','',NULL,69,142,NULL),(829,'Malati Honnaga','',NULL,'F','','',NULL,69,142,NULL),(830,'Pangela Honnaga','',NULL,'F','','',NULL,69,142,NULL),(831,'Parbati Honnaga','',NULL,'F','','',NULL,69,142,NULL),(832,'Buduni Honnaga(B)','',NULL,'F','','',NULL,69,142,NULL),(833,'Sita Honnaga','',NULL,'F','','',NULL,69,142,NULL),(834,'Budhuni Honnaga(C)','',NULL,'F','','',NULL,69,142,NULL),(835,'Masuri Honnaga','',NULL,'F','','',NULL,69,142,NULL),(836,'Binati Honnaga','',NULL,'F','','',NULL,69,142,NULL),(837,'Gangi Honnaga','',NULL,'F','','',NULL,69,142,NULL),(838,'Phulmani Honnaga','',NULL,'F','','',NULL,69,142,NULL),(839,'Sabitri Honnaga','',NULL,'F','','',NULL,69,142,NULL),(840,'Manju Honnaga','',NULL,'F','','',NULL,69,142,NULL),(1057,'Budhuni Chattar ','',NULL,'F','','',NULL,62,130,NULL),(1056,'Padmini Pingua ','',NULL,'F','','',NULL,62,130,NULL),(1055,'Menjari Hembram ','',NULL,'F','','',NULL,62,130,NULL),(1054,'Khaira Hembram ','',NULL,'F','','',NULL,62,130,NULL),(1053,'Suryamani chattar ','',NULL,'F','','',NULL,62,130,NULL),(1052,'Sumitra Chattar ','',NULL,'F','','',NULL,62,130,NULL),(1051,'Laxmi Chattar ','',NULL,'F','','',NULL,62,130,NULL),(1050,'Padmini munda Lohar ','',NULL,'F','','',NULL,62,130,NULL),(1049,'Lembo Pingua ','',NULL,'F','','',NULL,62,130,NULL),(1048,'Menja Chatter ','',NULL,'F','','',NULL,62,130,NULL),(1047,'Pani Pingua ','',NULL,'F','','',NULL,62,130,NULL),(1046,'Malati Sae ','',NULL,'F','','',NULL,62,130,NULL),(1045,'Shrimati Naik ','',NULL,'F','','',NULL,62,130,NULL),(1044,'Bhabani Pingua ','',NULL,'F','','',NULL,62,130,NULL),(1043,'Dasama Tiu ','',NULL,'F','','',NULL,62,130,NULL),(1042,'Rajani Chatter ','',NULL,'F','','',NULL,62,130,NULL),(1041,'Muktamani Tiria ','',NULL,'F','','',NULL,62,130,NULL),(1040,'Janaki Chatter ','',NULL,'F','','',NULL,62,130,NULL),(1039,'Sansari Sinku ','',NULL,'F','','',NULL,62,130,NULL),(1038,'Budhuni Chatter ','',NULL,'F','','',NULL,62,130,NULL),(1037,'Jemamani Tiu ','',NULL,'F','','',NULL,62,130,NULL),(1036,'Malati Chatter ','',NULL,'F','','',NULL,62,130,NULL),(1035,'Sukanti Purty ','',NULL,'F','','',NULL,62,130,NULL),(1034,'Kasturi Chatter ','',NULL,'F','','',NULL,62,130,NULL),(1033,'Sunita Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1032,'Sabita Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1031,'Jana Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1030,'Subha Bandar ','',NULL,'F','','',NULL,62,131,NULL),(1029,'Subuni Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1028,'Kuni Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1027,'Seti Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1026,'Asha Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1025,'Dasama Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1024,'Meena Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1023,'Rukmani Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1022,'Sanjulata Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1021,'Turi Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1020,'Sini Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1019,'Mirju Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1018,'Sambari Pingua ','',NULL,'F','','',NULL,62,131,NULL),(1017,'Nagari Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1016,'Padmabati Chattar ','',NULL,'F','','',NULL,62,131,NULL),(1015,'Mukta Chattar ','',NULL,'F','','',NULL,62,131,NULL),(894,'Mina Mahakud','',NULL,'F','','',NULL,67,139,NULL),(895,'Purnnami Mahakud','',NULL,'F','','',NULL,67,139,NULL),(896,'Gauri Mahakud','',NULL,'F','','',NULL,67,139,NULL),(897,'Sumitra Kandeyang','',NULL,'F','','',NULL,67,139,NULL),(898,'Jayanti Kandeyang','',NULL,'F','','',NULL,67,139,NULL),(899,'Minakumari Mahakud','',NULL,'F','','',NULL,67,139,NULL),(900,'Parbati Hembram','',NULL,'F','','',NULL,67,139,NULL),(901,'Sarati Behera','',NULL,'F','','',NULL,67,139,NULL),(902,'Saibani Behera','',NULL,'F','','',NULL,67,139,NULL),(903,'Pala Hembram','',NULL,'F','','',NULL,67,139,NULL),(904,'Sukanti Hembram(A)','',NULL,'F','','',NULL,67,139,NULL),(905,'Sukanti Hembram(B)','',NULL,'F','','',NULL,67,139,NULL),(906,'Shakuntala Kandeyang','',NULL,'F','','',NULL,67,139,NULL),(907,'Tulasi Tiu','',NULL,'F','','',NULL,67,139,NULL),(908,'Ambika kandeyang','',NULL,'F','','',NULL,67,139,NULL),(909,'Rajani Mahakud','',NULL,'F','','',NULL,67,139,NULL),(910,'Gangamani Hembramf','',NULL,'F','','',NULL,67,139,NULL),(911,'Hiramani Munduri','',NULL,'F','','',NULL,67,138,NULL),(912,'Sukamati Hembram','',NULL,'F','','',NULL,67,138,NULL),(913,'Nandi Hembram','',NULL,'F','','',NULL,67,138,NULL),(914,'Priyamani Mahakud','',NULL,'F','','',NULL,67,138,NULL),(915,'Phulamani Kandeyan','',NULL,'F','','',NULL,67,138,NULL),(916,'Marsa Malen Hembram','',NULL,'F','','',NULL,67,138,NULL),(917,'Somabari Hembram','',NULL,'F','','',NULL,67,138,NULL),(918,'Bhanumati Mahakud','',NULL,'F','','',NULL,67,138,NULL),(919,'Sanjita Kandeyan','',NULL,'F','','',NULL,67,138,NULL),(920,'Chandrika Kandeyan','',NULL,'F','','',NULL,67,138,NULL),(921,'Basanti Mahakud','',NULL,'F','','',NULL,67,138,NULL),(922,'Sunai Hembram','',NULL,'F','','',NULL,67,138,NULL),(923,'Bharati Mahakud','',NULL,'F','','',NULL,67,138,NULL),(924,'Sumitra Behera','',NULL,'F','','',NULL,67,138,NULL),(925,'Menja Hembram','',NULL,'F','','',NULL,67,138,NULL),(926,'Gangi Hembram','',NULL,'F','','',NULL,67,138,NULL),(927,'Subasini Mahakud','',NULL,'F','','',NULL,67,138,NULL),(928,'Jemamani Kandeyan','',NULL,'F','','',NULL,67,138,NULL),(929,'Ramani Hembram','',NULL,'F','','',NULL,67,138,NULL),(930,'Lillmani Mahakud','',NULL,'F','','',NULL,67,138,NULL),(1058,'Bela Purti ','',NULL,'F','','',NULL,62,130,NULL),(1059,'Dubgi Hembram ','',NULL,'F','','',NULL,62,130,NULL),(1060,'Sapani Pingua ','',NULL,'F','','',NULL,62,130,NULL),(1061,'Sombari soya ','',NULL,'F','','',NULL,62,130,NULL),(1062,'Pani Chattar ','',NULL,'F','','',NULL,62,130,NULL),(1063,'Turi Pingua ','',NULL,'F','','',NULL,62,130,NULL),(1064,'Deepanjali Patra ','',NULL,'F','','',NULL,55,124,NULL),(1065,'Minaka Mohanta ','',NULL,'F','','',NULL,55,124,NULL),(1066,'Tobharani Mohakud ','',NULL,'F','','',NULL,55,124,NULL),(1067,'Rebati Mohanta ','',NULL,'F','','',NULL,55,124,NULL),(1068,'Nirupama Mohanta ','',NULL,'F','','',NULL,55,124,NULL),(1069,'Sushanti Mohanta ','',NULL,'F','','',NULL,55,124,NULL),(1070,'Shantilata Mohanta ','',NULL,'F','','',NULL,55,124,NULL),(1071,'Chmpabati Hembram ','',NULL,'F','','',NULL,55,124,NULL),(1072,'Chanchala Mohanta ','',NULL,'F','','',NULL,55,124,NULL),(1073,'Parbati Bandra ','',NULL,'F','','',NULL,55,124,NULL),(1074,'Parbati Gagrai ','',NULL,'F','','',NULL,55,124,NULL),(1075,'Raimani Honnaga ','',NULL,'F','','',NULL,55,124,NULL),(1076,'Basanti Jamuda ','',NULL,'F','','',NULL,55,124,NULL),(1077,'Laxmirani Sinku ','',NULL,'F','','',NULL,55,124,NULL),(1078,'Nasamani Sinku ','',NULL,'F','','',NULL,55,124,NULL),(1079,'Menga Sinku ','',NULL,'F','','',NULL,55,124,NULL),(1080,'Lilmani Goipai ','',NULL,'F','','',NULL,55,124,NULL),(1081,'Namita Goipai ','',NULL,'F','','',NULL,55,124,NULL),(1082,'Bela Goipai ','',NULL,'F','','',NULL,55,124,NULL),(1083,'Laxmi Sinku ','',NULL,'F','','',NULL,55,124,NULL),(1084,'Sumati Bandra ','',NULL,'F','','',NULL,55,124,NULL),(1085,'Laxmi Goipai ','',NULL,'F','','',NULL,55,124,NULL);
/*!40000 ALTER TABLE `PERSON` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PERSON_ADOPT_PRACTICE`
--

DROP TABLE IF EXISTS `PERSON_ADOPT_PRACTICE`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `PERSON_ADOPT_PRACTICE` (
  `id` int(11) NOT NULL auto_increment,
  `person_id` int(11) NOT NULL,
  `practice_id` int(11) NOT NULL,
  `PRIOR_ADOPTION_FLAG` tinyint(1) default NULL,
  `DATE_OF_ADOPTION` date default NULL,
  `QUALITY` varchar(200) NOT NULL,
  `QUANTITY` int(11) default NULL,
  `QUANTITY_UNIT` varchar(150) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `PERSON_ADOPT_PRACTICE_person_id` (`person_id`),
  KEY `PERSON_ADOPT_PRACTICE_practice_id` (`practice_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `PERSON_ADOPT_PRACTICE`
--

LOCK TABLES `PERSON_ADOPT_PRACTICE` WRITE;
/*!40000 ALTER TABLE `PERSON_ADOPT_PRACTICE` DISABLE KEYS */;
/*!40000 ALTER TABLE `PERSON_ADOPT_PRACTICE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PERSON_GROUPS`
--

DROP TABLE IF EXISTS `PERSON_GROUPS`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `PERSON_GROUPS` (
  `id` int(11) NOT NULL auto_increment,
  `GROUP_NAME` varchar(100) NOT NULL,
  `DAYS` varchar(9) NOT NULL,
  `TIMINGS` time default NULL,
  `TIME_UPDATED` datetime NOT NULL,
  `village_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `PERSON_GROUPS_village_id` (`village_id`)
) ENGINE=MyISAM AUTO_INCREMENT=149 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `PERSON_GROUPS`
--

LOCK TABLES `PERSON_GROUPS` WRITE;
/*!40000 ALTER TABLE `PERSON_GROUPS` DISABLE KEYS */;
INSERT INTO `PERSON_GROUPS` VALUES (78,'Prem','Tuesday',NULL,'2009-12-15 22:38:02',28),(77,'Niloni','Friday',NULL,'2009-12-15 22:49:13',27),(76,'Production farmer group','',NULL,'2009-12-12 05:44:31',26),(74,'Kiran','',NULL,'2009-12-11 01:03:30',24),(75,'Jyoti','',NULL,'2009-12-11 01:03:30',24),(117,'sreishakti mahila sangh','Monday',NULL,'2010-01-12 23:48:17',50),(118,'Sibasakti, Bholanath','Monday','18:00:00','2010-01-27 04:14:14',52),(119,'Maa Tulashi, Baba Mukteswara','Tuesday','18:00:00','2010-01-27 04:00:51',52),(120,'Gajalaxmi, Maa Tarini','Wednesday','18:00:00','2010-01-27 03:54:22',52),(121,'Balhe Sagen, Aang Marshal','Saturday','17:00:00','2010-01-27 03:48:03',53),(79,'Sugandh','Tuesday',NULL,'2009-12-15 22:28:19',28),(80,'Turtan Singh','Tuesday',NULL,'2009-12-15 22:13:33',28),(81,'Sivasakthi','Sunday',NULL,'2009-12-15 22:07:52',29),(82,'Production farmer group 1','',NULL,'2009-12-15 23:47:22',30),(83,'Production farmer group 2','',NULL,'2009-12-16 01:07:25',25),(84,'Production farmer group 3','',NULL,'2009-12-16 01:05:53',25),(85,'Amarnath Kisan Samu','Wednesday','17:00:00','2009-12-23 20:57:04',38),(86,'Shree Ganesh Kisan Samu','',NULL,'2009-12-23 21:02:00',39),(87,'Kisan Samu','Friday','17:00:00','2009-12-23 21:03:12',40),(88,'Amarnath Kisan Samu','Wednesday',NULL,'2009-12-23 21:27:13',38),(89,'Shri Jagadguru Panchacharya sangh','',NULL,'2010-01-04 23:28:34',43),(90,'Mohammad Paigambar mahila SHG','',NULL,'2010-01-04 23:28:34',43),(91,'AAkkamahadevi Mahila swa sahay sangh','',NULL,'2010-01-04 23:28:34',43),(92,' Shri Gramadevi mahila SHG','',NULL,'2010-01-04 23:36:52',44),(93,' Shri Ranichennamma SHG','',NULL,'2010-01-04 23:36:52',44),(94,' Shri Saraswati Strishakti sangh','',NULL,'2010-01-04 23:36:52',44),(95,'Shri nidhi raitar kshetra patha shale Sangh ','',NULL,'2010-01-04 23:36:52',44),(96,'Shri Akkamahadevi Mahila Swasahay Sangh','',NULL,'2010-01-04 23:36:52',44),(97,'Shri Jagadguru Panchacharya sangh','',NULL,'2010-01-05 01:01:48',45),(98,'Mohammad Paigambar mahila SHG','',NULL,'2010-01-05 01:01:48',45),(99,'Mabusubani mahila SHG','',NULL,'2010-01-05 01:01:48',45),(100,'Akkamahadevi Mahila swa sahay sangh','',NULL,'2010-01-05 01:01:48',45),(101,'Narasimhdevar sangh','',NULL,'2010-01-05 01:15:38',46),(102,'Anandavana','',NULL,'2010-01-05 01:30:45',47),(103,'Ranichennmma mahila sangh','',NULL,'2010-01-05 01:30:45',47),(104,'Mate mahadevi Mahila sangh','',NULL,'2010-01-05 01:30:45',47),(105,'Neelambika Strishakti sangha','',NULL,'2010-01-05 01:33:56',48),(106,'Kalmeshwar Swasahay sangh','',NULL,'2010-01-05 01:33:56',48),(107,'Shri Annapurneshwari Mahila SHG','',NULL,'2010-01-05 01:33:56',48),(108,'Shri Akkamahadevi Mahila SHG','',NULL,'2010-01-05 01:38:56',49),(109,'Shri Mallikarjun purush SHG','',NULL,'2010-01-05 01:38:56',49),(110,'Shri Pandurang Vitthal purush SHG','',NULL,'2010-01-05 01:38:56',49),(111,'Shri Laxmi Mahila SHG','',NULL,'2010-01-05 01:38:56',49),(112,'Shri Adishakti Mahila SHG','',NULL,'2010-01-05 01:38:56',49),(113,'Janotthan Shri Gayatridevi Mahila SHG','',NULL,'2010-01-05 01:46:29',50),(114,'Janotthan Shri Hemaraddi Mahila SHG','',NULL,'2010-01-05 01:46:29',50),(115,'Shri Jatingeshwar SHG','',NULL,'2010-01-08 00:00:41',50),(116,'Public & Vijayalaxmi SHG','',NULL,'2010-01-07 23:19:03',50),(122,'Marangbanga, Dharitree','Sunday','18:00:00','2010-01-27 03:42:09',53),(146,'Marshal Mahila Mandal','',NULL,'2010-02-01 03:41:06',82),(124,'Maa Basuki Devi, Maa Santoshi','Thursday','18:30:00','2010-01-31 23:46:57',55),(125,'Sagun Sarna,Marshal Mahila Kendra','Friday','18:30:00','2010-01-27 02:57:24',56),(126,'Shiv Parbati, Kaa Shanti Niketan','Sunday','18:30:00','2010-01-27 02:51:59',57),(127,'Shivani,Bijal Bale Bijali Taras','Saturday','18:30:00','2010-01-27 02:43:57',58),(128,'Athra Deuli, Maa Laxmi','Tuesday','18:30:00','2010-01-27 02:10:32',59),(129,'Marangburu Samled,Sagar Serali','Sunday','18:30:00','2010-01-27 02:02:54',60),(130,'Maa Mangala, Maa Kichikeshwari','Monday','18:00:00','2010-01-31 23:35:44',62),(131,'Sri Krishna, Maa Tulashi','Friday','18:00:00','2010-01-31 23:19:12',62),(132,'Maa Gajabiani, Baitrani Om Maa Tarini','Saturday','18:00:00','2010-01-31 23:12:45',62),(133,'Maa Binapani, Maa Durga','Wednesday','18:00:00','2010-01-27 00:31:47',63),(134,'Sibasakti,Bholanath','Monday','18:00:00','2010-01-18 00:42:01',52),(145,'Fulwari Mahila Mandal','',NULL,'2010-02-01 03:36:59',81),(144,'Tiliye Baha','',NULL,'2010-02-01 03:32:46',80),(138,'Laxminarayan','Thursday','18:00:00','2010-01-27 05:19:35',67),(139,'Maa Parbati','Friday','18:00:00','2010-01-27 05:15:01',67),(140,'Maa Chandipat,Maa Tarini','Tuesday','18:00:00','2010-01-31 22:55:22',68),(141,'Maa Besauli,Laxminarayan','Wednesday','18:00:00','2010-01-31 22:45:45',68),(142,'Sarjamburu,Dinga Marshal,Maa Gouri Shree Chandyapat','Saturday','18:00:00','2010-01-27 05:00:48',69),(143,'Sarjamburu,Dinga Marshal,Maa Gouri Shree Chandyapat','Sunday','18:00:00','2010-01-27 04:54:00',69),(147,'Sarjom Baha Mahila Mandal','',NULL,'2010-02-01 03:43:46',83),(148,'Vina Mahila Mandal','',NULL,'2010-02-01 03:47:34',84);
/*!40000 ALTER TABLE `PERSON_GROUPS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PERSON_MEETING_ATTENDANCE`
--

DROP TABLE IF EXISTS `PERSON_MEETING_ATTENDANCE`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `PERSON_MEETING_ATTENDANCE` (
  `id` int(11) NOT NULL auto_increment,
  `screening_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  `expressed_interest_practice_id` int(11) default NULL,
  `EXPRESSED_INTEREST` longtext NOT NULL,
  `expressed_adoption_practice_id` int(11) default NULL,
  `EXPRESSED_ADOPTION` longtext NOT NULL,
  `expressed_question_practice_id` int(11) default NULL,
  `EXPRESSED_QUESTION` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `PERSON_MEETING_ATTENDANCE_screening_id` (`screening_id`),
  KEY `PERSON_MEETING_ATTENDANCE_person_id` (`person_id`),
  KEY `PERSON_MEETING_ATTENDANCE_expressed_interest_practice_id` (`expressed_interest_practice_id`),
  KEY `PERSON_MEETING_ATTENDANCE_expressed_adoption_practice_id` (`expressed_adoption_practice_id`),
  KEY `PERSON_MEETING_ATTENDANCE_expressed_question_practice_id` (`expressed_question_practice_id`)
) ENGINE=MyISAM AUTO_INCREMENT=96 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `PERSON_MEETING_ATTENDANCE`
--

LOCK TABLES `PERSON_MEETING_ATTENDANCE` WRITE;
/*!40000 ALTER TABLE `PERSON_MEETING_ATTENDANCE` DISABLE KEYS */;
INSERT INTO `PERSON_MEETING_ATTENDANCE` VALUES (28,24,109,9,'cauliflower transplantation',8,'',NULL,''),(29,24,110,9,'cauliflower transplantation',8,'',NULL,''),(30,24,106,8,'',8,'',NULL,''),(31,24,107,9,'cauliflower transplantation',8,'',NULL,''),(32,24,108,9,'cauliflower transplantation',8,'',NULL,''),(33,24,105,NULL,'',NULL,'',NULL,''),(34,24,111,NULL,'',NULL,'',NULL,''),(35,24,112,NULL,'',NULL,'',NULL,''),(36,24,113,NULL,'',NULL,'',NULL,''),(37,24,114,NULL,'',NULL,'',NULL,''),(38,24,115,NULL,'',NULL,'',NULL,''),(39,24,116,NULL,'',NULL,'',NULL,''),(40,24,117,NULL,'',NULL,'',NULL,''),(41,24,118,NULL,'',NULL,'',NULL,''),(42,24,119,9,'cauliflower transplantation',8,'',NULL,''),(43,24,120,9,'cauliflower transplantation',8,'',NULL,''),(44,24,121,NULL,'',NULL,'',NULL,''),(45,25,109,NULL,'',3,'Potato sowing',NULL,''),(46,25,110,NULL,'',3,'Potato sowing',NULL,''),(47,25,106,NULL,'',3,'Potato sowing',NULL,''),(48,25,107,NULL,'',3,'Potato sowing',NULL,''),(49,25,108,NULL,'',3,'Potato sowing',NULL,''),(50,25,105,8,'Cauliflower, cabbage nursery & transplantation',3,'Potato sowing',NULL,''),(51,25,111,8,'',3,'Potato sowing',NULL,''),(52,25,112,NULL,'',3,'Potato sowing',NULL,''),(53,25,114,NULL,'',3,'Potato sowing',NULL,''),(54,25,115,NULL,'',3,'Potato sowing',NULL,''),(55,25,116,NULL,'',3,'Potato sowing',NULL,''),(56,25,117,NULL,'',3,'Potato sowing',NULL,''),(57,25,118,NULL,'',3,'Potato sowing',NULL,''),(58,25,119,NULL,'',3,'Potato sowing',NULL,''),(59,25,120,NULL,'',3,'Potato sowing',NULL,''),(60,26,174,9,'',NULL,'',NULL,''),(61,26,175,9,'',NULL,'',NULL,''),(62,26,176,8,'cauliflower',3,'Potato sowing',NULL,''),(63,26,177,NULL,'',NULL,'',NULL,''),(64,26,178,NULL,'',3,'Potato sowing',NULL,''),(65,26,179,9,'cabbage & cauliflower',NULL,'',NULL,''),(66,26,180,9,'cabbage nursey & transplantation',NULL,'',NULL,''),(67,26,181,NULL,'',3,'Potato sowing',NULL,''),(68,26,182,NULL,'',NULL,'',NULL,''),(69,26,183,NULL,'',NULL,'',NULL,''),(70,26,184,NULL,'',NULL,'',NULL,''),(71,26,185,NULL,'',3,'Potato sowing',NULL,''),(72,26,186,NULL,'',NULL,'',NULL,''),(73,26,187,NULL,'',3,'Potato sowing',NULL,''),(74,26,188,9,'cabbage',NULL,'',NULL,''),(75,26,189,9,'cabbage',NULL,'',NULL,''),(76,26,190,9,'cauliflower nursery & transplantation',NULL,'',NULL,''),(77,26,191,9,'cabbage',NULL,'',NULL,''),(78,27,174,NULL,'',NULL,'',NULL,''),(79,27,175,NULL,'',NULL,'',NULL,''),(80,27,176,9,'ca',NULL,'',NULL,''),(81,27,177,NULL,'',NULL,'',NULL,''),(82,27,178,9,'',NULL,'',NULL,''),(83,27,179,NULL,'',NULL,'',NULL,''),(84,27,180,NULL,'',NULL,'',NULL,''),(85,27,181,NULL,'',NULL,'',NULL,''),(86,27,182,NULL,'',NULL,'',NULL,''),(87,27,183,NULL,'',NULL,'',NULL,''),(88,27,184,NULL,'',NULL,'',NULL,''),(89,27,185,NULL,'',NULL,'',NULL,''),(90,27,186,NULL,'',NULL,'',NULL,''),(91,27,187,NULL,'',NULL,'',NULL,''),(92,27,188,NULL,'',NULL,'',NULL,''),(93,27,189,NULL,'',NULL,'',NULL,''),(94,27,190,NULL,'',NULL,'',NULL,''),(95,27,191,NULL,'',NULL,'',NULL,'');
/*!40000 ALTER TABLE `PERSON_MEETING_ATTENDANCE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PERSON_RELATIONS`
--

DROP TABLE IF EXISTS `PERSON_RELATIONS`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `PERSON_RELATIONS` (
  `id` int(11) NOT NULL auto_increment,
  `person_id` int(11) NOT NULL,
  `relative_id` int(11) NOT NULL,
  `TYPE_OF_RELATIONSHIP` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `PERSON_RELATIONS_person_id` (`person_id`),
  KEY `PERSON_RELATIONS_relative_id` (`relative_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `PERSON_RELATIONS`
--

LOCK TABLES `PERSON_RELATIONS` WRITE;
/*!40000 ALTER TABLE `PERSON_RELATIONS` DISABLE KEYS */;
/*!40000 ALTER TABLE `PERSON_RELATIONS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRACTICES`
--

DROP TABLE IF EXISTS `PRACTICES`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `PRACTICES` (
  `id` int(11) NOT NULL auto_increment,
  `PRACTICE_NAME` varchar(200) NOT NULL,
  `SEASONALITY` varchar(3) NOT NULL,
  `SUMMARY` longtext NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `PRACTICES`
--

LOCK TABLES `PRACTICES` WRITE;
/*!40000 ALTER TABLE `PRACTICES` DISABLE KEYS */;
INSERT INTO `PRACTICES` VALUES (1,'Vermicompost','Kha',''),(2,'Harvesting','Kha',''),(3,'Sowing','Rab',''),(6,'Intercultural','Rou',''),(10,'Duck care and treatment','Kha',''),(8,'Nursery','Rou',''),(9,'Transplantation','Rou',''),(11,'Insecticidal treatment','Rab','');
/*!40000 ALTER TABLE `PRACTICES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REGION`
--

DROP TABLE IF EXISTS `REGION`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `REGION` (
  `id` int(11) NOT NULL auto_increment,
  `REGION_NAME` varchar(100) NOT NULL,
  `START_DATE` date default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `REGION`
--

LOCK TABLES `REGION` WRITE;
/*!40000 ALTER TABLE `REGION` DISABLE KEYS */;
INSERT INTO `REGION` VALUES (1,'Pioneers ',NULL),(2,'Crusaders',NULL),(3,'Beacons ',NULL);
/*!40000 ALTER TABLE `REGION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REVIEWER`
--

DROP TABLE IF EXISTS `REVIEWER`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `REVIEWER` (
  `id` int(11) NOT NULL auto_increment,
  `REVIEWER_NAME` varchar(100) NOT NULL,
  `REVIEWER_COMMENTS` longtext NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `REVIEWER`
--

LOCK TABLES `REVIEWER` WRITE;
/*!40000 ALTER TABLE `REVIEWER` DISABLE KEYS */;
/*!40000 ALTER TABLE `REVIEWER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SCREENING`
--

DROP TABLE IF EXISTS `SCREENING`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `SCREENING` (
  `id` int(11) NOT NULL auto_increment,
  `DATE` date NOT NULL,
  `START_TIME` time NOT NULL,
  `END_TIME` time NOT NULL,
  `LOCATION` varchar(200) NOT NULL,
  `TARGET_PERSON_ATTENDANCE` int(11) default NULL,
  `TARGET_AUDIENCE_INTEREST` int(11) default NULL,
  `TARGET_ADOPTIONS` int(11) default NULL,
  `village_id` int(11) NOT NULL,
  `fieldofficer_id` int(11) default NULL,
  `animator_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `SCREENING_village_id` (`village_id`),
  KEY `SCREENING_fieldofficer_id` (`fieldofficer_id`),
  KEY `SCREENING_animator_id` (`animator_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `SCREENING`
--

LOCK TABLES `SCREENING` WRITE;
/*!40000 ALTER TABLE `SCREENING` DISABLE KEYS */;
INSERT INTO `SCREENING` VALUES (26,'2009-11-13','07:00:00','08:30:00','',NULL,NULL,NULL,27,3,35),(25,'2009-11-15','07:00:00','08:30:00','',NULL,NULL,NULL,29,3,39),(24,'2009-11-22','07:00:00','08:30:00','School',NULL,NULL,NULL,29,3,39),(27,'2009-11-20','07:00:00','08:30:00','',NULL,NULL,NULL,27,NULL,35);
/*!40000 ALTER TABLE `SCREENING` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SCREENING_farmer_groups_targeted`
--

DROP TABLE IF EXISTS `SCREENING_farmer_groups_targeted`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `SCREENING_farmer_groups_targeted` (
  `id` int(11) NOT NULL auto_increment,
  `screening_id` int(11) NOT NULL,
  `persongroups_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `screening_id` (`screening_id`,`persongroups_id`),
  KEY `persongroups_id_refs_id_512348e` (`persongroups_id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `SCREENING_farmer_groups_targeted`
--

LOCK TABLES `SCREENING_farmer_groups_targeted` WRITE;
/*!40000 ALTER TABLE `SCREENING_farmer_groups_targeted` DISABLE KEYS */;
INSERT INTO `SCREENING_farmer_groups_targeted` VALUES (27,26,77),(26,25,81),(25,24,81),(30,27,0);
/*!40000 ALTER TABLE `SCREENING_farmer_groups_targeted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SCREENING_videoes_screened`
--

DROP TABLE IF EXISTS `SCREENING_videoes_screened`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `SCREENING_videoes_screened` (
  `id` int(11) NOT NULL auto_increment,
  `screening_id` int(11) NOT NULL,
  `video_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `screening_id` (`screening_id`,`video_id`),
  KEY `video_id_refs_id_123d9047` (`video_id`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `SCREENING_videoes_screened`
--

LOCK TABLES `SCREENING_videoes_screened` WRITE;
/*!40000 ALTER TABLE `SCREENING_videoes_screened` DISABLE KEYS */;
INSERT INTO `SCREENING_videoes_screened` VALUES (31,27,19),(30,27,18),(29,26,17),(28,25,17),(27,24,19);
/*!40000 ALTER TABLE `SCREENING_videoes_screened` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `STATE`
--

DROP TABLE IF EXISTS `STATE`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `STATE` (
  `id` int(11) NOT NULL auto_increment,
  `STATE_NAME` varchar(100) NOT NULL,
  `region_id` int(11) NOT NULL,
  `START_DATE` date default NULL,
  PRIMARY KEY  (`id`),
  KEY `STATE_region_id` (`region_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `STATE`
--

LOCK TABLES `STATE` WRITE;
/*!40000 ALTER TABLE `STATE` DISABLE KEYS */;
INSERT INTO `STATE` VALUES (1,'Madhya Pradesh',1,NULL),(2,'Jharkhand',2,NULL),(3,'Orissa',2,NULL),(4,'West Bengal',2,NULL),(5,'Karnataka',3,NULL);
/*!40000 ALTER TABLE `STATE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TRAINING`
--

DROP TABLE IF EXISTS `TRAINING`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `TRAINING` (
  `id` int(11) NOT NULL auto_increment,
  `TRAINING_PURPOSE` longtext NOT NULL,
  `TRAINING_OUTCOME` longtext NOT NULL,
  `TRAINING_START_DATE` date default NULL,
  `TRAINING_END_DATE` date default NULL,
  `village_id` int(11) NOT NULL,
  `dm_id` int(11) NOT NULL,
  `fieldofficer_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `TRAINING_village_id` (`village_id`),
  KEY `TRAINING_dm_id` (`dm_id`),
  KEY `TRAINING_fieldofficer_id` (`fieldofficer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `TRAINING`
--

LOCK TABLES `TRAINING` WRITE;
/*!40000 ALTER TABLE `TRAINING` DISABLE KEYS */;
/*!40000 ALTER TABLE `TRAINING` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TRAINING_animators_trained`
--

DROP TABLE IF EXISTS `TRAINING_animators_trained`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `TRAINING_animators_trained` (
  `id` int(11) NOT NULL auto_increment,
  `training_id` int(11) NOT NULL,
  `animator_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `training_id` (`training_id`,`animator_id`),
  KEY `animator_id_refs_id_630d4e47` (`animator_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `TRAINING_animators_trained`
--

LOCK TABLES `TRAINING_animators_trained` WRITE;
/*!40000 ALTER TABLE `TRAINING_animators_trained` DISABLE KEYS */;
/*!40000 ALTER TABLE `TRAINING_animators_trained` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VIDEO`
--

DROP TABLE IF EXISTS `VIDEO`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `VIDEO` (
  `id` int(11) NOT NULL auto_increment,
  `TITLE` varchar(200) NOT NULL,
  `VIDEO_TYPE` int(11) NOT NULL,
  `DURATION` time default NULL,
  `language_id` int(11) NOT NULL,
  `SUMMARY` longtext NOT NULL,
  `PICTURE_QUALITY` varchar(200) NOT NULL,
  `AUDIO_QUALITY` varchar(200) NOT NULL,
  `EDITING_QUALITY` varchar(200) NOT NULL,
  `EDIT_START_DATE` date default NULL,
  `EDIT_FINISH_DATE` date default NULL,
  `THEMATIC_QUALITY` varchar(200) NOT NULL,
  `VIDEO_PRODUCTION_START_DATE` date NOT NULL,
  `VIDEO_PRODUCTION_END_DATE` date NOT NULL,
  `STORYBASE` int(11) NOT NULL,
  `STORYBOARD_FILENAME` varchar(100) NOT NULL,
  `RAW_FILENAME` varchar(100) NOT NULL,
  `MOVIE_MAKER_PROJECT_FILENAME` varchar(100) NOT NULL,
  `FINAL_EDITED_FILENAME` varchar(100) NOT NULL,
  `village_id` int(11) NOT NULL,
  `facilitator_id` int(11) NOT NULL,
  `cameraoperator_id` int(11) NOT NULL,
  `reviewer_id` int(11) default NULL,
  `APPROVAL_DATE` date default NULL,
  `supplementary_video_produced_id` int(11) default NULL,
  `VIDEO_SUITABLE_FOR` int(11) NOT NULL,
  `REMARKS` longtext NOT NULL,
  `ACTORS` varchar(1) NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `VIDEO_language_id` (`language_id`),
  KEY `VIDEO_village_id` (`village_id`),
  KEY `VIDEO_facilitator_id` (`facilitator_id`),
  KEY `VIDEO_cameraoperator_id` (`cameraoperator_id`),
  KEY `VIDEO_reviewer_id` (`reviewer_id`),
  KEY `VIDEO_supplementary_video_produced_id` (`supplementary_video_produced_id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `VIDEO`
--

LOCK TABLES `VIDEO` WRITE;
/*!40000 ALTER TABLE `VIDEO` DISABLE KEYS */;
INSERT INTO `VIDEO` VALUES (17,'Potato sowing',1,NULL,4,'','','','',NULL,NULL,'','2009-10-28','2009-11-16',1,'','','','',25,34,34,NULL,NULL,NULL,1,'','I','2009-12-16 00:22:32'),(16,'Green-Pea Sowing',1,NULL,4,'','','','',NULL,NULL,'','2009-11-17','2009-11-17',1,'','','','',30,41,34,NULL,NULL,NULL,1,'','I','2009-12-15 23:58:46'),(15,'cabbage intercultural',1,NULL,3,'','','','',NULL,NULL,'','2009-11-19','2009-12-19',1,'','','','',26,34,34,NULL,NULL,NULL,1,'','I','2009-12-15 22:53:49'),(22,'7 days duck feed and treatment',1,NULL,125,'','','','',NULL,NULL,'','2009-09-01','2009-09-01',1,'','','','',62,59,63,NULL,NULL,NULL,1,'','I','2010-01-31 22:30:17'),(14,'Potato intercultural',1,NULL,3,'','','','',NULL,NULL,'','2009-11-19','2009-11-19',1,'','','','',26,34,34,NULL,NULL,NULL,1,'','I','2009-12-12 08:47:19'),(18,'cabbage nursery',1,NULL,3,'','','','',NULL,NULL,'','2009-10-10','2009-10-23',1,'','','','',25,34,34,NULL,NULL,NULL,1,'','I','2009-12-17 07:25:44'),(19,'cauliflower nursery',1,NULL,3,'','','','',NULL,NULL,'','2009-10-01','2009-10-23',1,'','','','',25,34,34,NULL,NULL,NULL,1,'','I','2009-12-16 02:29:12'),(20,'cabbage transplantation',1,NULL,3,'','','','',NULL,NULL,'','2009-10-01','2009-10-07',1,'','','','',26,40,34,NULL,NULL,NULL,1,'','I','2009-12-16 02:42:34'),(21,'Makha Harvest',1,NULL,128,'This movie deals with the harvest of corn. When you should harvest your planet?  How you know when to harvest your crop.  Once you have harvested, when and where should you appropriately store your corn.  If you harvest on time, however end up leaving your cobs in the wrong place they will end up with disease and your crop will be lost. ','Good','Good','Great','2009-11-03','2010-01-01','','2009-10-01','2010-01-02',1,'','','','',38,47,47,NULL,NULL,NULL,4,'','F','2010-01-10 01:58:36'),(23,'7 days duck feed and treatment',1,NULL,123,'','','','',NULL,NULL,'','2009-09-01','2009-09-01',1,'','','','',62,63,59,NULL,NULL,NULL,1,'','I','2010-01-31 22:37:09');
/*!40000 ALTER TABLE `VIDEO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VIDEO_farmers_shown`
--

DROP TABLE IF EXISTS `VIDEO_farmers_shown`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `VIDEO_farmers_shown` (
  `id` int(11) NOT NULL auto_increment,
  `video_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `video_id` (`video_id`,`person_id`),
  KEY `person_id_refs_id_3825c139` (`person_id`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `VIDEO_farmers_shown`
--

LOCK TABLES `VIDEO_farmers_shown` WRITE;
/*!40000 ALTER TABLE `VIDEO_farmers_shown` DISABLE KEYS */;
INSERT INTO `VIDEO_farmers_shown` VALUES (26,17,193),(25,16,192),(23,14,104),(24,15,104),(33,22,283),(28,19,194),(31,18,194),(29,20,104),(32,21,195),(34,23,931);
/*!40000 ALTER TABLE `VIDEO_farmers_shown` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VIDEO_related_agricultural_practices`
--

DROP TABLE IF EXISTS `VIDEO_related_agricultural_practices`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `VIDEO_related_agricultural_practices` (
  `id` int(11) NOT NULL auto_increment,
  `video_id` int(11) NOT NULL,
  `practices_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `video_id` (`video_id`,`practices_id`),
  KEY `practices_id_refs_id_71dca078` (`practices_id`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `VIDEO_related_agricultural_practices`
--

LOCK TABLES `VIDEO_related_agricultural_practices` WRITE;
/*!40000 ALTER TABLE `VIDEO_related_agricultural_practices` DISABLE KEYS */;
INSERT INTO `VIDEO_related_agricultural_practices` VALUES (22,16,3),(20,14,6),(30,22,10),(21,15,6),(28,18,8),(23,17,3),(25,19,8),(26,20,9),(29,21,2),(31,23,10);
/*!40000 ALTER TABLE `VIDEO_related_agricultural_practices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VILLAGE`
--

DROP TABLE IF EXISTS `VILLAGE`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `VILLAGE` (
  `id` int(11) NOT NULL auto_increment,
  `VILLAGE_NAME` varchar(100) NOT NULL,
  `block_id` int(11) NOT NULL,
  `NO_OF_HOUSEHOLDS` int(11) default NULL,
  `POPULATION` int(11) default NULL,
  `ROAD_CONNECTIVITY` varchar(100) NOT NULL,
  `CONTROL` tinyint(1) default NULL,
  `START_DATE` date default NULL,
  PRIMARY KEY  (`id`),
  KEY `VILLAGE_block_id` (`block_id`)
) ENGINE=MyISAM AUTO_INCREMENT=85 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `VILLAGE`
--

LOCK TABLES `VILLAGE` WRITE;
/*!40000 ALTER TABLE `VILLAGE` DISABLE KEYS */;
INSERT INTO `VILLAGE` VALUES (28,'Kinsu',9,NULL,NULL,'',0,NULL),(27,'Gufu',9,NULL,NULL,'',0,NULL),(26,'Tati',9,NULL,NULL,'',NULL,NULL),(25,'Jibilong',9,NULL,NULL,'',0,NULL),(24,'Navatoli 1',9,NULL,NULL,'',0,NULL),(73,'Jhunriposhi',13,NULL,NULL,'',NULL,NULL),(52,'Deuli',12,NULL,NULL,'',0,NULL),(29,'Gopla',9,NULL,NULL,'',0,NULL),(30,'Bandhu',9,NULL,NULL,'',NULL,NULL),(31,'Lohajimi',9,NULL,NULL,'',NULL,NULL),(32,'Kajurdag',9,NULL,NULL,'',NULL,NULL),(33,'Mansingpura',4,NULL,NULL,'Good',NULL,NULL),(34,'Neemkhada',4,NULL,NULL,'Good',NULL,NULL),(35,'Kisanghar',4,NULL,NULL,'',NULL,NULL),(37,'Pandutalab',4,NULL,NULL,'Good',NULL,NULL),(38,'Sitapuri (Small)',4,NULL,NULL,'Bad',NULL,'2009-11-11'),(39,'Shampura',4,NULL,NULL,'',NULL,NULL),(40,'Semli',4,NULL,NULL,'',NULL,NULL),(41,'Jamasindh',4,NULL,NULL,'',NULL,NULL),(42,'Bisali',4,NULL,NULL,'',NULL,NULL),(43,'SS Koppa',15,NULL,NULL,'',NULL,NULL),(44,'kamplikoppa',25,NULL,NULL,'',NULL,NULL),(45,'BN Koppa',25,NULL,NULL,'',NULL,NULL),(46,'Dastikoppa',26,NULL,NULL,'',0,NULL),(47,'Hirehonnalli',26,NULL,NULL,'',NULL,NULL),(48,'Ganjigatti',25,NULL,NULL,'',NULL,NULL),(49,'Huniskatte',25,NULL,NULL,'',0,NULL),(50,'Mukkal',25,NULL,NULL,'',0,NULL),(53,'Baria',12,NULL,NULL,'',0,NULL),(72,'Palsagadia',12,NULL,NULL,'',NULL,NULL),(55,'Ektali',13,NULL,NULL,'',0,NULL),(56,'Mangarh',13,NULL,NULL,'',0,NULL),(57,'Basantpur_Naiksahi',13,NULL,NULL,'',0,NULL),(58,'Basantpur',13,NULL,NULL,'',0,NULL),(59,'Kumdabadi',13,NULL,NULL,'',0,NULL),(60,'Kanthikena',13,NULL,NULL,'',0,NULL),(74,'Rangalbeda',12,NULL,NULL,'',NULL,NULL),(62,'Khandbandha',13,NULL,NULL,'',0,NULL),(63,'Badaposhi',13,NULL,NULL,'',0,NULL),(75,'Badhubheda',12,NULL,NULL,'',NULL,NULL),(71,'Kaluakhaman',13,NULL,NULL,'',0,NULL),(67,'Ramchandrapur',12,NULL,NULL,'',0,NULL),(68,'Chandusahi',12,NULL,NULL,'',0,NULL),(69,'Dumbisahi',12,NULL,NULL,'',0,NULL),(70,'Kendumundhi',12,NULL,NULL,'',NULL,NULL),(76,'Diajodi',12,NULL,NULL,'',NULL,NULL),(77,'Tangabila',13,NULL,NULL,'',NULL,NULL),(78,'Dhuduku',13,NULL,NULL,'',NULL,NULL),(79,'Bisipur',13,NULL,NULL,'',NULL,NULL),(80,'Sundari bhosatoli',9,NULL,NULL,'',0,NULL),(81,'sundari pakartoli',9,NULL,NULL,'',0,NULL),(82,'Kokiya',9,NULL,NULL,'',0,NULL),(83,'Prachartoli',9,NULL,NULL,'',0,NULL),(84,'Tirla',9,NULL,NULL,'',0,NULL);
/*!40000 ALTER TABLE `VILLAGE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Field Officer'),(2,'Development Manager');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_5886d21f` (`permission_id`)
) ENGINE=MyISAM AUTO_INCREMENT=148 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (146,1,94),(145,1,92),(144,1,91),(143,1,89),(142,1,88),(141,1,86),(140,1,85),(139,1,83),(138,1,82),(137,1,80),(136,1,79),(135,1,77),(134,1,76),(133,1,71),(132,1,70),(131,1,68),(130,1,67),(129,1,65),(128,1,64),(127,1,62),(126,1,61),(125,1,59),(124,1,58),(123,1,56),(122,1,55),(121,1,50),(120,1,49),(119,1,47),(118,1,46),(117,1,44),(116,1,43),(115,1,41),(114,1,29),(113,1,28),(110,2,92),(109,2,91),(108,2,89),(107,2,88),(106,2,86),(105,2,85),(104,2,83),(103,2,82),(102,2,80),(101,2,79),(100,2,77),(99,2,76),(98,2,74),(97,2,73),(96,2,71),(95,2,70),(94,2,68),(93,2,67),(92,2,66),(91,2,65),(90,2,64),(89,2,62),(88,2,61),(87,2,59),(86,2,58),(85,2,56),(84,2,55),(83,2,53),(82,2,52),(81,2,50),(80,2,49),(79,2,47),(78,2,46),(77,2,44),(76,2,43),(75,2,32),(74,2,29),(73,2,28),(111,2,94),(112,2,95),(147,1,95);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_message_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=604 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=100 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add message',5,'add_message'),(14,'Can change message',5,'change_message'),(15,'Can delete message',5,'delete_message'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add region',8,'add_region'),(23,'Can change region',8,'change_region'),(24,'Can delete region',8,'delete_region'),(25,'Can add equipment holder',9,'add_equipmentholder'),(26,'Can change equipment holder',9,'change_equipmentholder'),(27,'Can delete equipment holder',9,'delete_equipmentholder'),(28,'Can add reviewer',10,'add_reviewer'),(29,'Can change reviewer',10,'change_reviewer'),(30,'Can delete reviewer',10,'delete_reviewer'),(31,'Can add development manager',11,'add_developmentmanager'),(32,'Can change development manager',11,'change_developmentmanager'),(33,'Can delete development manager',11,'delete_developmentmanager'),(34,'Can add state',12,'add_state'),(35,'Can change state',12,'change_state'),(36,'Can delete state',12,'delete_state'),(37,'Can add partners',13,'add_partners'),(38,'Can change partners',13,'change_partners'),(39,'Can delete partners',13,'delete_partners'),(40,'Can add field officer',14,'add_fieldofficer'),(41,'Can change field officer',14,'change_fieldofficer'),(42,'Can delete field officer',14,'delete_fieldofficer'),(43,'Can add district',15,'add_district'),(44,'Can change district',15,'change_district'),(45,'Can delete district',15,'delete_district'),(46,'Can add block',16,'add_block'),(47,'Can change block',16,'change_block'),(48,'Can delete block',16,'delete_block'),(49,'Can add village',17,'add_village'),(50,'Can change village',17,'change_village'),(51,'Can delete village',17,'delete_village'),(52,'Can add monthly cost per village',18,'add_monthlycostpervillage'),(53,'Can change monthly cost per village',18,'change_monthlycostpervillage'),(54,'Can delete monthly cost per village',18,'delete_monthlycostpervillage'),(55,'Can add person groups',19,'add_persongroups'),(56,'Can change person groups',19,'change_persongroups'),(57,'Can delete person groups',19,'delete_persongroups'),(58,'Can add person',20,'add_person'),(59,'Can change person',20,'change_person'),(60,'Can delete person',20,'delete_person'),(61,'Can add person relations',21,'add_personrelations'),(62,'Can change person relations',21,'change_personrelations'),(63,'Can delete person relations',21,'delete_personrelations'),(64,'Can add animator',22,'add_animator'),(65,'Can change animator',22,'change_animator'),(66,'Can delete animator',22,'delete_animator'),(67,'Can add training',23,'add_training'),(68,'Can change training',23,'change_training'),(69,'Can delete training',23,'delete_training'),(70,'Can add animator assigned village',24,'add_animatorassignedvillage'),(71,'Can change animator assigned village',24,'change_animatorassignedvillage'),(72,'Can delete animator assigned village',24,'delete_animatorassignedvillage'),(73,'Can add animator salary per month',25,'add_animatorsalarypermonth'),(74,'Can change animator salary per month',25,'change_animatorsalarypermonth'),(75,'Can delete animator salary per month',25,'delete_animatorsalarypermonth'),(76,'Can add language',26,'add_language'),(77,'Can change language',26,'change_language'),(78,'Can delete language',26,'delete_language'),(79,'Can add video',27,'add_video'),(80,'Can change video',27,'change_video'),(81,'Can delete video',27,'delete_video'),(82,'Can add practices',28,'add_practices'),(83,'Can change practices',28,'change_practices'),(84,'Can delete practices',28,'delete_practices'),(85,'Can add screening',29,'add_screening'),(86,'Can change screening',29,'change_screening'),(87,'Can delete screening',29,'delete_screening'),(88,'Can add person meeting attendance',30,'add_personmeetingattendance'),(89,'Can change person meeting attendance',30,'change_personmeetingattendance'),(90,'Can delete person meeting attendance',30,'delete_personmeetingattendance'),(91,'Can add person adopt practice',31,'add_personadoptpractice'),(92,'Can change person adopt practice',31,'change_personadoptpractice'),(93,'Can delete person adopt practice',31,'delete_personadoptpractice'),(94,'Can add equipment id',32,'add_equipmentid'),(95,'Can change equipment id',32,'change_equipmentid'),(96,'Can delete equipment id',32,'delete_equipmentid'),(97,'Can add random',33,'add_random'),(98,'Can change random',33,'change_random'),(99,'Can delete random',33,'delete_random');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'digitalgreen','','','dg@digitalgreen.org','sha1$3f48d$2f5f291662df3f33e06e9f6929f3ffcbcc9b9fcd',1,1,1,'2010-01-31 05:05:35','2009-08-21 07:43:36'),(2,'development_manager','','','','sha1$581bb$5eaa974a972b014114126572145280d5d4d5a147',1,1,0,'2009-10-12 02:58:15','2009-08-25 11:12:13'),(3,'field_officer','','','','sha1$c9bff$35f5eab360e9113ebc6a780d7fdfcd6619e24f1e',1,1,0,'2010-01-31 05:06:39','2009-08-25 11:14:45'),(4,'satyam','','','','sha1$db6fc$d5ab2748c88285bbc7f2582f977c58362b5580c3',1,1,0,'2009-10-22 12:28:59','2009-10-12 14:32:07'),(5,'archana','','','','sha1$4a949$8455e2f12b4ea32b042176edb4060177100ed88f',1,1,0,'2010-01-14 04:43:18','2009-10-12 14:33:43'),(6,'ramachandra','','','','sha1$40d5a$e2c6c432f7ccf6d93c37328d10dc009ff11e39f2',1,1,0,'2009-10-26 04:28:29','2009-10-12 14:34:29'),(7,'chandrashekhar','','','','sha1$b993f$611432113fe34d2354b39753b77c78fdb3ce6b43',1,1,0,'2010-02-01 04:20:07','2009-10-12 14:36:40'),(8,'muthumari','','','','sha1$4b579$4d2e4dafe374ebcf241d806745ecaf862a57664e',1,1,0,'2010-02-01 03:30:17','2009-10-12 14:37:54'),(9,'abhishek','','','','sha1$5203e$9452ac231c8a5caa3bfb12a72faf618714684612',1,1,0,'2010-01-15 21:59:13','2009-10-12 14:38:21'),(10,'kevin','','','','sha1$8b18a$1cf2133582e9dc4b22dfe9b939c09f9ba89f7af0',1,1,0,'2010-01-07 19:51:15','2009-10-12 14:38:36'),(11,'nadagouda','','','','sha1$2ddd9$1f7c4d439d3042fdb98f34b53027f784d947daa7',1,1,0,'2009-11-05 03:52:19','2009-10-12 14:41:48'),(12,'avinash','','','','sha1$71ae1$957dc33a382032189f1a21f4c84318d7321311a7',1,1,0,'2009-11-02 11:02:37','2009-10-12 14:42:27'),(13,'gulzar','','','','sha1$7623a$043277e6f00d7fb7fca6e61d23c2f7c9fdeee109',1,1,0,'2009-10-22 12:08:45','2009-10-12 14:43:10');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f116770` (`group_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,2),(2,3,1),(7,10,1),(4,9,1),(5,5,1),(6,7,1),(8,8,1),(9,6,1),(10,4,1),(11,11,2),(12,12,2),(13,13,2);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_random`
--

DROP TABLE IF EXISTS `dashboard_random`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `dashboard_random` (
  `id` int(11) NOT NULL auto_increment,
  `random_no` varchar(300) NOT NULL,
  `random_date` date default NULL,
  `radom_time` time default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `dashboard_random`
--

LOCK TABLES `dashboard_random` WRITE;
/*!40000 ALTER TABLE `dashboard_random` DISABLE KEYS */;
INSERT INTO `dashboard_random` VALUES (1,'asdsa','2009-08-27','20:52:06'),(2,'dsfsd','2009-08-27','20:54:42'),(3,'sxasdasdas','2009-08-27','20:54:52'),(4,'2','2009-08-10','06:00:00'),(5,'5','2009-08-10','06:00:00'),(6,'csd','2009-08-31','17:44:52'),(7,'csd','2009-08-31','17:44:52'),(8,'csd','2009-08-31','17:44:52');
/*!40000 ALTER TABLE `dashboard_random` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL auto_increment,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=856 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2009-08-21 07:44:28',1,8,'1','Region1',1,''),(2,'2009-08-21 07:44:34',1,8,'2','Region2',1,''),(3,'2009-08-21 07:44:40',1,8,'3','Region3',1,''),(4,'2009-08-21 07:45:09',1,11,'1','asd',1,''),(5,'2009-08-21 07:45:32',1,11,'1','asd',3,''),(6,'2009-08-21 07:47:58',1,11,'2','Mr. Gulzar',1,''),(7,'2009-08-21 07:48:33',1,11,'3','Mr. Avinash',1,''),(8,'2009-08-21 07:48:56',1,11,'4','Dr. Nadagouda',1,''),(9,'2009-08-21 07:49:46',1,12,'1','Madhya Pradesh',1,''),(10,'2009-08-21 07:49:59',1,12,'2','Jharkhand',1,''),(11,'2009-08-21 07:50:07',1,12,'3','Orissa',1,''),(12,'2009-08-21 07:50:16',1,12,'4','West Bengal',1,''),(13,'2009-08-21 07:50:24',1,12,'5','Karnataka',1,''),(14,'2009-08-21 07:51:14',1,14,'1','Kevin Gandhi',1,''),(15,'2009-08-21 07:51:33',1,14,'2','Abhishek',1,''),(16,'2009-08-21 07:52:12',1,14,'3','Muthumari',1,''),(17,'2009-08-21 07:52:31',1,14,'4','Chandrashekhar',1,''),(18,'2009-08-21 07:52:46',1,14,'5','Ramachandra',1,''),(19,'2009-08-21 07:52:58',1,14,'6','Archana',1,''),(20,'2009-08-21 07:53:30',1,13,'1','PRADAN',1,''),(21,'2009-08-21 07:53:48',1,13,'2','BAIF',1,''),(22,'2009-08-21 07:54:08',1,13,'3','GREEN Foundation',1,''),(23,'2009-08-21 07:54:25',1,13,'4','SPS',1,''),(24,'2009-08-21 07:57:30',1,14,'7','Mr. Gulzar',1,''),(25,'2009-08-21 07:58:17',1,15,'1','Dindori ',1,''),(26,'2009-08-21 08:13:34',1,15,'2','Mandla ',1,''),(27,'2009-08-21 08:14:09',1,15,'3','Dewas',1,''),(28,'2009-08-21 08:14:48',1,15,'4','West Singhbum',1,''),(29,'2009-08-21 08:15:15',1,15,'5','Khunti ',1,''),(30,'2009-08-21 08:15:48',1,15,'6','Karanjia ',1,''),(31,'2009-08-21 08:16:30',1,14,'8','Mr. Avinash',1,''),(32,'2009-08-21 08:16:45',1,15,'7','Purulia ',1,''),(33,'2009-08-21 08:17:31',1,15,'8','Dharwad ',1,''),(34,'2009-08-21 08:18:07',1,14,'9','Dr. Nadagouda',1,''),(35,'2009-08-21 08:18:21',1,15,'9','Kushalnagar ',1,''),(36,'2009-08-21 08:18:50',1,15,'10','Bangalore Rural',1,''),(37,'2009-08-21 08:19:30',1,16,'1','Samnapur',1,''),(38,'2009-08-21 08:19:39',1,16,'2','Saka',1,''),(39,'2009-08-21 08:19:53',1,16,'3','Mogaon',1,''),(40,'2009-08-21 08:20:11',1,16,'4','Bagli',1,''),(41,'2009-08-21 08:20:27',1,16,'5','Amarpur',1,''),(42,'2009-08-21 08:20:39',1,16,'6','Chaibasa',1,''),(43,'2009-08-21 08:20:51',1,16,'7','Chakradhapur',1,''),(44,'2009-08-21 08:21:06',1,16,'8','Hatgamaria',1,''),(45,'2009-08-21 08:21:21',1,16,'9','Thorpa',1,''),(46,'2009-08-21 08:21:38',1,16,'10','Artiki',1,''),(47,'2009-08-21 08:21:48',1,16,'11','Muru',1,''),(48,'2009-08-21 08:22:02',1,16,'12','Karanjia',1,''),(49,'2009-08-21 08:22:14',1,16,'13','Jashipur',1,''),(50,'2009-08-21 08:22:32',1,16,'14','Purulia',1,''),(51,'2009-08-21 08:22:44',1,16,'15','Surshettikoppa',1,''),(52,'2009-08-21 08:22:54',1,16,'16','Kushalnagar',1,''),(53,'2009-08-21 08:23:05',1,16,'17','Kodugu',1,''),(54,'2009-08-21 08:23:17',1,16,'18','Hunsur',1,''),(55,'2009-08-21 08:23:28',1,16,'19','Kanakapura',1,''),(56,'2009-08-21 08:24:37',1,17,'1','temp1',1,''),(57,'2009-08-21 08:25:00',1,20,'1','person1',1,''),(58,'2009-08-21 08:25:55',1,19,'1','Group1',1,''),(59,'2009-08-21 08:26:27',1,22,'1','Animator1',1,''),(60,'2009-08-21 08:28:24',1,26,'1','Hindi',1,''),(61,'2009-08-21 08:28:31',1,26,'2','English',1,''),(62,'2009-08-21 08:28:46',1,26,'3','Mundari',1,''),(63,'2009-08-21 08:29:02',1,26,'4','Sadri',1,''),(64,'2009-08-21 08:32:26',1,28,'1','Vermicompost',1,''),(65,'2009-08-21 08:51:11',1,27,'1','Tomato Harvesting',1,''),(66,'2009-08-21 09:16:57',1,27,'1','Tomato Harvesting',2,'Changed storyboard_filename.'),(67,'2009-08-21 13:31:52',1,28,'2','Harvesting',1,''),(68,'2009-08-21 13:32:05',1,28,'3','Sowing',1,''),(69,'2009-08-21 13:32:27',1,20,'2','person2',1,''),(70,'2009-08-21 13:32:39',1,20,'3','person3',1,''),(71,'2009-08-21 13:33:01',1,20,'4','person4',1,''),(72,'2009-08-21 13:33:22',1,20,'5','person5',1,''),(73,'2009-08-21 13:33:39',1,20,'6','person6',1,''),(74,'2009-08-21 13:33:55',1,20,'7','person7',1,''),(75,'2009-08-21 13:34:10',1,20,'8','person8',1,''),(76,'2009-08-21 13:34:36',1,20,'9','person9',1,''),(77,'2009-08-21 13:34:53',1,20,'10','person10',1,''),(78,'2009-08-21 13:41:35',1,27,'2','Lac spraying ',1,''),(79,'2009-08-21 13:41:48',1,27,'2','Lac spraying ',2,'No fields changed.'),(80,'2009-08-21 13:54:15',1,17,'2','village1',1,''),(81,'2009-08-21 13:54:25',1,17,'3','village2',1,''),(82,'2009-08-21 13:54:34',1,17,'4','village3',1,''),(83,'2009-08-21 13:54:43',1,17,'5','village4',1,''),(84,'2009-08-21 13:54:56',1,17,'6','village5',1,''),(85,'2009-08-21 13:59:14',1,27,'3','Lac spraying and harvesting',1,''),(86,'2009-08-21 14:37:24',1,27,'4','video-temp',1,''),(87,'2009-08-22 03:51:31',1,29,'1','Screening object',1,''),(88,'2009-08-22 04:18:25',1,29,'2','Screening object',1,''),(89,'2009-08-23 00:26:37',1,29,'3','Screening object',1,''),(90,'2009-08-23 00:28:48',1,29,'3','2009-08-23 village1',2,'Added person meeting attendance \"PersonMeetingAttendance object\".'),(91,'2009-08-25 11:06:26',1,3,'1','Field Officer',1,''),(92,'2009-08-25 11:11:00',1,3,'2','Development Manager',1,''),(93,'2009-08-25 11:12:13',1,4,'2','development_manager',1,''),(94,'2009-08-25 11:14:08',1,4,'2','development_manager',2,'Changed is_staff and groups.'),(95,'2009-08-25 11:14:45',1,4,'3','field_officer',1,''),(96,'2009-08-25 11:15:18',1,4,'3','field_officer',2,'Changed is_staff and groups.'),(97,'2009-08-25 23:40:50',1,29,'3','2009-08-23 village1',2,'No fields changed.'),(98,'2009-08-27 08:22:36',1,33,'1','Random object',1,''),(99,'2009-08-27 08:25:10',1,33,'2','Random object',1,''),(100,'2009-08-27 08:25:20',1,33,'3','Random object',1,''),(101,'2009-08-29 04:05:01',1,22,'2','animator2',1,''),(102,'2009-08-31 00:28:59',1,33,'4','Random object',1,''),(103,'2009-08-31 00:35:50',1,33,'5','Random object',1,''),(104,'2009-08-31 05:18:55',1,33,'6','Random object',1,''),(105,'2009-08-31 05:19:26',1,33,'7','Random object',1,''),(106,'2009-08-31 05:19:41',1,33,'8','Random object',1,''),(107,'2009-09-02 05:57:00',1,27,'4','video-temp',2,'No fields changed.'),(108,'2009-09-02 05:57:37',1,27,'4','video-temp',2,'No fields changed.'),(109,'2009-09-04 02:44:14',1,11,'5','asd',1,''),(110,'2009-09-04 02:44:40',1,11,'5','asd',2,'No fields changed.'),(111,'2009-09-04 02:44:57',1,11,'5','asd',3,''),(112,'2009-09-04 05:45:07',1,11,'6','dssfdsfsdf',1,''),(113,'2009-09-04 05:45:46',1,11,'6','dssfdsfsdf',3,''),(114,'2009-09-07 04:57:15',1,22,'1','Animator1',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(115,'2009-09-09 10:00:17',1,22,'3','animator3',1,''),(116,'2009-09-10 09:05:46',1,11,'7','temp',1,''),(117,'2009-09-10 09:05:59',1,11,'7','temp',3,''),(118,'2009-09-11 00:36:39',1,29,'4','2009-09-11 village3',1,''),(119,'2009-09-11 00:40:09',1,29,'4','2009-09-11 village3',3,''),(120,'2009-09-11 04:26:48',1,29,'3','2009-08-23 village3',2,'Changed village and animator.'),(121,'2009-09-12 11:07:37',1,19,'2','temp',1,''),(122,'2009-09-12 11:45:44',1,11,'8','sdsada',1,''),(123,'2009-09-12 11:46:38',1,11,'9','sadasdasdasd',1,''),(124,'2009-09-12 11:46:49',1,11,'9','sadasdasdasd',3,''),(125,'2009-09-12 11:46:49',1,11,'8','sdsada',3,''),(126,'2009-09-13 00:38:37',1,5,'109','scs',1,''),(127,'2009-09-13 00:38:49',1,5,'109','scs',3,''),(128,'2009-09-15 03:52:39',1,29,'5','2009-09-15 village3',1,''),(129,'2009-09-15 03:52:56',1,29,'5','2009-09-15 village3',3,''),(130,'2009-09-15 03:54:50',1,29,'6','2009-09-15 temp1',1,''),(131,'2009-09-15 03:55:00',1,29,'6','2009-09-15 temp1',3,''),(132,'2009-09-15 03:56:01',1,22,'4','animator4',1,''),(133,'2009-09-15 03:56:11',1,29,'7','2009-09-15 temp1',1,''),(134,'2009-09-15 03:57:03',1,29,'7','2009-09-15 temp1',3,''),(135,'2009-09-17 04:21:32',1,19,'1','Group1',2,'Changed village.'),(136,'2009-09-17 04:22:09',1,20,'1','person1',2,'Changed group.'),(137,'2009-09-17 04:22:21',1,20,'2','person2',2,'Changed group.'),(138,'2009-09-17 04:22:31',1,20,'3','person3',2,'Changed group.'),(139,'2009-09-17 04:22:40',1,20,'4','person4',2,'Changed group.'),(140,'2009-09-18 02:16:57',1,29,'8','2009-09-18 village3',1,''),(141,'2009-09-18 02:34:08',1,29,'9','2009-09-18 temp1',1,''),(142,'2009-09-18 02:40:36',1,29,'10','2009-09-18 temp1',1,''),(143,'2009-09-18 03:20:15',1,29,'11','2009-09-18 temp1',1,''),(144,'2009-09-18 03:20:45',1,29,'11','2009-09-18 temp1',3,''),(145,'2009-09-18 03:24:11',1,29,'14','2009-09-18 temp1',1,''),(146,'2009-09-18 03:24:22',1,29,'14','2009-09-18 temp1',3,''),(147,'2009-09-18 03:31:48',1,29,'15','2009-09-18 village3',1,''),(148,'2009-09-18 03:33:43',1,29,'16','2009-09-18 village3',1,''),(149,'2009-09-18 03:34:51',1,29,'16','2009-09-18 village3',3,''),(150,'2009-09-18 03:34:51',1,29,'15','2009-09-18 village3',3,''),(151,'2009-09-19 01:29:28',1,17,'2','village1',2,'No fields changed.'),(152,'2009-09-19 01:59:35',1,17,'7','temp',1,''),(153,'2009-09-20 18:47:42',1,17,'8','sadsada',1,''),(154,'2009-09-20 18:47:59',1,17,'8','sadsada',3,''),(155,'2009-09-20 18:49:21',1,17,'9','Village6',1,''),(156,'2009-09-21 01:24:10',1,19,'12','dffsd',1,''),(157,'2009-09-21 01:24:24',1,19,'12','dffsd',3,''),(158,'2009-09-21 01:24:24',1,19,'11','sasda',3,''),(159,'2009-09-22 04:28:01',1,17,'10','village7',1,''),(160,'2009-09-22 04:30:04',1,19,'13','Grp1',2,'Added person \"p1\". Added person \"p2\".'),(161,'2009-09-22 06:12:09',1,22,'5','a7',1,''),(162,'2009-09-22 06:16:28',1,19,'14','Grp2',2,'Added person \"p3\".'),(163,'2009-09-22 11:23:33',1,29,'17','2009-09-22 temp1',1,''),(164,'2009-09-28 00:52:20',1,26,'5','sada',3,''),(165,'2009-09-28 01:51:40',1,26,'7','lang2',1,''),(166,'2009-09-28 02:01:25',1,26,'8','',3,''),(167,'2009-09-28 02:41:07',1,26,'11','sasdad',1,''),(168,'2009-09-28 02:41:23',1,26,'11','sasdad',3,''),(169,'2009-09-28 02:41:23',1,26,'10','12312',3,''),(170,'2009-09-28 02:41:23',1,26,'9','123',3,''),(171,'2009-09-28 02:41:23',1,26,'7','lang2',3,''),(172,'2009-09-28 02:41:23',1,26,'6','lang1',3,''),(173,'2009-09-28 03:22:33',1,26,'15','sad',1,''),(174,'2009-09-28 03:22:50',1,26,'15','sad',3,''),(175,'2009-09-28 03:23:59',1,26,'18','sadsd',3,''),(176,'2009-09-28 03:23:59',1,26,'17','sadsd',3,''),(177,'2009-09-28 03:23:59',1,26,'16','sadsd',3,''),(178,'2009-09-28 03:24:12',1,26,'14','english',3,''),(179,'2009-09-28 03:24:12',1,26,'13','english',3,''),(180,'2009-09-28 03:24:12',1,26,'12','english',3,''),(181,'2009-09-28 03:24:26',1,26,'19','Telgu',1,''),(182,'2009-09-28 03:39:48',1,26,'20','asdas',3,''),(183,'2009-09-30 06:48:04',1,26,'23','english111',3,''),(184,'2009-09-30 06:48:04',1,26,'22','12432',3,''),(185,'2009-09-30 06:48:04',1,26,'21','12432',3,''),(186,'2009-09-30 09:05:46',1,26,'31','asdsadas',3,''),(187,'2009-09-30 09:05:46',1,26,'30','l3',3,''),(188,'2009-09-30 09:05:46',1,26,'29','l2',3,''),(189,'2009-09-30 09:05:46',1,26,'28','xczxasdasd',3,''),(190,'2009-09-30 09:05:46',1,26,'27','sdasdasdsa ascmasdlkmaslk',3,''),(191,'2009-09-30 09:05:46',1,26,'26','sadasadsad',3,''),(192,'2009-09-30 09:05:46',1,26,'25','tsm',3,''),(193,'2009-09-30 09:05:46',1,26,'24','l1',3,''),(194,'2009-09-30 22:59:09',1,26,'33','temp2',1,''),(195,'2009-09-30 23:14:00',1,26,'33','temp2',3,''),(196,'2009-09-30 23:14:00',1,26,'32','tmep1',3,''),(197,'2009-09-30 23:20:15',1,26,'35','temp2',1,''),(198,'2009-09-30 23:20:43',1,26,'35','temp2',3,''),(199,'2009-09-30 23:21:24',1,26,'36','temp2',1,''),(200,'2009-09-30 23:44:44',1,26,'39','blah',1,''),(201,'2009-10-01 02:33:57',1,26,'41','temp1',1,''),(202,'2009-10-01 02:34:07',1,26,'42','temp1',1,''),(203,'2009-10-01 02:34:15',1,26,'42','temp1',2,'No fields changed.'),(204,'2009-10-01 08:15:46',1,26,'48','<function language at 0x9c8ba3c>',3,''),(205,'2009-10-01 08:15:46',1,26,'47','<function language at 0x903aa3c>',3,''),(206,'2009-10-01 08:15:46',1,26,'46','<function language at 0x90c4b54>',3,''),(207,'2009-10-01 08:15:46',1,26,'45','<function language at 0x9988b1c>',3,''),(208,'2009-10-01 08:15:46',1,26,'44','<function language at 0xa56cae4>',3,''),(209,'2009-10-01 08:15:46',1,26,'43','<function language at 0xa052ca4>',3,''),(210,'2009-10-01 08:15:46',1,26,'42','temp1',3,''),(211,'2009-10-01 08:15:46',1,26,'41','temp1',3,''),(212,'2009-10-01 08:15:46',1,26,'40','hh',3,''),(213,'2009-10-01 08:15:46',1,26,'39','blah',3,''),(214,'2009-10-01 08:15:46',1,26,'38','Gujarati',3,''),(215,'2009-10-01 08:15:46',1,26,'37','temp1',3,''),(216,'2009-10-01 08:15:46',1,26,'36','temp2',3,''),(217,'2009-10-01 08:15:46',1,26,'34','temp1',3,''),(218,'2009-10-01 08:31:26',1,26,'55','lsdkfnsdlkfs',3,''),(219,'2009-10-01 08:31:26',1,26,'54','lsdkfnsdlkfs',3,''),(220,'2009-10-01 08:31:26',1,26,'53','sdfdmdsl;fmsd;lf',3,''),(221,'2009-10-01 08:31:26',1,26,'52','slksdkmaskldmas',3,''),(222,'2009-10-01 08:31:26',1,26,'51','<function language at 0xa1c2b54>',3,''),(223,'2009-10-01 08:31:26',1,26,'50','<function language at 0x9202b54>',3,''),(224,'2009-10-01 08:31:26',1,26,'49','<function language at 0x8aaad4c>',3,''),(225,'2009-10-01 08:32:28',1,26,'56','skdamldk',1,''),(226,'2009-10-01 08:35:52',1,26,'59','temwpsdfds',1,''),(227,'2009-10-01 08:37:32',1,26,'60','temp22lknk',3,''),(228,'2009-10-01 08:37:32',1,26,'59','temwpsdfds',3,''),(229,'2009-10-01 08:37:32',1,26,'58','temp22',3,''),(230,'2009-10-01 08:37:32',1,26,'57','temp2',3,''),(231,'2009-10-01 08:37:32',1,26,'56','skdamldk',3,''),(232,'2009-10-01 09:23:17',1,26,'75','sdmasldka',3,''),(233,'2009-10-01 09:23:17',1,26,'74','sd',3,''),(234,'2009-10-01 09:23:17',1,26,'73','dsd;fmsdf',3,''),(235,'2009-10-01 09:23:17',1,26,'72','sldkas',3,''),(236,'2009-10-01 09:23:17',1,26,'71','please',3,''),(237,'2009-10-01 09:23:17',1,26,'70','sdfsdf',3,''),(238,'2009-10-01 09:23:17',1,26,'69','faltus.d,masd;l',3,''),(239,'2009-10-01 09:23:17',1,26,'68','faltus.d,ma',3,''),(240,'2009-10-01 09:23:17',1,26,'67','faltu',3,''),(241,'2009-10-01 09:23:17',1,26,'66','fina;l',3,''),(242,'2009-10-01 09:23:17',1,26,'65','temp1',3,''),(243,'2009-10-01 09:23:17',1,26,'64','ldslmfdls;f',3,''),(244,'2009-10-01 09:23:17',1,26,'63','sadasd',3,''),(245,'2009-10-01 09:23:17',1,26,'62','temlsdfzx.c, zx',3,''),(246,'2009-10-01 09:23:17',1,26,'61','temlsdf',3,''),(247,'2009-10-01 09:27:12',1,26,'76','1',1,''),(248,'2009-10-01 09:27:34',1,26,'76','1',3,''),(249,'2009-10-01 10:34:25',1,26,'85','sdasd',3,''),(250,'2009-10-01 10:34:25',1,26,'84','1111',3,''),(251,'2009-10-01 10:34:25',1,26,'83','dd',3,''),(252,'2009-10-01 10:34:25',1,26,'82','1',3,''),(253,'2009-10-01 10:34:25',1,26,'81','4',3,''),(254,'2009-10-01 10:34:25',1,26,'80','3',3,''),(255,'2009-10-01 10:34:25',1,26,'79','2',3,''),(256,'2009-10-01 10:34:25',1,26,'78','1',3,''),(257,'2009-10-01 10:34:25',1,26,'77','1',3,''),(258,'2009-10-01 23:39:09',1,26,'92','6',3,''),(259,'2009-10-01 23:39:09',1,26,'91','5',3,''),(260,'2009-10-01 23:39:09',1,26,'90','5',3,''),(261,'2009-10-01 23:39:09',1,26,'89','4',3,''),(262,'2009-10-01 23:39:09',1,26,'88','3',3,''),(263,'2009-10-01 23:39:09',1,26,'87','2',3,''),(264,'2009-10-01 23:39:09',1,26,'86','1',3,''),(265,'2009-10-01 23:39:36',1,26,'93','1',1,''),(266,'2009-10-02 00:28:42',1,26,'98','7',3,''),(267,'2009-10-02 00:28:42',1,26,'97','7',3,''),(268,'2009-10-02 00:28:42',1,26,'96','6',3,''),(269,'2009-10-02 00:28:42',1,26,'95','3',3,''),(270,'2009-10-02 00:28:42',1,26,'94','1',3,''),(271,'2009-10-02 00:28:42',1,26,'93','1',3,''),(272,'2009-10-02 01:32:06',1,26,'111','hjjj',3,''),(273,'2009-10-02 01:32:06',1,26,'110','dsfdsf',3,''),(274,'2009-10-02 01:32:06',1,26,'109','2',3,''),(275,'2009-10-02 01:32:06',1,26,'108','hjjj',3,''),(276,'2009-10-02 01:32:06',1,26,'107','2',3,''),(277,'2009-10-02 01:32:06',1,26,'106','b',3,''),(278,'2009-10-02 01:32:06',1,26,'105','2sada',3,''),(279,'2009-10-02 01:32:06',1,26,'104','b',3,''),(280,'2009-10-02 01:32:06',1,26,'103','2sada',3,''),(281,'2009-10-02 01:32:06',1,26,'102','8',3,''),(282,'2009-10-02 01:32:06',1,26,'101','8',3,''),(283,'2009-10-02 01:32:06',1,26,'100','cynosure',3,''),(284,'2009-10-02 01:32:06',1,26,'99','2',3,''),(285,'2009-10-02 01:36:54',1,26,'115','asdas',1,''),(286,'2009-10-02 01:44:47',1,26,'119','sdasdasdasdss',3,''),(287,'2009-10-02 01:44:47',1,26,'118','sdasdasdas',3,''),(288,'2009-10-02 01:44:47',1,26,'117','sdasdasdas',3,''),(289,'2009-10-02 01:44:47',1,26,'116','232',3,''),(290,'2009-10-02 01:44:47',1,26,'115','asdas',3,''),(291,'2009-10-02 01:44:47',1,26,'114','sdsda',3,''),(292,'2009-10-02 01:44:47',1,26,'113','sdsda',3,''),(293,'2009-10-02 01:44:47',1,26,'112','sdsda',3,''),(294,'2009-10-04 00:41:08',1,8,'6','Region5',3,''),(295,'2009-10-04 00:41:08',1,8,'5','Region5',3,''),(296,'2009-10-04 00:41:08',1,8,'4','Region4',3,''),(297,'2009-10-05 04:08:41',1,8,'1','Madhya Pradesh',2,'Changed region_name.'),(298,'2009-10-05 04:08:48',1,8,'1','Madhya Pradesh',2,'No fields changed.'),(299,'2009-10-05 04:09:01',1,8,'2','Crusaders',2,'Changed region_name.'),(300,'2009-10-05 04:09:14',1,8,'3','Karnataka',2,'Changed region_name.'),(301,'2009-10-05 23:56:11',1,26,'122','english',3,''),(302,'2009-10-05 23:56:11',1,26,'121','sdf',3,''),(303,'2009-10-05 23:56:11',1,26,'120','temp1',3,''),(304,'2009-10-06 01:21:35',1,8,'7','<script type=\"text/javascript\">alert(\"HAHA!\")</script>',1,''),(305,'2009-10-06 01:23:12',1,8,'8','<script type=\"text/javascript\">alert(\"HAHA!\");</script>',1,''),(306,'2009-10-06 01:39:46',1,8,'8','<script type=\"text/javascript\">alert(\"HAHA!\");</script>',3,''),(307,'2009-10-06 01:39:46',1,8,'7','<script type=\"text/javascript\">alert(\"HAHA!\")</script>',3,''),(308,'2009-10-06 02:38:12',1,11,'10','a7',1,''),(309,'2009-10-06 02:38:21',1,11,'10','a7',3,''),(310,'2009-10-06 03:14:44',1,13,'5','asdasd',1,''),(311,'2009-10-06 03:14:59',1,13,'5','asdasd',3,''),(312,'2009-10-06 04:18:55',1,20,'16','asdas',1,''),(313,'2009-10-06 04:19:23',1,20,'16','asdas',3,''),(314,'2009-10-06 05:48:53',1,29,'18','2009-10-06 village7',1,''),(315,'2009-10-06 08:14:32',1,27,'5','lknlm',1,''),(316,'2009-10-06 08:14:45',1,27,'5','lknlm',3,''),(317,'2009-10-06 08:55:01',1,27,'6','sdfdksdlf',1,''),(318,'2009-10-06 08:55:18',1,27,'6','sdfdksdlf',3,''),(319,'2009-10-06 08:56:29',1,17,'10','village7',3,''),(320,'2009-10-06 08:56:29',1,17,'9','Village6',3,''),(321,'2009-10-06 08:56:29',1,17,'7','temp',3,''),(322,'2009-10-06 08:56:29',1,17,'6','village5',3,''),(323,'2009-10-06 08:56:29',1,17,'5','village4',3,''),(324,'2009-10-06 08:56:29',1,17,'4','village3',3,''),(325,'2009-10-06 08:56:29',1,17,'3','village2',3,''),(326,'2009-10-06 08:56:29',1,17,'2','village1',3,''),(327,'2009-10-06 08:56:29',1,17,'1','temp1',3,''),(328,'2009-10-06 08:58:06',1,17,'10','village7',3,''),(329,'2009-10-06 08:58:06',1,17,'9','Village6',3,''),(330,'2009-10-06 08:58:06',1,17,'7','temp',3,''),(331,'2009-10-06 08:58:06',1,17,'6','village5',3,''),(332,'2009-10-06 08:58:06',1,17,'5','village4',3,''),(333,'2009-10-06 08:58:06',1,17,'4','village3',3,''),(334,'2009-10-06 08:58:06',1,17,'3','village2',3,''),(335,'2009-10-06 08:58:06',1,17,'2','village1',3,''),(336,'2009-10-06 08:58:06',1,17,'1','temp1',3,''),(337,'2009-10-06 08:58:44',1,12,'6','xz',3,''),(338,'2009-10-06 09:02:58',1,17,'11','Village1',1,''),(339,'2009-10-06 09:03:47',1,22,'6','Animator1',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(340,'2009-10-06 09:04:04',1,22,'7','Animator2',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(341,'2009-10-06 09:04:22',1,22,'8','Animator3',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(342,'2009-10-06 09:04:40',1,22,'9','Animator4',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(343,'2009-10-06 09:04:56',1,22,'10','Animator5',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(344,'2009-10-06 09:07:27',1,19,'15','Group1',2,'Added person \"Person1\". Added person \"Person2\".'),(345,'2009-10-06 09:08:06',1,19,'16','Group2',2,'Added person \"Person3\". Added person \"Person4\".'),(346,'2009-10-06 09:09:06',1,19,'17','Group3',2,'Added person \"Person5\". Added person \"Person6\".'),(347,'2009-10-06 09:09:16',1,19,'19','Group5',3,''),(348,'2009-10-06 09:09:16',1,19,'18','Group4',3,''),(349,'2009-10-06 09:14:14',1,17,'11','Village1',2,'Changed partner for animator \"Animator2\". Changed partner for animator \"Animator3\". Changed partner for animator \"Animator4\".'),(350,'2009-10-06 09:15:36',1,17,'12','Village2',1,''),(351,'2009-10-06 09:16:34',1,20,'23','per1',1,''),(352,'2009-10-06 09:17:08',1,20,'24','per2',1,''),(353,'2009-10-06 09:17:31',1,20,'25','per3',1,''),(354,'2009-10-06 09:17:50',1,20,'26','per4',1,''),(355,'2009-10-06 09:19:39',1,17,'13','Village3',1,''),(356,'2009-10-06 09:20:49',1,19,'23','G1',2,'Added person \"p1\". Added person \"p2\". Added person \"p3\".'),(357,'2009-10-06 09:21:45',1,19,'24','G2',2,'Added person \"p4\".'),(358,'2009-10-06 09:22:25',1,19,'25','G3',2,'Added person \"p5\".'),(359,'2009-10-06 09:23:31',1,22,'11','anim1',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(360,'2009-10-06 09:24:00',1,22,'12','anim2',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(361,'2009-10-06 09:24:17',1,22,'13','anim3',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(362,'2009-10-06 09:24:36',1,22,'14','a1',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(363,'2009-10-06 09:24:48',1,22,'15','a2',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(364,'2009-10-06 09:25:01',1,22,'16','a3',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(365,'2009-10-06 09:26:37',1,27,'7','video1',1,''),(366,'2009-10-06 09:32:57',1,29,'19','2009-10-06 Village3',1,''),(367,'2009-10-06 09:42:08',1,27,'8','video2',1,''),(368,'2009-10-06 09:43:04',1,27,'9','video3',1,''),(369,'2009-10-08 02:02:04',1,12,'7','temp1',3,''),(370,'2009-10-08 03:02:28',1,16,'20','sadasda',3,''),(371,'2009-10-08 04:03:34',1,16,'22','sadasds',3,''),(372,'2009-10-08 04:03:34',1,16,'21','kjzxkjc',3,''),(373,'2009-10-08 04:46:58',1,12,'8','kjk',3,''),(374,'2009-10-08 04:49:30',1,15,'11','adas',3,''),(375,'2009-10-08 04:58:51',1,8,'9','dsfdsf',3,''),(376,'2009-10-08 05:29:09',1,12,'9','sdadasd',3,''),(377,'2009-10-11 02:09:20',1,19,'26','asdad',3,''),(378,'2009-10-11 02:09:36',1,20,'32','sda',3,''),(379,'2009-10-11 07:09:27',1,19,'27','try1',3,''),(380,'2009-10-11 07:09:59',1,20,'33','try1',3,''),(381,'2009-10-11 09:25:29',1,19,'30','sakdjalks',3,''),(382,'2009-10-11 09:25:29',1,19,'29','sasd',3,''),(383,'2009-10-11 09:25:29',1,19,'28','t1',3,''),(384,'2009-10-11 09:25:49',1,20,'34','sdf,dkns',3,''),(385,'2009-10-11 10:15:18',1,17,'14','assa',1,''),(386,'2009-10-11 10:16:18',1,17,'14','assa',3,''),(387,'2009-10-11 10:56:58',1,20,'35','tempp1',3,''),(388,'2009-10-11 11:13:21',1,19,'32','tempgrp',3,''),(389,'2009-10-11 11:13:21',1,19,'31','sadas',3,''),(390,'2009-10-11 12:34:59',1,29,'20','2009-10-12 Village3',1,''),(391,'2009-10-12 02:57:22',3,16,'23','b1',1,''),(392,'2009-10-12 02:59:25',2,16,'23','b1asd',2,'Changed block_name.'),(393,'2009-10-12 03:17:31',1,16,'23','b1asd',3,''),(394,'2009-10-12 03:18:10',1,15,'9','Kushalnagar ',2,'Changed fieldofficer.'),(395,'2009-10-12 03:20:27',1,15,'7','Purulia ',2,'Changed fieldofficer.'),(396,'2009-10-12 03:21:32',1,14,'10','Satyam Salil',1,''),(397,'2009-10-12 03:21:52',1,15,'2','Mandla ',2,'Changed fieldofficer.'),(398,'2009-10-12 03:23:12',1,15,'1','Dindori ',2,'Changed fieldofficer.'),(399,'2009-10-12 03:25:53',1,14,'9','Dr. Nadagouda',3,''),(400,'2009-10-12 03:25:53',1,14,'8','Mr. Avinash',3,''),(401,'2009-10-12 03:25:53',1,14,'7','Mr. Gulzar',3,''),(402,'2009-10-12 13:40:23',1,19,'33','sadas',3,''),(403,'2009-10-12 13:41:41',1,20,'38','p444',3,''),(404,'2009-10-12 13:41:41',1,20,'37','p111',3,''),(405,'2009-10-12 13:41:41',1,20,'36','p222',3,''),(406,'2009-10-12 13:44:34',1,12,'10','tmeep1',3,''),(407,'2009-10-12 13:49:59',1,3,'2','Development Manager',2,'Changed permissions.'),(408,'2009-10-12 13:53:17',1,3,'1','Field Officer',2,'Changed permissions.'),(409,'2009-10-12 14:32:07',1,4,'4','satyam',1,''),(410,'2009-10-12 14:33:43',1,4,'5','archana',1,''),(411,'2009-10-12 14:34:29',1,4,'6','ramachandra',1,''),(412,'2009-10-12 14:36:40',1,4,'7','chandrashekhar',1,''),(413,'2009-10-12 14:37:54',1,4,'8','muthumari',1,''),(414,'2009-10-12 14:38:21',1,4,'9','abhishek',1,''),(415,'2009-10-12 14:38:36',1,4,'10','kevin',1,''),(416,'2009-10-12 14:38:52',1,4,'10','kevin',2,'Changed groups.'),(417,'2009-10-12 14:39:08',1,4,'9','abhishek',2,'Changed is_staff and groups.'),(418,'2009-10-12 14:39:43',1,4,'5','archana',2,'Changed is_staff and groups.'),(419,'2009-10-12 14:40:03',1,4,'7','chandrashekhar',2,'Changed is_staff and groups.'),(420,'2009-10-12 14:40:19',1,4,'10','kevin',2,'Changed is_staff.'),(421,'2009-10-12 14:40:32',1,4,'8','muthumari',2,'Changed is_staff and groups.'),(422,'2009-10-12 14:40:46',1,4,'6','ramachandra',2,'Changed is_staff and groups.'),(423,'2009-10-12 14:40:57',1,4,'4','satyam',2,'Changed is_staff and groups.'),(424,'2009-10-12 14:41:48',1,4,'11','nadagouda',1,''),(425,'2009-10-12 14:42:01',1,4,'11','nadagouda',2,'Changed is_staff and groups.'),(426,'2009-10-12 14:42:27',1,4,'12','avinash',1,''),(427,'2009-10-12 14:42:38',1,4,'12','avinash',2,'Changed is_staff and groups.'),(428,'2009-10-12 14:43:10',1,4,'13','gulzar',1,''),(429,'2009-10-12 14:43:32',1,4,'13','gulzar',2,'Changed is_staff and groups.'),(430,'2009-10-12 14:49:16',1,17,'13','Village3',3,''),(431,'2009-10-12 14:49:16',1,17,'12','Village2',3,''),(432,'2009-10-12 14:49:16',1,17,'11','Village1',3,''),(433,'2009-10-12 15:33:36',1,17,'15','t1',1,''),(434,'2009-10-12 15:34:33',1,17,'15','t1',3,''),(435,'2009-10-12 15:36:00',1,17,'16','v1',1,''),(436,'2009-10-12 15:36:34',1,17,'16','v1',3,''),(437,'2009-10-13 05:51:54',1,17,'17','village1',1,''),(438,'2009-10-13 06:01:03',1,19,'34','group1',2,'Added person \"person1\". Added person \"person2\".'),(439,'2009-10-13 06:10:35',1,17,'18','village2',1,''),(440,'2009-10-14 00:54:54',1,24,'19','AnimatorAssignedVillage object',1,''),(441,'2009-10-14 00:55:13',1,24,'20','AnimatorAssignedVillage object',1,''),(442,'2009-10-14 00:55:31',1,24,'21','AnimatorAssignedVillage object',1,''),(443,'2009-10-14 01:01:56',1,27,'10','video1',1,''),(444,'2009-10-14 01:02:43',1,27,'11','video2',1,''),(445,'2009-10-22 11:56:57',1,17,'18','village2',3,''),(446,'2009-10-22 11:56:57',1,17,'17','village1',3,''),(447,'2009-10-23 00:00:23',1,17,'19','village1',1,''),(448,'2009-10-23 04:13:51',1,20,'43','p3',3,''),(449,'2009-10-23 04:13:51',1,20,'42','p1',3,''),(450,'2009-10-23 04:13:51',1,20,'41','p2',3,''),(451,'2009-10-23 04:14:12',1,19,'41','grp3',3,''),(452,'2009-10-23 04:14:12',1,19,'40','g2',3,''),(453,'2009-10-23 04:14:12',1,19,'39','g1',3,''),(454,'2009-10-23 07:41:03',8,15,'12','Khunti',1,''),(455,'2009-10-23 19:40:11',12,26,'123','Ho',1,''),(456,'2009-10-23 19:40:16',12,26,'124','Ho',1,''),(457,'2009-10-23 19:40:30',12,26,'125','Oriya',1,''),(458,'2009-10-23 19:40:45',12,26,'126','Bengali',1,''),(459,'2009-10-26 12:46:45',1,19,'50','dsdfdsf',3,''),(460,'2009-10-26 12:46:45',1,19,'49','dsdfdsf',3,''),(461,'2009-10-26 12:46:45',1,19,'48','dsdfdsf',3,''),(462,'2009-10-26 12:46:45',1,19,'47','dsdfdsf',3,''),(463,'2009-10-26 12:46:45',1,19,'46','dsdfdsf',3,''),(464,'2009-10-26 12:46:45',1,19,'45','dsdfdsf',3,''),(465,'2009-10-26 12:46:45',1,19,'44','dsdfdsf',3,''),(466,'2009-10-26 12:46:45',1,19,'43','grp11',3,''),(467,'2009-10-26 12:46:45',1,19,'42','grp232',3,''),(468,'2009-10-26 12:47:08',1,20,'62','sdasd',3,''),(469,'2009-10-26 12:47:08',1,20,'59','sdasd',3,''),(470,'2009-10-26 12:47:08',1,20,'56','sdasd',3,''),(471,'2009-10-26 12:47:08',1,20,'53','sdasd',3,''),(472,'2009-10-26 12:47:08',1,20,'52','sdsdad',3,''),(473,'2009-10-26 12:47:08',1,20,'51','sda',3,''),(474,'2009-10-26 12:47:08',1,20,'50','sdasd',3,''),(475,'2009-10-26 12:47:08',1,20,'49','per3',3,''),(476,'2009-10-26 12:47:08',1,20,'48','sdad',3,''),(477,'2009-10-26 12:47:08',1,20,'47','perwe',3,''),(478,'2009-10-26 12:47:08',1,20,'46','perere',3,''),(479,'2009-10-26 12:47:08',1,20,'45','pwerer',3,''),(480,'2009-10-26 12:47:08',1,20,'44','per1',3,''),(481,'2009-10-27 03:28:11',1,20,'73','6person',3,''),(482,'2009-10-27 03:28:11',1,20,'72','5person',3,''),(483,'2009-10-27 03:28:11',1,20,'71','4person',3,''),(484,'2009-10-27 03:28:11',1,20,'70','per3',3,''),(485,'2009-10-27 03:28:11',1,20,'69','per2',3,''),(486,'2009-10-27 03:28:11',1,20,'68','per1',3,''),(487,'2009-10-27 03:28:27',1,19,'52','group4',3,''),(488,'2009-10-27 03:28:27',1,19,'51','group1',3,''),(489,'2009-10-27 03:49:55',1,19,'53','grp1',2,'No fields changed.'),(490,'2009-10-27 03:53:56',1,19,'53','grp1',2,'Added person \"per4\".'),(491,'2009-10-27 22:53:48',1,15,'13','dfdsfsd',3,''),(492,'2009-10-27 23:37:18',1,8,'10','sadasd',1,''),(493,'2009-10-27 23:37:54',1,11,'11','sdsa',3,''),(494,'2009-10-27 23:38:52',1,8,'10','sadasd',3,''),(495,'2009-10-28 03:31:24',1,11,'13','weqw',3,''),(496,'2009-10-28 03:31:24',1,11,'12','sadsa',3,''),(497,'2009-10-28 23:53:25',1,20,'77','per4',3,''),(498,'2009-10-28 23:53:25',1,20,'76','per3',3,''),(499,'2009-10-28 23:53:25',1,20,'75','per2',3,''),(500,'2009-10-28 23:53:25',1,20,'74','per1',3,''),(501,'2009-10-28 23:53:45',1,19,'53','grp1',3,''),(502,'2009-10-29 02:52:39',1,22,'20','a1',1,''),(503,'2009-10-30 04:49:23',1,19,'54','dssdds',1,''),(504,'2009-10-30 05:08:50',1,19,'55','dsasdd',1,''),(505,'2009-10-30 05:09:30',1,19,'56','dfdsdfs',1,''),(506,'2009-10-30 05:25:12',1,19,'57','dfdsdfssadasda',1,''),(507,'2009-10-30 05:25:39',1,19,'58','dfdsdfssadasda',1,''),(508,'2009-10-30 06:14:08',1,19,'58','dfdsdfssadasda',3,''),(509,'2009-10-30 06:14:08',1,19,'57','dfdsdfssadasda',3,''),(510,'2009-10-30 06:14:08',1,19,'56','dfdsdfs',3,''),(511,'2009-10-30 06:14:08',1,19,'55','dsasdd',3,''),(512,'2009-10-30 06:14:08',1,19,'54','dssdds',3,''),(513,'2009-10-30 06:58:40',1,19,'59','sadasd',1,''),(514,'2009-10-30 06:59:51',1,19,'60','sadasd',1,''),(515,'2009-10-31 02:49:43',10,14,'1','Kevin Gandhi',2,'Changed age and hire_date.'),(516,'2009-10-31 02:49:54',10,14,'1','Kevin Gandhi',2,'No fields changed.'),(517,'2009-10-31 03:00:30',10,14,'1','Kevin Gandhi',2,'Changed phone_no and address.'),(518,'2009-11-01 21:24:26',1,24,'24','AnimatorAssignedVillage object',3,''),(519,'2009-11-01 21:24:26',1,24,'23','AnimatorAssignedVillage object',3,''),(520,'2009-11-01 21:24:26',1,24,'22','AnimatorAssignedVillage object',3,''),(521,'2009-11-05 03:34:56',5,26,'127','kannada',1,''),(522,'2009-11-05 06:17:32',1,22,'26','dfsdf',3,''),(523,'2009-11-05 06:17:32',1,22,'25','dfsdf',3,''),(524,'2009-11-05 06:17:32',1,22,'24','dfsdf',3,''),(525,'2009-11-05 06:17:32',1,22,'23','dfsdf',3,''),(526,'2009-11-05 06:17:32',1,22,'22','dfsdf',3,''),(527,'2009-11-05 06:17:32',1,22,'21','dfsdf',3,''),(528,'2009-11-05 10:38:01',1,17,'19','village1',3,''),(529,'2009-11-05 11:41:39',1,17,'20','village1',1,''),(530,'2009-11-05 11:43:17',1,17,'21','village2',1,''),(531,'2009-11-05 11:43:42',1,24,'27','AnimatorAssignedVillage object',1,''),(532,'2009-11-05 11:43:51',1,24,'28','AnimatorAssignedVillage object',1,''),(533,'2009-11-05 11:44:00',1,24,'29','AnimatorAssignedVillage object',1,''),(534,'2009-11-05 11:44:09',1,24,'30','AnimatorAssignedVillage object',1,''),(535,'2009-11-05 11:44:20',1,24,'31','AnimatorAssignedVillage object',1,''),(536,'2009-11-05 11:45:08',1,19,'61','group1',2,'Added person \"per1\". Added person \"per2\". Added person \"per3\".'),(537,'2009-11-05 11:45:38',1,19,'62','group2',2,'Added person \"per4\". Added person \"per5\".'),(538,'2009-11-05 11:46:11',1,19,'61','group1',2,'Changed person_name for person \"person1\". Changed person_name for person \"person2\". Changed person_name for person \"person3\".'),(539,'2009-11-05 11:46:29',1,19,'62','group2',2,'Changed person_name for person \"person4\". Changed person_name for person \"person5\".'),(540,'2009-11-05 11:46:59',1,19,'63','group3',2,'Added person \"person6\". Added person \"person7\".'),(541,'2009-11-05 11:47:44',1,19,'64','grp1',2,'Added person \"per1\". Added person \"per2\". Added person \"per3\".'),(542,'2009-11-05 11:48:30',1,19,'65','grp2',2,'Added person \"per4\". Added person \"per5\". Added person \"per6\".'),(543,'2009-11-05 12:00:06',1,17,'20','village1',2,'No fields changed.'),(544,'2009-11-05 12:06:56',1,24,'32','AnimatorAssignedVillage object',1,''),(545,'2009-11-05 12:10:39',1,27,'12','video1',1,''),(546,'2009-11-07 01:57:22',1,17,'21','village2',2,'Added Person group \"grp3\".'),(547,'2009-11-07 02:02:03',1,24,'33','AnimatorAssignedVillage object',1,''),(548,'2009-11-07 02:02:20',1,24,'34','AnimatorAssignedVillage object',1,''),(549,'2009-11-07 02:03:06',1,24,'34','AnimatorAssignedVillage object',2,'Changed village.'),(550,'2009-11-07 02:24:57',1,28,'4','interagricultural  ',1,''),(551,'2009-11-10 12:10:40',1,14,'11','sad',3,''),(552,'2009-11-11 01:53:19',1,13,'6','sadas',3,''),(553,'2009-11-13 03:24:02',1,20,'101','dasda',3,''),(554,'2009-11-13 03:24:12',1,20,'100','dasda',3,''),(555,'2009-11-13 10:49:20',1,20,'103','sada',3,''),(556,'2009-11-13 10:49:20',1,20,'102','asdsa',3,''),(557,'2009-11-13 10:49:36',1,19,'71','sda',3,''),(558,'2009-11-13 10:49:36',1,19,'70','sadasd',3,''),(559,'2009-11-13 10:49:36',1,19,'69','sdad',3,''),(560,'2009-11-13 10:49:36',1,19,'68','sdad',3,''),(561,'2009-11-13 10:49:36',1,19,'67','asdasd',3,''),(562,'2009-11-13 11:08:27',1,28,'5','sdad',3,''),(563,'2009-11-13 11:08:37',1,28,'4','interagricultural  ',3,''),(564,'2009-11-15 08:09:01',1,26,'124','Ho',3,''),(565,'2009-11-17 00:30:20',1,17,'23','sdsad',2,'Added Person group \"ZSxAs\".'),(566,'2009-11-17 00:30:42',1,17,'23','sdsad',3,''),(567,'2009-11-17 00:30:42',1,17,'22','dsfds',3,''),(568,'2009-11-23 05:37:21',1,27,'13','sdasd',3,''),(569,'2009-11-23 05:40:59',1,29,'21','2009-11-23 village2',1,''),(570,'2009-12-01 11:29:37',1,8,'3','Beacons ',2,'Changed region_name.'),(571,'2009-12-01 11:30:07',1,8,'1','Pioneers ',2,'Changed region_name.'),(572,'2009-12-11 00:55:25',8,16,'9','Torpa',2,'Changed block_name.'),(573,'2009-12-11 00:55:47',8,16,'10','Erki',2,'Changed block_name.'),(574,'2009-12-11 00:56:02',8,16,'11','Murhu',2,'Changed block_name.'),(575,'2009-12-11 00:56:37',8,16,'24','Khunti',1,''),(576,'2009-12-11 01:03:30',8,17,'24','Navatoli 1',1,''),(577,'2009-12-11 01:04:08',8,17,'24','Navatoli 1',2,'No fields changed.'),(578,'2009-12-11 21:55:47',8,17,'25','Jibilong',1,''),(579,'2009-12-11 21:56:11',8,22,'34','Salim',1,''),(580,'2009-12-11 22:29:27',8,17,'26','Tati',1,''),(581,'2009-12-11 22:50:26',8,22,'34','Salim',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(582,'2009-12-11 23:15:41',8,28,'6','Intercultural',1,''),(583,'2009-12-11 23:26:15',8,28,'7','Intercultural',1,''),(584,'2009-12-12 05:44:31',8,19,'76','Production farmer group',1,''),(585,'2009-12-12 08:47:19',8,27,'14','Potato intercultural',1,''),(586,'2009-12-15 21:49:34',8,17,'27','Gufu',1,''),(587,'2009-12-15 21:52:26',8,17,'28','Kinsu',1,''),(588,'2009-12-15 21:56:09',8,17,'29','Gopla',1,''),(589,'2009-12-15 21:58:15',8,24,'38','AnimatorAssignedVillage object',1,''),(590,'2009-12-15 21:59:54',8,24,'39','AnimatorAssignedVillage object',1,''),(591,'2009-12-15 22:07:53',8,19,'81','Sivasakthi',2,'Added person \"Dropathi Devi\". Added person \"Subatra devi\". Added person \"Milo Devi\". Added person \"Milo Kumari\". Added person \"Rahil Gudia\". Added person \"Salomi Gudia\". Added person \"Bahamani Gudia\". Added person \"Gaangi Gudia\". Added person \"Juliani Gudia\". Added person \"Sibiyani Gudia\". Added person \"Magdali Kandulona\". Added person \"Magadali Gudia\". Added person \"Somari Gudia\". Added person \"Munni Gudia\". Added person \"Binna Gudia\". Added person \"Pyari Devi\". Added person \"Ethwari Gudia\".'),(592,'2009-12-15 22:13:33',8,19,'80','Turtan Singh',2,'Added person \"Hanna Bhengra\". Added person \"Barosi Bhengra\". Added person \"Jyoti Bhengra\". Added person \"Kuwari Bhengra\". Added person \"Mukta Bhengra\". Added person \"Somari Bhengra\". Added person \"Saniyaro Bhengra\". Added person \"Agata Bhengra\". Added person \"Gaangi Bhengra\". Added person \"Chandu Bhengra\". Added person \"Sushma Bhengra\". Added person \"Ethwari badh\". Added person \"Jano Bhengra\". Added person \"Birsi Bhengra\". Added person \"Birsi Bhengra\".'),(593,'2009-12-15 22:28:19',8,19,'79','Sugandh',2,'Added person \"Shanti Bhengra\". Added person \"Sumanti Bhengra\". Added person \"Pyaro Bhengra\". Added person \"Josphina Bhengra\". Added person \"Jhony Topno\". Added person \"Birsi Topno\". Added person \"Jhariyo Topno\". Added person \"Ushki Topno\". Added person \"Gaangimuni Topno\". Added person \"Dashmi Topno\". Added person \"Chami Topno\". Added person \"Somari Topna\". Added person \"Nandi Bhengra\". Added person \"Mukta Bhengra\". Added person \"Jhony Bhengra\". Added person \"Anju Bhengra\". Added person \"Sushila Bhengra\".'),(594,'2009-12-15 22:38:02',8,19,'78','Prem',2,'Added person \"Samme Bhengra\". Added person \"Dulari Bhengra\". Added person \"Sunita Gudia\". Added person \"Jagangi Gudia\". Added person \"Hanna Gudia\". Added person \"Butan Hemrom\". Added person \"MuniBhengra\". Added person \"Randai Bhengra\". Added person \"Budhni Bhengra\". Added person \"Somari Bhengra\". Added person \"Luisa Bhengra\". Added person \"Rahil Bhengra\". Added person \"Chandu Bhengra\". Added person \"Chirlu Bhengra\". Added person \"Pratima Bhengra\". Added person \"Gaangi Bhengra\". Added person \"Jhingi Bhengra\". Added person \"Chami Bhengra\". Added person \"Singi Bhengra\". Added person \"Radhi Bhengra\".'),(595,'2009-12-15 22:49:13',8,19,'77','Niloni',2,'Added person \"Lalita Devi\". Added person \"Pushpa devi\". Added person \"Bimala Devi A\". Added person \"Kalavati Devi \". Added person \"Dasmi Devi\". Added person \"Malati devi A\". Added person \"Kunti Devi A\". Added person \"Shanti Devi\". Added person \"Bijan Devi\". Added person \"Rajmuni Devi\". Added person \"Malati devi B\". Added person \"Nankur Devi\". Added person \"Mankuwar Devi\". Added person \"Itwari Devi\". Added person \"Bimala Devi B\". Added person \"Rita Devi\". Added person \"Bolo Devi\". Added person \"Urmila Devi\".'),(596,'2009-12-15 22:53:49',8,27,'15','cabbage intercultural',1,''),(597,'2009-12-15 22:58:23',8,22,'40','Habil',1,''),(598,'2009-12-15 23:04:19',8,22,'40','Habil',2,'No fields changed.'),(599,'2009-12-15 23:39:09',8,17,'30','Bandhu',1,''),(600,'2009-12-15 23:47:22',8,19,'82','Production farmer group 1',1,''),(601,'2009-12-15 23:53:18',8,22,'41','Sudeep',1,''),(602,'2009-12-15 23:54:31',8,24,'44','AnimatorAssignedVillage object',1,''),(603,'2009-12-15 23:55:16',8,24,'45','AnimatorAssignedVillage object',1,''),(604,'2009-12-15 23:58:46',8,27,'16','Green-Pea Sowing',1,''),(605,'2009-12-16 00:07:55',8,17,'31','Lohajimi',1,''),(606,'2009-12-16 00:09:20',8,17,'32','Kajurdag',1,''),(607,'2009-12-16 00:15:45',8,19,'83','Production farmer group 2',1,''),(608,'2009-12-16 00:22:32',8,27,'17','Potato sowing',1,''),(609,'2009-12-16 00:32:01',8,28,'8','Nursery',1,''),(610,'2009-12-16 01:05:53',8,19,'84','Production farmer group 3',1,''),(611,'2009-12-16 01:07:25',8,19,'83','Production farmer group 2',2,'Added person \"Rahil Topno\".'),(612,'2009-12-16 01:11:11',8,27,'18','cabbage sowing',1,''),(613,'2009-12-16 02:29:12',8,27,'19','cauliflower nursery',1,''),(614,'2009-12-16 02:39:25',8,28,'9','Transplantation',1,''),(615,'2009-12-16 02:42:34',8,27,'20','cabbage transplantation',1,''),(616,'2009-12-16 02:55:01',8,22,'39','Sameer',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(617,'2009-12-16 03:12:29',8,29,'24','2009-11-22 Gopla',1,''),(618,'2009-12-16 03:20:01',8,29,'25','2009-11-15 Gopla',1,''),(619,'2009-12-16 03:30:56',8,29,'26','2009-11-13 Gufu',1,''),(620,'2009-12-16 03:35:54',8,29,'27','2009-11-20 Gufu',1,''),(621,'2009-12-17 07:25:30',8,27,'18','cabbage nursery',2,'Changed title.'),(622,'2009-12-17 07:25:44',1,27,'18','cabbage nursery',2,'No fields changed.'),(623,'2009-12-17 07:28:56',1,22,'38','Sameer',3,''),(624,'2009-12-17 07:29:06',1,22,'37','Sameer',3,''),(625,'2009-12-17 07:30:16',1,22,'36','Sameer',3,''),(626,'2009-12-22 03:29:11',10,17,'33','Mansingpura',1,''),(627,'2009-12-22 03:32:56',10,17,'34','Neemkhada',1,''),(628,'2009-12-22 03:33:24',10,17,'33','Mansingpura',2,'No fields changed.'),(629,'2009-12-22 03:35:48',10,17,'34','Neemkhada',2,'No fields changed.'),(630,'2009-12-22 03:40:04',10,17,'35','Kisanghar',1,''),(631,'2009-12-23 20:46:38',10,17,'36','Pandutalab',1,''),(632,'2009-12-23 20:49:58',10,17,'37','Pandutalab',1,''),(633,'2009-12-23 20:51:56',10,17,'36','Pandutalab',2,'No fields changed.'),(634,'2009-12-23 20:57:04',10,17,'38','Sitapuri (Small)',1,''),(635,'2009-12-23 20:58:48',10,24,'49','AnimatorAssignedVillage object',1,''),(636,'2009-12-23 21:02:00',10,17,'39','Shampura',1,''),(637,'2009-12-23 21:03:12',10,17,'40','Semli',1,''),(638,'2009-12-23 21:04:10',10,17,'41','Jamasindh',1,''),(639,'2009-12-23 21:04:51',10,17,'42','Bisali',1,''),(640,'2009-12-23 21:07:30',10,17,'38','Sitapuri (Small)',2,'No fields changed.'),(641,'2009-12-23 21:27:13',10,19,'88','Amarnath Kisan Samu',1,''),(642,'2010-01-04 23:28:34',5,17,'43','SS Koppa',1,''),(643,'2010-01-04 23:29:38',5,16,'25','ss koppa',1,''),(644,'2010-01-04 23:36:52',5,17,'44','kamplikoppa',1,''),(645,'2010-01-05 01:01:48',5,17,'45','BN Koppa',1,''),(646,'2010-01-05 01:10:39',5,16,'26','kalgattigi',1,''),(647,'2010-01-05 01:15:38',5,17,'46','Dastikoppa',1,''),(648,'2010-01-05 01:30:45',5,17,'47','Hirehonnalli',1,''),(649,'2010-01-05 01:33:56',5,17,'48','Ganjigatti',1,''),(650,'2010-01-05 01:38:56',5,17,'49','Huniskatte',1,''),(651,'2010-01-05 01:46:29',5,17,'50','Mukkal',1,''),(652,'2010-01-07 22:35:16',5,24,'50','AnimatorAssignedVillage object',1,''),(653,'2010-01-07 22:35:49',5,24,'51','AnimatorAssignedVillage object',1,''),(654,'2010-01-07 22:36:09',5,24,'52','AnimatorAssignedVillage object',1,''),(655,'2010-01-07 22:36:36',5,24,'53','AnimatorAssignedVillage object',1,''),(656,'2010-01-07 22:36:59',5,24,'54','AnimatorAssignedVillage object',1,''),(657,'2010-01-07 22:38:17',5,24,'55','AnimatorAssignedVillage object',1,''),(658,'2010-01-07 23:17:37',5,19,'116','Public & Vijayalaxmi SHG',2,'Added person \"Nagappa Jaygoudar\". Added person \"Ramesh kamplikoppa\". Added person \"Shankarappa chinchali\". Added person \"Basappa goudara\". Added person \"Lingareddy naduvinamnai\". Added person \"Nagaraj muttagi\". Added person \"Nigappa sherewad\". Added person \"Chanabasappa shetteppanavar\". Added person \"Swamiji\". Added person \"Ireppa kabber\". Added person \"Parappa ganti\". Added person \"Irapaiah neeralagi\". Added person \"Fakirappa siddappanavar\". Added person \"Kubergouda doddagoudar\". Added person \"Honavva\". Added person \"Reshma\". Added person \"Sharravva\". Added person \"Gangamma\". Added person \"Kammalavva\". Added person \"Sahebi\". Added person \"Paravva\". Added person \"Rajibi\". Added person \"Manjula\". Added person \"Yallamma\". Added person \"Tayavva\". Added person \"Renuka\". Added person \"Tippava\". Added person \"Manjula \". Added person \"Devakka\". Added person \"Savavva\".'),(659,'2010-01-07 23:19:03',5,19,'116','Public & Vijayalaxmi SHG',2,'Added person \"Madevi Ganti\".'),(660,'2010-01-07 23:30:55',5,19,'115','Shri Jatingeshwar SHG',2,'Added person \"Iravva hulugur\". Added person \"Shantavva\". Added person \"Ningavva\". Added person \"Devakka\". Added person \"Kamalavva\". Added person \"Sushilavva\". Added person \"Renavva\". Added person \"Iravva hulgur\". Added person \"Shivakka\". Added person \"Sarswati\". Added person \"Shekavva\". Added person \"Kallavva\". Added person \"Devakka\". Added person \"Manjula\". Added person \"Basavva\". Added person \"Nelavva\". Added person \"Yellavva \". Added person \"Jayashri\". Added person \"Neelamma\". Added person \"Gangavva \". Added person \"Gadigavva\". Added person \"Neelavva\". Added person \"Rudravva Jaygoudra\". Added person \"Fakiravva\". Added person \"Channavva\". Added person \"Madevi\". Added person \"Ratnavva\". Added person \"Parvatavva\". Added person \"Mallavva \". Added person \"Gangavva\".'),(661,'2010-01-08 00:00:41',5,19,'115','Shri Jatingeshwar SHG',2,'Added person \"Hanumavva\". Added person \"Shantavva\". Added person \"Chanamma\". Added person \"Saraswati Aralikatti\". Added person \"Basavva\". Added person \"Shantavva\". Added person \"Akkamma\".'),(662,'2010-01-10 01:51:03',10,26,'128','Neemardi',1,''),(663,'2010-01-10 01:58:36',10,27,'21','Makha Harvest',1,''),(664,'2010-01-10 23:35:03',1,17,'21','village2',3,''),(665,'2010-01-10 23:35:03',1,17,'20','village1',3,''),(666,'2010-01-10 23:36:21',1,28,'7','Intercultural',3,''),(667,'2010-01-11 06:41:57',1,8,'11','TEST',1,''),(668,'2010-01-11 06:42:40',1,8,'11','TEST',3,''),(669,'2010-01-11 06:43:11',1,8,'12','TEST',1,''),(670,'2010-01-12 03:48:34',1,8,'12','TEST',3,''),(671,'2010-01-12 03:52:48',1,8,'13','TEST1',1,''),(672,'2010-01-12 04:50:31',1,8,'14','TEST',1,''),(673,'2010-01-12 08:12:41',1,8,'14','TEST',3,''),(674,'2010-01-12 08:12:41',1,8,'13','TEST1',3,''),(675,'2010-01-12 08:22:38',1,8,'15','TEST',1,''),(676,'2010-01-12 23:40:44',5,17,'50','Mukkal',2,'Changed block. Added animator \"Kalappa Badiger\".'),(677,'2010-01-12 23:47:06',5,19,'117','sreishakti mahila sangh',1,''),(678,'2010-01-12 23:48:09',5,19,'117','sreishakti mahila sangh',2,'No fields changed.'),(679,'2010-01-12 23:48:17',5,19,'117','sreishakti mahila sangh',2,'No fields changed.'),(680,'2010-01-14 04:49:44',5,17,'50','Mukkal',2,'Changed block.'),(681,'2010-01-14 04:53:43',5,17,'43','SS Koppa',2,'Changed name for animator \"Vandana\".'),(682,'2010-01-17 22:14:25',7,15,'14','Mayurbhanj',1,''),(683,'2010-01-17 22:14:28',7,16,'27','Jashipur',1,''),(684,'2010-01-17 22:18:26',7,17,'51','Ektali',1,''),(685,'2010-01-17 22:21:02',7,15,'15','Mayurbhanj',1,''),(686,'2010-01-17 22:21:16',7,16,'28','Jashipur',1,''),(687,'2010-01-17 22:53:47',7,17,'52','Deuli',1,''),(688,'2010-01-17 22:57:44',7,22,'59','Koutaki Nayak',1,''),(689,'2010-01-17 23:02:26',7,17,'53','Baria',1,''),(690,'2010-01-17 23:04:30',7,17,'54','Deuli',1,''),(691,'2010-01-17 23:04:45',7,22,'62','Ramakant',1,''),(692,'2010-01-17 23:09:04',7,17,'55','Ektali',1,''),(693,'2010-01-17 23:09:08',7,22,'64','Hrushikesh Goipai',1,''),(694,'2010-01-17 23:15:41',7,17,'56','Mangarh',1,''),(695,'2010-01-17 23:19:45',7,17,'57','Basantpur_Naiksahi',1,''),(696,'2010-01-17 23:21:53',7,17,'58','Basantpur',1,''),(697,'2010-01-17 23:22:16',7,22,'64','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(698,'2010-01-17 23:25:51',7,17,'59','Kumdabadi',1,''),(699,'2010-01-17 23:25:57',7,24,'63','AnimatorAssignedVillage object',1,''),(700,'2010-01-17 23:28:54',7,17,'60','Kanthikena',1,''),(701,'2010-01-17 23:28:59',7,24,'64','AnimatorAssignedVillage object',1,''),(702,'2010-01-17 23:33:31',7,17,'61','Khandbandha',1,''),(703,'2010-01-17 23:38:16',7,17,'62','Khandbandha',1,''),(704,'2010-01-17 23:39:18',7,17,'63','Badaposhi',1,''),(705,'2010-01-17 23:39:26',7,22,'68','Paray Pingua',1,''),(706,'2010-01-17 23:40:02',7,17,'64','Khandbandha',1,''),(707,'2010-01-17 23:40:13',7,24,'67','AnimatorAssignedVillage object',1,''),(708,'2010-01-17 23:46:09',7,17,'65','Chandusahi',1,''),(709,'2010-01-17 23:50:42',7,22,'69','Kuni',1,''),(710,'2010-01-18 00:33:42',7,19,'134','Sibasakti,Bholanath',1,''),(711,'2010-01-18 00:42:01',7,19,'134','Sibasakti,Bholanath',2,'Added person \"Pramila Nayak(B)\".'),(712,'2010-01-19 11:32:57',1,8,'15','TEST',3,''),(713,'2010-01-19 11:44:02',1,17,'66','Test Village',1,''),(714,'2010-01-19 11:47:15',1,24,'68','AnimatorAssignedVillage object',1,''),(715,'2010-01-19 11:49:46',1,24,'69','AnimatorAssignedVillage object',1,''),(716,'2010-01-19 11:50:29',1,24,'70','AnimatorAssignedVillage object',1,''),(717,'2010-01-19 12:09:41',1,19,'135','grp1',2,'Added person \"p1\". Added person \"p2\".'),(718,'2010-01-19 12:11:10',1,19,'136','grp2',2,'Added person \"p3\". Added person \"p4\".'),(719,'2010-01-19 12:12:16',1,19,'137','grp3',2,'Added person \"p5\". Added person \"p6\".'),(720,'2010-01-19 12:15:32',1,22,'70','a1',2,'Changed csp_flag, camera_operator_flag and facilitator_flag.'),(721,'2010-01-19 12:15:54',1,22,'71','a2',2,'Changed csp_flag, camera_operator_flag and facilitator_flag.'),(722,'2010-01-19 12:16:14',1,22,'72','a3',2,'Changed csp_flag, camera_operator_flag and facilitator_flag.'),(723,'2010-01-19 12:23:42',1,17,'66','Test Village',2,'No fields changed.'),(724,'2010-01-27 00:17:11',7,19,'133','Maa Binapani, Maa Durga',2,'Added person \"Binati Naik\". Added person \"Hemalata Naik\". Added person \"Maalati Naik\". Added person \"Srimani Naik\". Added person \"Keshni Naik\". Added person \"Pakana Naik\". Added person \"Painta Naik\". Added person \"Sita Naik\". Added person \"Malli Naik\". Added person \"Ratani Naik\". Added person \"Somabari Naik\". Added person \"Saita Naik\". Added person \"Sukumati Naik\". Added person \"Khaira Naik\". Added person \"Padmini Naik\". Added person \"Dhukhini Hembram\". Added person \"Bini Hembram\". Added person \"Raibari Hembram\". Added person \"Suryamani  Hembram\". Added person \"Sumi Purty (A)\". Added person \"Bali Hembram\". Added person \"Mani Purty\". Added person \"Jayanti Lohar\". Added person \"Gurubari Lohar\". Added person \"Laxmi Hembram\". Added person \"Khirodi Behera\". Added person \"Sumi Purty (b)\". Added person \"Pani Hembram\".'),(725,'2010-01-27 00:17:21',7,19,'133','Maa Binapani, Maa Durga',2,'Added person \"Binati Naik\". Added person \"Hemalata Naik\". Added person \"Maalati Naik\". Added person \"Srimani Naik\". Added person \"Keshni Naik\". Added person \"Pakana Naik\". Added person \"Painta Naik\". Added person \"Sita Naik\". Added person \"Malli Naik\". Added person \"Ratani Naik\". Added person \"Somabari Naik\". Added person \"Saita Naik\". Added person \"Sukumati Naik\". Added person \"Khaira Naik\". Added person \"Padmini Naik\". Added person \"Dhukhini Hembram\". Added person \"Bini Hembram\". Added person \"Raibari Hembram\". Added person \"Suryamani  Hembram\". Added person \"Sumi Purty (A)\". Added person \"Bali Hembram\". Added person \"Mani Purty\". Added person \"Jayanti Lohar\". Added person \"Gurubari Lohar\". Added person \"Laxmi Hembram\". Added person \"Khirodi Behera\". Added person \"Sumi Purty (b)\". Added person \"Pani Hembram\".'),(726,'2010-01-27 00:17:25',7,19,'133','Maa Binapani, Maa Durga',2,'Added person \"Binati Naik\". Added person \"Hemalata Naik\". Added person \"Maalati Naik\". Added person \"Srimani Naik\". Added person \"Keshni Naik\". Added person \"Pakana Naik\". Added person \"Painta Naik\". Added person \"Sita Naik\". Added person \"Malli Naik\". Added person \"Ratani Naik\". Added person \"Somabari Naik\". Added person \"Saita Naik\". Added person \"Sukumati Naik\". Added person \"Khaira Naik\". Added person \"Padmini Naik\". Added person \"Dhukhini Hembram\". Added person \"Bini Hembram\". Added person \"Raibari Hembram\". Added person \"Suryamani  Hembram\". Added person \"Sumi Purty (A)\". Added person \"Bali Hembram\". Added person \"Mani Purty\". Added person \"Jayanti Lohar\". Added person \"Gurubari Lohar\". Added person \"Laxmi Hembram\". Added person \"Khirodi Behera\". Added person \"Sumi Purty (b)\". Added person \"Pani Hembram\".'),(727,'2010-01-27 00:23:51',7,19,'133','Maa Binapani, Maa Durga',2,'No fields changed.'),(728,'2010-01-27 00:31:47',7,19,'133','Maa Binapani, Maa Durga',2,'No fields changed.'),(729,'2010-01-27 00:44:12',7,19,'132','Maa Gajabiani, Baitrani Om Maa Tarini',2,'Added person \"Laxmi Chattar\". Added person \"Malati Pingua\". Added person \"Chmpabati Pingua\". Added person \"Rani Chattar\". Added person \"Sumtra Sai\". Added person \"Nirash Chattar\". Added person \"Sandhari Chattar\". Added person \"Gurubari Chattar\". Added person \"Yatri Chattar\". Added person \"Mukta Chattar\". Added person \"Sukrumani Pingua\". Added person \"Suryamani Chattar\". Added person \"Padmini Naik\". Added person \"Jaumani Naik\". Added person \"Pramila Naik\". Added person \"Malli Naik\". Added person \"Rajani Naik\". Added person \"Sabita Naik\". Added person \"Sumitra Naik\". Added person \"Kainta Naik\". Added person \"Saraswati Naik\". Added person \"Sadhabani Naik\". Added person \"Beni Naik\". Added person \"Jaumani Naik\". Added person \"Suniti Naik\". Added person \"Daimati Naik\". Added person \"Mandakini Naik\".'),(730,'2010-01-27 01:03:45',7,19,'131','Sri Krishna, Maa Tulashi',2,'Added person \"Rukmani Chattar\". Added person \"Meena Pingua\". Added person \"Dasama Pingua\". Added person \"Asha Pingua\". Added person \"Seti Pingua\". Added person \"Kuni Chattar\". Added person \"Subuni Pingua\". Added person \"Subha Bandar\". Added person \"Jana Pingua\". Added person \"Sabita Chattar\". Added person \"Sunita Chattar\". Added person \"Binati Chattar\". Added person \"Sangita Chattar\". Added person \"Jamuna Chattar\". Added person \"Jana Pingua\". Added person \"Sita Chattar\". Added person \"Mukta Chattar\". Added person \"Padmabati Chattar\". Added person \"Nagari Chattar\". Added person \"Sambari Pingua\". Added person \"Mirju Chattar\". Added person \"Sini Chattar\". Added person \"Turi Pingua\". Added person \"Sanjulata Chattar\".'),(731,'2010-01-27 01:48:37',7,19,'130','Maa Mangala, Maa Kichikeshwari',2,'Added person \"Kasturi Chatter\". Added person \"Sukanti Purty\". Added person \"Malati Chatter\". Added person \"Jemamani Tiu\". Added person \"Budhuni Chatter\". Added person \"Sansari Sinku\". Added person \"Janaki Chatter\". Added person \"Muktamani Tiria\". Added person \"Rajani Chatter\". Added person \"Dasama Tiu\". Added person \"Bhabani Pingua\". Added person \"Shrimati Naik\". Added person \"Malati Sae\". Added person \"Pani Pingua\". Added person \"Menja Chatter\". Added person \"Lembo Pingua\". Added person \"Padmini munda Lohar\". Added person \"Laxmi Chattar\". Added person \"Sumitra Chattar\". Added person \"Suryamani chattar\". Added person \"Khaira Hembram\". Added person \"Menjari Hembram\". Added person \"Padmini Pingua\". Added person \"Budhuni Chattar\". Added person \"Bela Purti\". Added person \"Dubgi Hembram\". Added person \"Sapani Pingua\". Added person \"Sombari soya\". Added person \"Pani Chattar\". Added person \"Turi Pingua\".'),(732,'2010-01-27 02:02:54',7,19,'129','Marangburu Samled,Sagar Serali',2,'Changed days. Added person \"Malati Tudu\". Added person \"Maidi Tudu\". Added person \"Duli Tudu(A)\". Added person \"Duli Tudu(B)\". Added person \"Hiramani Tudu\". Added person \"Sebati Tudu\". Added person \"Sita Tudu(A)\". Added person \"Raude Tudu\". Added person \"Sita Tudu(B)\". Added person \"Jhanamani Tudu\". Added person \"Paya Hansda\". Added person \"Jaba Tudu\". Added person \"Hiramani Tudu\". Added person \"Sukmati Hansda\". Added person \"Parbati Tudu\". Added person \"Jima Honaga\". Added person \"Chhabi Kisku\". Added person \"Nangi Tudu\". Added person \"Nitima Honaga\". Added person \"Rani Tudu\". Added person \"Raimat Tudu\". Added person \"Phulamani Soren\". Added person \"Manki Soren\". Added person \"Metal Soren\". Added person \"Sakra Tudu\".'),(733,'2010-01-27 02:10:32',7,19,'128','Athra Deuli, Maa Laxmi',2,'Changed days. Added person \"Jayanti Honnaga(A)\". Added person \"Raimani Honnaga\". Added person \"Lalmati Honnaga\". Added person \"Harsamani Honnaga\". Added person \"Hiramani Honnaga\". Added person \"Jayanti Honaga(B)\". Added person \"Dusi Honnaga\". Added person \"Champabati Honnaga\". Added person \"Sulekha Honnaga\". Added person \"Kanti Dehuri\". Added person \"Budhini Honnaga\". Added person \"Panabati Honnga\". Added person \"Sumitra Honnaga\". Added person \"Chandumani Honnaga\". Added person \"Damayanti Honnaga\". Added person \"Jemamani Honnga\". Added person \"Keshini Honnaga\". Added person \"Juneidevi Honnaga\". Added person \"Sabitri Honnaga\". Added person \"Muni Honnaga\". Added person \"Menjri Honnaga\". Added person \"Tribeni Dehuri\".'),(734,'2010-01-27 02:42:23',7,19,'127','Shivani,Bijal Bale Bijali Taras',2,'Changed days. Added person \"Sakuntala Tudu\". Added person \"Manania Tudu\". Added person \"Basumati Tudu\". Added person \"Sanamani Tudu\". Added person \"Gurubari Pingua\". Added person \"Padmabati Tudu\". Added person \"Dhujamani Tudu\". Added person \"Parbati Tudu\". Added person \"Baijaynti Hansda\". Added person \"Baijaynti Hansda\". Added person \"Manita Tudu\". Added person \"Pana Murmu\". Added person \"Hira mani Hasada\". Added person \"Jhingimani Alda\". Added person \"Sakra Murmu\". Added person \"Ranimani Hembram\". Added person \"Champa Hembram\". Added person \"Mainabati Tudu\". Added person \"Champabati Hansda\". Added person \"Bija Soren\". Added person \"Rani Soren\". Added person \"Nasa Besra\". Added person \"Pani Besra\". Added person \"Raimani Soren\". Added person \"Dulari Hembram\". Added person \"Yamunamani Soren\". Added person \"Salama Soren\". Added person \"Nagimani Soren\". Added person \"Chhita Hansda\". Added person \"Karmi Hansda\".'),(735,'2010-01-27 02:43:57',7,19,'127','Shivani,Bijal Bale Bijali Taras',2,'Added person \"Bini Hembram\". Added person \"Raibari Hembram\".'),(736,'2010-01-27 02:51:59',7,19,'126','Shiv Parbati, Kaa Shanti Niketan',2,'Changed days. Added person \"Bimala Naik\". Added person \"Tulasi Naik\". Added person \"Nandini Naik\". Added person \"Srimati Naik\". Added person \"Padmabati Naik\". Added person \"Bilasi Naik\". Added person \"Puspalata Naik\". Added person \"Daita Naik\". Added person \"Beni Naik\". Added person \"Ruduni Naik\". Added person \"Sasmita Mohakud\". Added person \"Pramila Naik\". Added person \"Bimala Naik\". Added person \"Mandadari Naik\". Added person \"Rahaswari Naik\". Added person \"Bilasi Naik\". Added person \"Sabitri Naik\". Added person \"Aira  Naik\". Added person \"Nalita Naik\". Added person \"Saradi Naik\". Added person \"Mangali  Naik\". Added person \"Sulekha Naik\". Added person \"Adara Naik\". Added person \"Pemi Naik\". Added person \"Jaleswari Naik\". Added person \"Ruduna Naik\". Added person \"Sebati Naik\". Added person \"Binati Naik\".'),(737,'2010-01-27 02:57:24',7,19,'125','Sagun Sarna,Marshal Mahila Kendra',2,'Added person \"Phulamani Marandi\". Added person \"Basanti Tudu (A)\". Added person \"Dulimani Beshra\". Added person \"Basanti Tudu (B)\". Added person \"Yamuna Hembram\". Added person \"Malaho Tudu\". Added person \"Phulamani Soren\". Added person \"Jauna Beshara\". Added person \"Sumi Tudu\". Added person \"Pauri Tudu\". Added person \"Samiya Tudu\". Added person \"Sahagi Tudu\". Added person \"Jamumuna Majhi\". Added person \"Subani Besra\". Added person \"Lilmani Soren\". Added person \"Gouri Tudu\". Added person \"Padmabati Tudu\". Added person \"Ganga Kisku\". Added person \"Maina Tudu\". Added person \"Manak Tudu\". Added person \"Gangi Tudu\". Added person \"Shanti Tudu\". Added person \"Manasirani Majhi\". Added person \"Dukhini Hembram\".'),(738,'2010-01-27 03:02:55',7,19,'124','Maa Basuki Devi, Maa Santoshi',2,'Added person \"Kanchan Lohar\". Added person \"Jeetmani Mohanta\". Added person \"Deepanjali Patra\". Added person \"Minaka Mohanta\". Added person \"Tobharani Mohakud\". Added person \"Rebati Mohanta\". Added person \"Nirupama Mohanta\". Added person \"Sushanti Mohanta\". Added person \"Shantilata Mohanta\". Added person \"Chmpabati Hembram\". Added person \"Chanchala Mohanta\". Added person \"Parbati Bandra\". Added person \"Parbati Gagrai\". Added person \"Raimani Honnaga\". Added person \"Basanti Jamuda\". Added person \"Laxmirani Sinku\". Added person \"Nasamani Sinku\". Added person \"Menga Sinku\". Added person \"Lilmani Goipai\". Added person \"Namita Goipai\". Added person \"Bela Goipai\". Added person \"Laxmi Sinku\". Added person \"Sumati Bandra\". Added person \"Laxmi Goipai\". Added person \"Rashmi Rekha Naik\".'),(739,'2010-01-27 03:17:00',7,19,'123','Subhalaxmi',2,'Added person \"Nrupati Nayak\". Added person \"Sakuntala Nayak\". Added person \"Tillottama Nayak\". Added person \"Latika Nayak\". Added person \"Binati Nayak\". Added person \"Paramani Nayak\". Added person \"Chanchala Nayak\". Added person \"Puspalata Nayak\". Added person \"Madhabi Nayak\". Added person \"Rukmani Nayak\".'),(740,'2010-01-27 03:42:09',7,19,'122','Marangbanga, Dharitree',2,'Added person \"Sunamani Chattar\". Added person \"Sarojini Chattar\". Added person \"Srimati Chattar\". Added person \"Malati Chattar\". Added person \"Damayanti Chatar\". Added person \"Jannamani Chattar\". Added person \"Sita Chattar\". Added person \"Gurubari Chatar\". Added person \"Sabitree Chattar\". Added person \"Nandi Chatar\". Added person \"Jhunu Guiya\". Added person \"Junee Purty\". Added person \"Pyari Chatar\". Added person \"Kuni Guiya\". Added person \"Binapani Chattar\". Added person \"Parbati Guiya\". Added person \"Sukumati Chatar\". Added person \"Sushama Chatar\". Added person \"Sumitra Chatar\". Added person \"Menja Chatar\". Added person \"Mangulli Chatar\". Added person \"Jana Chatar\". Added person \"Sukumati Chatar(B)\". Added person \"Basanti Chatar\". Added person \"Saibanee Chatar\". Added person \"Baijayanti Chatar\". Added person \"Somabari Chatar\". Added person \"Sini Chatar\". Added person \"Sakuntalla Bankira\".'),(741,'2010-01-27 03:48:03',7,19,'121','Balhe Sagen, Aang Marshal',2,'Added person \"Kasturi Chattar\". Added person \"Sasmita Chattar\". Added person \"Raibari Chattar\". Added person \"Suru Chatar\". Added person \"Basanti Chattar\". Added person \"Sushilla Chattar\". Added person \"Lakshmi  Chattar\". Added person \"Meena Chattar\". Added person \"Tillatamma  Chattar\". Added person \"Samabari Chattar\". Added person \"Jemamani Chattar\". Added person \"Chamanu Chattar\". Added person \"Sushama Tiria\". Added person \"Basanti Bankira\". Added person \"Hachi Chatar\". Added person \"Sukanti Bankira\". Added person \"Jayanti Chatar\". Added person \"Pullamani Bankira\". Added person \"Raimani Chatar\". Added person \"Dashama Tiria\". Added person \"Nillima Chatar\". Added person \"Surjyamani Tiria\". Added person \"Durapati Bankira\". Added person \"Buduni  Bankira\". Added person \"Debaki Chatar\". Added person \"Srimati Chatar\".'),(742,'2010-01-27 03:54:22',7,19,'120','Gajalaxmi, Maa Tarini',2,'Added person \"Rebati Nayak\". Added person \"Pramila Nayak\". Added person \"Purabi Nayak\". Added person \"Padmini Nayak\". Added person \"Tilattama Nayak\". Added person \"Satyabhama Nayak\". Added person \"Shakuntala Nayak\". Added person \"Jayanti Nayak\". Added person \"Netramani Nayak\". Added person \"Tapaswini Nayak\". Added person \"Bhabani Nayak(B)\". Added person \"Binati Nayak\". Added person \"Raimani Pingua\". Added person \"Gurubari Pingua\". Added person \"Chandu Pingua\". Added person \"Samabari Pingua(A)\". Added person \"Damayanti Nayak\". Added person \"Rukmani Patra\". Added person \"Jayanti Patra\". Added person \"Damayanti Pingua\". Added person \"Chami Pingua\". Added person \"Gangi Hembram\". Added person \"Pramila Tiria\". Added person \"Asha Patra\". Added person \"Samabari Pingua(B)\". Added person \"Sukanti Pingua\". Added person \"Laxmi Pingua\". Added person \"Charima Pingua\".'),(743,'2010-01-27 04:00:51',7,19,'119','Maa Tulashi, Baba Mukteswara',2,'Added person \"Jashoda Nayak\". Added person \"Jatani Nayak\". Added person \"Pukulli Nayak\". Added person \"Babita Nayak\". Added person \"Chabirani Nayak\". Added person \"Sakuntala Nayak\". Added person \"Mahendri Nayak\". Added person \"Gitarani Nayak\". Added person \"Sumanti Nayak\". Added person \"Kasturi Nayak\". Added person \"Bhabani Nayak\". Added person \"Runurani Nayak\". Added person \"Bhoumirani Nayak\". Added person \"Manjulata Nayak\". Added person \"Ranjeeta Nayak\". Added person \"Surekha Nayak\". Added person \"Manjubala  Nayak\". Added person \"Mahendri Nayak\". Added person \"Sujata Nayak\". Added person \"Kanakalata  Nayak\". Added person \"Mita Nayak\". Added person \"Dalimba Nayak\". Added person \"Sanjukta Nayak\". Added person \"Premalata Nayak\". Added person \"Kasturi Nayak\". Added person \"Banita Nayak\". Added person \"Rajani Nayak\". Added person \"Srimati Bewa\". Added person \"Kishori Nayak\". Added person \"Maitree Nayak\".'),(744,'2010-01-27 04:13:23',7,19,'118','Sibasakti, Bholanath',2,'Added person \"Jyosnamayee Nayak\". Added person \"Padmasani Nayak\". Added person \"Dalimba Nayak\". Added person \"Tribeni Nayak\". Added person \"Tilottama Nayak\". Added person \"Sabita Nayak(A)\". Added person \"Gouribati Nayak\". Added person \"Droupadri Nayak(A)\". Added person \"Droupadri Nayak(B)\". Added person \"Sabita Nayak(B)\". Added person \"Sakuntala Nayak\". Added person \"Damayanti Nayak\". Added person \"Bhanumati Nayak\". Added person \"Jayanti Nayak\". Added person \"Droupadri Nayak(C)\". Added person \"Nidramani Nayak\". Added person \"Mandodari Nayak\". Added person \"Sasikala Nayak\". Added person \"Kusumanjali Nayak\". Added person \"Manjulata Nayak\". Added person \"Bhabani Nayak\". Added person \"Kautuki Nayak\". Added person \"Sulochana Nayak\". Added person \"Bharati Nayak\". Added person \"Kanakalata Nayak\". Added person \"Tusarkanti Nayak\". Added person \"Debaki Nayak\". Added person \"Pramila Nayak\". Added person \"Gandhari Nayak\". Added person \"Gitanjali Nayak\".'),(745,'2010-01-27 04:14:14',7,19,'118','Sibasakti, Bholanath',2,'Added person \"Pramila Naik(B)\".'),(746,'2010-01-27 04:31:43',7,17,'67','Ramchandrapur',1,''),(747,'2010-01-27 04:34:47',7,17,'68','Chandusahi',1,''),(748,'2010-01-27 04:37:43',7,17,'69','Dumbisahi',1,''),(749,'2010-01-27 04:37:48',7,22,'69','Kuni',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(750,'2010-01-27 04:54:00',7,19,'143','Sarjamburu,Dinga Marshal,Maa Gouri Shree Chandyapat',2,'Changed group_name. Added person \"Pyari Sundhi\". Added person \"Hemamalini Sundhi\". Added person \"Sini Soye\". Added person \"Subani soye\". Added person \"Rina Soye\". Added person \"Barsa Hesa\". Added person \"Menjari Hesa\". Added person \"Jambi Kandayang\". Added person \"Dasama Kandayang\". Added person \"Kirati Soya\". Added person \"Rajani Soya\". Added person \"Kuni Rani Sundhi\". Added person \"Dasama Soya\". Added person \"Chireng Hesa\". Added person \"Anami Kendayang\". Added person \"Surmi Soya\". Added person \"Kudugi Kendayang\". Added person \"Juguni Hesa\". Added person \"Jatri Mahakud\". Added person \"Purnami sundhi\". Added person \"Surjamani Sundhi\". Added person \"Sujuki Soye\". Added person \"Srimati Tiu\".'),(751,'2010-01-27 05:00:48',7,19,'142','Sarjamburu,Dinga Marshal,Maa Gouri Shree Chandyapat',2,'Changed group_name. Added person \"Jangamani Honnaga\". Added person \"Assai Honnaga\". Added person \"Gangi Honnaga\". Added person \"Sumitra Honnaga\". Added person \"Mechcha Honnaga\". Added person \"Basanti Honnaga\". Added person \"Jana Honnaga\". Added person \"Budhuni Honnaga\". Added person \"Diugi Honnaga\". Added person \"Hauri Honnaga\". Added person \"Jahari Honnaga\". Added person \"Munguli Honnaga\". Added person \"Malati Honnaga\". Added person \"Pangela Honnaga\". Added person \"Parbati Honnaga\". Added person \"Buduni Honnaga(B)\". Added person \"Sita Honnaga\". Added person \"Budhuni Honnaga(C)\". Added person \"Masuri Honnaga\". Added person \"Binati Honnaga\". Added person \"Gangi Honnaga\". Added person \"Phulmani Honnaga\". Added person \"Sabitri Honnaga\". Added person \"Manju Honnaga\".'),(752,'2010-01-27 05:05:47',7,19,'141','Maa Besauli,Laxminarayan',2,'Added person \"Smt. Balema Hesah\". Added person \"Smt. Jayanti Hesah\". Added person \"Smt . Naguri Purtty\". Added person \"Smt. Bahmain Hesah\". Added person \"Mani Purtty\". Added person \"Jayanti Hesah\". Added person \"Laxmi Buliuli\". Added person \"Chandini Buliuli\". Added person \"Premanjali Pat Pingua\". Added person \"Smt. Jambi Buliuli\". Added person \"Rashasmi Purty\". Added person \"Smt. Bela Pingua\". Added person \"Smt. Laxmi Dei\". Added person \"Smt. Binodini Dei\". Added person \"Smt. Sulochana Dei\". Added person \"Smt. Kunta Dei\". Added person \"Smt. Kokila Dei\". Added person \"Smt. Mithila Dei\". Added person \"Smt. Sumati Dei\". Added person \"Smt. Surekha Dei\". Added person \"Smt. Saraswati Mahakud\". Added person \"Smt. Padmabati Dei\". Added person \"Smt. Sharala Mahakud\". Added person \"Smt. Dukhini Mahakud\". Added person \"Smt. Ambika Dei\". Added person \"Dalimba Dei\". Added person \"Lilabati Dei\".'),(753,'2010-01-27 05:10:04',7,19,'140','Maa Tarini,Maa Chandipat',2,'Added person \"Tilattama Nayak\". Added person \"Rukmani Bewa\". Added person \"Kanchana Nayak\". Added person \"Gitamani Nayak\". Added person \"Bhanumati Nayak\". Added person \"Sarojeeni Nayak\". Added person \"Labanya Bewa\". Added person \"Bimala Nayak\". Added person \"Jayimani Nayak\". Added person \"Purnami Naik\". Added person \"Saraswati Nayak\". Added person \"Debasri Nayak\". Added person \"Sabitri Nayak\". Added person \"Indumati Nayak\". Added person \"Jemamani Purty\". Added person \"Subhadra Pingua\". Added person \"Namsi Purty\". Added person \"Masuree Pingua\". Added person \"Mita Pingua\". Added person \"Sombari Pingua\". Added person \"Belmatee Pingua\". Added person \"Padmabati Nayak\". Added person \"Suduni Pingua\". Added person \"Malati Nayak\". Added person \"Parbati Purti\". Added person \"Minako Kuldi\".'),(754,'2010-01-27 05:11:25',7,19,'140','Maa Chandipat,Maa Tarini',2,'Changed group_name.'),(755,'2010-01-27 05:15:01',7,19,'139','Maa Parbati',2,'Added person \"Mina Mahakud\". Added person \"Purnnami Mahakud\". Added person \"Gauri Mahakud\". Added person \"Sumitra Kandeyang\". Added person \"Jayanti Kandeyang\". Added person \"Minakumari Mahakud\". Added person \"Parbati Hembram\". Added person \"Sarati Behera\". Added person \"Saibani Behera\". Added person \"Pala Hembram\". Added person \"Sukanti Hembram(A)\". Added person \"Sukanti Hembram(B)\". Added person \"Shakuntala Kandeyang\". Added person \"Tulasi Tiu\". Added person \"Ambika kandeyang\". Added person \"Rajani Mahakud\". Added person \"Gangamani Hembramf\".'),(756,'2010-01-27 05:19:35',7,19,'138','Laxminarayan',2,'Added person \"Hiramani Munduri\". Added person \"Sukamati Hembram\". Added person \"Nandi Hembram\". Added person \"Priyamani Mahakud\". Added person \"Phulamani Kandeyan\". Added person \"Marsa Malen Hembram\". Added person \"Somabari Hembram\". Added person \"Bhanumati Mahakud\". Added person \"Sanjita Kandeyan\". Added person \"Chandrika Kandeyan\". Added person \"Basanti Mahakud\". Added person \"Sunai Hembram\". Added person \"Bharati Mahakud\". Added person \"Sumitra Behera\". Added person \"Menja Hembram\". Added person \"Gangi Hembram\". Added person \"Subasini Mahakud\". Added person \"Jemamani Kandeyan\". Added person \"Ramani Hembram\". Added person \"Lillmani Mahakud\".'),(757,'2010-01-27 05:29:26',7,22,'75','Kuni Rani Sundhi',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(758,'2010-01-27 05:30:00',7,22,'74','Kuni Rani Sundhi',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(759,'2010-01-27 05:30:22',7,22,'73','Kuni Rani Sundhi',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(760,'2010-01-27 05:30:47',7,22,'68','Paray Pingua',2,'No fields changed.'),(761,'2010-01-27 05:31:23',7,22,'67','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(762,'2010-01-27 05:31:52',7,22,'67','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(763,'2010-01-27 05:32:24',7,22,'66','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(764,'2010-01-27 05:32:42',7,22,'66','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(765,'2010-01-27 05:33:10',7,22,'65','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(766,'2010-01-27 05:33:27',7,22,'65','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(767,'2010-01-27 05:34:21',7,22,'63','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(768,'2010-01-27 05:34:41',7,22,'63','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(769,'2010-01-27 05:55:15',1,22,'65','Hrushikesh Goipai',3,''),(770,'2010-01-27 05:55:15',1,22,'66','Hrushikesh Goipai',3,''),(771,'2010-01-27 05:55:15',1,22,'67','Hrushikesh Goipai',3,''),(772,'2010-01-27 05:55:29',1,22,'56','Hrushikesh Goipai',3,''),(773,'2010-01-27 05:55:29',1,22,'64','Hrushikesh Goipai',3,''),(774,'2010-01-27 05:55:48',1,22,'74','Kuni Rani Sundhi',3,''),(775,'2010-01-27 05:55:48',1,22,'73','Kuni Rani Sundhi',3,''),(776,'2010-01-27 05:56:10',1,22,'57','Koutaki',3,''),(777,'2010-01-27 05:56:48',1,22,'61','Ramakant',3,''),(778,'2010-01-27 05:56:48',1,22,'60','Ramakanta',3,''),(779,'2010-01-27 05:57:18',7,22,'63','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(780,'2010-01-27 05:57:37',7,22,'75','Kuni Rani Sundhi',2,'No fields changed.'),(781,'2010-01-27 05:58:50',7,22,'68','Paray Pingua',2,'Changed village for animator assigned village \"AnimatorAssignedVillage object\".'),(782,'2010-01-27 05:59:08',7,22,'63','Hrushikesh Goipai',2,'No fields changed.'),(783,'2010-01-27 05:59:21',7,22,'62','Ramakant',2,'No fields changed.'),(784,'2010-01-27 05:59:41',7,22,'59','Koutaki Nayak',2,'No fields changed.'),(785,'2010-01-27 06:01:52',7,17,'70','Kendumundhi',1,''),(786,'2010-01-27 06:01:57',7,22,'58','Bihar Singh',2,'Changed home_village.'),(787,'2010-01-27 06:14:39',1,17,'65','Chandusahi',3,''),(788,'2010-01-27 09:48:29',1,17,'64','Khandbandha',3,''),(789,'2010-01-27 09:49:10',1,17,'62','Khandbandha',2,'Added animator \"Paray Pingua\".'),(790,'2010-01-27 09:50:15',1,17,'61','Khandbandha',3,''),(791,'2010-01-27 09:51:06',1,17,'51','Ektali',3,''),(792,'2010-01-27 09:51:52',1,17,'36','Pandutalab',3,''),(793,'2010-01-27 09:52:46',1,17,'54','Deuli',3,''),(794,'2010-01-27 10:10:23',1,17,'66','Test Village',3,''),(795,'2010-01-27 10:11:28',1,24,'39','AnimatorAssignedVillage object',3,''),(796,'2010-01-30 02:00:52',7,26,'132','Santhali',1,''),(797,'2010-01-31 21:46:06',7,24,'104','AnimatorAssignedVillage object',1,''),(798,'2010-01-31 21:49:05',7,17,'71','Kaluakhaman',1,''),(799,'2010-01-31 21:55:44',7,22,'58','Bihar Singh',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(800,'2010-01-31 21:57:36',7,17,'72','Palsagadia',1,''),(801,'2010-01-31 21:58:39',7,17,'73','Jhunriposhi',1,''),(802,'2010-01-31 21:58:49',7,22,'58','Bihar Singh',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(803,'2010-01-31 21:59:23',7,17,'74','Rangalbeda',1,''),(804,'2010-01-31 22:00:05',7,17,'75','Badhubheda',1,''),(805,'2010-01-31 22:01:07',7,22,'58','Bihar Singh',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(806,'2010-01-31 22:01:43',7,17,'76','Diajodi',1,''),(807,'2010-01-31 22:02:54',7,22,'58','Bihar Singh',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(808,'2010-01-31 22:04:04',7,17,'77','Tangabila',1,''),(809,'2010-01-31 22:04:38',7,17,'78','Dhuduku',1,''),(810,'2010-01-31 22:04:53',7,22,'58','Bihar Singh',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(811,'2010-01-31 22:05:28',7,17,'79','Bisipur',1,''),(812,'2010-01-31 22:05:34',7,22,'58','Bihar Singh',2,'Added animator assigned village \"AnimatorAssignedVillage object\".'),(813,'2010-01-31 22:06:44',7,22,'63','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(814,'2010-01-31 22:07:20',7,22,'63','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(815,'2010-01-31 22:08:08',7,22,'63','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(816,'2010-01-31 22:08:49',7,22,'63','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(817,'2010-01-31 22:09:43',7,22,'63','Hrushikesh Goipai',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(818,'2010-01-31 22:10:31',7,22,'59','Koutaki Nayak',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(819,'2010-01-31 22:11:07',7,22,'59','Koutaki Nayak',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(820,'2010-01-31 22:11:37',7,22,'59','Koutaki Nayak',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(821,'2010-01-31 22:12:08',7,22,'59','Koutaki Nayak',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(822,'2010-01-31 22:12:53',7,22,'59','Koutaki Nayak',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(823,'2010-01-31 22:13:44',7,22,'63','Hrushikesh Goipai',2,'No fields changed.'),(824,'2010-01-31 22:14:20',7,22,'59','Koutaki Nayak',2,'No fields changed.'),(825,'2010-01-31 22:14:53',7,22,'58','Bihar Singh',2,'No fields changed.'),(826,'2010-01-31 22:20:30',7,22,'78','Santosh Naik',1,''),(827,'2010-01-31 22:29:07',7,28,'10','Duck care and treatment',1,''),(828,'2010-01-31 22:30:17',7,27,'22','7 days duck feed and treatment',1,''),(829,'2010-01-31 22:34:31',7,20,'931','Malati Pingua',1,''),(830,'2010-01-31 22:37:09',7,27,'23','7 days duck feed and treatment',1,''),(831,'2010-01-31 22:45:45',7,19,'141','Maa Besauli,Laxminarayan',2,'Added person \"Smt. Balema Hesah\". Added person \"Smt. Jayanti Hesah\". Added person \"Smt . Naguri Purtty\". Added person \"Smt. Bahmain Hesah\". Added person \"Mani Purtty\". Added person \"Jayanti Hesah\". Added person \"Laxmi Buliuli\". Added person \"Laxmi Buliuli\". Added person \"Premanjali Pat Pingua\". Added person \"Smt. Jambi Buliuli\". Added person \"Rashasmi Purty\". Added person \"Smt. Bela Pingua\". Added person \"Smt. Laxmi Dei\". Added person \"Smt. Binodini Dei\". Added person \"Smt. Sulochana Dei\". Added person \"Smt. Kunta Dei\". Added person \"Smt. Kokila Dei\". Added person \"Smt. Mithila Dei\". Added person \"Smt. Sumati Dei\". Added person \"Smt. Surekha Dei\". Added person \"Smt. Saraswati Mahakud\". Added person \"Smt. Padmabati Dei\". Added person \"Smt. Sharala Mahakud\". Added person \"Smt. Dukhini Mahakud\". Added person \"Smt. Ambika Dei\". Added person \"Dalimba Dei\". Added person \"Lilabati Dei\".'),(832,'2010-01-31 22:55:22',7,19,'140','Maa Chandipat,Maa Tarini',2,'Added person \"Tilattama Nayak\". Added person \"Rukmani Bewa\". Added person \"Kanchana Nayak\". Added person \"Gitamani Nayak\". Added person \"Bhanumati Nayak\". Added person \"Sarojeeni Nayak\". Added person \"Labanya Bewa\". Added person \"Bimala Nayak\". Added person \"Jayimani Nayak\". Added person \"Purnami Naik\". Added person \"Saraswati Nayak\". Added person \"Debasri Nayak\". Added person \"Sabitri Nayak\". Added person \"Indumati Nayak\". Added person \"Jemamani Purty\". Added person \"Subhadra Pingua\". Added person \"Namsi Purty\". Added person \"Masuree Pingua\". Added person \"Mita Pingua\". Added person \"Sombari Pingua\". Added person \"Belmatee Pingua\". Added person \"Padmabati Nayak\". Added person \"Suduni Pingua\". Added person \"Malati Nayak\". Added person \"Parbati Purti\". Added person \"Minako Kuldi\".'),(833,'2010-01-31 23:12:45',7,19,'132','Maa Gajabiani, Baitrani Om Maa Tarini',2,'Added person \"Malati Pingua \". Added person \"Chmpabati Pingua \". Added person \"Rani Chattar \". Added person \"Sumtra Sai \". Added person \"Nirash Chattar \". Added person \"Sandhari Chattar \". Added person \"Gurubari Chattar \". Added person \"Yatri Chattar \". Added person \"Mukta Chattar \". Added person \"Sukrumani Pingua \". Added person \"Suryamani Chattar \". Added person \"Padmini Naik \". Added person \"Jaumani Naik \". Added person \"Pramila Naik \". Added person \"Malli Naik \". Added person \"Rajani Naik \". Added person \"Sabita Naik \". Added person \"Sumitra Naik \". Added person \"Kainta Naik \". Added person \"Saraswati Naik \". Added person \"Sadhabani Naik \". Added person \"Beni Naik \". Added person \"Jaumani Naik \". Added person \"Suniti Naik \". Added person \"Daimati Naik \". Added person \"Mandakini Naik \". Changed person_name for person \"Laxmi Chattar \".'),(834,'2010-01-31 23:19:12',7,19,'131','Sri Krishna, Maa Tulashi',2,'Added person \"Sangita Chattar \". Added person \"Jamuna Chattar \". Added person \"Jana Pingua \". Added person \"Sita Chattar \". Added person \"Mukta Chattar \". Added person \"Padmabati Chattar \". Added person \"Nagari Chattar \". Added person \"Sambari Pingua \". Added person \"Mirju Chattar \". Added person \"Sini Chattar \". Added person \"Turi Pingua \". Added person \"Sanjulata Chattar \". Added person \"Rukmani Chattar \". Added person \"Meena Pingua \". Added person \"Dasama Pingua \". Added person \"Asha Pingua \". Added person \"Seti Pingua \". Added person \"Kuni Chattar \". Added person \"Subuni Pingua \". Added person \"Subha Bandar \". Added person \"Jana Pingua \". Added person \"Sabita Chattar \". Added person \"Sunita Chattar \". Changed person_name for person \"Binati Chattar \".'),(835,'2010-01-31 23:35:44',7,19,'130','Maa Mangala, Maa Kichikeshwari',2,'Added person \"Kasturi Chatter \". Added person \"Sukanti Purty \". Added person \"Malati Chatter \". Added person \"Jemamani Tiu \". Added person \"Budhuni Chatter \". Added person \"Sansari Sinku \". Added person \"Janaki Chatter \". Added person \"Muktamani Tiria \". Added person \"Rajani Chatter \". Added person \"Dasama Tiu \". Added person \"Bhabani Pingua \". Added person \"Shrimati Naik \". Added person \"Malati Sae \". Added person \"Pani Pingua \". Added person \"Menja Chatter \". Added person \"Lembo Pingua \". Added person \"Padmini munda Lohar \". Added person \"Laxmi Chattar \". Added person \"Sumitra Chattar \". Added person \"Suryamani chattar \". Added person \"Khaira Hembram \". Added person \"Menjari Hembram \". Added person \"Padmini Pingua \". Added person \"Budhuni Chattar \". Added person \"Bela Purti \". Added person \"Dubgi Hembram \". Added person \"Sapani Pingua \". Added person \"Sombari soya \". Added person \"Pani Chattar \". Added person \"Turi Pingua \".'),(836,'2010-01-31 23:46:57',7,19,'124','Maa Basuki Devi, Maa Santoshi',2,'Added person \"Deepanjali Patra \". Added person \"Minaka Mohanta \". Added person \"Tobharani Mohakud \". Added person \"Rebati Mohanta \". Added person \"Nirupama Mohanta \". Added person \"Sushanti Mohanta \". Added person \"Shantilata Mohanta \". Added person \"Chmpabati Hembram \". Added person \"Chanchala Mohanta \". Added person \"Parbati Bandra \". Added person \"Parbati Gagrai \". Added person \"Raimani Honnaga \". Added person \"Basanti Jamuda \". Added person \"Laxmirani Sinku \". Added person \"Nasamani Sinku \". Added person \"Menga Sinku \". Added person \"Lilmani Goipai \". Added person \"Namita Goipai \". Added person \"Bela Goipai \". Added person \"Laxmi Sinku \". Added person \"Sumati Bandra \". Added person \"Laxmi Goipai \". Changed person_name for person \"Kanchan Lohar \". Changed person_name for person \"Jeetmani Mohanta \".'),(837,'2010-02-01 03:05:58',8,17,'80','Sundari bhosatoli',1,''),(838,'2010-02-01 03:08:04',8,17,'81','sundari pakartoli',1,''),(839,'2010-02-01 03:09:21',8,17,'82','Kokiya',1,''),(840,'2010-02-01 03:11:09',8,17,'83','Prachartoli',1,''),(841,'2010-02-01 03:12:20',8,17,'84','Tirla',1,''),(842,'2010-02-01 03:14:55',8,17,'81','sundari pakartoli',2,'No fields changed.'),(843,'2010-02-01 03:15:35',8,17,'82','Kokiya',2,'No fields changed.'),(844,'2010-02-01 03:16:27',8,17,'83','Prachartoli',2,'No fields changed.'),(845,'2010-02-01 03:17:49',8,17,'84','Tirla',2,'No fields changed.'),(846,'2010-02-01 03:20:21',8,22,'79','Paribal',1,''),(847,'2010-02-01 03:21:29',8,22,'79','Paribal',2,'Added animator assigned village \"AnimatorAssignedVillage object\". Added animator assigned village \"AnimatorAssignedVillage object\".'),(848,'2010-02-01 03:32:46',8,19,'144','Tiliye Baha',1,''),(849,'2010-02-01 03:36:59',8,19,'145','Fulwari Mahila Mandal',1,''),(850,'2010-02-01 03:41:06',8,19,'146','Marshal Mahila Mandal',1,''),(851,'2010-02-01 03:43:46',8,19,'147','Sarjom Baha Mahila Mandal',1,''),(852,'2010-02-01 03:47:34',8,19,'148','Vina Mahila Mandal',1,''),(853,'2010-02-01 04:23:24',7,28,'11','Insecticidal treatment',1,''),(854,'2010-02-01 06:15:21',1,20,'1086','dsfsdf',1,''),(855,'2010-02-01 06:15:35',1,20,'1086','dsfsdf',3,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'message','auth','message'),(6,'content type','contenttypes','contenttype'),(7,'session','sessions','session'),(8,'region','dashboard','region'),(9,'equipment holder','dashboard','equipmentholder'),(10,'reviewer','dashboard','reviewer'),(11,'development manager','dashboard','developmentmanager'),(12,'state','dashboard','state'),(13,'partners','dashboard','partners'),(14,'field officer','dashboard','fieldofficer'),(15,'district','dashboard','district'),(16,'block','dashboard','block'),(17,'village','dashboard','village'),(18,'monthly cost per village','dashboard','monthlycostpervillage'),(19,'person groups','dashboard','persongroups'),(20,'person','dashboard','person'),(21,'person relations','dashboard','personrelations'),(22,'animator','dashboard','animator'),(23,'training','dashboard','training'),(24,'animator assigned village','dashboard','animatorassignedvillage'),(25,'animator salary per month','dashboard','animatorsalarypermonth'),(26,'language','dashboard','language'),(27,'video','dashboard','video'),(28,'practices','dashboard','practices'),(29,'screening','dashboard','screening'),(30,'person meeting attendance','dashboard','personmeetingattendance'),(31,'person adopt practice','dashboard','personadoptpractice'),(32,'equipment id','dashboard','equipmentid'),(33,'random','dashboard','random');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY  (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('e9c567d8ed982ba14ed052670ef1073c','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-06 22:04:12'),('2f850debd5bd7932adb94d2800358ef7','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-04 17:39:49'),('4da201bfe40c569ce5e2040e22c1bd89','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-04 15:15:34'),('7ee03814500aee9f6846defbc055a9de','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-27 05:23:44'),('91f0ae8f8585cff7b40829ac9c66a3b2','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-06 22:03:02'),('c7a40f025514fc758bb196822fad4f8b','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2009-09-15 10:13:50'),('aed4a189bdf6a452d64fb71a7df888e8','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-20 22:38:01'),('8a7c35adb1b44c23cda86ad003c7b1e6','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2009-09-05 19:29:32'),('d2112729d74dda121e84edbeafd5d771','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2009-09-21 14:37:52'),('122f05a37bd40dd97f81e726df36a2a8','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-19 22:08:42'),('c31a838ba1e48c0681f737e122dcf422','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-20 17:15:55'),('6c48b398e0e3442a3f53c3f4afb13e68','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-22 22:16:36'),('b1e54365549d80ea462c12aaebc22c4a','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-11-24 05:08:13'),('6e72d2c9e33e70b59fd87c07b9fce4e3','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-09-28 23:45:23'),('5a7023ca247b009e60df5ae0207d2b94','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-06 23:11:29'),('1a124bac5ba3071bfec6aa7a5e9855f9','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-22 23:47:46'),('9e0f087f4fb183ae3104033c3763759d','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-21 11:28:29'),('4a2fe186f7019e1b33a68e7c5e8a0545','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-22 23:35:51'),('b8fe68ed7eabc350b29740176053755f','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-14 23:43:34'),('57e961e2d02fc3cd54f16bf927dc49d4','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-20 09:40:18'),('c03e5e07a4dc2bcd73f06b5643b78dbf','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-24 13:43:58'),('de4614a8e0fb3a38258322277ec6ae2b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-22 23:42:14'),('3b5bc8b51071f4f728b10192b9031fc8','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEMdS5mZmI2YTY2MzViNzYxYjM1NDk0\nMGY3NzAyM2NjYjkyYQ==\n','2009-11-16 11:02:37'),('ce4db53cd93da081f254b1738f4855f6','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-25 13:06:19'),('8f89820b7e824491fc9988f159b69402','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS44MzVjNmJjMjUxMzAwMDEyNjY5\nMDhjMmNhYjUwYjAwNw==\n','2009-10-25 23:26:51'),('84af6113376a766d9834f09616bb27b6','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-25 23:31:25'),('19f1552999efd876e625a4930393dc43','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-26 00:32:56'),('c38475298c7e448026aec3f2b01362c1','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS44MzVjNmJjMjUxMzAwMDEyNjY5\nMDhjMmNhYjUwYjAwNw==\n','2009-10-26 02:37:35'),('500c31ab41a463ef4a2bf3b9169d45ad','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-26 02:47:28'),('62fce5bd5339262d512cbf2088fbc1df','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS44MzVjNmJjMjUxMzAwMDEyNjY5\nMDhjMmNhYjUwYjAwNw==\n','2009-10-26 02:56:36'),('2fa0fe71e847d9a032ccbae20cd02eac','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS45YzY1NGM5NTY2YWU1MzM5ZWUz\nNWUxMzk2YWU0NjNjMQ==\n','2009-10-26 02:58:15'),('06df2b90b00a5a2551d121e4cbe59640','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-26 03:15:43'),('9e7e8300da4d917810954f3a6feb2df2','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-26 12:41:24'),('75124717d5da3cb1e7202caa043d1885','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-26 14:19:33'),('f1fdd4a3754e70ec72c7483e6b9199b4','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mMDQ3ZmRkNDliMGJkNTAzODk2\nNGYxZTk3MmE3MjIwMw==\n','2009-10-26 14:44:38'),('207396de799807b166e342e0ecfdfcc6','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-26 14:45:59'),('44e198125d7e30a1083b10cc03814b92','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-27 05:54:04'),('4be41929ef741bb214b4334b8722ef39','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-27 06:03:25'),('c8b9c5c1428f0a4f4127f019f7c70cd7','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-27 06:07:35'),('5a77b12782fb40140918b769bfea8681','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-28 00:49:58'),('4decc8d20b4879ec03a5c176596f25c7','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-28 01:22:34'),('8f0204f51ab0583bba25c0c8b19e03b4','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-10-30 15:45:33'),('a410f785791b26964fe832013708aed0','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2009-11-14 07:18:54'),('0134708261dca068f329538741082fc5','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEKdS44NzI2YmY1NjNlNmU1NjViMGZi\nMGVlMWZmZmEwOWNhMA==\n','2009-11-14 02:37:17'),('6528d04071809c966e566a0be4983edb','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2009-11-13 06:42:04'),('2b3d23ebc36bccbe015e675f647162cf','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2009-11-13 12:48:50'),('d4f2bacdc0e43a8e7201b2c692562508','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEGdS42MDA1ZTgzN2VkZjBiM2RjZmE4\nNjI5NDgwOTA3NmY5Mw==\n','2009-11-09 04:28:29'),('ffd9c9f5636cb4877bdd4331eb165864','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-11-08 00:14:40'),('bb6003d8cd91b1e21f8eeb4fa1b2b9aa','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2009-11-06 08:11:49'),('86c4d3815da60b21dd64546ce3a3cb12','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2009-11-06 19:51:07'),('a9d154e2dd0da84e905daee4a81e3afb','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEHdS41ZmZkMWQ4ZTNkYzIyZTgzN2Nj\nZGJjYTY5YzhiNThiYQ==\n','2009-11-06 06:43:45'),('27edae6c7129b2661e535d28f563891c','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mMDQ3ZmRkNDliMGJkNTAzODk2\nNGYxZTk3MmE3MjIwMw==\n','2009-11-05 12:28:59'),('9845c2e98ee74bcce3888e255c353ff3','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigELdS42NzhjOWE2YzY2OGE0NTQ3ZjJi\nMjQxODE0YmVmZGFmYw==\n','2009-11-19 03:52:19'),('8f9a800ace11f6cc6abae24ae5fbf10d','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2009-11-19 03:49:36'),('f729d399f3e77ad4052092972fda712b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-12-29 23:37:49'),('e855bb2132a2e4a68a9127788a639f2b','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2009-12-19 18:33:56'),('0d9a21c098d9973530852bbcaa9f5120','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2009-12-16 18:38:20'),('2c383d530182d9beca17c9cea0ccbf5f','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2009-12-14 23:02:57'),('01d3d47ba38ec322e6c72417ed9755d1','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEKdS44NzI2YmY1NjNlNmU1NjViMGZi\nMGVlMWZmZmEwOWNhMA==\n','2010-01-05 02:59:38'),('c3218ec47c86b8228790aa4d41f1d11c','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2009-12-21 05:19:14'),('e003d90a95c3977467d70c37e649949d','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-05 03:38:35'),('5179c57ac10ad2d95d1c7c3df26463d1','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-05 03:29:35'),('c7d62e4b086d1ca99eddfa8b845cd478','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-06 13:55:59'),('67e1e86bb67d109d4a14903a71a8115a','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-06 00:03:41'),('963eba4d251f39c15d09bb525278a51b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-05 03:33:51'),('034119625adf487118745bf88e7a65e8','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-05 03:59:00'),('5252445dfc0ffbfd224f662662a37513','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-05 03:57:55'),('b9ba2d1968e7a7987f0bbd120aa63de9','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-05 04:05:30'),('0803f09b73a10d9a71c735e410b91db9','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-20 01:49:54'),('84642a2c8f90d84ae32dfa76190259d6','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:45'),('e825a99f689902173688de03aea70bfe','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-13 00:14:41'),('c9324dad4bd89f64f366c7069b4bcc31','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:45'),('2fb0c34507a0eb369886c9f01a612fba','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:48'),('0e14b5d9c9fbceceb527268c103ae16f','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:48'),('dadff586c647d14a5abc31654244eab8','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:48'),('7163f88760b55370b58c8306eccef3e7','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:49'),('14278eb87727debaa257671f41372867','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:49'),('ade16878ae0e6b4e7aee26e9609908a5','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:49'),('3e889c0e2515f2b4d5334c7f7c7962a1','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:49'),('c4449b0c2ca2e41bea0f1c8966c271b4','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:49'),('10d010a1807ab59454e4af5114588721','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:49'),('951802dcc11b01f346d50399c80c4723','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:49'),('55d947568caa79b3f007371d20ded0e6','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:50'),('3a438f4d10f9804bba13283c86ebcafc','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:50'),('6b8444ec6404505c7b0a4c4eb8006b2b','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:50'),('dbdaf755a4a782969177aba95e30fbbb','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-13 01:32:50'),('5a1c9c62497ddba99f73e424503c4064','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEIdS5mODA5NjY1MmNhZWRkNGMyYjM0\nMDY4NmY3MzU1NWFkMg==\n','2010-01-17 04:53:48'),('cba3c836b1f9e50ab8976ec77f1e1f22','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-01-19 01:46:46'),('8961f0ad2f00bf7b3c836aba32e95ffb','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-01-22 02:43:13'),('54dfcb6658a8c069d2f72ba040011b2b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEKdS44NzI2YmY1NjNlNmU1NjViMGZi\nMGVlMWZmZmEwOWNhMA==\n','2010-01-21 19:51:15'),('03fc90149641c66e7b998d936a2b347f','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEFdS41NDIzNzg0Y2I5OTVkZTJiMjlj\nNGJlMTc1ZDFjMGU0YQ==\n','2010-01-21 21:59:56'),('c90e809dbce7f06de519c989b69dd0de','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-01-22 00:09:39'),('d5654943a2dd4476902144c2b516d635','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-02 12:28:32'),('76f5fbca79b5f2d3b22b6039bf2888cc','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-02 12:29:29'),('e9c9dac95893a32ba70fbe98b19706d9','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-26 23:06:39'),('860f7f77fc1c69b86d6526aea021d043','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('8c7ff6e37c4646b1f052c064aad0ddd1','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-01-29 21:59:24'),('128539602b47daaadbbc82c2072640fe','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('264339ff7536453c30ca839da535eabf','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-01-28 05:00:32'),('87e388df7ddbee4ff655e745ed0a7adf','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-01-28 06:41:53'),('180ab71f017e22c03837cdc799d390bb','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('1b25379d0b096bd265aa3076228c4c13','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('844d10d9d200f9ddb5a6cb65dada4e83','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('ba8d964d46b450c2be2f925b5f2c9793','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('f85a1f8061dd2911f65408f8ea06a3dd','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('bf6a96824248df4be61209c549c4d79a','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('3b9bcaf937652136a6850ea5a3d68a3b','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('e8d1500adf8ce9ad3a8c36982909f290','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('f57c05a1f6a58f931ea1b164f75bd2b6','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('b5b4c041b162f9ba97048a96d5cf60fa','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('d992e9ccfa854771ec15a0a14ab6bd26','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('7f38beb536af105a4091dee49720a115','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:31'),('82f2c7840cda24b59d5ee6696dddf6d0','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:32'),('bf843e419478cce79d03348111e1c3d3','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-01 12:53:32'),('c9202c5d911d69a076fcce7358a0991a','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-02 12:20:46'),('33728a0f4e9be2dda60360a83ab66319','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-05 00:20:56'),('17ebc78d56e2d7721f9df3a5c6cd570a','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-07 01:31:15'),('7d8af7eddd75b102b189e39af58a8029','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-08 19:09:40'),('2d3745bed9aba9e0d3f75d6848fd23e7','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxN2RhN2JjMDRmNWZlY2I0MmNiNWFlZGEy\nNWI5ZTVk\n','2010-02-11 00:08:59'),('f07be4126605161e32fd782dc09d9941','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-10 05:39:29'),('89363475fbf0d8c1c24cdef8cb2c944a','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-12 00:42:36'),('980af3d746230b636ad3579b312c6c94','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-02-12 12:03:54'),('5d844ad35f719c41c8c9f66e2993fedd','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5jMmQ1YjI0ODdiMWQyYzVmNTkw\nNWExNzFmNGE1OWVhYw==\n','2010-02-14 03:17:27'),('7126a52a4dfbbf5d1207f06373e471a1','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-02-15 04:37:30'),('ba3c38ac99eb1a36f395c64850dc1c48','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-02-14 23:56:06'),('b6d81adef01aefe76db95a779bc0b824','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-02-14 05:07:28'),('aedc28cdc205783850e8926a8eb76d4d','gAJ9cQEuZGQ5OGZkMTFiMjQ5YzQ4Yjk4YjA1NWE0MDgzNTVjOTQ=\n','2010-02-15 03:52:34');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-02-01 14:31:10
