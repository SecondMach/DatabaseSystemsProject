"""A program to:
- Load our CSVs containing our data into pandas DataFrames
- Convert them to 3NF, and save the results as parquet files
"""

__author__ = "Debra Ritter"

import re
import pandas as pd

# Not in 3NF
bios_df: pd.DataFrame = pd.read_csv("clean-data/bios_locs.csv")

# Not in 1NF
results_df: pd.DataFrame = pd.read_csv("clean-data/results.csv")
athlete_events_df: pd.DataFrame = pd.read_csv("athlete_events.csv")
noc_regions_df: pd.DataFrame = pd.read_csv("clean-data/noc_regions.csv")

def get_gender(event: str) -> str:
    """Gets the gender from an event
    Args:
        event::str
            An unformatted string which is the name of the event
            
    Returns:
        gender::str
            A single character string representing the gender of the event
    """
    if "Men" in event:
        return 'M'
    if "Women" in event:
        return 'F'
    return 'X'

def format_event(event: str) -> str:
    """Removes non gender andl non-alphabetical characters from event string
    including spaces, apostrophes, etc

    Args:
        event::str
            An unformatted string which is the name of the event

    Returns:
        formatted_event::str
            A formatted event string
    """
    if 'Men\'s' in event:
        event = event.replace('Men\'s', '')
    elif 'Women\'s' in event:
        event = event.replace('Women\'s', '')
    elif 'Men' in event:
        event = event.replace('Men', '')
    elif 'Women' in event:
        event = event.replace('Women', '')

    formatted_event = re.sub(r'[^a-zA-Z0-9]', '', event)

    return formatted_event


# Note that our relational database needs to be reformatted to have everything
# fit in at least 3NF.
OlympicGames = athlete_events_df[['Year', 'Season', 'City']].drop_duplicates()
OlympicGames.to_csv('OlympicGames.csv', index=False)

Event = athlete_events_df[['Year', 'Event']].drop_duplicates()
Event['Gender'] = Event['Event'].apply(get_gender)
Event['Event'] = Event['Event'].apply(format_event)
Event.to_csv('Event.csv', index=False)

Athlete = bios_df[['athlete_id', 'name', 'born_date', 'born_country',]]

renamed_athlete_cols = {col: col.capitalize() for col in Athlete.columns}
Athlete.rename(columns=renamed_athlete_cols, inplace=True)
Athlete.to_csv('Athlete.csv', index=False)

CitizenOf = bios_df[['athlete_id', 'NOC']].drop_duplicates()
CitizenOf.rename(columns={
    'athlete_id': 'Athlete_ID'
}, inplace=True)
CitizenOf.to_csv('CitizenOf.csv', index=False)

Country = noc_regions_df[['NOC', 'region']].drop_duplicates()

Country.rename(columns={
    'region': 'FullName'
}, inplace=True)

Country.to_csv('Country.csv', index=False)

# EventPlayedIn = athlete_events_df[['Year', 'City', 'Event']].drop_duplicates()
# EventPlayedIn['Event'] = EventPlayedIn['Event'].apply(format_event)
# EventPlayedIn.to_csv('EventPlayedIn.csv', index=False)

# AthleteParticipated = results_df[['athlete_id', 'event', 'year']].drop_duplicates()
# AthleteParticipated.rename(columns={
#     'athlete_id': 'Athlete_ID',
#     'event': 'Event',
#     'year': 'Year'
# }, inplace=True)
# AthleteParticipated['Event'] = AthleteParticipated['Event'].apply(format_event)
# AthleteParticipated.to_csv('AthleteParticipated.csv', index=False)

Result = results_df[['athlete_id', 'event', 'year', 'place', 'noc']].drop_duplicates()
Result.rename(columns={
    'athlete_id': 'Athlete_ID',
    'event': 'Event',
    'year': 'Year',
    'place': 'Place'
}, inplace=True)
Result['Event'] = Result['Event'].apply(format_event)
Result.to_csv('Result.csv', index=False)
