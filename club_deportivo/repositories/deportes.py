from db.connection import obtener_conexion

""" Obtener todos los deportes """
def obtener_todos():
    conexion = obtener_conexion()

    if conexion is None:
        return None

    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, nombre
            FROM deportes
            ORDER BY id ASC
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()