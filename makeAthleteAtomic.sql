-- Get first and last names to check
SELECT
    Name,
    -- Extract First Name (the part before the first space)
    SUBSTRING_INDEX(Name, ' ', 1) AS FirstName,
    -- Extract Last Name (the part after the last space)
    SUBSTRING_INDEX(Name, ' ', -1) AS LastName
FROM
    Athlete;

-- Create New Columns
ALTER TABLE Athlete
ADD COLUMN FirstName VARCHAR(100),
ADD COLUMN LastName VARCHAR(100);

UPDATE Athlete
SET
	FirstName = SUBSTRING_INDEX(Name, ' ', 1),
	LastName = SUBSTRING_INDEX(Name, ' ', -1);

Select FirstName, LastName FROM Athlete;

ALTER TABLE Athlete
DROP COLUMN Name;
