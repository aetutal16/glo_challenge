from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Conexión a PostgreSQL
def connect_db():
    try:
    
        #Ajustar las siguientes líneas luego de las pruebas
        conn = psycopg2.connect(
            dbname="globant_challenge",
            user="postgres",
            password="passwordupdated",
            host="localhost",
            port="5432"
        )
        
        return conn
    except Exception as e:
    
        print(f"Error de conexión: {e}")
        return None

# Función para insertar los datos en la tabla de PostgreSQL
def insert_data(df, table_name):

    conn = connect_db()
    
    if conn:
    
        #Eliminar la siguiente línea después de las pruebas
        print("Conectado!")
        cursor = conn.cursor()
        for _, row in df.iterrows():
        
            query = sql.SQL("INSERT INTO {} VALUES (%s, %s)").format(sql.Identifier(table_name))
            cursor.execute(query, tuple(row))
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    return False

# Ruta para subir el archivo CSV
@app.route('/upload_csv', methods=['POST'])
def upload_csv():

    file = request.files['file']
    
    if file.filename == '':
            return jsonify({"error": "El nombre del archivo está vacío"}), 400

    if not file:
        return jsonify({"error": "No se subió ningún archivo"}), 400
    
    try:
        # Leer el CSV con pandas
        #Ajustar el siguiente código porque se está leyendo la primera línea como encabezado
        df = pd.read_csv(file)

        # Insertar datos en la tabla de PostgreSQL
        if insert_data(df, 'test_department'):
            return jsonify({"message": "Datos insertados correctamente"}), 201
        else:
            return jsonify({"error": "Fallo al insertar datos"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)