"""A program to put formatted CSV files on AWS
"""

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

# 2. Create the Connection String to the SERVER (No DB name yet)
DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URI)

    print("Loading CSV files...")
    data_files = {
        'City': 'cities.csv',
        'OlympicGames': 'OlympicGames.csv',
        'Event': 'Event.csv',
        'Athlete': 'Athlete.csv',
        'CitizenOf': 'CitizenOf.csv',
        'Country': 'Country.csv',
        'Result': 'Result.csv'
    }

    for table_name, file_name in data_files.items():
        try:
            df = pd.read_csv(file_name)
            # Pass the ENGINE, not the connection, for auto-commit
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            print(f" -> Success: {table_name}")
        except FileNotFoundError:
            print(f" -> Error: File {file_name} not found.")
            
    print("\nAll operations complete.")

except OperationalError as e:
    print("\nCONNECTION ERROR: Could not connect to AWS.")
    print("1. Check your Security Group (Allow Port 3306 from your IP).")
    print("2. Check your username/password.")
    print(f"Details: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
