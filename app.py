from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

import os

app = Flask(__name__)
CORS(app)

# Configuración de MongoDB adaptada para funcionar dentro de Docker
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# Seleccionamos la base de datos "walle_db" y la colección "bitacora"
db = client["walle_db"]
coleccion = db["bitacora"]

@app.route('/bitacora', methods=['POST'])
def registrar_evento():
    try:
        # Atrapamos el texto que manda la app de la tablet
        texto_recibido = request.get_data(as_text=True)
        
        # Limpiamos el texto para quitar la palabra "evento="
        accion = texto_recibido.replace("evento=", "").strip()
        
        if not accion:
            return jsonify({"error": "Datos vacíos"}), 400

        # Creamos el registro con la fecha y hora exacta del servidor
        registro = {
            "accion": accion,
            "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Guardamos el registro permanentemente en MongoDB
        coleccion.insert_one(registro)

        # Imprimimos en la consola del servidor para tener un control visual
        print(f" [GUARDADO EN DB] Acción: {accion} | Hora: {registro['fecha_hora']}")
        
        return jsonify({"mensaje": "Guardado exitosamente"}), 200

    except Exception as e:
        print(f"Error al guardar: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
   # <-- NUEVA RUTA PARA EL FRONTEND -->
@app.route('/api/logs', methods=['GET'])
def obtener_logs():
    try:
        # Usamos la variable "coleccion" que definiste arriba
        logs = list(coleccion.find({}, {"_id": 0}).sort("_id", -1).limit(50))
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # El 0.0.0.0 permite que acepte tráfico desde el internet exterior
    app.run(host='0.0.0.0', port=5000)

