SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `dating_app`
--
-- BEFORE RUNNING, DISABLE FOREIGN KEY CHECKS
-- --------------------------------------------------------

--
-- Drop and replace tables
--

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `status`;
DROP TABLE IF EXISTS `access_control`;
DROP TABLE IF EXISTS `state`;
DROP TABLE IF EXISTS `age_interests`;
DROP TABLE IF EXISTS `gender_interests`;
DROP TABLE IF EXISTS `hobbies`;
DROP TABLE IF EXISTS `hobby_interests`;
DROP TABLE IF EXISTS `user_email`;
DROP TABLE IF EXISTS `user_interaction`;
DROP TABLE IF EXISTS `user_photo`;
DROP TABLE IF EXISTS `gender`;
DROP TABLE IF EXISTS `user`;

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;

-- --------------------------------------------------------

--
-- Table structure for table `gender`
--

CREATE TABLE `gender` (
  `gender_ID` int(5) AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`gender_ID`)
);

-- --------------------------------------------------------

--
-- Table structure for table `gender_interests`
--

CREATE TABLE `gender_interests` (
  `gender_ID` int(5) NOT NULL,
  `user_ID` int(5) NOT NULL
);

--
-- Table structure for table `status`
--

CREATE TABLE `status` (
  `status_name` varchar(10) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `hobbies`
--

CREATE TABLE `hobbies` (
  `hobby_name` varchar(99) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `hobby_interests`
--

CREATE TABLE `hobby_interests` (
  `user_ID` int(5) NOT NULL,
  `hobby_name` varchar(99) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `state`
--

CREATE TABLE `state` (
  `state` varchar(2) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_ID` int(5) AUTO_INCREMENT,
  `first_name` varchar(40),
  `last_name` varchar(40),
  `city` varchar(40),
  `state` varchar(2),
  `birthday` date,
  `bio` varchar(450),
  `gender_ID` int(5),
  PRIMARY KEY (`user_ID`)
);

-- --------------------------------------------------------

--
-- Table structure for table `access_control`
--

CREATE TABLE `access_control` (
  `user_ID` int(5) NOT NULL,
  `username` varchar(40) NOT NULL,
  `clear_pw` varchar(256) NOT NULL,
  `cipher_pw` varchar(64) NOT NULL,
  `salt` varchar(20) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `user_email`
--

CREATE TABLE `user_email` (
  `user_ID` int(5) NOT NULL,
  `email` varchar(100) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `user_interaction`
--

CREATE TABLE `user_interaction` (
  `user_ID_1` int(5) NOT NULL,
  `user_ID_2` int(5) NOT NULL,
  `status` varchar(10) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `user_photo`
--

CREATE TABLE `user_photo` (
  `photo_ID` int(5) NOT NULL,
  `user_ID` int(5) NOT NULL,
  `file_locale` varchar(1000) NOT NULL,
  `photo_pos` int(3) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `age_interests`
--

CREATE TABLE `age_interests` (
  `user_ID` int(5) NOT NULL,
  `low_age` int(2),
  `high_age` int(2)
);


--
-- Indexes for dumped tables
--

--
-- Indexes for table `age_interests`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`status_name`);

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
-- Indexes for table `state`
--
ALTER TABLE `state`
  ADD PRIMARY KEY (`state`);

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
-- Indexes for table `age_interests`
--
ALTER TABLE `age_interests`
  ADD PRIMARY KEY (`user_ID`);

--
-- Indexes for table `access_control`
--
ALTER TABLE `access_control`
  ADD PRIMARY KEY (`user_ID`);

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
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`gender_ID`) REFERENCES `gender` (`gender_ID`),
  ADD CONSTRAINT `user_ibfk_2` FOREIGN KEY (`state`) REFERENCES `state` (`state`);

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
  ADD CONSTRAINT `user_interaction_ibfk_2` FOREIGN KEY (`user_ID_2`) REFERENCES `user` (`user_ID`),
  ADD CONSTRAINT `user_interaction_ibfk_3` FOREIGN KEY (`status`) REFERENCES `status` (`status_name`);

--
-- Constraints for table `user_photo`
--
ALTER TABLE `user_photo`
  ADD CONSTRAINT `user_photo_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `user` (`user_ID`);

--
-- Constraints for table `access_control`
--
ALTER TABLE `access_control`
  ADD CONSTRAINT `access_control_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `user` (`user_ID`);
COMMIT;

--
-- Constraints for table `age_interests`
--
ALTER TABLE `age_interests`
  ADD CONSTRAINT `age_interests_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `user` (`user_ID`);

-- DISABLE FOREIGN KEY CHECKS BEFORE RUNNING

-- DROP OLD DATA

DELETE FROM state;
DELETE FROM access_control;
DELETE FROM status;
DELETE FROM gender;
DELETE FROM gender_interests;
DELETE FROM hobbies;
DELETE FROM hobby_interests;
DELETE FROM user;
DELETE FROM user_email;
DELETE FROM user_interaction;
DELETE FROM user_photo;
DELETE FROM age_interests;

-- GENDER TABLE INSERTS

INSERT INTO gender VALUES (1, 'Male');
INSERT INTO gender VALUES (2, 'Female');
INSERT INTO gender VALUES (3, 'Other');

-- STATUS TABLE INSERTS

INSERT INTO status VALUES('like');
INSERT INTO status VALUES('dislike');
INSERT INTO status VALUES('block');

-- HOBBY TABLE INSERTS

INSERT INTO hobbies VALUES
('surfing'),('woodworking'),('painting'),('writing'),('soccer'),('pottery'),('archery'),('horseback riding'),('pickleball'),('hiking'),('snowboarding'),('canoeing'),
('golfing'),('reading'),('traveling'),('cooking'),('watching movies'),('playing video games'),('dancing'),('photography'),('cycling'),('running'),('yoga'),
('playing musical instruments'),('swimming'),('playing board games'),('gardening'),('volunteering'),('fishing'),('camping'),('birdwatching'),('DIY');

-- STATE TABLE INSERTS

INSERT INTO `state` (state) VALUES
  ('AL'), ('AK'), ('AZ'), ('AR'), ('CA'), ('CO'), ('CT'), ('DE'), ('FL'), ('GA'), ('HI'), ('ID'), ('IL'), ('IN'), ('IA'), ('KS'), ('KY'), ('LA'), ('ME'), ('MD'),
	('MA'), ('MI'), ('MN'), ('MS'), ('MO'), ('MT'), ('NE'), ('NV'), ('NH'), ('NJ'), ('NM'), ('NY'), ('NC'), ('ND'), ('OH'), ('OK'), ('OR'), ('PA'), ('RI'), ('SC'),
	('SD'), ('TN'), ('TX'), ('UT'), ('VT'), ('VA'), ('WA'), ('WV'), ('WI'), ('WY');

-- USER TABLE INSERTS

INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Judy', 'Jones', 'Cincinnati', 'OH', '2001-08-26', 'Favorite color: purple; I love my Scion tC.', '2', '00001');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Arlene', 'Spencer', 'Keyport', 'NJ', '1957-10-12', 'Im an office administrator and my blood type is B-.', '2', '00002');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Leonard', 'Smith', 'Marietta', 'GA', '1952-12-27', 'Im a Capricorn looking for a Zemini', '1', '00003');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Jorge', 'Lowe', 'Everett', 'WA', '1999-05-18', 'Let me share my credit card information with you', '1', '00004');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Carolyn', 'King', 'Walsenburg', 'CO', '1960-12-14', 'I can play the flute like its nobodys business, and I can beat you to the bottom of the hill on my snowboard', '2', '00005');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Andrea', 'Tolar', 'Mclain', 'MS', '1940-11-12', 'I am ready to settle down and find my soul mate.', '2', '00006');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Brian', 'Siegle', 'Providence', 'RI', '2000-10-10', 'Lets get an ice cream cone', '1', '00007');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Roy', 'Starr', 'Evansville', 'IN', '1970-12-28', 'The furthest I ever hiked was 2650 miles in one shot.', '3', '00008');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Jeanne', 'Moses', 'Elroy', 'WI', '1996-06-15', 'I play Monopoly competitively', '2', '00009');
INSERT INTO `user` (`first_name`, `last_name`, `city`, `state`, `birthday`, `bio`, `gender_ID`, `user_ID`) VALUES ('Marie', 'Conley', 'Edinburg', 'IL', '1998-10-29', 'Owner operator of Dun Rite Lawn Maintenance. Call 217-623-0918 for a free quote.', '2', '00010');

