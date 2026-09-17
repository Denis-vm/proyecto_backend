import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


# Carga las variables definidas en el archivo .env
load_dotenv()


def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        return conexion

    except Error as error:
        print(f"Error al conectar con MySQL: {error}")
        return None