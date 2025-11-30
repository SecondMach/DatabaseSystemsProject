ALTER TABLE Athlete
MODIFY COLUMN Athlete_id INT NOT NULL AUTO_INCREMENT;


ALTER TABLE CitizenOf
MODIFY COLUMN Athlete_ID INT NOT NULL;

ALTER TABLE CitizenOf 
ADD CONSTRAINT FK_CitizenOf_Athlete -- Constraint Name
FOREIGN KEY (Athlete_ID)            -- Column in the CitizenOf table
REFERENCES Athlete (Athlete_id);    -- Table and column it references

ALTER TABLE City
MODIFY COLUMN NOC VARCHAR(4) NOT NULL;

ALTER TABLE Country
MODIFY COLUMN NOC VARCHAR(4) NOT NULL;

-- Does not initially run. City has NOCs that Country doesn't have
-- SOLUTION: Find NOCs Country doesn't have and add them
ALTER TABLE City 
ADD CONSTRAINT FK_City_NOC
FOREIGN KEY (NOC)
REFERENCES Country (NOC);

-- Get NOCs Country doesn't have via left join, answers:
-- NLD
-- GRC
-- DEU
-- CHE
SELECT DISTINCT T1.NOC
FROM City AS T1
LEFT JOIN Country AS T2 ON T1.NOC = T2.NOC
WHERE T2.NOC IS NULL;

-- Insert into Country so FK reference can be made
INSERT INTO Country (NOC, FullName) VALUES ('NLD', 'Netherlands');
INSERT INTO Country (NOC, FullName) VALUES ('GRC', 'Greece');
INSERT INTO Country (NOC, FullName) VALUES ('DEU', 'Germany');
INSERT INTO Country (NOC, FullName) VALUES ('CHE', 'Switzerland');

ALTER TABLE Result
MODIFY COLUMN Athlete_id INT NOT NULL;

ALTER TABLE Result 
ADD CONSTRAINT FK_Result_Athlete_ID
FOREIGN KEY (Athlete_ID)
REFERENCES Athlete (Athlete_id);


-- Gets a NULL VALUE error initially
ALTER TABLE Result
MODIFY COLUMN NOC VARCHAR(4) NOT NULL;


-- Only one result is given, we'll research this and update. (Slalom 2022)
SELECT * FROM Result WHERE NOC IS NULL;

-- Result is Canada (NOC is CAN)
UPDATE Result
SET NOC = 'CAN' WHERE Athlete_id = 148986;


ALTER TABLE Result 
ADD CONSTRAINT FK_Result_NOC
FOREIGN KEY (NOC)
REFERENCES Country (NOC);

-- Get NOCs Country doesn't have via left join, answers:
-- LBN
-- SGP
-- ROC
-- EOR
-- COR
SELECT DISTINCT T1.NOC
FROM Result AS T1
LEFT JOIN Country AS T2 ON T1.NOC = T2.NOC
WHERE T2.NOC IS NULL;

INSERT INTO Country (NOC, FullName) VALUES ('LBN', 'Lebanon');
INSERT INTO Country (NOC, FullName) VALUES ('SGP', 'Singapore');

-- ROC: Russian Olympic Committee (used when Russia competes under a neutral flag)
INSERT INTO Country (NOC, FullName) VALUES ('ROC', 'Russian Olympic Committee');

-- EOR: Refugee Olympic Team (used for athletes competing under the Olympic flag)
INSERT INTO Country (NOC, FullName) VALUES ('EOR', 'Refugee Olympic Team');

-- COR: Corocoro (a common placeholder or lesser-known code, often requiring context; using 'Corocoro' as a generic place name)
-- Note: 'COR' is not a standard ISO 3166 code. In Olympic history, it was sometimes used for the Democratic Republic of Congo (formerly COK) or as a non-standard entry.
INSERT INTO Country (NOC, FullName) VALUES ('COR', 'Corocoro (Non-Standard)');


SELECT * FROM Result WHERE Place IS NULL;

ALTER TABLE OlympicGames  
ADD CONSTRAINT FK_OlympicGames_City
FOREIGN KEY (City)
REFERENCES City (City);

CREATE INDEX idx_City_Name 
ON City (City);
