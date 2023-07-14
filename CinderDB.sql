-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 14, 2023 at 02:37 PM
-- Server version: 10.3.28-MariaDB
-- PHP Version: 7.2.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ezavarel`
--

-- --------------------------------------------------------

--
-- Table structure for table `gender`
--

CREATE TABLE `gender` (
  `gender_ID` int(5) NOT NULL,
  `name` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `gender_interests`
--

CREATE TABLE `gender_interests` (
  `gender_ID` int(5) NOT NULL,
  `user_ID` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `hobbies`
--

CREATE TABLE `hobbies` (
  `hobby_name` varchar(99) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `hobby_interests`
--

CREATE TABLE `hobby_interests` (
  `user_ID` varchar(5) NOT NULL,
  `hobby_name` varchar(99) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `first_name` varchar(40) NOT NULL,
  `last_name` varchar(40) NOT NULL,
  `city` varchar(40) NOT NULL,
  `state` varchar(2) NOT NULL,
  `birthday` date NOT NULL,
  `bio` varchar(450) NOT NULL,
  `gender_ID` int(5) NOT NULL,
  `user_ID` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_email`
--

CREATE TABLE `user_email` (
  `user_ID` varchar(5) NOT NULL,
  `email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_interaction`
--

CREATE TABLE `user_interaction` (
  `user_ID_1` varchar(5) NOT NULL,
  `user_ID_2` varchar(5) NOT NULL,
  `status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_photo`
--

CREATE TABLE `user_photo` (
  `photo_ID` varchar(24) NOT NULL,
  `user_ID` varchar(5) NOT NULL,
  `file_locale` varchar(1000) NOT NULL,
  `photo_pos` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `gender`
--
ALTER TABLE `gender`
  ADD PRIMARY KEY (`gender_ID`);

--
-- Indexes for table `gender_interests`
--
ALTER TABLE `gender_interests`
  ADD PRIMARY KEY (`user_ID`,`gender_ID`),
  ADD KEY `user_ID` (`gender_ID`),
  ADD KEY `user_ID_2` (`user_ID`);

--
-- Indexes for table `hobbies`
--
ALTER TABLE `hobbies`
  ADD PRIMARY KEY (`hobby_name`);

--
-- Indexes for table `hobby_interests`
--
ALTER TABLE `hobby_interests`
  ADD PRIMARY KEY (`user_ID`,`hobby_name`),
  ADD KEY `user_ID` (`user_ID`,`hobby_name`),
  ADD KEY `hobby_name` (`hobby_name`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_ID`),
  ADD UNIQUE KEY `user_ID` (`user_ID`),
  ADD KEY `gender_ID` (`gender_ID`);

--
-- Indexes for table `user_email`
--
ALTER TABLE `user_email`
  ADD PRIMARY KEY (`email`),
  ADD KEY `user_ID` (`user_ID`);

--
-- Indexes for table `user_interaction`
--
ALTER TABLE `user_interaction`
  ADD KEY `user_ID_1` (`user_ID_1`,`user_ID_2`),
  ADD KEY `user_ID_2` (`user_ID_2`);

--
-- Indexes for table `user_photo`
--
ALTER TABLE `user_photo`
  ADD PRIMARY KEY (`photo_ID`),
  ADD KEY `user_ID` (`user_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `gender_interests`
--
ALTER TABLE `gender_interests`
  ADD CONSTRAINT `gender_interests_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `user` (`user_ID`),
  ADD CONSTRAINT `gender_interests_ibfk_2` FOREIGN KEY (`gender_ID`) REFERENCES `gender` (`gender_ID`);

--
-- Constraints for table `hobby_interests`
--
ALTER TABLE `hobby_interests`
  ADD CONSTRAINT `hobby_interests_ibfk_1` FOREIGN KEY (`hobby_name`) REFERENCES `hobbies` (`hobby_name`),
  ADD CONSTRAINT `hobby_interests_ibfk_2` FOREIGN KEY (`user_ID`) REFERENCES `user` (`user_ID`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`gender_ID`) REFERENCES `gender` (`gender_ID`);

--
-- Constraints for table `user_email`
--
ALTER TABLE `user_email`
  ADD CONSTRAINT `user_email_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `user` (`user_ID`);

--
-- Constraints for table `user_interaction`
--
ALTER TABLE `user_interaction`
  ADD CONSTRAINT `user_interaction_ibfk_1` FOREIGN KEY (`user_ID_1`) REFERENCES `user` (`user_ID`),
  ADD CONSTRAINT `user_interaction_ibfk_2` FOREIGN KEY (`user_ID_2`) REFERENCES `user` (`user_ID`);

--
-- Constraints for table `user_photo`
--
ALTER TABLE `user_photo`
  ADD CONSTRAINT `user_photo_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `user` (`user_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
