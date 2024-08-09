from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Configura la base de datos
def init_db():
    with sqlite3.connect('logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_hora TEXT,
                nombre_servicio TEXT,
                nivel_severidad TEXT,
                mensaje TEXT
            )
        ''')
        conn.commit()

# Cargar tokens desde un archivo de configuración
with open('config.json') as f:
    config = json.load(f)
VALID_TOKENS = set(config['tokens'])

# Endpoint para recibir logs
@app.route('/logs', methods=['POST'])
def recibir_logs():
    # Verifica el token en el encabezado de la solicitud
    token = request.headers.get('Authorization')
    if not token or token.split(' ')[1] not in VALID_TOKENS:
        return jsonify({"error": "Token de autenticacion invalido"}), 403
    
    if request.is_json:
        logs = request.get_json()
        fecha_hora = logs.get('fecha_hora')
        nombre_servicio = logs.get('nombre_servicio')
        nivel_severidad = logs.get('nivel_severidad')
        mensaje = logs.get('mensaje')

        # Almacena el logs en la base de datos
        with sqlite3.connect('logs.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (fecha_hora, nombre_servicio, nivel_severidad, mensaje)
                VALUES (?, ?, ?, ?)
            ''', (fecha_hora, nombre_servicio, nivel_severidad, mensaje))
            conn.commit()

        return jsonify({"mensaje": "logs recibido exitosamente"}), 200
    return jsonify({"error": "Formato de datos incorrecto"}), 400

# Endpoint para consultar logs
@app.route('/consulta_logs', methods=['GET'])
def consulta_logs():
    nivel_severidad = request.args.get('nivel_severidad')
    
    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if nivel_severidad:
        query += " AND nivel_severidad = ?"
        params.append(nivel_severidad)

    with sqlite3.connect('logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        logs = cursor.fetchall()

    resultado = [
        {
            "id": row[0],
            "fecha_hora": row[1],
            "nombre_servicio": row[2],
            "nivel_severidad": row[3],
            "mensaje": row[4]
        }
        for row in logs
    ]
    return jsonify(resultado), 200

if __name__ == '__main__':
    init_db()
    app.run(port=5000)