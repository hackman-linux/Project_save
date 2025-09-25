/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: canteen_management
-- ------------------------------------------------------
-- Server version	10.11.13-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES
(2,'add_user'),
(1,'user');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES
(2,1,5),
(1,1,25),
(3,2,25),
(4,2,26);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add System Configuration',6,'add_systemconfig'),
(22,'Can change System Configuration',6,'change_systemconfig'),
(23,'Can delete System Configuration',6,'delete_systemconfig'),
(24,'Can view System Configuration',6,'view_systemconfig'),
(25,'Can add User',7,'add_user'),
(26,'Can change User',7,'change_user'),
(27,'Can delete User',7,'delete_user'),
(28,'Can view User',7,'view_user'),
(29,'Can add User Activity',8,'add_useractivity'),
(30,'Can change User Activity',8,'change_useractivity'),
(31,'Can delete User Activity',8,'delete_useractivity'),
(32,'Can view User Activity',8,'view_useractivity'),
(33,'Can add User Session',9,'add_usersession'),
(34,'Can change User Session',9,'change_usersession'),
(35,'Can delete User Session',9,'delete_usersession'),
(36,'Can view User Session',9,'view_usersession'),
(37,'Can add Ingredient',10,'add_menuitemingredient'),
(38,'Can change Ingredient',10,'change_menuitemingredient'),
(39,'Can delete Ingredient',10,'delete_menuitemingredient'),
(40,'Can view Ingredient',10,'view_menuitemingredient'),
(41,'Can add Daily Menu',11,'add_dailymenu'),
(42,'Can change Daily Menu',11,'change_dailymenu'),
(43,'Can delete Daily Menu',11,'delete_dailymenu'),
(44,'Can view Daily Menu',11,'view_dailymenu'),
(45,'Can add Menu Category',12,'add_menucategory'),
(46,'Can change Menu Category',12,'change_menucategory'),
(47,'Can delete Menu Category',12,'delete_menucategory'),
(48,'Can view Menu Category',12,'view_menucategory'),
(49,'Can add Menu Item',13,'add_menuitem'),
(50,'Can change Menu Item',13,'change_menuitem'),
(51,'Can delete Menu Item',13,'delete_menuitem'),
(52,'Can view Menu Item',13,'view_menuitem'),
(53,'Can add daily menu items',14,'add_dailymenuitems'),
(54,'Can change daily menu items',14,'change_dailymenuitems'),
(55,'Can delete daily menu items',14,'delete_dailymenuitems'),
(56,'Can view daily menu items',14,'view_dailymenuitems'),
(57,'Can add menu item favorite',15,'add_menuitemfavorite'),
(58,'Can change menu item favorite',15,'change_menuitemfavorite'),
(59,'Can delete menu item favorite',15,'delete_menuitemfavorite'),
(60,'Can view menu item favorite',15,'view_menuitemfavorite'),
(61,'Can add menu item ingredient relation',16,'add_menuitemingredientrelation'),
(62,'Can change menu item ingredient relation',16,'change_menuitemingredientrelation'),
(63,'Can delete menu item ingredient relation',16,'delete_menuitemingredientrelation'),
(64,'Can view menu item ingredient relation',16,'view_menuitemingredientrelation'),
(65,'Can add Menu Item Review',17,'add_menuitemreview'),
(66,'Can change Menu Item Review',17,'change_menuitemreview'),
(67,'Can delete Menu Item Review',17,'delete_menuitemreview'),
(68,'Can view Menu Item Review',17,'view_menuitemreview'),
(69,'Can add Order',18,'add_order'),
(70,'Can change Order',18,'change_order'),
(71,'Can delete Order',18,'delete_order'),
(72,'Can view Order',18,'view_order'),
(73,'Can add Order History',19,'add_orderhistory'),
(74,'Can change Order History',19,'change_orderhistory'),
(75,'Can delete Order History',19,'delete_orderhistory'),
(76,'Can view Order History',19,'view_orderhistory'),
(77,'Can add Order Item',20,'add_orderitem'),
(78,'Can change Order Item',20,'change_orderitem'),
(79,'Can delete Order Item',20,'delete_orderitem'),
(80,'Can view Order Item',20,'view_orderitem'),
(81,'Can add Order Queue Item',21,'add_orderqueue'),
(82,'Can change Order Queue Item',21,'change_orderqueue'),
(83,'Can delete Order Queue Item',21,'delete_orderqueue'),
(84,'Can view Order Queue Item',21,'view_orderqueue'),
(85,'Can add reorder item',22,'add_reorderitem'),
(86,'Can change reorder item',22,'change_reorderitem'),
(87,'Can delete reorder item',22,'delete_reorderitem'),
(88,'Can view reorder item',22,'view_reorderitem'),
(89,'Can add Payment Provider',23,'add_paymentprovider'),
(90,'Can change Payment Provider',23,'change_paymentprovider'),
(91,'Can delete Payment Provider',23,'delete_paymentprovider'),
(92,'Can view Payment Provider',23,'view_paymentprovider'),
(93,'Can add Payment',24,'add_payment'),
(94,'Can change Payment',24,'change_payment'),
(95,'Can delete Payment',24,'delete_payment'),
(96,'Can view Payment',24,'view_payment'),
(97,'Can add Payment Webhook',25,'add_paymentwebhook'),
(98,'Can change Payment Webhook',25,'change_paymentwebhook'),
(99,'Can delete Payment Webhook',25,'delete_paymentwebhook'),
(100,'Can view Payment Webhook',25,'view_paymentwebhook'),
(101,'Can add Wallet Transaction',26,'add_wallettransaction'),
(102,'Can change Wallet Transaction',26,'change_wallettransaction'),
(103,'Can delete Wallet Transaction',26,'delete_wallettransaction'),
(104,'Can view Wallet Transaction',26,'view_wallettransaction'),
(105,'Can add Notification Template',27,'add_notificationtemplate'),
(106,'Can change Notification Template',27,'change_notificationtemplate'),
(107,'Can delete Notification Template',27,'delete_notificationtemplate'),
(108,'Can view Notification Template',27,'view_notificationtemplate'),
(109,'Can add Notification',28,'add_notification'),
(110,'Can change Notification',28,'change_notification'),
(111,'Can delete Notification',28,'delete_notification'),
(112,'Can view Notification',28,'view_notification'),
(113,'Can add Notification Preference',29,'add_notificationpreference'),
(114,'Can change Notification Preference',29,'change_notificationpreference'),
(115,'Can delete Notification Preference',29,'delete_notificationpreference'),
(116,'Can view Notification Preference',29,'view_notificationpreference'),
(117,'Can add User Notification',30,'add_usernotification'),
(118,'Can change User Notification',30,'change_usernotification'),
(119,'Can delete User Notification',30,'delete_usernotification'),
(120,'Can view User Notification',30,'view_usernotification'),
(121,'Can add Daily Sales Report',31,'add_dailysalesreport'),
(122,'Can change Daily Sales Report',31,'change_dailysalesreport'),
(123,'Can delete Daily Sales Report',31,'delete_dailysalesreport'),
(124,'Can view Daily Sales Report',31,'view_dailysalesreport'),
(125,'Can add System Analytics',32,'add_systemanalytics'),
(126,'Can change System Analytics',32,'change_systemanalytics'),
(127,'Can delete System Analytics',32,'delete_systemanalytics'),
(128,'Can view System Analytics',32,'view_systemanalytics'),
(129,'Can add Menu Item Performance',33,'add_menuitemperformance'),
(130,'Can change Menu Item Performance',33,'change_menuitemperformance'),
(131,'Can delete Menu Item Performance',33,'delete_menuitemperformance'),
(132,'Can view Menu Item Performance',33,'view_menuitemperformance'),
(133,'Can add Report',34,'add_report'),
(134,'Can change Report',34,'change_report'),
(135,'Can delete Report',34,'delete_report'),
(136,'Can view Report',34,'view_report'),
(137,'Can add Report Subscription',35,'add_reportsubscription'),
(138,'Can change Report Subscription',35,'change_reportsubscription'),
(139,'Can delete Report Subscription',35,'delete_reportsubscription'),
(140,'Can view Report Subscription',35,'view_reportsubscription'),
(141,'Can add Report Template',36,'add_reporttemplate'),
(142,'Can change Report Template',36,'change_reporttemplate'),
(143,'Can delete Report Template',36,'delete_reporttemplate'),
(144,'Can view Report Template',36,'view_reporttemplate'),
(145,'Can add User Activity Report',37,'add_useractivityreport'),
(146,'Can change User Activity Report',37,'change_useractivityreport'),
(147,'Can delete User Activity Report',37,'delete_useractivityreport'),
(148,'Can view User Activity Report',37,'view_useractivityreport'),
(149,'Can add audit log',38,'add_auditlog'),
(150,'Can change audit log',38,'change_auditlog'),
(151,'Can delete audit log',38,'delete_auditlog'),
(152,'Can view audit log',38,'view_auditlog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `password` varchar(128) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `id` uuid NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(17) NOT NULL,
  `role` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `employee_id` varchar(20) DEFAULT NULL,
  `department` varchar(100) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `wallet_balance` decimal(10,2) NOT NULL,
  `preferred_payment_method` varchar(20) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_email_verified` tinyint(1) NOT NULL,
  `email_verification_token` varchar(100) NOT NULL,
  `password_reset_token` varchar(100) NOT NULL,
  `password_reset_expires` datetime(6) DEFAULT NULL,
  `last_activity` datetime(6) DEFAULT NULL,
  `login_count` int(10) unsigned NOT NULL CHECK (`login_count` >= 0),
  `failed_login_attempts` int(10) unsigned NOT NULL CHECK (`failed_login_attempts` >= 0),
  `account_locked_until` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`),
  UNIQUE KEY `employee_id` (`employee_id`),
  KEY `auth_user_email_ece7f7_idx` (`email`),
  KEY `auth_user_role_f90fd2_idx` (`role`),
  KEY `auth_user_status_79e21c_idx` (`status`),
  KEY `auth_user_employe_d6f0da_idx` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES
('pbkdf2_sha256$600000$kuD9eby6YWVgEb0oAgGAIV$kJ2PaWdQYd/e+1GKglORqwf217p21ckqxV6GfbDvL/I=',0,'fouda','Fouda','Odile',0,1,'c1297951-544f-451b-ba74-4244292d26b5','fouda@oapi.int','690 456 789','canteen_admin','active','','Management','',0.00,'wallet','2025-09-11 15:49:58.958373','2025-09-23 15:40:20.366450','2025-09-11 15:49:58.958433',0,'','',NULL,'2025-09-23 15:40:20.478478',37,0,NULL),
('pbkdf2_sha256$600000$KebfPYm7urGtTNcjLJzasW$Br/5yEyQg70cwhwRaCoOZERSx+akojeaLQ/QK2PLgog=',0,'herve','Herve','Kamga',0,1,'542a1848-e278-48fd-afa5-470669646751','herve@oapi.int','','employee','active','emplo001','IT','',0.00,'wallet','2025-09-07 19:55:44.194068','2025-09-23 17:11:42.175776','2025-09-07 19:55:44.194148',0,'','',NULL,'2025-09-23 17:11:42.742862',46,0,NULL),
('pbkdf2_sha256$600000$ybK0VWC0ZKVRHVTRhZ6D76$hUBbgNkt3Gr9efcXVkzLaXcir9mrt/hgiO9tscXE1ac=',0,'MasterRed','Arthur','George',0,1,'e2718c6a-1aad-4b8d-adaf-9a25c1ffd8fd','george@oapi.int','696129297','employee','active','emplo003','Finance','',0.00,'wallet','2025-09-22 18:44:01.726623','2025-09-22 18:45:00.012681','2025-09-22 18:44:01.726690',0,'','',NULL,'2025-09-22 18:45:00.115850',1,0,NULL),
('pbkdf2_sha256$600000$xtuTPAnJKqaVgbbfMY8Z3p$lnbVX0Xb1yfp56ovKnt1cLgqvzo/zCvriH5gcWMK+xA=',1,'codex','souleman','genie',1,1,'8ee9f77e-149b-4050-9861-fb3422e4b055','ndjodongouhs@gmail.com','+237696730882','employee','active',NULL,'','',0.00,'wallet','2025-09-05 21:02:03.736797','2025-09-23 13:41:16.466799','2025-09-05 21:02:03.736872',0,'','',NULL,'2025-09-22 18:48:23.970092',27,0,NULL);
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` uuid NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` uuid NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_systemconfig`
--

DROP TABLE IF EXISTS `authentication_systemconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `authentication_systemconfig` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(100) NOT NULL,
  `app_version` varchar(20) NOT NULL,
  `timezone` varchar(50) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `language` varchar(10) NOT NULL,
  `opening_time` time(6) NOT NULL,
  `closing_time` time(6) NOT NULL,
  `order_processing_time` int(11) NOT NULL,
  `max_daily_orders` int(11) NOT NULL,
  `cancellation_window` int(11) NOT NULL,
  `allow_advance_orders` tinyint(1) NOT NULL,
  `mtn_enabled` tinyint(1) NOT NULL,
  `mtn_api_key` varchar(255) DEFAULT NULL,
  `mtn_merchant_id` varchar(100) DEFAULT NULL,
  `mtn_environment` varchar(20) NOT NULL,
  `orange_enabled` tinyint(1) NOT NULL,
  `orange_api_key` varchar(255) DEFAULT NULL,
  `orange_merchant_id` varchar(100) DEFAULT NULL,
  `orange_environment` varchar(20) NOT NULL,
  `payment_timeout` int(11) NOT NULL,
  `transaction_fee` decimal(5,2) NOT NULL,
  `min_order_amount` decimal(10,2) NOT NULL,
  `auto_refund` tinyint(1) NOT NULL,
  `email_enabled` tinyint(1) NOT NULL,
  `smtp_server` varchar(100) NOT NULL,
  `smtp_port` int(11) NOT NULL,
  `from_email` varchar(254) NOT NULL,
  `smtp_username` varchar(100) DEFAULT NULL,
  `smtp_password` varchar(100) DEFAULT NULL,
  `sms_enabled` tinyint(1) NOT NULL,
  `sms_provider` varchar(50) NOT NULL,
  `sms_api_key` varchar(255) DEFAULT NULL,
  `sms_from_number` varchar(20) DEFAULT NULL,
  `push_enabled` tinyint(1) NOT NULL,
  `firebase_server_key` varchar(255) DEFAULT NULL,
  `session_timeout` int(11) NOT NULL,
  `password_min_length` int(11) NOT NULL,
  `require_uppercase` tinyint(1) NOT NULL,
  `require_numbers` tinyint(1) NOT NULL,
  `require_special_chars` tinyint(1) NOT NULL,
  `max_login_attempts` int(11) NOT NULL,
  `lockout_duration` int(11) NOT NULL,
  `enable_2fa` tinyint(1) NOT NULL,
  `log_security_events` tinyint(1) NOT NULL,
  `require_password_change` tinyint(1) NOT NULL,
  `auto_backup` tinyint(1) NOT NULL,
  `backup_frequency` varchar(20) NOT NULL,
  `backup_time` time(6) NOT NULL,
  `backup_retention` int(11) NOT NULL,
  `performance_monitoring` tinyint(1) NOT NULL,
  `log_level` varchar(20) NOT NULL,
  `log_retention` int(11) NOT NULL,
  `email_alerts` tinyint(1) NOT NULL,
  `maintenance_mode` tinyint(1) NOT NULL,
  `maintenance_message` longtext NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_systemconfig`
--

LOCK TABLES `authentication_systemconfig` WRITE;
/*!40000 ALTER TABLE `authentication_systemconfig` DISABLE KEYS */;
INSERT INTO `authentication_systemconfig` VALUES
(1,'Canteen Management System','1.0.0','UTC','XAF','en','08:00:00.000000','18:00:00.000000',15,200,10,1,1,NULL,NULL,'sandbox',0,NULL,NULL,'sandbox',120,2.50,100.00,1,1,'smtp.example.com',587,'admin@example.com',NULL,NULL,0,'twilio',NULL,NULL,0,NULL,60,8,1,1,0,5,15,0,1,0,1,'daily','02:00:00.000000',30,1,'INFO',30,1,0,'System under maintenance, please check back later.','2025-09-07 12:22:33.463877');
/*!40000 ALTER TABLE `authentication_systemconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daily_menu`
--

DROP TABLE IF EXISTS `daily_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_menu` (
  `id` uuid NOT NULL,
  `date` date NOT NULL,
  `special_message` longtext NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`),
  KEY `daily_menu_date_a2ec82_idx` (`date`),
  KEY `daily_menu_is_publ_f7f8fe_idx` (`is_published`),
  KEY `daily_menu_created_by_id_a8b587bf_fk_auth_user_id` (`created_by_id`),
  CONSTRAINT `daily_menu_created_by_id_a8b587bf_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_menu`
--