-- EMAIL TABLE INSERTS

INSERT INTO user_email VALUES('00001', 'JudyTJones@dawnchaser.com');
INSERT INTO user_email VALUES('00002', 'ArleneFSpencer@armyspy.com');
INSERT INTO user_email VALUES('00003', 'LeonardCSmith@onestopbaseball.com');
INSERT INTO user_email VALUES('00004', 'JorgeWLowe@rhyta.com');
INSERT INTO user_email VALUES('00005', 'CarolynKKing@teknikgillis.com');
INSERT INTO user_email VALUES('00006', 'AndreaJTolar@dayrep.com');
INSERT INTO user_email VALUES('00007', 'BrianBSiegle@dotzippy.com');
INSERT INTO user_email VALUES('00008', 'RoyWStarr@rcsenterprise.com');
INSERT INTO user_email VALUES('00009', 'JeanneLMoses@jourrapide.com');
INSERT INTO user_email VALUES('00010', 'MarieAConley@zahraacenter.com');

-- USER HOBBY TABLE INSERTS

INSERT INTO hobby_interests VALUES ('00001', 'hiking');
INSERT INTO hobby_interests VALUES ('00001', 'soccer');
INSERT INTO hobby_interests VALUES ('00002', 'pickleball');
INSERT INTO hobby_interests VALUES ('00003', 'soccer');
INSERT INTO hobby_interests VALUES ('00004', 'horseback riding');
INSERT INTO hobby_interests VALUES ('00005', 'pottery');
INSERT INTO hobby_interests VALUES ('00006', 'writing');
INSERT INTO hobby_interests VALUES ('00007', 'soccer');
INSERT INTO hobby_interests VALUES ('00007', 'canoeing');
INSERT INTO hobby_interests VALUES ('00007', 'surfing');
INSERT INTO hobby_interests VALUES ('00008', 'painting');
INSERT INTO hobby_interests VALUES ('00008', 'pottery');
INSERT INTO hobby_interests VALUES ('00009', 'snowboarding');
INSERT INTO hobby_interests VALUES ('00010', 'woodworking');
INSERT INTO hobby_interests VALUES ('00010', 'archery');

