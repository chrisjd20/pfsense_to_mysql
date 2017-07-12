-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.7.11 - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5167
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- Creating the read only user
-- CREATE USER 'vpn-test-read'@'%' IDENTIFIED BY 'somepassword';
-- GRANT SELECT ON `vpn-test`.* TO 'vpn-test-read'@'%';

-- Dumping database structure for vpn-test
CREATE DATABASE IF NOT EXISTS `vpn-test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `vpn-test`;

-- Dumping structure for table vpn-test.users
CREATE TABLE IF NOT EXISTS `users` (
  `username` varchar(60) NOT NULL,
  `date` tinytext,
  `password` text,
  PRIMARY KEY (`username`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table vpn-test.users: ~1 rows (approximately)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
REPLACE INTO `users` (`username`, `date`, `password`) VALUES
	('bob@test.local', '2030-07-12 00:30:04.206803+00:00', 'cold'),
	('cindy@test.local', '2030-07-12 00:30:04.206803+00:00', 'diameter'),
	('clark@test.local', '2030-07-12 00:30:04.206803+00:00', 'doing'),
	('george@test.local', '2030-07-12 00:30:04.206803+00:00', 'roll'),
	('steve@test.local', '2030-07-12 00:30:04.206803+00:00', 'steep'),
	('sue@test.local', '2030-07-12 00:30:04.206803+00:00', 'flow'),
	('wendy@test.local', '2030-07-12 00:30:04.206803+00:00', 'hung');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
