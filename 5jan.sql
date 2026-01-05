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
  `course_name` varchar(100) NOT NULL,
  `sks` int DEFAULT '2',
  `color` varchar(20) DEFAULT '#3b82f6',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.courses: ~8 rows (approximately)
INSERT INTO `courses` (`id`, `user_id`, `course_name`, `sks`, `color`, `created_at`) VALUES
	(1, 1, 'Mathematics', 3, '#3b82f6', '2026-01-05 11:34:49'),
	(2, 1, 'Physics', 3, '#ef4444', '2026-01-05 11:34:49'),
	(3, 1, 'Computer Science', 4, '#10b981', '2026-01-05 11:34:49'),
	(4, 1, 'English', 2, '#8b5cf6', '2026-01-05 11:34:49'),
	(5, 2, 'Calculus', 3, '#f59e0b', '2026-01-05 11:34:49'),
	(6, 2, 'Statistics', 2, '#ec4899', '2026-01-05 11:34:49'),
	(7, 3, 'Programming', 4, '#8b5cf6', '2026-01-05 11:34:49'),
	(8, 3, 'Database', 3, '#10b981', '2026-01-05 11:34:49');

-- Dumping structure for table scholar.tasks
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `deadline` date DEFAULT NULL,
  `sks` int DEFAULT '2',
  `jenis` varchar(50) DEFAULT 'tugas',
  `estimasi_waktu` int DEFAULT '2',
  `priority` varchar(20) DEFAULT 0xF09F9FA22053616E746169,
  `progress` int DEFAULT '0',
  `course_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.tasks: ~8 rows (approximately)
INSERT INTO `tasks` (`id`, `user_id`, `title`, `deadline`, `sks`, `jenis`, `estimasi_waktu`, `priority`, `progress`, `course_id`, `created_at`) VALUES
	(1, 1, 'Linear Algebra Assignment', '2025-12-22', 2, 'tugas', 7, '🔴 Mendesak', 0, 1, '2026-01-05 11:34:49'),
	(2, 1, 'Quantum Physics Project', '2025-12-31', 3, 'proyek', 3, '🟢 Santai', 0, 2, '2026-01-05 11:34:49'),
	(3, 1, 'Web Programming Project', '2026-01-10', 4, 'proyek', 5, '🟡 Sedang', 0, 3, '2026-01-05 11:34:49'),
	(4, 1, 'English Essay', '2026-01-15', 2, 'tugas', 2, '🟢 Santai', 0, 4, '2026-01-05 11:34:49'),
	(5, 2, 'Derivatives Quiz', '2025-12-23', 1, 'kuis', 1, '🔴 Mendesak', 0, 5, '2026-01-05 11:34:49'),
	(6, 2, 'Integration Homework', '2025-12-23', 2, 'tugas', 2, '🔴 Mendesak', 0, 5, '2026-01-05 11:34:49'),
	(7, 3, 'Data Structures Final Exam', '2026-01-05', 2, 'uas', 2, '🔴 Mendesak', 0, 7, '2026-01-05 11:34:49'),
	(8, 3, 'SQL Database Project', '2026-01-12', 3, 'proyek', 4, '🟡 Sedang', 0, 8, '2026-01-05 11:34:49'),
	(9, 3, 'English', '2026-01-06', 2, 'kuis', 2, '🔴 Mendesak', 0, 7, '2026-01-05 13:49:58');

-- Dumping structure for table scholar.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_premium` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.users: ~3 rows (approximately)
INSERT INTO `users` (`id`, `username`, `email`, `password`, `is_premium`, `created_at`) VALUES
	(1, 'test', 'test@gmail.com', '111', 1, '2026-01-05 11:34:49'),
	(2, 'test1', 'test1@gmail.com', '111', 0, '2026-01-05 11:34:49'),
	(3, 'test2', 'test2@gmail.com', '123', 0, '2026-01-05 11:34:49');

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
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `weekly_capacity_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table scholar.weekly_capacity: ~3 rows (approximately)
INSERT INTO `weekly_capacity` (`id`, `user_id`, `daily_hours`) VALUES
	(1, 1, 4),
	(2, 2, 3),
	(3, 3, 2);

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
