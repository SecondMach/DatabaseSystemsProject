
SELECT
    (SELECT MAX(LENGTH(Event)) FROM Result) AS MaxEventLength,
    (SELECT MAX(LENGTH(noc)) FROM Result) AS MaxNOCLength,
	(SELECT MAX(LENGTH(Season)) FROM OlympicGames) AS MaxSeason,
	(SELECT MAX(LENGTH(City)) FROM OlympicGames) AS MaxCity,
	(SELECT MAX(LENGTH(Gender)) FROM Event) AS MaxGender,
	(SELECT MAX(LENGTH(FullName)) FROM Country) AS MaxFullName,
	(SELECT MAX(LENGTH(Born_date)) FROM Athlete) AS MaxBornDate,
	(SELECT MAX(LENGTH(Born_country)) FROM Athlete) AS MaxBornCountry;