-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 23, 2026 at 06:29 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `game grid deployed`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_create_tournaments`
--

CREATE TABLE `admin_create_tournaments` (
  `tournament_name` varchar(100) NOT NULL,
  `id` int(10) NOT NULL,
  `game` varchar(100) NOT NULL,
  `tournament_type` varchar(100) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `venue` varchar(100) NOT NULL,
  `maximum_teams` int(11) NOT NULL,
  `reg_last_date` date NOT NULL,
  `status` varchar(50) NOT NULL,
  `winner` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_create_tournaments`
--

INSERT INTO `admin_create_tournaments` (`tournament_name`, `id`, `game`, `tournament_type`, `start_date`, `end_date`, `venue`, `maximum_teams`, `reg_last_date`, `status`, `winner`, `is_deleted`, `deleted_at`) VALUES
('GPAN cricket tournament', 1, 'cricket', 'Knockout', '2026-08-01', '2026-08-05', 'Ahilyanagar', 8, '2026-07-25', 'Ongoing', NULL, 0, NULL),
('GPAN Football Tournament', 2, 'Football', 'Knockout', '2026-08-01', '2026-08-05', 'Ahilyanagar', 7, '2026-07-31', 'Ongoing', NULL, 0, NULL),
('CHESS TOURNAMENT', 3, 'CHESS', 'Knockout', '2026-08-15', '2026-08-20', 'AHILYANAGAR', -3, '2026-08-12', 'Upcoming', NULL, 1, '2026-08-23 21:50:42'),
('kho-kho tournament', 5, 'KHO KHO', 'Knockout', '2026-08-17', '2026-08-21', 'ahilyanagar', 8, '2026-08-16', 'Completed', NULL, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `admin_dashboard`
--

CREATE TABLE `admin_dashboard` (
  `module` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_edit_tournaments`
--

CREATE TABLE `admin_edit_tournaments` (
  `tournament_name` varchar(100) NOT NULL,
  `game` varchar(50) NOT NULL,
  `tournament_type` varchar(25) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `venue` varchar(100) NOT NULL,
  `maximum_teams` int(3) NOT NULL,
  `reg_last_date` date NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_manage_tournaments`
--

CREATE TABLE `admin_manage_tournaments` (
  `id` int(10) NOT NULL,
  `tournament_name` varchar(100) NOT NULL,
  `game` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `venue` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `action` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_manage_users`
--

CREATE TABLE `admin_manage_users` (
  `id` int(10) NOT NULL,
  `fullname` varchar(50) NOT NULL,
  `username` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mobile` int(10) NOT NULL,
  `action` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_profile`
--

CREATE TABLE `admin_profile` (
  `fullname` varchar(40) NOT NULL,
  `username` varchar(15) NOT NULL,
  `email` varchar(40) NOT NULL,
  `mobile` bigint(10) NOT NULL,
  `new_password` varchar(15) NOT NULL,
  `confirm_password` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_profile`
--

INSERT INTO `admin_profile` (`fullname`, `username`, `email`, `mobile`, `new_password`, `confirm_password`) VALUES
('Administrator', 'admin', 'admin@gmail.com', 8742952892, '12345', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `admin_published_notifications`
--

CREATE TABLE `admin_published_notifications` (
  `id` int(10) NOT NULL,
  `title` varchar(50) NOT NULL,
  `message` varchar(200) NOT NULL,
  `publish_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_published_notifications`
--

INSERT INTO `admin_published_notifications` (`id`, `title`, `message`, `publish_date`) VALUES
(1, '', 'welcome users', '2026-07-28'),
(2, '', '.........................................................', '2026-07-30'),
(3, 'Upcoming Matches ', 'Computer vs Production ', '2026-08-03'),
(4, 'publish', 'publish notifications\r\n', '2026-08-25'),
(5, 'hii', 'hello players\r\n', '2026-08-13'),
(6, 'hi', 'hii', '2026-08-12'),
(7, 'akj askjc', 'nakfsa', '2026-08-21'),
(8, 'hello users', 'hiiii', '2026-08-12'),
(9, 'hiii', 'userssssssssa', '2026-08-12');

-- --------------------------------------------------------

--
-- Table structure for table `admin_published_results`
--

CREATE TABLE `admin_published_results` (
  `id` int(10) NOT NULL,
  `tournament` varchar(100) NOT NULL,
  `winner` varchar(100) NOT NULL,
  `runnerup` varchar(100) NOT NULL,
  `score` varchar(100) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_published_results`
--

INSERT INTO `admin_published_results` (`id`, `tournament`, `winner`, `runnerup`, `score`, `date`) VALUES
(1, 'GPAN Football Tournament', 'CO', 'CM', '4-2', '2026-08-04');

-- --------------------------------------------------------

--
-- Table structure for table `admin_recent_activies`
--

CREATE TABLE `admin_recent_activies` (
  `date` date NOT NULL,
  `activity` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `message` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`name`, `email`, `subject`, `message`) VALUES
('abc', 'abc@gmail.com', 'message', 'hi');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `username` varchar(20) NOT NULL,
  `password` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `matches`
--

CREATE TABLE `matches` (
  `id` int(11) NOT NULL,
  `tournament_id` int(11) NOT NULL,
  `match_no` int(11) NOT NULL,
  `team_a` varchar(100) DEFAULT NULL,
  `team_b` varchar(100) DEFAULT NULL,
  `match_date` date DEFAULT NULL,
  `match_time` time DEFAULT NULL,
  `venue` varchar(150) DEFAULT NULL,
  `round` varchar(50) DEFAULT NULL,
  `winner` varchar(100) DEFAULT NULL,
  `score_team_a` varchar(20) DEFAULT NULL,
  `score_team_b` varchar(20) DEFAULT NULL,
  `player_of_match` varchar(100) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `matches`
--

INSERT INTO `matches` (`id`, `tournament_id`, `match_no`, `team_a`, `team_b`, `match_date`, `match_time`, `venue`, `round`, `winner`, `score_team_a`, `score_team_b`, `player_of_match`, `remarks`, `status`) VALUES
(1, 2, 1, 'Computer', 'Civil', '2026-08-01', '12:30:00', 'Ahilyanagar', 'League', 'cComputer', '112-2', '102-10', 'aditya kulkarni', '', 'completed'),
(3, 2, 2, 'co', 'cm', '2026-08-01', '03:30:00', 'GP Ground', 'league', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(4, 2, 3, 'Mechenical', 'Electrical', '2026-08-05', '12:30:00', 'GPAN Ground', 'League', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(7, 1, 3, 'IS', 'PG', '2026-08-03', '12:30:00', 'GPAN Ground', 'League', NULL, NULL, NULL, NULL, NULL, 'ongoing'),
(10, 2, 4, 'IS', 'PG', '2026-08-13', '08:09:00', 'ahilyanager', 'quater final', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(11, 3, 1, 'CO', 'CM', '2026-08-15', '12:30:00', 'AV HALL', 'KNOCK OUT', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(12, 3, 2, 'PG', 'IS', '2026-08-15', '02:30:00', 'AV HALL', 'KNOCK OUT', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(13, 3, 3, 'ME', 'EJ', '2026-08-16', '12:30:00', 'AV HALL', 'KNOCK OUT', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(14, 3, 4, 'EE', 'CE', '2026-08-16', '02:30:00', 'AV HALL', 'KNOCK OUT', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(15, 3, 5, 'WINNER KO 1', 'WINNER KO 2', '2026-08-18', '12:30:00', 'AV HALL', 'SEMI SFINAL', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(16, 3, 6, 'WINNER KO 3', 'WINNER KO 4', '2026-08-18', '02:30:00', 'AV HALL', 'SEMI FINAL', NULL, NULL, NULL, NULL, NULL, 'upcoming'),
(17, 3, 7, 'SEMI FINAL 1', 'SEMI FINAL 2', '2026-08-20', '12:30:00', 'AV HALL', 'FINAL', NULL, NULL, NULL, NULL, NULL, 'upcoming');

-- --------------------------------------------------------

--
-- Table structure for table `registrations`
--

CREATE TABLE `registrations` (
  `id` int(11) NOT NULL,
  `tournament_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `team_name` varchar(100) NOT NULL,
  `registered_on` timestamp NOT NULL DEFAULT current_timestamp(),
  `captain_name` varchar(100) NOT NULL,
  `captain_mobile` bigint(10) NOT NULL,
  `player_names` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `registrations`
--

INSERT INTO `registrations` (`id`, `tournament_id`, `username`, `team_name`, `registered_on`, `captain_name`, `captain_mobile`, `player_names`) VALUES
(6, 2, 'atharv_2708_', 'computers', '2026-07-31 05:57:21', 'ABC', 1234567890, 'ABC, PQR, XYZ, MNO, KLM'),
(8, 1, 'abc123', 'RCB', '2026-08-03 05:39:39', 'Rajat Patidar', 8739264287, 'Virat Kohli, Virat Kohli, Virat Kohli, Virat Kohli'),
(9, 1, 'atharv123', 'MI', '2026-08-04 18:21:01', 'Rohit Sharma', 7923846109, 'Rohit Sharma, Jasprit Bumrah');

-- --------------------------------------------------------

--
-- Table structure for table `sign_up`
--

CREATE TABLE `sign_up` (
  `fullname` varchar(40) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `mobile` bigint(10) NOT NULL,
  `password` varchar(15) NOT NULL,
  `confirm_password` varchar(15) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sign_up`
--

INSERT INTO `sign_up` (`fullname`, `username`, `email`, `mobile`, `password`, `confirm_password`, `is_deleted`, `deleted_at`) VALUES
('ABC', 'abc123', 'abc@gmail.com', 9983957222, '123', '123', 0, NULL),
('Aditya Shinde', 'hazelgod', 'aditya18@gmail.com', 2147483647, '181818', '181818', 0, NULL),
('Atharv Sudrik', 'atharv_2708_', 'atharvsudrik45@gmail.com', 2147483647, '1234', '1234', 0, NULL),
('Kiran Nimbalkar', 'kiran123', 'kiran@123gmail.com', 2147483647, '1234', '1234', 0, NULL),
('Abc', 'Abc', 'Abc@gmail.com', 12345678, 'Abc', 'Abc', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_notifications`
--

CREATE TABLE `user_notifications` (
  `publish_date` date NOT NULL,
  `message` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_notifications`
--

INSERT INTO `user_notifications` (`publish_date`, `message`) VALUES
('2026-07-28', 'Welcome all Users\r\n'),
('2026-07-28', 'Welcome Users');

-- --------------------------------------------------------

--
-- Table structure for table `user_profile`
--

CREATE TABLE `user_profile` (
  `name` varchar(40) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` int(10) NOT NULL,
  `school/college` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_results`
--

CREATE TABLE `user_results` (
  `tournaments` varchar(100) NOT NULL,
  `position` int(2) NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_tournaments`
--

CREATE TABLE `user_tournaments` (
  `id` int(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `game` varchar(40) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_create_tournaments`
--
ALTER TABLE `admin_create_tournaments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin_manage_tournaments`
--
ALTER TABLE `admin_manage_tournaments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin_manage_users`
--
ALTER TABLE `admin_manage_users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin_published_notifications`
--
ALTER TABLE `admin_published_notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin_published_results`
--
ALTER TABLE `admin_published_results`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `matches`
--
ALTER TABLE `matches`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_tournament` (`tournament_id`);

--
-- Indexes for table `registrations`
--
ALTER TABLE `registrations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tournament_id` (`tournament_id`);

--
-- Indexes for table `user_tournaments`
--
ALTER TABLE `user_tournaments`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_create_tournaments`
--
ALTER TABLE `admin_create_tournaments`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `admin_manage_tournaments`
--
ALTER TABLE `admin_manage_tournaments`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `admin_manage_users`
--
ALTER TABLE `admin_manage_users`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `admin_published_notifications`
--
ALTER TABLE `admin_published_notifications`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `admin_published_results`
--
ALTER TABLE `admin_published_results`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `matches`
--
ALTER TABLE `matches`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `registrations`
--
ALTER TABLE `registrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user_tournaments`
--
ALTER TABLE `user_tournaments`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `matches`
--
ALTER TABLE `matches`
  ADD CONSTRAINT `fk_tournament` FOREIGN KEY (`tournament_id`) REFERENCES `admin_create_tournaments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `registrations`
--
ALTER TABLE `registrations`
  ADD CONSTRAINT `registrations_ibfk_1` FOREIGN KEY (`tournament_id`) REFERENCES `admin_create_tournaments` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
