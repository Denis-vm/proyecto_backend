from db.connection import ejecutar_consulta

# Obtener todos los deportes
def obtener_todos():
    sql = """
        SELECT id, nombre
        FROM deportes
        ORDER BY id ASC
    """

    return ejecutar_consulta(sql)