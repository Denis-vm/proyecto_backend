from db.connection import ejecutar_consulta

#   Retorna las canchas aplicando los filtros y la paginación
def obtener_todas(filtros):
    sql = """
        SELECT
            id,
            nombre,
            id_deporte,
            precio_hora,
            techada,
            activa
        FROM canchas
        WHERE (%s IS NULL OR id_deporte = %s)
          AND (%s IS NULL OR LOWER(nombre) LIKE LOWER(%s))
          AND (%s IS NULL OR techada = %s)
          AND (%s IS NULL OR activa = %s)
        ORDER BY id ASC
        LIMIT %s OFFSET %s
    """

    parametros = (
        filtros["id_deporte"],
        filtros["id_deporte"],

        filtros["nombre"],
        f'%{filtros["nombre"]}%' if filtros["nombre"] else None,

        filtros["techada"],
        filtros["techada"],

        filtros["activa"],
        filtros["activa"],

        filtros["limite"],
        filtros["offset"]
    )

    return ejecutar_consulta(sql, parametros)


# Cancha por id

def obtener_por_id(id):

    sql = """
        SELECT
            id,
            nombre,
            id_deporte,
            precio_hora,
            techada,
            activa
        FROM canchas
        WHERE id = %s
    """

    filas = ejecutar_consulta(sql, (id,))

    return filas[0] if filas else None

#Cuenta cuántas canchas cumplen con los filtros
def contar_canchas(filtros):
    sql = """
        SELECT COUNT(*) AS total
        FROM canchas
        WHERE (%s IS NULL OR id_deporte = %s)
          AND (%s IS NULL OR LOWER(nombre) LIKE LOWER(%s))
          AND (%s IS NULL OR techada = %s)
          AND (%s IS NULL OR activa = %s)
    """

    parametros = (
        filtros["id_deporte"],
        filtros["id_deporte"],

        filtros["nombre"],
        f'%{filtros["nombre"]}%' if filtros["nombre"] else None,

        filtros["techada"],
        filtros["techada"],

        filtros["activa"],
        filtros["activa"]
    )

    resultado = ejecutar_consulta(sql, parametros)

    return resultado[0]["total"]


# Verifica si existe un deporte por su ID
def existe_deporte(id_deporte):

    sql = """
        SELECT id
        FROM deportes
        WHERE id = %s
    """

    filas = ejecutar_consulta(sql, (id_deporte,))

    return bool(filas)


# Crea una nueva cancha
def crear_cancha(datos):

    sql = """
        INSERT INTO canchas (
            nombre,
            id_deporte,
            precio_hora,
            techada,
            activa
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    parametros = (
        datos["nombre"],
        datos["id_deporte"],
        datos["precio_hora"],
        datos["techada"],
        datos["activa"]
    )

    resultado = ejecutar_consulta(sql, parametros, modificar=True)

    return resultado


# ACTUAZLIZAR 
def actualizar_cancha(id, datos):

    campos = []
    parametros = []

    for campo, valor in datos.items():
        campos.append(f"{campo} = %s")
        parametros.append(valor)

    parametros.append(id)

    sql = f"""
        UPDATE canchas
        SET {", ".join(campos)}
        WHERE id = %s
    """

    ejecutar_consulta(sql, tuple(parametros), modificar=True)


#DELETE
def tiene_reservas(id):

    sql = """
        SELECT id
        FROM reservas
        WHERE id_cancha = %s
        LIMIT 1
    """

    filas = ejecutar_consulta(sql, (id,))

    return bool(filas)

def eliminar_cancha(id):

    sql = """
        DELETE FROM canchas
        WHERE id = %s
    """

    ejecutar_consulta(sql, (id,), modificar=True)


#GET CANCHAS DISPONIBLES
def obtener_disponibles(fecha, hora_inicio, hora_fin, filtros):

    sql = """
        SELECT
            c.id,
            c.nombre,
            c.id_deporte,
            c.precio_hora,
            c.techada,
            c.activa
        FROM canchas c
        WHERE c.activa = TRUE
          AND (%s IS NULL OR c.id_deporte = %s)
          AND (%s IS NULL OR c.techada = %s)
          AND NOT EXISTS (
              SELECT 1
              FROM reservas r
              WHERE r.id_cancha = c.id
                AND r.estado = 'confirmada'
                AND r.fecha_hora_inicio < %s
                AND r.fecha_hora_fin > %s
          )
        ORDER BY c.id ASC
        LIMIT %s OFFSET %s
    """

    parametros = (
        filtros["id_deporte"],
        filtros["id_deporte"],
        filtros["techada"],
        filtros["techada"],
        f"{fecha} {hora_fin}",
        f"{fecha} {hora_inicio}",
        filtros["limite"],
        filtros["offset"]
    )

    return ejecutar_consulta(sql, parametros)

def contar_disponibles(fecha, hora_inicio, hora_fin, filtros):

    sql = """
        SELECT COUNT(*) AS total
        FROM canchas c
        WHERE c.activa = TRUE
          AND (%s IS NULL OR c.id_deporte = %s)
          AND (%s IS NULL OR c.techada = %s)
          AND NOT EXISTS (
              SELECT 1
              FROM reservas r
              WHERE r.id_cancha = c.id
                AND r.estado = 'confirmada'
                AND r.fecha_hora_inicio < %s
                AND r.fecha_hora_fin > %s
          )
    """

    parametros = (
        filtros["id_deporte"],
        filtros["id_deporte"],
        filtros["techada"],
        filtros["techada"],
        f"{fecha} {hora_fin}",
        f"{fecha} {hora_inicio}"
    )

    resultado = ejecutar_consulta(sql, parametros)

    return resultado[0]["total"]