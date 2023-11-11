CREATE DATABASE IF NOT EXISTS flask2;
USE flask2;

DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `fname` varchar(45) NOT NULL,
  `lname` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `manager_id` int DEFAULT '0',
  `job_title` varchar(45) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `fname` varchar(45) NOT NULL,
  `lname` varchar(45) NOT NULL,
  `employee_id` int UNSIGNED NOT NULL,
  `phone` varchar(45) NOT NULL,
  `city` varchar(45) DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  `language` varchar(45) DEFAULT NULL,
  `lead_generated_at` date NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_employee_id_idx` (`employee_id`),
  CONSTRAINT `fk_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `service`;
CREATE TABLE `service` (
    `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `price` FLOAT NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
    `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `customer_id` int UNSIGNED NOT NULL,
    `service_id` int UNSIGNED NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
     KEY `fk_customer_id_idx` (`customer_id`),
     KEY `fk_service_id_idx` (`service_id`),
  CONSTRAINT `fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`),
  CONSTRAINT `fk_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;