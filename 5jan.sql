-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.4.3 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for scholar
CREATE DATABASE IF NOT EXISTS `scholar` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `scholar`;

-- Dumping structure for table scholar.courses
CREATE TABLE IF NOT EXISTS `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `sks` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.courses: ~0 rows (approximately)

-- Dumping structure for table scholar.tasks
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `sks` int DEFAULT NULL,
  `jenis` varchar(50) DEFAULT NULL,
  `estimasi_waktu` int DEFAULT NULL,
  `priority` varchar(20) DEFAULT NULL,
  `progress` int DEFAULT '0',
  `course_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.tasks: ~5 rows (approximately)
INSERT INTO `tasks` (`id`, `user_id`, `course_name`, `title`, `deadline`, `sks`, `jenis`, `estimasi_waktu`, `priority`, `progress`, `course_id`) VALUES
	(1, 1, NULL, 'start', '2025-12-22', 2, 'uts', 7, '🔴 Mendesak', 0, NULL),
	(2, 1, NULL, 'test', '2025-12-31', 2, 'proyek', 3, '🟢 Santai', 0, NULL),
	(3, 2, NULL, '1', '2025-12-23', 1, 'kuis', 1, '🔴 Mendesak', 0, NULL),
	(4, 2, NULL, '2', '2025-12-23', 2, 'kuis', 2, '🔴 Mendesak', 0, NULL),
	(5, 3, NULL, 'Math', '2026-01-05', 2, 'uas', 2, '🔴 Mendesak', 0, NULL);

-- Dumping structure for table scholar.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `is_premium` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.users: ~3 rows (approximately)
INSERT INTO `users` (`id`, `username`, `email`, `password`, `is_premium`) VALUES
	(1, 'test', 'test@gmail.com', '111', 1),
	(2, 'test1', 'test1@gmail.com', '111', 0),
	(3, 'test2', 'test2@gmail.com', '123', 0);

-- Dumping structure for table scholar.user_settings
CREATE TABLE IF NOT EXISTS `user_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `daily_capacity` int DEFAULT '2',
  `notification_enabled` tinyint(1) DEFAULT '1',
  `theme` varchar(20) DEFAULT 'light',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_settings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.user_settings: ~0 rows (approximately)

-- Dumping structure for table scholar.weekly_capacity
CREATE TABLE IF NOT EXISTS `weekly_capacity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `daily_hours` int DEFAULT '2',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.weekly_capacity: ~1 rows (approximately)
INSERT INTO `weekly_capacity` (`id`, `user_id`, `daily_hours`) VALUES
	(1, 3, 2);

-- Dumping structure for table scholar.weekly_schedule
CREATE TABLE IF NOT EXISTS `weekly_schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `day_name` varchar(20) DEFAULT NULL,
  `hours_available` int DEFAULT '2',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `weekly_schedule_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.weekly_schedule: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
