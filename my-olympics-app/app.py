from flask import Flask, render_template, jsonify, request, redirect, url_for
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# REPLACE THESE WITH YOUR AWS/AZURE DETAILS
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

# --- PAGE ROUTES ---
# These serve your specific HTML files
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/games.html')
def games():
    return render_template('games.html')

@app.route('/athlete.html')
def athletes_page():
    return render_template('athlete.html')

@app.route('/analytics.html')
def analytics():
    return render_template('analytics.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

# --- API ROUTES (The "Brain") ---

# 1. Get Athletes (For the table in athlete.html)
@app.route('/api/athletes', methods=['GET'])
def get_athletes():
    try:
        with engine.connect() as conn:
            # Matches the columns in your HTML table
            query = text("SELECT Born_date, Born_country, FirstName, LastName FROM Athlete LIMIT 100")
            result = conn.execute(query)
            # Convert database rows to a list of dictionaries (JSON)
            athletes = [
                {"born_date": row[0], "born_country": row[1], "first_name": row[2], "last_name": row[3]}
                for row in result
            ]
        return jsonify(athletes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. Add Athlete (For the form in athlete.html)
@app.route('/api/athletes', methods=['POST'])
def add_athlete():
    data = request.json
    try:
        with engine.connect() as conn:
            # Note that Athlete_ID is auto-incremented
            query = text("""
                INSERT INTO Athlete (Born_date, Born_country, FirstName, LastName)
                VALUES (:Born_date, :Born_country, :FirstName, :LastName)
            """)
            conn.execute(query, data)
            conn.commit()
        return jsonify({"message": "Athlete added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Get Chart Data (For analytics.html)
@app.route('/api/analytics')
def get_analytics():
    # Example: Top 5 countries by total medals (You can adjust this query!)
    with engine.connect() as conn:
        query = text("SELECT country, SUM(medals) as total FROM Athlete GROUP BY country ORDER BY total DESC LIMIT 5")
        result = conn.execute(query)
        data = [{"label": row[0], "value": row[1]} for row in result]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)