# Proyecto Backend - Club Deportivo

Sistema de gestión backend para el **Club Deportivo**, desarrollado en Python con Flask y MySQL 8 containerizado mediante Docker.

## 👥 Integrantes del Equipo

- **Matias Soletta** - Padrón: `116388`
- **Denis Vasquez** - Padrón: `116220`
- **[Nombre del Integrante]** - Padrón: `[Número]`

## 📌 Versiones Utilizadas

El proyecto fue desarrollado y probado con las siguientes versiones del entorno:

- **Python:** `3.10+`
- **MySQL:** `8.0` (vía imagen oficial de Docker `mysql:8.0`)
- **Docker Engine:** `20.10+`
- **Docker Compose:** `2.0+`
- **Flask:** `3.x`
- **mysql-connector-python:** `26.7.0` (conector nativo para MySQL)
- **python-dotenv:** `1.0.1` (gestión de variables de entorno)

## 🧠 Supuestos Adoptados

Para el diseño e implementación de este proyecto se tomaron las siguientes decisiones y supuestos técnicos:

1. **Gestión de Credenciales (`.env`):** Por buenas prácticas de seguridad, el archivo `.env` que contiene las credenciales de conexión está excluido del control de versiones (`.gitignore`). Debe ser creado manualmente en la raíz del proyecto antes de iniciar la aplicación.
2. **Inicialización automática de la Base de Datos:** Se asume el uso de Docker para el despliegue del entorno de desarrollo. La base de datos `club_deportivo` es creada automáticamente por la variable `MYSQL_DATABASE` de Docker. Por esta razón, el script `init_db.sql` se enfoca únicamente en posicionarse sobre la base (`USE club_deportivo;`) e instanciar las tablas y datos iniciales.
3. **Consultas SQL Explícitas sin ORM:** No se utiliza ningún ORM. Todas las sentencias SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) están escritas de forma explícita y parametrizada usando `mysql-connector-python` para prevenir vulnerabilidades de SQL Injection.
4. **Persistencia y Reset:** Los datos de la base de datos persisten en un volumen de Docker (`mysql_data`). Si se requiere reiniciar el estado inicial de la base de datos a partir del script `init_db.sql`, es necesario destruir el volumen mediante `docker-compose down -v`.
5. **Formato de Respuestas de la API:** Todos los endpoints responden en formato JSON e incluyen los códigos de estado HTTP estándar (`200`, `201`, `400`, `404`, `500`).

## ⚙️ Configuración del Entorno (`.env`)

Crea un archivo llamado `.env` en la raíz del proyecto para definir las credenciales que utilizará la aplicación para conectarse al contenedor de MySQL.

Contenido requerido para `.env`:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=club_deportivo
DB_USER=root
DB_PASSWORD=root
```

## 🚀 Pasos de Instalación y Ejecución

Sigue estos pasos en orden para levantar la aplicación desde un repositorio recién clonado:

### 1. Clonar el repositorio
```bash
git clone https://github.com/Denis-vm/proyecto_backend.git
cd proyecto_backend
```

### 2. Crear el archivo de configuración `.env`
Crea el archivo `.env` en la raíz del proyecto e ingresa las credenciales de la base de datos:

```bash
nano .env
```
*(o abre el archivo con tu editor de texto preferido y pega la configuración indicada arriba).*

### 3. Levantar la base de datos con Docker
Ejecuta el siguiente comando para levantar el contenedor de MySQL en segundo plano e inicializar el esquema y datos iniciales:

```bash
docker-compose up -d
```

Verifica que el contenedor esté corriendo y escuchando en el puerto `3306`:
```bash
docker ps
```

### 4. Crear e instalar el entorno virtual de Python
```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual (Linux / macOS)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 5. Iniciar la API Flask
```bash
python main.py
```

La aplicación estará escuchando solicitudes en `http://localhost:5000`.

## 📬 Ejemplos de Solicitudes

A continuación se detallan ejemplos de cómo consultar la API mediante comandos `curl`:

### 1. Obtener lista de deportes
- **Método:** `GET`
- **Endpoint:** `/deportes`

```bash
curl -X GET http://localhost:5000/deportes
```

**Respuesta esperada (`200 OK`):**
```json
[
  {
    "id": 1,
    "nombre": "Fútbol"
  },
  {
    "id": 2,
    "nombre": "Tenis"
  },
  {
    "id": 3,
    "nombre": "Pádel"
  }
]
```

### 2. Registrar un nuevo deporte
- **Método:** `POST`
- **Endpoint:** `/deportes`
- **Header:** `Content-Type: application/json`

```bash
curl -X POST http://localhost:5000/deportes \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Básquet"}'
```

**Respuesta esperada (`201 Created`):**
```json
{
  "id": 4,
  "nombre": "Básquet"
}
```

## 🛢️ Reinicio de la Base de Datos

Si realizas modificaciones en `init_db.sql` y deseas reiniciar la base de datos a su estado inicial:

```bash
# Detener contenedores y eliminar el volumen de datos guardados
docker-compose down -v

# Volver a levantar el contenedor e inicializar datos
docker-compose up -d
```