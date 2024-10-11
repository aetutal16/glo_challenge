from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
import hashlib

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Check that the env variables are right
# print(os.getenv("DB_NAME"))

# Connection toPostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

# Function to calculate the hash for the file
def calculate_file_hash(file):
    print("Working 2!!------------------")
    file.seek(0) # Ensure we are at the start of the file
    file_content = file.read()
    file.seek(0) # Ensure we are at the start of the file
    return hashlib.sha256(file_content).hexdigest()

# Function to check if the file was already updated using the hash
def is_file_already_uploaded(file_hash):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT 1 FROM file_uploads WHERE file_hash = %s"
        cursor.execute(query, (file_hash,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    return False

# Function to save the hash into the file_uploads table
def log_file_upload(file_name, file_hash):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO file_uploads (file_name, file_hash) VALUES (%s, %s)"
        cursor.execute(query, (file_name, file_hash))
        conn.commit()
        cursor.close()
        conn.close()

# Function to insert the data into the postgres table
def insert_data(df, table_name, num_columns):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        placeholders = ', '.join(['%s'] * num_columns)
        query = sql.SQL(f"INSERT INTO {{}} VALUES ({placeholders})").format(sql.Identifier(table_name))
        
        try:
            for _, row in df.iterrows():
                
                #With this line the error when try to insert null values in postgres is corrected
                row = row.replace({pd.NA: None, pd.NaT: None}).to_list()
                #---------------------------------------------

                cursor.execute(query, tuple(row))
            conn.commit()
        except Exception as e:
            print(f"Failed to insert data: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
        return True
    return False

# Route to check if the server is working
@app.route('/', methods=['GET'])
def home():
    return "Flask server is working"

# Route to upload the csv file
@app.route('/upload_csv/<table_name>', methods=['POST'])

def upload_csv(table_name):
    file = request.files.get('file')
    
    if not file:
        return jsonify({"error": "No file was uploaded"}), 400
    
    try:
        print("Working 2!!!!-------")
        file_hash = calculate_file_hash(file)
        
        if is_file_already_uploaded(file_hash):
            return jsonify({"error": "The file has already been uploaded before"}), 400
        
        df = pd.read_csv(file, header = None)
        
        # Check the number of columns according to the table
        if table_name == 'dim_departments':
            expected_columns = 2
        elif table_name == 'dim_jobs':
            expected_columns = 2
        elif table_name == 'fact_hired_employees':
            expected_columns = 5
        else:
            return jsonify({"error": "Invalid table"}), 400
        
        if df.shape[1] != expected_columns:
            return jsonify({"error": f"The csv file should have {expected_columns} columns"}), 400
        
        if insert_data(df, table_name, expected_columns):
            
            log_file_upload(file.filename, file_hash)
            return jsonify({"message": "Data inserted correctly!"}), 201
        
        else:
            return jsonify({"error": "Error inserting data"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    
    #app.run(debug=True)

    #This line was added because of docker
    app.run(debug = True, host='0.0.0.0', port=5000)