LOCK TABLES `daily_menu` WRITE;
/*!40000 ALTER TABLE `daily_menu` DISABLE KEYS */;
/*!40000 ALTER TABLE `daily_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daily_menu_items`
--

DROP TABLE IF EXISTS `daily_menu_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_menu_items` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `daily_price` decimal(8,2) DEFAULT NULL,
  `daily_stock` int(10) unsigned DEFAULT NULL CHECK (`daily_stock` >= 0),
  `is_featured_today` tinyint(1) NOT NULL,
  `display_order` int(10) unsigned NOT NULL CHECK (`display_order` >= 0),
  `daily_menu_id` uuid NOT NULL,
  `menu_item_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `daily_menu_items_daily_menu_id_menu_item_id_df382109_uniq` (`daily_menu_id`,`menu_item_id`),
  KEY `daily_menu_items_menu_item_id_03c24834_fk_menu_item_id` (`menu_item_id`),
  CONSTRAINT `daily_menu_items_daily_menu_id_c7b018ad_fk_daily_menu_id` FOREIGN KEY (`daily_menu_id`) REFERENCES `daily_menu` (`id`),
  CONSTRAINT `daily_menu_items_menu_item_id_03c24834_fk_menu_item_id` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_menu_items`
--

LOCK TABLES `daily_menu_items` WRITE;
/*!40000 ALTER TABLE `daily_menu_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `daily_menu_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daily_sales_report`
--

DROP TABLE IF EXISTS `daily_sales_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_sales_report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_orders` int(10) unsigned NOT NULL CHECK (`total_orders` >= 0),
  `completed_orders` int(10) unsigned NOT NULL CHECK (`completed_orders` >= 0),
  `cancelled_orders` int(10) unsigned NOT NULL CHECK (`cancelled_orders` >= 0),
  `total_revenue` decimal(12,2) NOT NULL,
  `gross_revenue` decimal(12,2) NOT NULL,
  `net_revenue` decimal(12,2) NOT NULL,
  `wallet_payments` decimal(12,2) NOT NULL,
  `mtn_payments` decimal(12,2) NOT NULL,
  `orange_payments` decimal(12,2) NOT NULL,
  `unique_customers` int(10) unsigned NOT NULL CHECK (`unique_customers` >= 0),
  `new_customers` int(10) unsigned NOT NULL CHECK (`new_customers` >= 0),
  `repeat_customers` int(10) unsigned NOT NULL CHECK (`repeat_customers` >= 0),
  `average_order_value` decimal(8,2) NOT NULL,
  `average_prep_time` decimal(5,2) NOT NULL,
  `peak_hour` time(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_sales_report`
--

LOCK TABLES `daily_sales_report` WRITE;
/*!40000 ALTER TABLE `daily_sales_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `daily_sales_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES
(1,'2025-09-05 22:13:34.578176','1','user',1,'[{\"added\": {}}]',3,'8ee9f77e-149b-4050-9861-fb3422e4b055'),
(2,'2025-09-06 07:21:40.250759','2','add_user',1,'[{\"added\": {}}]',3,'8ee9f77e-149b-4050-9861-fb3422e4b055');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(6,'authentication','systemconfig'),
(7,'authentication','user'),
(8,'authentication','useractivity'),
(9,'authentication','usersession'),
(4,'contenttypes','contenttype'),
(11,'menu','dailymenu'),
(14,'menu','dailymenuitems'),
(12,'menu','menucategory'),
(13,'menu','menuitem'),
(15,'menu','menuitemfavorite'),
(10,'menu','menuitemingredient'),
(16,'menu','menuitemingredientrelation'),
(17,'menu','menuitemreview'),
(28,'notifications','notification'),
(29,'notifications','notificationpreference'),
(27,'notifications','notificationtemplate'),
(30,'notifications','usernotification'),
(18,'orders','order'),
(19,'orders','orderhistory'),
(20,'orders','orderitem'),
(21,'orders','orderqueue'),
(22,'orders','reorderitem'),
(24,'payments','payment'),
(23,'payments','paymentprovider'),
(25,'payments','paymentwebhook'),
(26,'payments','wallettransaction'),
(38,'reports','auditlog'),
(31,'reports','dailysalesreport'),
(33,'reports','menuitemperformance'),
(34,'reports','report'),
(35,'reports','reportsubscription'),
(36,'reports','reporttemplate'),
(32,'reports','systemanalytics'),
(37,'reports','useractivityreport'),
(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-09-05 20:36:12.979111'),
(2,'contenttypes','0002_remove_content_type_name','2025-09-05 20:36:15.264638'),
(3,'auth','0001_initial','2025-09-05 20:36:22.264127'),
(4,'auth','0002_alter_permission_name_max_length','2025-09-05 20:36:23.319214'),
(5,'auth','0003_alter_user_email_max_length','2025-09-05 20:36:23.387290'),
(6,'auth','0004_alter_user_username_opts','2025-09-05 20:36:23.442333'),
(7,'auth','0005_alter_user_last_login_null','2025-09-05 20:36:23.508600'),
(8,'auth','0006_require_contenttypes_0002','2025-09-05 20:36:23.560432'),
(9,'auth','0007_alter_validators_add_error_messages','2025-09-05 20:36:23.635064'),
(10,'auth','0008_alter_user_username_max_length','2025-09-05 20:36:23.706175'),
(11,'auth','0009_alter_user_last_name_max_length','2025-09-05 20:36:23.790401'),
(12,'auth','0010_alter_group_name_max_length','2025-09-05 20:36:24.548897'),
(13,'auth','0011_update_proxy_permissions','2025-09-05 20:36:24.619748'),
(14,'auth','0012_alter_user_first_name_max_length','2025-09-05 20:36:24.703237'),
(15,'authentication','0001_initial','2025-09-05 20:36:50.125677'),
(16,'admin','0001_initial','2025-09-05 20:36:53.024996'),
(17,'admin','0002_logentry_remove_auto_add','2025-09-05 20:36:53.114696'),
(18,'admin','0003_logentry_add_action_flag_choices','2025-09-05 20:36:53.260008'),
(19,'menu','0001_initial','2025-09-05 20:37:36.445613'),
(20,'orders','0001_initial','2025-09-05 20:38:05.362552'),
(21,'payments','0001_initial','2025-09-05 20:38:27.400977'),
(23,'reports','0001_initial','2025-09-05 20:39:27.586161'),
(24,'sessions','0001_initial','2025-09-05 20:39:28.956305'),
(26,'orders','0002_alter_order_options_alter_orderhistory_options_and_more','2025-09-10 18:20:04.468031'),
(27,'orders','0003_order_actual_prep_time','2025-09-11 16:35:24.857361'),
(30,'reports','0002_auditlog','2025-09-23 11:47:46.141335'),
(31,'notifications','0001_initial','2025-09-23 13:08:28.038254'),
(32,'notifications','0002_remove_notification_user_notification_target_user','2025-09-23 13:50:30.427640'),
(33,'notifications','0003_auto_20250923_1512','2025-09-23 15:17:39.704219'),
(34,'notifications','0004_auto_20250923_1623','2025-09-23 16:27:03.333245'),
(35,'notifications','0005_alter_usernotification_unique_together_and_more','2025-09-23 17:54:43.858468');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_category`
--

DROP TABLE IF EXISTS `menu_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_category` (
  `id` uuid NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `icon` varchar(50) NOT NULL,
  `color` varchar(20) NOT NULL,
  `display_order` int(10) unsigned NOT NULL CHECK (`display_order` >= 0),
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `menu_catego_is_acti_949851_idx` (`is_active`),
  KEY `menu_catego_display_20b596_idx` (`display_order`),
  KEY `menu_category_created_by_id_78b92991_fk_auth_user_id` (`created_by_id`),
  CONSTRAINT `menu_category_created_by_id_78b92991_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_category`
--

LOCK TABLES `menu_category` WRITE;
/*!40000 ALTER TABLE `menu_category` DISABLE KEYS */;
INSERT INTO `menu_category` VALUES
('c5e7cfc1-3f22-46eb-94eb-683e89533ec9','Main Course','Primary dishes and meals','bi-plate','primary',1,1,'2025-09-15 09:19:25.732326','2025-09-15 09:19:25.732406',NULL),
('83836b33-c950-4683-8abe-92dba9993028','Desserts','Sweet treats and desserts','bi-cake','warning',3,1,'2025-09-15 09:19:26.534550','2025-09-15 09:19:26.534651',NULL),
('62da8736-ea34-4aac-bb81-abe0b96b5661','Snacks','Light snacks and appetizers','bi-basket','success',4,1,'2025-09-15 09:19:26.908399','2025-09-15 09:19:26.908504',NULL),
('8b93e7e3-eb2f-40ce-9187-ed836289ccbc','Beverages','Drinks and refreshments','bi-cup','info',2,1,'2025-09-15 09:19:26.391738','2025-09-15 09:19:26.391806',NULL);
/*!40000 ALTER TABLE `menu_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_item`
--

DROP TABLE IF EXISTS `menu_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_item` (
  `id` uuid NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(8,2) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `calories` int(10) unsigned DEFAULT NULL CHECK (`calories` >= 0),
  `spice_level` varchar(20) NOT NULL,
  `dietary_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`dietary_tags`)),
  `allergens` longtext NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `daily_limit` int(10) unsigned NOT NULL CHECK (`daily_limit` >= 0),
  `current_stock` int(10) unsigned NOT NULL CHECK (`current_stock` >= 0),
  `low_stock_threshold` int(10) unsigned NOT NULL CHECK (`low_stock_threshold` >= 0),
  `preparation_time` int(10) unsigned NOT NULL CHECK (`preparation_time` >= 0),
  `cooking_instructions` longtext NOT NULL,
  `total_orders` int(10) unsigned NOT NULL CHECK (`total_orders` >= 0),
  `average_rating` decimal(3,2) NOT NULL,
  `total_reviews` int(10) unsigned NOT NULL CHECK (`total_reviews` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `is_special` tinyint(1) NOT NULL,
  `special_price` decimal(8,2) DEFAULT NULL,
  `special_until` datetime(6) DEFAULT NULL,
  `category_id` uuid NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_item_is_avai_85c7c7_idx` (`is_available`),
  KEY `menu_item_is_feat_4ae7e0_idx` (`is_featured`),
  KEY `menu_item_is_spec_b5e11a_idx` (`is_special`),
  KEY `menu_item_categor_c58e14_idx` (`category_id`,`is_available`),
  KEY `menu_item_total_o_a744a4_idx` (`total_orders`),
  KEY `menu_item_created_by_id_98c0cce9_fk_auth_user_id` (`created_by_id`),
  CONSTRAINT `menu_item_category_id_685695be_fk_menu_category_id` FOREIGN KEY (`category_id`) REFERENCES `menu_category` (`id`),
  CONSTRAINT `menu_item_created_by_id_98c0cce9_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item`
--

LOCK TABLES `menu_item` WRITE;
/*!40000 ALTER TABLE `menu_item` DISABLE KEYS */;
INSERT INTO `menu_item` VALUES
('db89e23c-3138-45ff-b337-0e67b952a1ed','Salad','',1500.00,'menu_items/salade.jpeg',NULL,'none','[\"vegetarian\"]','',1,100,100,10,5,'',0,0.00,0,'2025-09-15 13:36:13.759286','2025-09-15 13:36:14.252590',0,0,NULL,NULL,'c5e7cfc1-3f22-46eb-94eb-683e89533ec9','c1297951-544f-451b-ba74-4244292d26b5'),
('c15abc03-4fb9-46f2-95cf-29c660e1fb1d','Fish','',2000.00,'menu_items/download_JKKP3ax.jpeg',NULL,'none','[]','',1,100,100,10,10,'',0,0.00,0,'2025-09-15 10:28:52.005095','2025-09-15 10:28:52.242780',0,0,NULL,NULL,'62da8736-ea34-4aac-bb81-abe0b96b5661','c1297951-544f-451b-ba74-4244292d26b5'),
('a93f35f7-5a72-48db-b173-30c81134467a','smoothy','good teast',1500.00,'menu_items/dessert1.jpeg',NULL,'none','[]','',1,100,100,10,10,'',0,0.00,0,'2025-09-16 14:36:28.279680','2025-09-16 14:36:28.427190',0,0,NULL,NULL,'83836b33-c950-4683-8abe-92dba9993028','c1297951-544f-451b-ba74-4244292d26b5'),
('df89663a-23b7-4995-898a-3e4107980a42','Salad','',1500.00,'menu_items/salade_15D3Dnb.jpeg',NULL,'none','[\"vegetarian\"]','',1,100,100,10,5,'',0,0.00,0,'2025-09-15 13:36:24.432172','2025-09-15 13:36:24.836097',0,0,NULL,NULL,'c5e7cfc1-3f22-46eb-94eb-683e89533ec9','c1297951-544f-451b-ba74-4244292d26b5'),
('17341895-7196-4fae-a533-453ab5bd3697','Meat','',2500.00,'menu_items/meat.jpeg',NULL,'none','[\"spicy\"]','',1,100,100,10,30,'',0,0.00,0,'2025-09-15 13:42:35.545084','2025-09-15 13:42:36.696123',0,0,NULL,NULL,'62da8736-ea34-4aac-bb81-abe0b96b5661','c1297951-544f-451b-ba74-4244292d26b5'),
('2c6d282b-784e-45e3-97ca-543ea834e77d','Fish','',2000.00,'menu_items/download.jpeg',NULL,'none','[\"spicy\"]','',1,100,100,10,10,'',0,0.00,0,'2025-09-15 09:53:29.596784','2025-09-15 09:53:29.800269',0,0,NULL,NULL,'62da8736-ea34-4aac-bb81-abe0b96b5661','c1297951-544f-451b-ba74-4244292d26b5'),
('dba8e8f4-e2b3-4cbf-80b3-5f7448cc1557','cocktails','',5000.00,'',NULL,'none','[]','',1,100,100,10,5,'',0,0.00,0,'2025-09-16 15:12:25.247855','2025-09-16 15:12:25.247908',0,0,NULL,NULL,'8b93e7e3-eb2f-40ce-9187-ed836289ccbc','c1297951-544f-451b-ba74-4244292d26b5'),
('01162478-96b9-43e4-ac17-80b7ca2ec05c','wine','',10000.00,'menu_items/drink2.jpeg',NULL,'none','[]','',1,100,100,10,5,'',0,0.00,0,'2025-09-16 15:13:07.208517','2025-09-16 15:13:07.334760',0,0,NULL,NULL,'8b93e7e3-eb2f-40ce-9187-ed836289ccbc','c1297951-544f-451b-ba74-4244292d26b5'),
('94ab4670-fc91-4a69-9994-9a2c2629e393','Salad','',1500.00,'menu_items/salade_17Or0QF.jpeg',NULL,'none','[\"vegetarian\"]','',1,100,100,10,5,'',0,0.00,0,'2025-09-15 13:38:59.101544','2025-09-15 13:38:59.734130',0,0,NULL,NULL,'c5e7cfc1-3f22-46eb-94eb-683e89533ec9','c1297951-544f-451b-ba74-4244292d26b5');
/*!40000 ALTER TABLE `menu_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_item_favorite`
--

DROP TABLE IF EXISTS `menu_item_favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_item_favorite` (
  `id` uuid NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `menu_item_id` uuid NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menu_item_favorite_user_id_menu_item_id_0a4d4747_uniq` (`user_id`,`menu_item_id`),
  KEY `menu_item_f_user_id_b35fea_idx` (`user_id`),
  KEY `menu_item_favorite_menu_item_id_04099463_fk_menu_item_id` (`menu_item_id`),
  CONSTRAINT `menu_item_favorite_menu_item_id_04099463_fk_menu_item_id` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item` (`id`),
  CONSTRAINT `menu_item_favorite_user_id_81173692_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item_favorite`
--

LOCK TABLES `menu_item_favorite` WRITE;
/*!40000 ALTER TABLE `menu_item_favorite` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_item_favorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_item_ingredient`
--

DROP TABLE IF EXISTS `menu_item_ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_item_ingredient` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_allergen` tinyint(1) NOT NULL,
  `dietary_restrictions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`dietary_restrictions`)),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item_ingredient`
--

LOCK TABLES `menu_item_ingredient` WRITE;
/*!40000 ALTER TABLE `menu_item_ingredient` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_item_ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_item_ingredient_relation`
--

DROP TABLE IF EXISTS `menu_item_ingredient_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_item_ingredient_relation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `quantity` varchar(50) NOT NULL,
  `is_optional` tinyint(1) NOT NULL,
  `ingredient_id` bigint(20) NOT NULL,
  `menu_item_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menu_item_ingredient_rel_menu_item_id_ingredient__d90cc880_uniq` (`menu_item_id`,`ingredient_id`),
  KEY `menu_item_ingredient_ingredient_id_dcecf6d8_fk_menu_item` (`ingredient_id`),
  CONSTRAINT `menu_item_ingredient_ingredient_id_dcecf6d8_fk_menu_item` FOREIGN KEY (`ingredient_id`) REFERENCES `menu_item_ingredient` (`id`),
  CONSTRAINT `menu_item_ingredient_menu_item_id_c4526274_fk_menu_item` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item_ingredient_relation`
--

LOCK TABLES `menu_item_ingredient_relation` WRITE;
/*!40000 ALTER TABLE `menu_item_ingredient_relation` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_item_ingredient_relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_item_performance`
--

DROP TABLE IF EXISTS `menu_item_performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_item_performance` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `orders_count` int(10) unsigned NOT NULL CHECK (`orders_count` >= 0),
  `quantity_sold` int(10) unsigned NOT NULL CHECK (`quantity_sold` >= 0),
  `revenue` decimal(10,2) NOT NULL,
  `conversion_rate` decimal(5,2) NOT NULL,
  `average_rating` decimal(3,2) NOT NULL,
  `popularity_rank` int(10) unsigned DEFAULT NULL CHECK (`popularity_rank` >= 0),
  `revenue_rank` int(10) unsigned DEFAULT NULL CHECK (`revenue_rank` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `menu_item_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menu_item_performance_menu_item_id_date_fce6eb90_uniq` (`menu_item_id`,`date`),
  KEY `menu_item_performance_date_47f2b06b` (`date`),
  KEY `menu_item_p_date_aede94_idx` (`date`,`revenue`),
  KEY `menu_item_p_date_4d324c_idx` (`date`,`quantity_sold`),
  CONSTRAINT `menu_item_performance_menu_item_id_4a5e11cb_fk_menu_item_id` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item_performance`
--

LOCK TABLES `menu_item_performance` WRITE;
/*!40000 ALTER TABLE `menu_item_performance` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_item_performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_item_review`
--

DROP TABLE IF EXISTS `menu_item_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_item_review` (
  `id` uuid NOT NULL,
  `rating` int(10) unsigned NOT NULL CHECK (`rating` >= 0),
  `comment` longtext NOT NULL,
  `is_verified_purchase` tinyint(1) NOT NULL,
  `helpful_count` int(10) unsigned NOT NULL CHECK (`helpful_count` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `menu_item_id` uuid NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menu_item_review_menu_item_id_user_id_af2e8896_uniq` (`menu_item_id`,`user_id`),
  KEY `menu_item_r_menu_it_ba36c5_idx` (`menu_item_id`,`rating`),
  KEY `menu_item_r_is_veri_96e761_idx` (`is_verified_purchase`),
  KEY `menu_item_review_user_id_8d8331a9_fk_auth_user_id` (`user_id`),
  CONSTRAINT `menu_item_review_menu_item_id_807bfa86_fk_menu_item_id` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item` (`id`),
  CONSTRAINT `menu_item_review_user_id_8d8331a9_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item_review`
--

LOCK TABLES `menu_item_review` WRITE;
/*!40000 ALTER TABLE `menu_item_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_item_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_notification`
--

DROP TABLE IF EXISTS `notifications_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification` (
  `id` char(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `notification_type` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_notification_type` (`notification_type`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_notification`
--

LOCK TABLES `notifications_notification` WRITE;
/*!40000 ALTER TABLE `notifications_notification` DISABLE KEYS */;
INSERT INTO `notifications_notification` VALUES
('84f8736e-e28b-47e2-9d50-bc05280b548f','Test Notification','This is a test','system_announcement','2025-09-23 16:46:41',0);
/*!40000 ALTER TABLE `notifications_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_preference`
--

DROP TABLE IF EXISTS `notifications_preference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_preference` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email_enabled` tinyint(1) NOT NULL DEFAULT 1,
  `push_enabled` tinyint(1) NOT NULL DEFAULT 1,
  `order_notifications` tinyint(1) NOT NULL DEFAULT 1,
  `payment_notifications` tinyint(1) NOT NULL DEFAULT 1,
  `menu_notifications` tinyint(1) NOT NULL DEFAULT 1,
  `system_notifications` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `user_id` binary(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `notifications_preference_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_preference`
--

LOCK TABLES `notifications_preference` WRITE;
/*!40000 ALTER TABLE `notifications_preference` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications_preference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_template`
--

DROP TABLE IF EXISTS `notifications_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_template` (
  `id` char(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `notification_type` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_notification_type` (`notification_type`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_template`
--

LOCK TABLES `notifications_template` WRITE;
/*!40000 ALTER TABLE `notifications_template` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_user_notification`
--

DROP TABLE IF EXISTS `notifications_user_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_user_notification` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `is_read` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_user_notification`
--

LOCK TABLES `notifications_user_notification` WRITE;
/*!40000 ALTER TABLE `notifications_user_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications_user_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_order`
--

DROP TABLE IF EXISTS `orders_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_order` (
  `id` uuid NOT NULL,
  `order_number` varchar(32) NOT NULL,
  `status` varchar(20) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `tax_amount` decimal(10,2) NOT NULL,
  `service_fee` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `special_instructions` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `validated_at` datetime(6) DEFAULT NULL,
  `paid_at` datetime(6) DEFAULT NULL,
  `cancelled_at` datetime(6) DEFAULT NULL,
  `employee_id` uuid NOT NULL,
  `email` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `office_number` varchar(50) NOT NULL,
  `payment_method` varchar(30) DEFAULT NULL,
  `phone_number` varchar(50) NOT NULL,
  `actual_prep_time` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_number` (`order_number`),
  KEY `orders_orde_order_n_f3ada5_idx` (`order_number`),
  KEY `order_customer_id_9da9253f` (`employee_id`),
  KEY `orders_orde_employe_532148_idx` (`employee_id`,`created_at`),
  KEY `orders_orde_status_c6dd84_idx` (`status`),
  CONSTRAINT `order_employee_id_b74c8931_fk_auth_user_id` FOREIGN KEY (`employee_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_order`
--

LOCK TABLES `orders_order` WRITE;
/*!40000 ALTER TABLE `orders_order` DISABLE KEYS */;
INSERT INTO `orders_order` VALUES
('3b32e950-61bd-4b46-bc8b-1d1b9370b31d','AB10D50B5E85','cancelled',6000.00,0.00,0.00,6000.00,'','2025-09-16 14:20:57.808405','2025-09-22 18:29:34.296056',NULL,NULL,NULL,'542a1848-e278-48fd-afa5-470669646751','herve@oapi.int','Herve Kamga','1621',NULL,'+237 688 582 648',NULL),
('f5785d5c-bfa4-4e8f-8ca0-803c3c2be3a6','59E5E09A747B','VALIDATED',10000.00,0.00,0.00,10000.00,'provide the whole bottle in my office','2025-09-22 18:46:13.365934','2025-09-22 22:07:16.627724','2025-09-22 22:07:16.626688',NULL,NULL,'e2718c6a-1aad-4b8d-adaf-9a25c1ffd8fd','george@oapi.int','Arthur George','210',NULL,'+237 688 582 648',NULL),
('66ecf044-bddd-4561-8475-856f993da418','0B61C232D462','CANCELLED',5000.00,0.00,0.00,5000.00,'','2025-09-17 08:32:24.905761','2025-09-23 08:03:22.970903',NULL,NULL,'2025-09-23 08:03:22.970769','542a1848-e278-48fd-afa5-470669646751','herve@oapi.int','Herve Kamga','',NULL,'+237 688 582 648',NULL),
('d2a368a9-52f4-4115-800b-87929cc2a390','9A6DE2CF9199','VALIDATED',10000.00,0.00,0.00,10000.00,'','2025-09-16 15:14:40.696371','2025-09-23 08:02:30.428881','2025-09-23 08:02:30.428658',NULL,NULL,'542a1848-e278-48fd-afa5-470669646751','herve@oapi.int','Herve Kamga','1621',NULL,'+237 688 582 648',NULL),
('e2b54f1d-8218-4a3c-bcb7-92d929ec634e','7A5902A2B986','VALIDATED',10000.00,0.00,0.00,10000.00,'','2025-09-17 11:27:03.603644','2025-09-22 22:21:28.221880','2025-09-22 22:21:28.221587',NULL,NULL,'542a1848-e278-48fd-afa5-470669646751','herve@oapi.int','Herve Kamga','90',NULL,'+237 688 582 648',NULL),
('6ef5079f-921b-403d-b880-a1a5629b6b5b','019A9590C05C','VALIDATED',1500.00,0.00,0.00,1500.00,'','2025-09-23 14:23:53.229246','2025-09-23 14:24:39.410207','2025-09-23 14:24:39.410030',NULL,NULL,'542a1848-e278-48fd-afa5-470669646751','herve@oapi.int','Herve Kamga','1621',NULL,'+237 688 582 648',NULL),
('d9ea85e7-6826-42f2-a184-af48aea0ae7d','C69B71E9A75D','VALIDATED',1500.00,0.00,0.00,1500.00,'','2025-09-16 14:38:12.423988','2025-09-22 22:06:26.969707','2025-09-22 22:06:26.969512',NULL,NULL,'c1297951-544f-451b-ba74-4244292d26b5','fouda@oapi.int','Fouda Odile','2117',NULL,'+237 688 582 648',NULL);
/*!40000 ALTER TABLE `orders_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_orderhistory`
--

DROP TABLE IF EXISTS `orders_orderhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderhistory` (
  `id` uuid NOT NULL,
  `status_from` varchar(50) NOT NULL,
  `status_to` varchar(50) NOT NULL,
  `notes` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `changed_by_id` uuid DEFAULT NULL,
  `order_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_history_order_id_433e9d7e` (`order_id`),
  KEY `orders_orde_changed_96f2d2_idx` (`changed_by_id`,`timestamp`),
  CONSTRAINT `order_history_changed_by_id_9e2cdd24_fk_auth_user_id` FOREIGN KEY (`changed_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `order_history_order_id_433e9d7e_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderhistory`
--

LOCK TABLES `orders_orderhistory` WRITE;
/*!40000 ALTER TABLE `orders_orderhistory` DISABLE KEYS */;
INSERT INTO `orders_orderhistory` VALUES
('74da9fd6-1715-4f99-bd6c-08f7214f60af','CANCELLED','CANCELLED','Cancelled: item_not_available. ','2025-09-23 08:03:23.003752','c1297951-544f-451b-ba74-4244292d26b5','66ecf044-bddd-4561-8475-856f993da418'),
('6f6b8c9d-1974-4771-af50-14d9bb1f5b5d','PENDING','VALIDATED','Order confirmed by admin','2025-09-23 08:02:30.647174','c1297951-544f-451b-ba74-4244292d26b5','d2a368a9-52f4-4115-800b-87929cc2a390'),
('f0766fb5-b2a7-4ecb-b4e7-180c0a88a6d5','','PENDING','Order placed by employee','2025-09-16 15:14:41.061696','542a1848-e278-48fd-afa5-470669646751','d2a368a9-52f4-4115-800b-87929cc2a390'),
('6f75fcc4-f507-4294-b827-29d030603c05','CANCELLED','CANCELLED','Cancelled: item_not_available. ','2025-09-23 08:03:23.055019','c1297951-544f-451b-ba74-4244292d26b5','66ecf044-bddd-4561-8475-856f993da418'),
('799ff2d0-4784-4f56-aa55-34f4b2861786','CANCELLED','CANCELLED','Cancelled: item_not_available. ','2025-09-23 08:03:16.267001','c1297951-544f-451b-ba74-4244292d26b5','66ecf044-bddd-4561-8475-856f993da418'),
('ebc2b337-330b-49ec-ac96-3eed841d0efa','PENDING','CANCELLED','Cancelled: item_not_available. ','2025-09-23 08:03:16.217139','c1297951-544f-451b-ba74-4244292d26b5','66ecf044-bddd-4561-8475-856f993da418'),
('90a8e690-754d-4c31-9b29-4d3444937fbb','','PENDING','Order placed by employee','2025-09-22 18:46:13.741567','e2718c6a-1aad-4b8d-adaf-9a25c1ffd8fd','f5785d5c-bfa4-4e8f-8ca0-803c3c2be3a6'),
('648fe2c6-5323-4a02-a8d3-56dfea5ee43e','PENDING','VALIDATED','Order confirmed by canteen admin - ready for payment','2025-09-23 14:24:39.721395','c1297951-544f-451b-ba74-4244292d26b5','6ef5079f-921b-403d-b880-a1a5629b6b5b'),
('c400dd83-2e1b-4f92-bab6-865ad9ebb795','','PENDING','Order placed by employee','2025-09-17 08:32:25.567590','542a1848-e278-48fd-afa5-470669646751','66ecf044-bddd-4561-8475-856f993da418'),
('3f04d2bd-60c9-408b-961c-a4be289cd2e5','PENDING','VALIDATED','Order confirmed by admin','2025-09-22 22:21:28.330736','c1297951-544f-451b-ba74-4244292d26b5','e2b54f1d-8218-4a3c-bcb7-92d929ec634e'),
('e6c00066-65f7-4d1c-ab8a-b4eb130e4b5b','PENDING','cancelled','Cancelled: customer_request. ','2025-09-22 18:29:34.365651','c1297951-544f-451b-ba74-4244292d26b5','3b32e950-61bd-4b46-bc8b-1d1b9370b31d'),
('b09864b6-ebec-4d91-ad57-b949e9b48859','','PENDING','Order placed by employee','2025-09-16 14:38:13.102275','c1297951-544f-451b-ba74-4244292d26b5','d9ea85e7-6826-42f2-a184-af48aea0ae7d'),
('fb426952-7f7e-4c50-9b5d-cac462106d44','','PENDING','Order placed by employee','2025-09-17 11:27:05.904164','542a1848-e278-48fd-afa5-470669646751','e2b54f1d-8218-4a3c-bcb7-92d929ec634e'),
('c0607216-936b-4195-9d4c-ccdfcea1468b','PENDING','VALIDATED','Order confirmed by admin','2025-09-22 22:07:16.686678','c1297951-544f-451b-ba74-4244292d26b5','f5785d5c-bfa4-4e8f-8ca0-803c3c2be3a6'),
('209add41-d04d-4705-8235-e275282d56d0','CANCELLED','CANCELLED','Cancelled: item_not_available. ','2025-09-23 08:03:16.272510','c1297951-544f-451b-ba74-4244292d26b5','66ecf044-bddd-4561-8475-856f993da418'),
('e24c56a1-f8a3-40f5-b11c-e725787d95ca','CANCELLED','CANCELLED','Cancelled: item_not_available. ','2025-09-23 08:03:23.053688','c1297951-544f-451b-ba74-4244292d26b5','66ecf044-bddd-4561-8475-856f993da418'),
('f13ca71c-150c-4f6b-8305-e8a9d1d49034','','PENDING','Order placed by employee','2025-09-16 14:20:58.514054','542a1848-e278-48fd-afa5-470669646751','3b32e950-61bd-4b46-bc8b-1d1b9370b31d'),
('55180974-83e3-4311-bc86-f237c6823a3b','','PENDING','Order placed by employee','2025-09-23 14:23:53.611106','542a1848-e278-48fd-afa5-470669646751','6ef5079f-921b-403d-b880-a1a5629b6b5b'),
('68c5950a-cfad-4d85-918c-ffc23c4d1200','PENDING','VALIDATED','Order confirmed by admin','2025-09-22 22:06:27.095035','c1297951-544f-451b-ba74-4244292d26b5','d9ea85e7-6826-42f2-a184-af48aea0ae7d');
/*!40000 ALTER TABLE `orders_orderhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_orderitem`
--

DROP TABLE IF EXISTS `orders_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderitem` (
  `id` uuid NOT NULL,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` >= 0),
  `unit_price` decimal(10,2) NOT NULL,
  `menu_item_id` uuid NOT NULL,
  `order_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_item_order_id_0ca9e92e` (`order_id`),
  KEY `order_item_menu_item_id_cb981a32` (`menu_item_id`),
  CONSTRAINT `order_item_menu_item_id_cb981a32_fk_menu_item_id` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item` (`id`),
  CONSTRAINT `order_item_order_id_0ca9e92e_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderitem`
--

LOCK TABLES `orders_orderitem` WRITE;
/*!40000 ALTER TABLE `orders_orderitem` DISABLE KEYS */;
INSERT INTO `orders_orderitem` VALUES
('5c27ceed-a637-45d1-ade6-34b23de64f30',1,10000.00,'01162478-96b9-43e4-ac17-80b7ca2ec05c','e2b54f1d-8218-4a3c-bcb7-92d929ec634e'),
('984502ae-d1c1-477c-952d-8a9f63c9a3be',1,1500.00,'db89e23c-3138-45ff-b337-0e67b952a1ed','3b32e950-61bd-4b46-bc8b-1d1b9370b31d'),
('ac60bdbd-48b2-4745-8d63-8b335636e23b',1,1500.00,'a93f35f7-5a72-48db-b173-30c81134467a','d9ea85e7-6826-42f2-a184-af48aea0ae7d'),
('2f3bcdf6-ef7e-457b-933b-92dca30b6b88',1,2000.00,'2c6d282b-784e-45e3-97ca-543ea834e77d','3b32e950-61bd-4b46-bc8b-1d1b9370b31d'),
('9ef59483-dc9e-42a2-a826-9c1393e2afaa',1,10000.00,'01162478-96b9-43e4-ac17-80b7ca2ec05c','f5785d5c-bfa4-4e8f-8ca0-803c3c2be3a6'),
('6c912e90-f111-4a22-b6ff-d1c5016f4d3e',1,1500.00,'db89e23c-3138-45ff-b337-0e67b952a1ed','6ef5079f-921b-403d-b880-a1a5629b6b5b'),
('10723511-30d4-4c8e-94d5-e819db4bbefa',1,2500.00,'17341895-7196-4fae-a533-453ab5bd3697','3b32e950-61bd-4b46-bc8b-1d1b9370b31d'),
('442a2b07-95fb-4939-bdb2-ed3d3a35ff1c',1,5000.00,'dba8e8f4-e2b3-4cbf-80b3-5f7448cc1557','66ecf044-bddd-4561-8475-856f993da418'),
('3f3e99cd-42fb-41b1-ae4d-f526938f68ba',1,10000.00,'01162478-96b9-43e4-ac17-80b7ca2ec05c','d2a368a9-52f4-4115-800b-87929cc2a390');
/*!40000 ALTER TABLE `orders_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_orderqueue`
--

DROP TABLE IF EXISTS `orders_orderqueue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderqueue` (
  `id` char(32) NOT NULL,
  `queue_position` int(10) unsigned NOT NULL CHECK (`queue_position` >= 0),
  `created_at` datetime(6) NOT NULL,
  `order_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `orders_orde_queue_p_f23d33_idx` (`queue_position`,`created_at`),
  CONSTRAINT `order_queue_order_id_93dba60b_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderqueue`
--

LOCK TABLES `orders_orderqueue` WRITE;
/*!40000 ALTER TABLE `orders_orderqueue` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_orderqueue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_reorderitem`
--

DROP TABLE IF EXISTS `orders_reorderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_reorderitem` (
  `id` char(32) NOT NULL,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` >= 0),
  `last_ordered` datetime(6) NOT NULL,
  `order_count` int(10) unsigned NOT NULL CHECK (`order_count` >= 0),
  `menu_item_id` uuid NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reorder_item_user_id_menu_item_id_e3bbcd10_uniq` (`user_id`,`menu_item_id`),
  KEY `reorder_item_menu_item_id_48b34b1e_fk_menu_item_id` (`menu_item_id`),
  CONSTRAINT `reorder_item_menu_item_id_48b34b1e_fk_menu_item_id` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item` (`id`),
  CONSTRAINT `reorder_item_user_id_58f757dc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_reorderitem`
--

LOCK TABLES `orders_reorderitem` WRITE;
/*!40000 ALTER TABLE `orders_reorderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_reorderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_payment`
--

DROP TABLE IF EXISTS `payments_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_payment` (
  `id` uuid NOT NULL,
  `payment_reference` varchar(50) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `transaction_type` varchar(20) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` varchar(3) NOT NULL,
  `status` varchar(20) NOT NULL,
  `phone_number` varchar(17) NOT NULL,
  `transaction_id` varchar(100) NOT NULL,
  `external_reference` varchar(100) NOT NULL,
  `provider_response` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`provider_response`)),
  `transaction_fee` decimal(8,2) NOT NULL,
  `net_amount` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `processed_at` datetime(6) DEFAULT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `description` longtext NOT NULL,
  `failure_reason` longtext NOT NULL,
  `retry_count` int(10) unsigned NOT NULL CHECK (`retry_count` >= 0),
  `order_id` uuid DEFAULT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_reference` (`payment_reference`),
  KEY `payments_pa_created_3147e3_idx` (`created_at` DESC),
  KEY `payments_pa_status_7ad4af_idx` (`status`),
  KEY `payments_pa_payment_5c92d7_idx` (`payment_method`),
  KEY `payments_pa_user_id_7a85fd_idx` (`user_id`,`created_at` DESC),
  KEY `payments_payment_order_id_22c479b7_fk_order_id` (`order_id`),
  KEY `payments_payment_transaction_id_55f6af3a` (`transaction_id`),
  CONSTRAINT `payments_payment_order_id_22c479b7_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `payments_payment_user_id_f9db060a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_payment`
--

LOCK TABLES `payments_payment` WRITE;
/*!40000 ALTER TABLE `payments_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_provider`
--

DROP TABLE IF EXISTS `payments_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_provider` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `display_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `api_endpoint` varchar(200) NOT NULL,
  `api_key` varchar(255) NOT NULL,
  `secret_key` varchar(255) NOT NULL,
  `merchant_id` varchar(100) NOT NULL,
  `fee_percentage` decimal(5,4) NOT NULL,
  `minimum_fee` decimal(8,2) NOT NULL,
  `maximum_fee` decimal(8,2) NOT NULL,
  `min_amount` decimal(10,2) NOT NULL,
  `max_amount` decimal(10,2) NOT NULL,
  `daily_limit` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_provider`
--

LOCK TABLES `payments_provider` WRITE;
/*!40000 ALTER TABLE `payments_provider` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_provider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_wallet_transaction`
--

DROP TABLE IF EXISTS `payments_wallet_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_wallet_transaction` (
  `id` uuid NOT NULL,
  `transaction_type` varchar(10) NOT NULL,
  `source` varchar(20) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `balance_before` decimal(10,2) NOT NULL,
  `balance_after` decimal(10,2) NOT NULL,
  `description` varchar(255) NOT NULL,
  `reference` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `order_id` uuid DEFAULT NULL,
  `payment_id` uuid DEFAULT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_wa_user_id_d1f41b_idx` (`user_id`,`created_at` DESC),
  KEY `payments_wa_created_f5d04a_idx` (`created_at` DESC),
  KEY `payments_wallet_tran_created_by_id_ee96ab54_fk_auth_user` (`created_by_id`),
  KEY `payments_wallet_transaction_order_id_0de808ec_fk_order_id` (`order_id`),
  KEY `payments_wallet_tran_payment_id_4f0102f9_fk_payments_` (`payment_id`),
  CONSTRAINT `payments_wallet_tran_created_by_id_ee96ab54_fk_auth_user` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `payments_wallet_tran_payment_id_4f0102f9_fk_payments_` FOREIGN KEY (`payment_id`) REFERENCES `payments_payment` (`id`),
  CONSTRAINT `payments_wallet_transaction_order_id_0de808ec_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `payments_wallet_transaction_user_id_5f1658c4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_wallet_transaction`
--

LOCK TABLES `payments_wallet_transaction` WRITE;
/*!40000 ALTER TABLE `payments_wallet_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_wallet_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_webhook`
--

DROP TABLE IF EXISTS `payments_webhook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_webhook` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `provider` varchar(20) NOT NULL,
  `webhook_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`webhook_data`)),
  `processed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `processed_at` datetime(6) DEFAULT NULL,
  `payment_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_webhook_payment_id_fd9432bb_fk_payments_payment_id` (`payment_id`),
  CONSTRAINT `payments_webhook_payment_id_fd9432bb_fk_payments_payment_id` FOREIGN KEY (`payment_id`) REFERENCES `payments_payment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_webhook`
--

LOCK TABLES `payments_webhook` WRITE;
/*!40000 ALTER TABLE `payments_webhook` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_webhook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `id` uuid NOT NULL,
  `name` varchar(255) NOT NULL,
  `report_type` varchar(50) NOT NULL,
  `format` varchar(20) NOT NULL,
  `date_from` date NOT NULL,
  `date_to` date NOT NULL,
  `filters` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`filters`)),
  `status` varchar(20) NOT NULL,
  `file_path` varchar(100) DEFAULT NULL,
  `file_size` int(10) unsigned DEFAULT NULL CHECK (`file_size` >= 0),
  `created_at` datetime(6) NOT NULL,
  `started_at` datetime(6) DEFAULT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `error_message` longtext NOT NULL,
  `generated_by_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_report__a84470_idx` (`report_type`),
  KEY `report_status_74972f_idx` (`status`),
  KEY `report_generat_5528c6_idx` (`generated_by_id`),
  KEY `report_created_2a12c2_idx` (`created_at`),
  CONSTRAINT `report_generated_by_id_56877108_fk_auth_user_id` FOREIGN KEY (`generated_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_subscription`
--

DROP TABLE IF EXISTS `report_subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_subscription` (
  `id` uuid NOT NULL,
  `name` varchar(255) NOT NULL,
  `report_type` varchar(50) NOT NULL,
  `frequency` varchar(20) NOT NULL,
  `format` varchar(20) NOT NULL,
  `filters` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`filters`)),
  `is_active` tinyint(1) NOT NULL,
  `next_run` datetime(6) DEFAULT NULL,
  `last_run` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_subscription_created_by_id_6c77b54e_fk_auth_user_id` (`created_by_id`),
  KEY `report_subs_report__a08dab_idx` (`report_type`),
  KEY `report_subs_frequen_401ef9_idx` (`frequency`),
  KEY `report_subs_is_acti_b2cfb7_idx` (`is_active`,`next_run`),
  CONSTRAINT `report_subscription_created_by_id_6c77b54e_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_subscription`
--

LOCK TABLES `report_subscription` WRITE;
/*!40000 ALTER TABLE `report_subscription` DISABLE KEYS */;
/*!40000 ALTER TABLE `report_subscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_subscription_subscribers`
--

DROP TABLE IF EXISTS `report_subscription_subscribers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_subscription_subscribers` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `reportsubscription_id` uuid NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `report_subscription_subs_reportsubscription_id_us_e2004cbb_uniq` (`reportsubscription_id`,`user_id`),
  KEY `report_subscription_subscribers_user_id_ffc411a7_fk_auth_user_id` (`user_id`),
  CONSTRAINT `report_subscription__reportsubscription_i_4445ad90_fk_report_su` FOREIGN KEY (`reportsubscription_id`) REFERENCES `report_subscription` (`id`),
  CONSTRAINT `report_subscription_subscribers_user_id_ffc411a7_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_subscription_subscribers`
--

LOCK TABLES `report_subscription_subscribers` WRITE;
/*!40000 ALTER TABLE `report_subscription_subscribers` DISABLE KEYS */;
/*!40000 ALTER TABLE `report_subscription_subscribers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_template`
--

DROP TABLE IF EXISTS `report_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_template` (
  `id` uuid NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `report_type` varchar(50) NOT NULL,
  `template_config` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`template_config`)),
  `is_public` tinyint(1) NOT NULL,
  `usage_count` int(10) unsigned NOT NULL CHECK (`usage_count` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_temp_report__14f4b6_idx` (`report_type`),
  KEY `report_temp_is_publ_b77e47_idx` (`is_public`),
  KEY `report_temp_created_d1e951_idx` (`created_by_id`),
  CONSTRAINT `report_template_created_by_id_2e138a0c_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_template`
--

LOCK TABLES `report_template` WRITE;
/*!40000 ALTER TABLE `report_template` DISABLE KEYS */;
/*!40000 ALTER TABLE `report_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_auditlog`
--

DROP TABLE IF EXISTS `reports_auditlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports_auditlog` (
  `id` char(32) NOT NULL,
  `activity` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_auditlog`
--

LOCK TABLES `reports_auditlog` WRITE;
/*!40000 ALTER TABLE `reports_auditlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_auditlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_analytics`
--

DROP TABLE IF EXISTS `system_analytics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_analytics` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_users` int(10) unsigned NOT NULL CHECK (`total_users` >= 0),
  `active_users` int(10) unsigned NOT NULL CHECK (`active_users` >= 0),
  `new_users` int(10) unsigned NOT NULL CHECK (`new_users` >= 0),
  `total_orders` int(10) unsigned NOT NULL CHECK (`total_orders` >= 0),
  `successful_orders` int(10) unsigned NOT NULL CHECK (`successful_orders` >= 0),
  `cancelled_orders` int(10) unsigned NOT NULL CHECK (`cancelled_orders` >= 0),
  `total_revenue` decimal(12,2) NOT NULL,
  `average_order_value` decimal(8,2) NOT NULL,
  `average_prep_time` decimal(5,2) NOT NULL,
  `order_completion_rate` decimal(5,2) NOT NULL,
  `customer_satisfaction` decimal(3,2) NOT NULL,
  `peak_concurrent_users` int(10) unsigned NOT NULL CHECK (`peak_concurrent_users` >= 0),
  `system_uptime` decimal(5,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_analytics`
--

LOCK TABLES `system_analytics` WRITE;
/*!40000 ALTER TABLE `system_analytics` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_analytics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_activity`
--

DROP TABLE IF EXISTS `user_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_activity` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activity_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `user_agent` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`extra_data`)),
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_activi_user_id_3b1b11_idx` (`user_id`,`timestamp`),
  KEY `user_activi_activit_cdda35_idx` (`activity_type`),
  CONSTRAINT `user_activity_user_id_9d5b7120_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_activity`
--

LOCK TABLES `user_activity` WRITE;
/*!40000 ALTER TABLE `user_activity` DISABLE KEYS */;
INSERT INTO `user_activity` VALUES
(1,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-06 07:14:46.756660','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(2,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 11:57:42.827585','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(3,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 12:01:00.493279','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(4,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 12:21:01.215628','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(5,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 18:12:37.395369','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(6,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 19:02:42.179917','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(7,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 19:49:54.775831','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(8,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 19:56:18.268306','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(9,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 19:58:15.027395','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(10,'login','Failed login attempt','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 19:58:34.400301','{}','542a1848-e278-48fd-afa5-470669646751'),
(11,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 19:59:09.929056','{}','542a1848-e278-48fd-afa5-470669646751'),
(12,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 20:02:33.638538','{}','542a1848-e278-48fd-afa5-470669646751'),
(13,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 20:27:11.505456','{}','542a1848-e278-48fd-afa5-470669646751'),
(14,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 20:44:12.692489','{}','542a1848-e278-48fd-afa5-470669646751'),
(15,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 20:47:51.128720','{}','542a1848-e278-48fd-afa5-470669646751'),
(16,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 20:48:29.100092','{}','542a1848-e278-48fd-afa5-470669646751'),
(17,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 20:52:13.896989','{}','542a1848-e278-48fd-afa5-470669646751'),
(18,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 20:56:22.254055','{}','542a1848-e278-48fd-afa5-470669646751'),
(19,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 21:00:58.830200','{}','542a1848-e278-48fd-afa5-470669646751'),
(20,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 21:05:50.587870','{}','542a1848-e278-48fd-afa5-470669646751'),
(21,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 21:05:56.397713','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(22,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 21:39:26.867367','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(23,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 21:46:59.199267','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(24,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 21:50:10.614357','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(25,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 21:51:28.008762','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(26,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 22:00:58.719515','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(27,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 22:01:12.157717','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(28,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 22:01:22.652010','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(29,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 22:01:28.872009','{}','542a1848-e278-48fd-afa5-470669646751'),
(30,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 22:36:05.668816','{}','542a1848-e278-48fd-afa5-470669646751'),
(31,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 22:36:14.869718','{}','542a1848-e278-48fd-afa5-470669646751'),
(32,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 22:36:30.231684','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(33,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-07 22:36:42.058781','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(34,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 08:23:22.578063','{}','542a1848-e278-48fd-afa5-470669646751'),
(35,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 10:13:54.078228','{}','542a1848-e278-48fd-afa5-470669646751'),
(36,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 10:17:41.086022','{}','542a1848-e278-48fd-afa5-470669646751'),
(37,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 10:17:54.422505','{}','542a1848-e278-48fd-afa5-470669646751'),
(38,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 10:18:24.190604','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(39,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 11:37:38.173499','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(40,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 11:37:44.890368','{}','542a1848-e278-48fd-afa5-470669646751'),
(41,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 11:42:05.786277','{}','542a1848-e278-48fd-afa5-470669646751'),
(42,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 11:42:20.467181','{}','542a1848-e278-48fd-afa5-470669646751'),
(43,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 14:50:39.420342','{}','542a1848-e278-48fd-afa5-470669646751'),
(44,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 14:51:19.042654','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(45,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 14:54:50.276900','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(46,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 14:54:55.502749','{}','542a1848-e278-48fd-afa5-470669646751'),
(47,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 18:25:18.149230','{}','542a1848-e278-48fd-afa5-470669646751'),
(48,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-10 18:25:42.573486','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(49,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 08:03:26.060180','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(50,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 08:07:06.087450','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(51,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 08:08:18.857313','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(52,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 08:08:25.668342','{}','542a1848-e278-48fd-afa5-470669646751'),
(53,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 11:06:33.577810','{}','542a1848-e278-48fd-afa5-470669646751'),
(54,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 11:06:40.532200','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(55,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 12:49:50.309935','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(56,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 12:50:05.219098','{}','542a1848-e278-48fd-afa5-470669646751'),
(57,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 14:20:28.344088','{}','542a1848-e278-48fd-afa5-470669646751'),
(58,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 14:20:36.042729','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(59,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 14:22:31.335340','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(60,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 14:22:39.613431','{}','542a1848-e278-48fd-afa5-470669646751'),
(61,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 15:21:44.524291','{}','542a1848-e278-48fd-afa5-470669646751'),
(62,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 15:21:51.849788','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(63,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 15:50:23.570914','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(64,'login','Failed login attempt','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 15:50:30.040778','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(65,'login','Failed login attempt','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 15:50:38.514121','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(66,'login','Failed login attempt','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 15:50:50.750226','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(67,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-11 15:51:58.941039','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(68,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 07:30:08.676350','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(69,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 07:30:24.191694','{}','542a1848-e278-48fd-afa5-470669646751'),
(70,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 08:49:05.818302','{}','542a1848-e278-48fd-afa5-470669646751'),
(71,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 08:52:46.875048','{}','542a1848-e278-48fd-afa5-470669646751'),
(72,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 08:53:45.808263','{}','542a1848-e278-48fd-afa5-470669646751'),
(73,'login','Failed login attempt','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 08:53:55.505222','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(74,'login','Failed login attempt','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 08:54:05.923526','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(75,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 08:54:22.518857','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(76,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 09:52:47.545087','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(77,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 09:53:19.996825','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(78,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:26:09.137013','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(79,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:26:13.126922','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(80,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:33:29.859345','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(81,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:34:01.566567','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(82,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:36:24.028768','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(83,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:36:28.017303','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(84,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:44:30.597160','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(85,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:44:52.106846','{}','542a1848-e278-48fd-afa5-470669646751'),
(86,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:49:19.225250','{}','542a1848-e278-48fd-afa5-470669646751'),
(87,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 10:49:26.352166','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(88,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 11:20:29.162520','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(89,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 11:20:36.660595','{}','542a1848-e278-48fd-afa5-470669646751'),
(90,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 11:20:40.573783','{}','542a1848-e278-48fd-afa5-470669646751'),
(91,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-12 11:20:47.700632','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(92,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-14 19:46:45.324779','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(93,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 12:15:21.866595','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(94,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 12:15:28.901522','{}','542a1848-e278-48fd-afa5-470669646751'),
(95,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 13:23:10.545204','{}','542a1848-e278-48fd-afa5-470669646751'),
(96,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 13:33:27.955911','{}','542a1848-e278-48fd-afa5-470669646751'),
(97,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 13:35:05.092039','{}','542a1848-e278-48fd-afa5-470669646751'),
(98,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 13:35:11.826534','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(99,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 13:43:11.232292','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(100,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 13:43:17.608109','{}','542a1848-e278-48fd-afa5-470669646751'),
(101,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 14:56:42.690415','{}','542a1848-e278-48fd-afa5-470669646751'),
(102,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-15 14:56:49.194990','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(103,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-15 15:24:38.288404','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(104,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-15 15:50:39.371992','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(105,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-15 15:50:44.578031','{}','542a1848-e278-48fd-afa5-470669646751'),
(106,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 09:20:59.160469','{}','542a1848-e278-48fd-afa5-470669646751'),
(107,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 09:42:52.285512','{}','542a1848-e278-48fd-afa5-470669646751'),
(108,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 09:42:58.730589','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(109,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 09:55:21.880930','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(110,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 09:55:29.229839','{}','542a1848-e278-48fd-afa5-470669646751'),
(111,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 09:57:41.981558','{}','542a1848-e278-48fd-afa5-470669646751'),
(112,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 09:57:50.557514','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(113,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 11:18:12.385650','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(114,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 11:18:19.913988','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(115,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 11:52:21.319794','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(116,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 11:52:28.117687','{}','542a1848-e278-48fd-afa5-470669646751'),
(117,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 12:21:15.393338','{}','542a1848-e278-48fd-afa5-470669646751'),
(118,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 12:21:20.389056','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(119,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 12:32:16.600925','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(120,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-16 12:32:23.007044','{}','542a1848-e278-48fd-afa5-470669646751'),
(121,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 14:21:21.385076','{}','542a1848-e278-48fd-afa5-470669646751'),
(122,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 14:21:26.641911','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(123,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 14:51:34.240758','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(124,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 14:51:54.134031','{}','542a1848-e278-48fd-afa5-470669646751'),
(125,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 14:53:43.800041','{}','542a1848-e278-48fd-afa5-470669646751'),
(126,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 14:53:52.941066','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(127,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 15:11:56.432339','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(128,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 15:12:01.245969','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(129,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 15:13:40.289136','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(130,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-16 15:13:45.761816','{}','542a1848-e278-48fd-afa5-470669646751'),
(131,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 08:26:04.768974','{}','542a1848-e278-48fd-afa5-470669646751'),
(132,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 08:26:14.771054','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(133,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 08:31:19.832650','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(134,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 08:31:24.319298','{}','542a1848-e278-48fd-afa5-470669646751'),
(135,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 08:32:54.308723','{}','542a1848-e278-48fd-afa5-470669646751'),
(136,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 08:33:02.301132','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(137,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-17 08:34:54.985598','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(138,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 10:52:20.347765','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(139,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 10:52:28.974939','{}','542a1848-e278-48fd-afa5-470669646751'),
(140,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 11:14:35.467194','{}','542a1848-e278-48fd-afa5-470669646751'),
(141,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 11:14:40.506901','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(142,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 11:26:35.320501','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(143,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 11:26:39.753235','{}','542a1848-e278-48fd-afa5-470669646751'),
(144,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 11:27:12.906453','{}','542a1848-e278-48fd-afa5-470669646751'),
(145,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 11:27:19.004231','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(146,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 17:33:09.777855','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(147,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 17:33:15.044958','{}','542a1848-e278-48fd-afa5-470669646751'),
(148,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 17:33:32.789802','{}','542a1848-e278-48fd-afa5-470669646751'),
(149,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-17 17:33:38.603578','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(150,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-18 15:56:26.203683','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(151,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-18 15:56:36.600664','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(152,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 08:47:20.924911','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(153,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 08:48:41.708362','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(154,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 08:48:47.998851','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(155,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 08:56:01.426984','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(156,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 08:56:05.986382','{}','542a1848-e278-48fd-afa5-470669646751'),
(157,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 09:04:06.202640','{}','542a1848-e278-48fd-afa5-470669646751'),
(158,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 09:11:16.991484','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(159,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 10:35:28.460230','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(160,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 10:35:34.856433','{}','542a1848-e278-48fd-afa5-470669646751'),
(161,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 16:22:11.549232','{}','542a1848-e278-48fd-afa5-470669646751'),
(162,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 16:22:16.844974','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(163,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 16:24:55.784524','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(164,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 16:25:00.293467','{}','542a1848-e278-48fd-afa5-470669646751'),
(165,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 16:35:42.151965','{}','542a1848-e278-48fd-afa5-470669646751'),
(166,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 16:35:46.496397','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(167,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:07:45.985213','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(168,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:30:51.764066','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(169,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:30:58.307758','{}','542a1848-e278-48fd-afa5-470669646751'),
(170,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:39:55.443167','{}','542a1848-e278-48fd-afa5-470669646751'),
(171,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:40:02.019356','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(172,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:41:23.224425','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(173,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:41:27.955128','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(174,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:44:36.128795','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(175,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:45:00.157724','{}','e2718c6a-1aad-4b8d-adaf-9a25c1ffd8fd'),
(176,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:48:18.217733','{}','e2718c6a-1aad-4b8d-adaf-9a25c1ffd8fd'),
(177,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 18:48:24.153665','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(178,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 21:13:36.123509','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(179,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 21:13:42.569138','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(180,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 22:06:18.539657','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(181,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 22:07:40.564315','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(182,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 22:07:48.559463','{}','542a1848-e278-48fd-afa5-470669646751'),
(183,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 22:08:04.459811','{}','542a1848-e278-48fd-afa5-470669646751'),
(184,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-22 22:08:12.142810','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(185,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 09:27:55.704235','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(186,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 09:28:01.540620','{}','542a1848-e278-48fd-afa5-470669646751'),
(187,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 12:01:25.560406','{}','542a1848-e278-48fd-afa5-470669646751'),
(188,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 12:01:32.982582','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(189,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-23 13:39:36.648711','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(190,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-23 13:52:40.631037','{}','8ee9f77e-149b-4050-9861-fb3422e4b055'),
(191,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','2025-09-23 13:52:48.960267','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(192,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 14:22:42.975408','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(193,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 14:22:47.995827','{}','542a1848-e278-48fd-afa5-470669646751'),
(194,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 14:24:22.945113','{}','542a1848-e278-48fd-afa5-470669646751'),
(195,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 14:24:27.951133','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(196,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 14:27:53.952014','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(197,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 14:28:02.250416','{}','542a1848-e278-48fd-afa5-470669646751'),
(198,'logout','User logged out','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 15:40:15.965066','{}','542a1848-e278-48fd-afa5-470669646751'),
(199,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 15:40:20.537176','{}','c1297951-544f-451b-ba74-4244292d26b5'),
(200,'login','User logged in successfully','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0','2025-09-23 17:11:42.801875','{}','542a1848-e278-48fd-afa5-470669646751');
/*!40000 ALTER TABLE `user_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_activity_report`
--

DROP TABLE IF EXISTS `user_activity_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_activity_report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `login_count` int(10) unsigned NOT NULL CHECK (`login_count` >= 0),
  `orders_placed` int(10) unsigned NOT NULL CHECK (`orders_placed` >= 0),
  `total_spent` decimal(10,2) NOT NULL,
  `session_duration` bigint(20) DEFAULT NULL,
  `pages_viewed` int(10) unsigned NOT NULL CHECK (`pages_viewed` >= 0),
  `favorite_items_added` int(10) unsigned NOT NULL CHECK (`favorite_items_added` >= 0),
  `reviews_given` int(10) unsigned NOT NULL CHECK (`reviews_given` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_activity_report_user_id_date_eafd809e_uniq` (`user_id`,`date`),
  KEY `user_activity_report_date_d09b1e22` (`date`),
  KEY `user_activi_date_7f683f_idx` (`date`,`orders_placed`),
  KEY `user_activi_date_bf390d_idx` (`date`,`total_spent`),
  CONSTRAINT `user_activity_report_user_id_f70058cf_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_activity_report`
--

LOCK TABLES `user_activity_report` WRITE;
/*!40000 ALTER TABLE `user_activity_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_activity_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_session`
--

DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_session` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `session_key` varchar(40) NOT NULL,
  `ip_address` char(39) NOT NULL,
  `user_agent` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_activity` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_key` (`session_key`),
  KEY `user_session_user_id_babcef0a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `user_session_user_id_babcef0a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-23 19:03:31
