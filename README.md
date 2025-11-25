# Olympic Database for CSC4710 - Database Systems
## About data
Taken from https://github.com/KeithGalli/Olympics-Dataset/tree/master/clean-data
and
https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

Input data has not been uploaded to GitHub in this project

## New Schema

City(*hostCity, hostCountry)

OlympicGame(*year, season, hostCity)

Event(*event_name, gender, discipline)

Athlete(*athlete_id, name, DOB, countryBorn)

CitizenOf(*athleteID, *ISOCode)

Country(*ISOCode, fullName)

AthleteParticipation(*athlete_id, *year, *event_name, nationRepresented, placement)

## Methodology
Each of these relations were created with `pandas` and saved as CSVs in `format.py`

These CSVs were then uploaded to AWS in `populate.py` as SQL Tables

As the tables did not have primary keys, 