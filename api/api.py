from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Connection to postgreSQL
def connect_db():
    try:
        #Ajustar las siguientes lineas después de las pruebas
        conn = psycopg2.connect(
            dbname="globant_challenge",
            user="postgres",
            password="andres123",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Connection error: {e}")
        return None

# Route to check if the server is working
@app.route('/', methods=['GET'])
def home():
    return "Flask server is working"

# Function to insert data in the postgreSQL
def insert_data(df, table_name):
    conn = connect_db()
    if conn:
        #Remove the following line after the testing
        print("Connected!")
        cursor = conn.cursor()
        for _, row in df.iterrows():
            query = sql.SQL("INSERT INTO {} VALUES (%s, %s)").format(sql.Identifier(table_name))
            cursor.execute(query, tuple(row))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    return False

# Route to upload the csv using POST
@app.route('/upload_csv', methods=['POST'])
def upload_csv():

    if 'file' not in request.files:
        return jsonify({"error": "There is no file in the field file"}), 400

    file = request.files['file']
    
    if file.filename == '':
            return jsonify({"error": "The file's name is empty"}), 400

    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    try:

        df = pd.read_csv(file)

        # Check if the file contains 2 columns
        if df.shape[1] != 2:
            return jsonify({"error": "The csv file should contain exactly 2 columns"}), 400

        # Insert data into the postgres table
        if insert_data(df, 'test_departments'):
            return jsonify({"message": "Data inserted correctly"}), 201
        else:
            return jsonify({"error": "Failed to insert data"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)