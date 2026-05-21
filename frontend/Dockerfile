# Usamos una versión oficial y ligera de Python
FROM python:3.9-slim

# Creamos una carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos SOLO el requirements.txt primero (es una buena práctica)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de nuestro código (app.py, index.html, logo, etc.)
COPY . .

# Abrimos el puerto 5000
EXPOSE 5000

# Le decimos qué comando ejecutar al encender
CMD ["python", "app.py"]