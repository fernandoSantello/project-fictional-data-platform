CREATE DATABASE currency_data;

USE currency_data;

CREATE TABLE currency (
	id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    symbol CHAR(5) NULL,
    currencySymbol CHAR(10) NULL,
    type VARCHAR(10) NOT NULL,
    createdAt VARCHAR(50) NOT NULL,
    
    PRIMARY KEY(id)
);

CREATE TABLE rate (
	id INT NOT NULL AUTO_INCREMENT,
    id_currency INT NOT NULL,
    rateUSD float NULL,
    timestamp VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (id),
    FOREIGN KEY (id_currency) REFERENCES currency(id)
		ON UPDATE CASCADE
        ON DELETE NO ACTION
);

CREATE TABLE process_fail (
	id INT NOT NULL AUTO_INCREMENT,
    id_currency INT NOT NULL,
    error VARCHAR(50) NOT NULL,
    timestamp VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (id),
    FOREIGN KEY (id_currency) REFERENCES currency(id)
		ON UPDATE CASCADE
        ON DELETE NO ACTION
);