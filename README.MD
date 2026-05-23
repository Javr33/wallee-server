

![Arquitectura de Microservicios](https://img.shields.io/badge/Arquitectura-Microservicios-blue)
![Docker](https://img.shields.io/badge/Despliegue-Docker-2496ED?logo=docker&logoColor=white)
![DigitalOcean](https://img.shields.io/badge/Hosting-DigitalOcean-0080FF?logo=digitalocean&logoColor=white)
![Python Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask&logoColor=white)

> **Universidad:** Universidad Mariano Gálvez de Guatemala (UMG)  
> **Curso:** Sistemas Operativos 2  
> **Sección:** B  
> **Desarrolladores:** Javier Vela, Kabt´zin Velasco, Kevin Gabriel, Wendy Tomas  

---


## 📖 Descripción del Proyecto
Este repositorio contiene la arquitectura completa (Backend, Frontend y Base de Datos) para el sistema de telemetría y control del robot explorador **Wall-E**. El diseño se fundamenta en los principios de Sistemas Operativos Distribuidos, utilizando contenedores para aislar procesos, asegurar la persistencia de datos y garantizar una alta disponibilidad.

El núcleo operativo se basa en un enfoque de **Comunicación Dual**, donde la aplicación cliente no solo maniobra el hardware físico en tiempo real, sino que reporta la actividad de manera asíncrona hacia un servidor centralizado.

---

## 🏗️ Arquitectura de Microservicios
El sistema está construido y orquestado 100% mediante `docker-compose`, separando lógicamente cada capa de la aplicación:

| Servicio | Tecnología | Puerto Interno/Externo | Rol en el Sistema |
| :--- | :--- | :--- | :--- |
| **Frontend Web** | Nginx (Alpine) | `80:80` | Servidor web ultraligero que despacha el Dashboard de monitoreo en tiempo real. |
| **Backend Core** | Python (Flask) | `5000:5000` | Motor lógico del sistema. Procesa solicitudes REST, formatea datos y maneja excepciones severas. |
| **Base de Datos** | MongoDB | `27017:27017` | Motor NoSQL con persistencia mediante volúmenes Docker. Almacena las bitácoras. |

---

## ☁️ Infraestructura en la Nube (VPS)
- **Proveedor:** DigitalOcean
- **Sistema Operativo:** Ubuntu Server 22.04 LTS
- **IP Pública:** `159.223.152.192`
- **Orquestador:** Docker & Docker Compose v2

---



## 🌐 Endpoints de la API (Backend)
El backend procesa y audita el tráfico bajo el puerto `5000`.

### 1. Registro de Eventos
- **Ruta:** `POST /bitacora`
- **Descripción:** Recibe el comando desde la tablet, limpia la cadena de texto, adjunta una estampa de tiempo (`America/Guatemala`) y lo persiste en la base de datos.
- **Respuesta Exitosa:** `200 OK` `{"mensaje": "Guardado exitosamente"}`

### 2. Consulta de Bitácora
- **Ruta:** `GET /api/logs`
- **Descripción:** Utilizado por el Dashboard (Nginx) para consultar en tiempo real (vía *Fetch API*) los últimos 50 eventos ordenados de forma descendente.

### 3. Diagnóstico del Sistema
- **Ruta:** `GET /api/health`
- **Descripción:** Endpoint de salud que verifica el estado operativo del servicio sin saturar la Base de Datos. Retorna el *Uptime* (tiempo activo en segundos) y los metadatos del módulo.

---

## 🚀 Instrucciones de Despliegue

### Requisitos Previos
1. Entorno Linux con Docker y `docker-compose` instalados.
2. Git instalado para control de versiones.

### Pasos para iniciar el Servidor
1. Clonar el repositorio y entrar al directorio principal:
   ```bash
   cd wallee-server
2. Construir las imágenes y levantar el entorno en segundo plano:
   ```bash
   docker compose up -d --build
3. Comprobar que los 3 contenedores (walle_frontend, walle_backend, mongodb_walle) están arriba 
    ```bash
    docker compose ps
4. Consultar los logs en tiempo real (auditoría):
    ```bash
    docker compose logs -f backend
   docker compose stop backend
   ```
   Resultado: Imposibilidad de registro temporal. La aplicación móvil reporta Error 1103, el visualizador web queda congelado, pero la infraestructura física sigue en pie.
