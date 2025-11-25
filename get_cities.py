import pandas as pd
df = pd.read_csv('athlete_events.csv')
cities = df[['City']].drop_duplicates()
cities.to_csv('cities.csv', index=False)