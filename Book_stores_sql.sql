-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema book_store
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema book_store
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `book_store` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `book_store` ;

-- -----------------------------------------------------
-- Table `book_store`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `book_store`.`books` (
  `isbn` CHAR(10) NOT NULL,
  `author` VARCHAR(100) NOT NULL,
  `title` VARCHAR(128) NOT NULL,
  `price` FLOAT NOT NULL,
  `subject` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`isbn`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `book_store`.`members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `book_store`.`members` (
  `fname` VARCHAR(20) NOT NULL,
  `lname` VARCHAR(20) NOT NULL,
  `address` VARCHAR(50) NOT NULL,
  `city` VARCHAR(30) NOT NULL,
  `state` VARCHAR(20) NOT NULL,
  `zip` INT NOT NULL,
  `phone` VARCHAR(12) NULL DEFAULT NULL,
  `email` VARCHAR(40) NOT NULL,
  `userid` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(20) NULL DEFAULT NULL,
  `credidcardtype` VARCHAR(10) NULL DEFAULT NULL,
  `creditcardnumber` VARCHAR(16) NULL DEFAULT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `book_store`.`cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `book_store`.`cart` (
  `userid` INT NOT NULL,
  `isbn` CHAR(10) NOT NULL,
  `qty` INT NOT NULL,
  PRIMARY KEY (`userid`, `isbn`),
  INDEX `fk_cart_members1_idx` (`userid` ASC) VISIBLE,
  INDEX `fk_cart_books1` (`isbn` ASC) VISIBLE,
  CONSTRAINT `fk_cart_books1`
    FOREIGN KEY (`isbn`)
    REFERENCES `book_store`.`books` (`isbn`),
  CONSTRAINT `fk_cart_members1`
    FOREIGN KEY (`userid`)
    REFERENCES `book_store`.`members` (`userid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `book_store`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `book_store`.`orders` (
  `userid` INT NOT NULL,
  `ono` INT NOT NULL AUTO_INCREMENT,
  `recieved` DATE NOT NULL,
  `shipped` DATE NULL DEFAULT NULL,
  `shipAddress` VARCHAR(50) NULL DEFAULT NULL,
  `shipCity` VARCHAR(30) NULL DEFAULT NULL,
  `shipState` VARCHAR(20) NULL DEFAULT NULL,
  `shipZip` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ono`),
  INDEX `userid_idx` (`userid` ASC) VISIBLE,
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `book_store`.`members` (`userid`))
ENGINE = InnoDB
AUTO_INCREMENT = 47
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `book_store`.`orderdetails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `book_store`.`orderdetails` (
  `ono` INT NOT NULL,
  `isbn` CHAR(10) NOT NULL,
  `qty` INT NOT NULL,
  `price` FLOAT NOT NULL,
  PRIMARY KEY (`ono`, `isbn`),
  INDEX `fk_orderdetails_orders1_idx` (`ono` ASC) VISIBLE,
  INDEX `fk_orderdetails_books1_idx` (`isbn` ASC) VISIBLE,
  CONSTRAINT `fk_orderdetails_books1`
    FOREIGN KEY (`isbn`)
    REFERENCES `book_store`.`books` (`isbn`),
  CONSTRAINT `fk_orderdetails_orders1`
    FOREIGN KEY (`ono`)
    REFERENCES `book_store`.`orders` (`ono`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
