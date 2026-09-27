from db.connection import ejecutar_consulta


def obtener_todos(filtros):
    sql = """
        SELECT
            id,
            nombre,
            email,
            activo
        FROM socios
        WHERE (%s IS NULL OR LOWER(nombre) LIKE LOWER(%s))
          AND (%s IS NULL OR activo = %s)
        ORDER BY id ASC
        LIMIT %s OFFSET %s
    """

    parametros = (
        filtros["nombre"],
        f'%{filtros["nombre"]}%' if filtros["nombre"] else None,
        filtros["activo"],
        filtros["activo"],
        filtros["limite"],
        filtros["offset"]
    )

    return ejecutar_consulta(sql, parametros)


def contar_socios(filtros):
    sql = """
        SELECT COUNT(*) AS total
        FROM socios
        WHERE (%s IS NULL OR LOWER(nombre) LIKE LOWER(%s))
          AND (%s IS NULL OR activo = %s)
    """

    parametros = (
        filtros["nombre"],
        f'%{filtros["nombre"]}%' if filtros["nombre"] else None,
        filtros["activo"],
        filtros["activo"]
    )

    resultado = ejecutar_consulta(sql, parametros)

    return resultado[0]["total"]


def obtener_por_id(id):
    sql = """
        SELECT
            id,
            nombre,
            email,
            activo
        FROM socios
        WHERE id = %s
    """

    filas = ejecutar_consulta(sql, (id,))

    return filas[0] if filas else None


def existe_email(email, id_excluir=None):
    sql = """
        SELECT id
        FROM socios
        WHERE LOWER(email) = LOWER(%s)
    """

    parametros = [email]

    if id_excluir is not None:
        sql += " AND id <> %s"
        parametros.append(id_excluir)

    filas = ejecutar_consulta(sql, tuple(parametros))

    return bool(filas)


def crear_socio(datos):
    sql = """
        INSERT INTO socios (
            nombre,
            email,
            activo
        )
        VALUES (%s, %s, TRUE)
    """

    parametros = (
        datos["nombre"],
        datos["email"]
    )

    return ejecutar_consulta(
        sql,
        parametros,
        modificar=True
    )


def actualizar_socio(id, datos):
    campos = []
    parametros = []

    for campo, valor in datos.items():
        campos.append(f"{campo} = %s")
        parametros.append(valor)

    parametros.append(id)

    sql = f"""
        UPDATE socios
        SET {", ".join(campos)}
        WHERE id = %s
    """

    ejecutar_consulta(
        sql,
        tuple(parametros),
        modificar=True
    )