-- USER GENDER INTERESTS TABLE INSERTS

INSERT INTO gender_interests VALUES ('2', '00001');
INSERT INTO gender_interests VALUES ('1', '00002');
INSERT INTO gender_interests VALUES ('3', '00002');
INSERT INTO gender_interests VALUES ('2', '00003');
INSERT INTO gender_interests VALUES ('1', '00004');
INSERT INTO gender_interests VALUES ('1', '00005');
INSERT INTO gender_interests VALUES ('1', '00006');
INSERT INTO gender_interests VALUES ('2', '00007');
INSERT INTO gender_interests VALUES ('2', '00008');
INSERT INTO gender_interests VALUES ('3', '00008');
INSERT INTO gender_interests VALUES ('1', '00009');
INSERT INTO gender_interests VALUES ('2', '00010');


-- USER INTERACTION TABLE INSERTS
-- options: 'like', 'dislike', 'block'

INSERT INTO user_interaction VALUES ('00001', '00010', 'like');
INSERT INTO user_interaction VALUES ('00002', '00003', 'like');
INSERT INTO user_interaction VALUES ('00005', '00002', 'like');
INSERT INTO user_interaction VALUES ('00008', '00002', 'block');
INSERT INTO user_interaction VALUES ('00006', '00003', 'like');
INSERT INTO user_interaction VALUES ('00009', '00004', 'like');
INSERT INTO user_interaction VALUES ('00003', '00006', 'like');
INSERT INTO user_interaction VALUES ('00004', '00009', 'dislike');
INSERT INTO user_interaction VALUES ('00006', '00008', 'like');
INSERT INTO user_interaction VALUES ('00002', '00005', 'dislike');
INSERT INTO user_interaction VALUES ('00006', '00007', 'block');
INSERT INTO user_interaction VALUES ('00008', '00010', 'dislike');
INSERT INTO user_interaction VALUES ('00002', '00008', 'dislike');
INSERT INTO user_interaction VALUES ('00003', '00008', 'dislike');
INSERT INTO user_interaction VALUES ('00010', '00001', 'dislike');

-- USER PHOTO TABLE INSERT

