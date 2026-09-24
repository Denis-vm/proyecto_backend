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
        raise

# 
def ejecutar_consulta(sql, parametros=None, modificar=False):
    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(sql, parametros or ())

        if modificar:
            conexion.commit()
            return cursor.lastrowid

        return cursor.fetchall()

    except Error as error:
        conexion.rollback()
        print(f"Error al ejecutar consulta: {error}")
        raise

    finally:
        cursor.close()
        conexion.close()