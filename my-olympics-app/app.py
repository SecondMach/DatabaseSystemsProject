from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask import Response, send_file
from sqlalchemy import create_engine, text
import os

import pandas as pd
import matplotlib.pyplot as plt
import io
import seaborn as sns

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

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

# Get Athletes (For the table in athlete.html)
@app.route('/api/athletes', methods=['GET'])
def get_athletes():
    try:
        with engine.connect() as conn:
            # Matches the columns in your HTML table
            query = text("SELECT Athlete_id,Born_date, Born_country, FirstName, LastName FROM Athlete LIMIT 20")
            result = conn.execute(query)
            # Convert database rows to a list of dictionaries (JSON)
            athletes = [
                {
                "id": row[0],
                 "born_date": row[1],
                 "born_country": row[2],
                 "first_name": row[3],
                 "last_name": row[4]}
                for row in result
            ]
        return jsonify(athletes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Update Athlete (For the form in athlete.html)
@app.route('/api/athletes/<int:athlete_id>', methods=['PUT'])
def update_athlete(athlete_id):
    data = request.json
    try:
        with engine.connect() as conn:
            query = text("""
                UPDATE Athlete 
                SET Born_date = :Born_date, 
                    Born_country = :Born_country, 
                    FirstName = :FirstName, 
                    LastName = :LastName
                WHERE Athlete_id = :athlete_id
            """)
            # Combine the data from JSON with the ID from the URL
            conn.execute(query, {**data, "athlete_id": athlete_id})
            conn.commit()
        return jsonify({"message": "Athlete updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete Athlete (For the form in athlete.html)
@app.route('/api/athletes/<int:athlete_id>', methods=['DELETE'])
def delete_athlete(athlete_id):
    try:
        with engine.connect() as conn:
            query = text("DELETE FROM Result WHERE Athlete_id = :athlete_id")
            conn.execute(query, {"athlete_id": athlete_id})
            query = text("DELETE FROM CitizenOf WHERE Athlete_id = :athlete_id")
            conn.execute(query, {"athlete_id": athlete_id})
            query = text("DELETE FROM Athlete WHERE Athlete_id = :athlete_id")
            conn.execute(query, {"athlete_id": athlete_id})
            conn.commit()
        return jsonify({"message": "Athlete deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add Athlete (For the form in athlete.html)
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

# --- SEARCH ATHLETES ---
@app.route('/api/search_athletes')
def search_athletes():
    raw_q = request.args.get("q", "").strip()

    # empty search → return nothing (or return all if you prefer)
    if raw_q == "":
        return jsonify([])
    
    # break full queries into pieces
    parts = raw_q.split()
    like_q = f"%{raw_q}%"

    try:
        with engine.connect() as conn:
            # if user enters "Usain Bolt", we detect 2 parts
            if len(parts) >= 2:
                first, last = parts[0], parts[1]
                query = text("""
                    SELECT Athlete_id, Born_date, Born_country, FirstName, LastName
                    FROM Athlete
                    WHERE 
                        (FirstName LIKE :first AND LastName LIKE :last)
                        OR CONCAT(FirstName, ' ', LastName) LIKE :full
                        OR Athlete_id LIKE :full
                        OR Born_country LIKE :full
                    LIMIT 100
                """)
                params = {
                    "first": f"%{first}%",
                    "last": f"%{last}%",
                    "full": like_q
                }

            else:  
                # single-word search
                query = text("""
                    SELECT Athlete_id, Born_date, Born_country, FirstName, LastName
                    FROM Athlete
                    WHERE 
                        FirstName LIKE :q
                        OR LastName LIKE :q
                        OR CONCAT(FirstName, ' ', LastName) LIKE :q
                        OR Athlete_id LIKE :q
                        OR Born_country LIKE :q
                    LIMIT 100
                """)
                params = {"q": like_q}

            rs = conn.execute(query, params)

            results = [
                {
                    "id": row[0],
                    "born_date": row[1],
                    "born_country": row[2],
                    "first_name": row[3],
                    "last_name": row[4],
                }
                for row in rs
            ]
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Table Data (For analytics.html)
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    # Example: Top 5 countries by total medals (You can adjust this query!)
    with engine.connect() as conn:
        query = text("""SELECT c.FullName AS Name, COUNT(r.Place) AS MedalCount
                        FROM Country c
                        JOIN Result r ON c.NOC = r.NOC
                        WHERE r.Place IN (1, 2, 3)
                        GROUP BY c.FullName
                        ORDER BY MedalCount DESC
                        LIMIT 5""")
        result = conn.execute(query)
        data = [{"Name": row[0], "Medal Count": row[1]} for row in result]
    return jsonify(data)

# Get Host City Advantage Data (For analytics.html)
@app.route('/api/host_advantage', methods=['GET'])
def host_advantage():
    try:
        with engine.connect() as conn:
            query = text("""
                WITH HostYears AS (
                    SELECT 
                        og.Year,
                        c.NOC AS HostNOC,
                        c.FullName AS HostCountry
                    FROM OlympicGames og
                    JOIN City ci ON og.City = ci.City
                    JOIN Country c ON ci.NOC = c.NOC
                )
                SELECT 
                    h.Year,
                    h.HostCountry,
                    COUNT(r.Athlete_id) AS HostMedals
                FROM HostYears h
                LEFT JOIN Result r 
                    ON r.Year = h.Year 
                    AND r.NOC = h.HostNOC 
                    AND r.Place IN (1, 2, 3)
                GROUP BY h.Year, h.HostCountry
                ORDER BY h.Year;
            """)

            result = conn.execute(query)

            data = [
                {
                    "Year": row[0],
                    "HostCountry": row[1],
                    "HostMedals": row[2]
                }
                for row in result
            ]

        if not data:
            return jsonify({"empty": True})

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analytics/chart.png')
def analytics_chart():
    try:
        with engine.connect() as conn:
            query = text("""SELECT c.FullName AS Name, COUNT(r.Place) AS MedalCount
                    FROM Country c
                    JOIN Result r ON c.NOC = r.NOC
                    WHERE r.Place IN (1, 2, 3)
                    GROUP BY c.FullName
                    ORDER BY MedalCount DESC
                    LIMIT 5""")
            
            df = pd.read_sql(query, conn)

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x="Name", y="MedalCount", data=df, palette="viridis")
        ax.set_title("Top 5 Countries by Total Medals")
        ax.set_xlabel("Country")
        ax.set_ylabel("Medal Count")
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')

    except Exception as e:
        print("Error generating chart:", e)
        return str(e), 500

# Host City Advantage Chart    
@app.route('/analytics/host_chart.png')
def host_advantage_chart():
    try:
        with engine.connect() as conn:
            query = text("""
                WITH HostYears AS (
                    SELECT 
                        og.Year,
                        c.NOC AS HostNOC,
                        c.FullName AS HostCountry
                    FROM OlympicGames og
                    JOIN City ci ON og.City = ci.City
                    JOIN Country c ON ci.NOC = c.NOC
                )
                SELECT 
                    h.Year,
                    h.HostCountry,
                    COUNT(r.Athlete_id) AS HostMedals
                FROM HostYears h
                LEFT JOIN Result r 
                    ON r.Year = h.Year 
                    AND r.NOC = h.HostNOC 
                    AND r.Place IN (1, 2, 3)
                GROUP BY h.Year, h.HostCountry
                ORDER BY h.Year;
            """)

            df = pd.read_sql(query, conn)

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x="Year", y="HostMedals", data=df, palette="crest")
        ax.set_title("Host City Advantage — Medals Won by Host Country")
        ax.set_xlabel("Olympic Year")
        ax.set_ylabel("Medals Won")
        plt.xticks(rotation=45)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')

    except Exception as e:
        print("Error generating host chart:", e)
        return str(e), 500

# Get Olympic Games (For games.html)
@app.route('/api/games', methods=['GET'])
def get_games():
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    og.Year,
                    og.Season,
                    og.City,
                    c2.FullName AS Country
                FROM OlympicGames og
                JOIN City c ON og.City = c.City
                JOIN Country c2 ON c.NOC = c2.NOC
                ORDER BY og.Year DESC
            """)
            result = conn.execute(query)

            games = [
                {
                    "year": row[0],
                    "season": row[1],
                    "city": row[2],
                    "country": row[3]
                }
                for row in result
            ]

        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Filter Olympic Games (For games.html)
@app.route('/api/games/filter', methods=['GET'])
def filter_games():
    season = request.args.get("season", None)
    year = request.args.get("year", None)

    try:
        conditions = []
        params = {}

        if season and season != "All Types":
            conditions.append("og.Season = :season")
            params["season"] = season

        if year and year != "All Years":
            conditions.append("og.Year = :year")
            params["year"] = year

        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        with engine.connect() as conn:
            query = text(f"""
                SELECT 
                    og.Year,
                    og.Season,
                    og.City,
                    c2.FullName AS Country
                FROM OlympicGames og
                JOIN City c ON og.City = c.City
                JOIN Country c2 ON c.NOC = c2.NOC
                {where_clause}
                ORDER BY og.Year DESC
            """)

            result = conn.execute(query, params)

            games = [
                {
                    "year": row[0],
                    "season": row[1],
                    "city": row[2],
                    "country": row[3]
                }
                for row in result
            ]

        return jsonify(games)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Login Route (For login.html)
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    # Hardcoded admin credentials
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['is_admin'] = True
    else:
        session['is_admin'] = False

    return redirect('/athlete.html')

@app.route('/api/whoami')
def whoami():
    return jsonify({
        "is_admin": session.get("is_admin", False)
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index.html')

if __name__ == '__main__':
    app.run(debug=True)
