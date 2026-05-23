from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
import time  # <-- CAMBIO ADICIONAL SECCIÓN B: Importación para cálculo de métricas de tiempo

# Inicializamos el contador de tiempo en el que se enciende el servidor
HORA_INICIO = time.time()

app = Flask(__name__)
CORS(app)

# <-- CAMBIO REALIZADO POR: Javier V., Kabt´zin V., Kevin, Wendy T. (Sección B) -->
@app.before_request
def auditar_peticion_grupo():
    # Registra en la consola del servidor de forma sutil quién consulta la API
    origen = request.headers.get('User-Agent', 'Desconocido')
    print(f" [AUDITORÍA SEC-B] Ruta: {request.path} | Método: {request.method} | Agente: {origen[:40]}")

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
        # Usamos la variable "coleccion" que se definió arriba
        logs = list(coleccion.find({}, {"_id": 0}).sort("_id", -1).limit(50))
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# <-- CAMBIO ADICIONAL POR: Javier V., Kabt´zin V., Kevin, Wendy T. (Sección B) -->
# Endpoint de Diagnóstico y Métricas del Sistema sin alterar la Base de Datos
@app.route('/api/health', methods=['GET'])
def verificar_salud_sistema():
    try:
        # Calculamos dinámicamente cuántos segundos lleva operando la app
        uptime_segundos = int(time.time() - HORA_INICIO)
        return jsonify({
            "estado": "OPERACIONAL",
            "modulo": "WALL-E Backend Core",
            "version_api": "1.2.0-SecB",
            "tiempo_activo_segundos": uptime_segundos,
            "grupo_desarrollo": "Seccion B (Javier Vela, Kabt'zin Velasco, Kevin, Wendy Tomas)"
        }), 200
    except Exception as e:
        return jsonify({"estado": "ERROR", "error": str(e)}), 500

if __name__ == '__main__':
    # El 0.0.0.0 permite que acepte tráfico desde el internet exterior
    app.run(host='0.0.0.0', port=5000)
