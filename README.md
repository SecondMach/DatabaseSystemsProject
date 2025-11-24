# Olympic Database for CSC4710 - Database Systems
## About data
Taken from https://github.com/KeithGalli/Olympics-Dataset/tree/master/clean-data

Data has not been uploaded to GitHub in this project

## New Schema

OlympicGame(__year__, season, hostCity)
YearHosted(__year__, hostCity) **[NEW]**
City(__hostCity__, hostCountry) **[NEW]**

Sport(__year__, event, gender)
DisciplineOf(__event__, discipline) **[NEW]**

Athlete(__athlete_id__, name, DOB, countryBorn, nationPlayedFor)
Country(__ISOCode__, fullName)

EventPlayedIn(__year__, __hostCity__, __event__)
AthleteParticipated(__year__, __event__, __athleteID__)
Result(__athleteID__, __year__, __event__, placement)
CitizenOf(__athleteID__, __ISOCode__)