--
-- NOTE: the database name here must match which is given in the <python_path>/mtms/base/configs.py file
--

-- clearing old
DROP DATABASE IF EXISTS `metro_db`;

-- adding fresh
CREATE DATABASE IF NOT EXISTS `metro_db`;
USE `metro_db`;

CREATE TABLE IF NOT EXISTS `routes` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `route_id` varchar(128) NOT NULL UNIQUE,
  `route_name` varchar(32) NOT NULL,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO `routes`(`route_id`, `route_name`) VALUES
("c1696b0f-6650-4d75-8fc3-124d79be8828", "Red Line"),
("ba8c085d-d4b7-46ba-9645-c358c4151e66", "Yellow Line");

CREATE TABLE IF NOT EXISTS `stations` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `station_id` varchar(128) NOT NULL UNIQUE,
  `station_name` varchar(64) NOT NULL,
  `route_id` varchar(128) NOT NULL,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_stat_rt_id` FOREIGN KEY (`route_id`) REFERENCES `routes` (`route_id`)
);

INSERT INTO `stations`(`station_id`, `station_name`, `route_id`) VALUES
('96e4c838-240b-446b-a758-a9e7f3890b34', 'South Extenstion', 'c1696b0f-6650-4d75-8fc3-124d79be8828'),
('7d59b1d6-6803-482f-8e0f-55ad07f743e5', 'Gokulpuri', 'c1696b0f-6650-4d75-8fc3-124d79be8828'),
('01eba78e-7a6e-457a-a50f-295164749f0e', 'Dilshad Garden', 'ba8c085d-d4b7-46ba-9645-c358c4151e66');

CREATE TABLE IF NOT EXISTS `bookings` (
	`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`booking_id` char(36) NOT NULL UNIQUE,
	`medium_id` char(36) NOT NULL,
	`medium` char(1) NOT NULL,
	`stat_start` char(36) DEFAULT NULL,
	`stat_end` char(36) DEFAULT NULL,
	`fare` float DEFAULT NULL,
	`is_started` int NOT NULL DEFAULT '1',
	`is_complete` int NOT NULL DEFAULT '0',
	`is_currupt` int NOT NULL DEFAULT '0',
	`datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT `fk_bk_stat_id_1` FOREIGN KEY (`stat_start`) REFERENCES `stations` (`station_id`),
	CONSTRAINT `fk_bk_stat_id_2` FOREIGN KEY (`stat_end`) REFERENCES `stations` (`station_id`)
);

CREATE TABLE IF NOT EXISTS `fare_stations` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `from_station` char(36) NOT NULL,
  `to_station` char(36) NOT NULL,
  `amt` float,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP
);

-- setting up "fare_stations" table
insert into fare_stations (from_station, to_station) select a.station_id as from_station, b.station_id as to_station from stations as a cross join stations as b;
	
update fare_stations set amt = ROUND((RAND() * (100-10))+15);
update fare_stations set amt = 10 where from_station = to_station;

CREATE TABLE IF NOT EXISTS `station_close_status` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `station_id` char(36) NOT NULL,
  `status` int(1) NOT NULL DEFAULT 1,
  `reason` varchar(128) NULL,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_scs_stat_id` FOREIGN KEY (`station_id`) REFERENCES `stations` (`station_id`)
);

INSERT INTO `station_close_status`(`station_id`) SELECT `station_id` FROM `stations`;

CREATE TABLE IF NOT EXISTS `cards` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `card_id` varchar(128) NOT NULL,
  `bal` float NOT NULL DEFAULT '100',
  `last_book` char(36) DEFAULT NULL,
  `is_active` int(1) NOT NULL DEFAULT '1',
  `in_station` int(1) NOT NULL DEFAULT '0',
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `tokens` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `token_id` char(36) NOT NULL UNIQUE,
  `is_active` int NOT NULL DEFAULT 1,
  `in_station` int NOT NULL DEFAULT 0,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `trans_id` char(36) NOT NULL UNIQUE,
  `mode` varchar(16) NOT NULL,
  `upi_id` varchar(36) DEFAULT NULL,
  `card_no` varchar(4) DEFAULT NULL,
  `card_exp` varchar(64) DEFAULT NULL,
  `amount` float NOT NULL,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(64) NOT NULL,
  `email` varchar(256) NOT NULL,
  `password` varchar(128) NOT NULL,
  `role` int(1) NOT NULL,
  `is_active` int(1) NOT NULL DEFAULT 1,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO `users`(`name`, `email`, `password`, `role`, `is_active`) VALUES('admin', 'admin@mtms.com', 'admin', 0, 1);

-- due to some unknown error while inserting through the
-- python mysql connector, the last INSERT command is
-- not executing so creaeting and dropping the FOO table
-- helps in it. 
CREATE TABLE IF NOT EXISTS foo(
	id int NULL
);
DROP TABLE IF EXISTS foo;
