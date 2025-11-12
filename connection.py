from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER= os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    # Create a database engine
    engine = create_engine(DATABASE_URI)

    # Establish a connection using a 'with' block for automatic cleanup
    with engine.connect() as connection:
        print("✅ Connection to the MySQL database was successful!")

        # Execute a simple test query
        query = text("SELECT version();")
        result = connection.execute(query)

        # Fetch and print the result
        db_version = result.scalar()
        print(f"Database version: {db_version}")

except OperationalError as e:
    print(f"❌ Could not connect to the database. Please check your configuration.")
    print(f"Error details: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")