INSERT INTO user_photo VALUES ('1', '1', '/1_1.jpg', '1');
INSERT INTO user_photo VALUES ('2', '2', '/2_1.jpg', '1');
INSERT INTO user_photo VALUES ('3', '3', '/3_1.jpg', '1');
INSERT INTO user_photo VALUES ('4', '4', '/4_1.jpg', '1');
INSERT INTO user_photo VALUES ('5', '5', '/5_1.jpg', '1');
INSERT INTO user_photo VALUES ('6', '6', '/6_1.jpg', '1');
INSERT INTO user_photo VALUES ('7', '7', '/7_1.jpg', '1');
INSERT INTO user_photo VALUES ('8', '8', '/8_1.jpg', '1');
INSERT INTO user_photo VALUES ('9', '9', '/9_1.jpg', '1');
INSERT INTO user_photo VALUES ('10', '10', '/10_1.jpg', '1');
INSERT INTO user_photo VALUES ('11', '7', '/7_2.jpg', '2');
INSERT INTO user_photo VALUES ('12', '7', '/7_3.jpg', '3');
INSERT INTO user_photo VALUES ('13', '10', '/10_2.jpg', '2');

INSERT INTO access_control VALUES (1, 'jjones', 'hCRDacCE', '596ff907ae907389362029d7540fe600dfbd6d9f5c5e0c0619993a47a451ac55', 'pXTiBZSazf9lhPzwqDAi');
INSERT INTO access_control VALUES (2, 'aspencer', 'B75KPaHU', '9945dcd0c7dfa5e726253b4483dc075915c236404d0fa5178af9b6beb6241836', 'kXDZXJeG3yDUCgeovqNu');
INSERT INTO access_control VALUES (3, 'lsmith', 'b7om6ynU', '9037b0e507fdebaa68d1694723e3d6fa1f7474ad9e31d567d88baf5e3c02c0fc', 'BKameHtXFVktzNmejAwe');
INSERT INTO access_control VALUES (4, 'jlowe', 'RTvF4xLo', '1a2d2f8b33b3d0dc26c6bce8f6c7c25de806768bae028dbb1fd226cd6f07ba4a', 'wIXLvlY4bnnDl7VzyWSw');
INSERT INTO access_control VALUES (5, 'cking', 'WgGlOuZX', 'b5ca1c7ddae00048ac6c8bc091079e4e77bc6104decc847a505579367d753e1a', '5D7OJS7GBQM1eWQKTCwI');
INSERT INTO access_control VALUES (6, 'atolar', 'iIWLODVm', '84a9827c721c62b0165ca82050a87a6acbf75d02bdcd847fd7e50b7ccbce0e43', 'LIrmNFUjSoAzQSGwQe4z');
INSERT INTO access_control VALUES (7, 'bsiegle', '69Q9ls4D', '52a78143978a0086fe2a07f32b56e4590752c3e2bf2e65d1a76773c766d9cbc2', 'K3N03uqOldHuI9POMKrt');
INSERT INTO access_control VALUES (8, 'rstarr', 'P9uRUDVD', 'd9b205a11b906117d20e0e11858e6eb621c541ae2a4f0586c085ec634720e1af', '08s84aQpDud154U09Ijs');
INSERT INTO access_control VALUES (9, 'jmoses', 'U1OCVHc7', '7d683f52c12472c804dde1afb63d8045fb8c652d33050b316bf61daf21a841e8', 'zR0L9UszEbrw2jquBqtK');
INSERT INTO access_control VALUES (10, 'mconley', 'YPe7N3ak', '58556917ef2dc837def9f4b75adb3aaee2c21de87dd418482e3d5688a5e41f27', 'FPCFJQqNaMZmOeFVGSRW');

INSERT INTO age_interests VALUES (1, 18, 25);
INSERT INTO age_interests VALUES (2, 60, 70);
INSERT INTO age_interests VALUES (3, 55, 80);
INSERT INTO age_interests VALUES (4, 18, 30);
INSERT INTO age_interests VALUES (5, 58, 65);
INSERT INTO age_interests VALUES (6, 21, 30);
INSERT INTO age_interests VALUES (7, 18, 30);
INSERT INTO age_interests VALUES (8, 30, 50);
INSERT INTO age_interests VALUES (9, 23, 32);
INSERT INTO age_interests VALUES (10, 21, 30);