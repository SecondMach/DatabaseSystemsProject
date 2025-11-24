"""A program to put formatted CSV files on AWS
"""

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Define the Database Name you WANT to use
CHOSEN_DB_NAME = "olympics_data" 

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

# 2. Create the Connection String to the SERVER (No DB name yet)
SERVER_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"

try:
    # --- STEP 1: Create the Database if it doesn't exist ---
    print("Connecting to SQL Server to check for database...")
    server_engine = create_engine(SERVER_URI)
    
    # We use a temporary connection to create the DB
    with server_engine.connect() as conn:
        # 'commit' is needed because CREATE DATABASE cannot run inside a transaction block in some drivers
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {CHOSEN_DB_NAME}"))
        print(f"Database '{CHOSEN_DB_NAME}' is ready.")

    # Dispose of the server engine
    server_engine.dispose()

    # --- STEP 2: Connect to the specific Database ---
    DATABASE_URI = f"{SERVER_URI}/{CHOSEN_DB_NAME}"
    engine = create_engine(DATABASE_URI)

    print("Loading CSV files...")
    # Load CSVs (Assuming files are in the same directory)
    data_files = {
        'OlympicGames': 'OlympicGames.csv',
        'YearHosted': 'YearHosted.csv',
        'Sport': 'Sport.csv',
        'DisciplineOf': 'DisciplineOf.csv',
        'Athlete': 'Athlete.csv',
        'Country': 'Country.csv',
        'EventPlayedIn': 'EventPlayedIn.csv',
        'AthleteParticipated': 'AthleteParticipated.csv',
        'Result': 'Result.csv',
        'CitizenOf': 'CitizenOf.csv'
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
    