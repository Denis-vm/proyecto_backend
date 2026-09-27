from db.connection import ejecutar_consulta


def obtener_todas(filtros):
    sql = """
        SELECT
            id,
            id_socio,
            id_cancha,
            fecha_hora_inicio,
            fecha_hora_fin,
            estado,
            precio_hora,
            precio_total
        FROM reservas
        WHERE (%s IS NULL OR id_cancha = %s)
          AND (%s IS NULL OR id_socio = %s)
          AND (%s IS NULL OR estado = %s)
          AND (%s IS NULL OR DATE(fecha_hora_inicio) >= %s)
          AND (%s IS NULL OR DATE(fecha_hora_inicio) <= %s)
        ORDER BY id ASC
        LIMIT %s OFFSET %s
    """

    parametros = (
        filtros["id_cancha"],
        filtros["id_cancha"],
        filtros["id_socio"],
        filtros["id_socio"],
        filtros["estado"],
        filtros["estado"],
        filtros["fecha_desde"],
        filtros["fecha_desde"],
        filtros["fecha_hasta"],
        filtros["fecha_hasta"],
        filtros["limite"],
        filtros["offset"]
    )

    return ejecutar_consulta(sql, parametros)


def contar_reservas(filtros):
    sql = """
        SELECT COUNT(*) AS total
        FROM reservas
        WHERE (%s IS NULL OR id_cancha = %s)
          AND (%s IS NULL OR id_socio = %s)
          AND (%s IS NULL OR estado = %s)
          AND (%s IS NULL OR DATE(fecha_hora_inicio) >= %s)
          AND (%s IS NULL OR DATE(fecha_hora_inicio) <= %s)
    """

    parametros = (
        filtros["id_cancha"],
        filtros["id_cancha"],
        filtros["id_socio"],
        filtros["id_socio"],
        filtros["estado"],
        filtros["estado"],
        filtros["fecha_desde"],
        filtros["fecha_desde"],
        filtros["fecha_hasta"],
        filtros["fecha_hasta"]
    )

    resultado = ejecutar_consulta(sql, parametros)

    return resultado[0]["total"]


def obtener_por_id(id):
    sql = """
        SELECT
            id,
            id_socio,
            id_cancha,
            fecha_hora_inicio,
            fecha_hora_fin,
            estado,
            precio_hora,
            precio_total
        FROM reservas
        WHERE id = %s
    """

    filas = ejecutar_consulta(sql, (id,))

    return filas[0] if filas else None


def obtener_socio(id):
    sql = """
        SELECT id, activo
        FROM socios
        WHERE id = %s
    """

    filas = ejecutar_consulta(sql, (id,))

    return filas[0] if filas else None


def obtener_cancha(id):
    sql = """
        SELECT id, precio_hora, activa
        FROM canchas
        WHERE id = %s
    """

    filas = ejecutar_consulta(sql, (id,))

    return filas[0] if filas else None


def existe_superposicion_cancha(
    id_cancha,
    inicio,
    fin
):
    sql = """
        SELECT id
        FROM reservas
        WHERE id_cancha = %s
          AND estado = 'confirmada'
          AND fecha_hora_inicio < %s
          AND fecha_hora_fin > %s
        LIMIT 1
    """

    filas = ejecutar_consulta(
        sql,
        (
            id_cancha,
            fin,
            inicio
        )
    )

    return bool(filas)


def existe_superposicion_socio(
    id_socio,
    inicio,
    fin
):
    sql = """
        SELECT id
        FROM reservas
        WHERE id_socio = %s
          AND estado = 'confirmada'
          AND fecha_hora_inicio < %s
          AND fecha_hora_fin > %s
        LIMIT 1
    """

    filas = ejecutar_consulta(
        sql,
        (
            id_socio,
            fin,
            inicio
        )
    )

    return bool(filas)


def crear_reserva(datos):
    sql = """
        INSERT INTO reservas (
            id_socio,
            id_cancha,
            fecha_hora_inicio,
            fecha_hora_fin,
            estado,
            precio_hora,
            precio_total
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            'confirmada',
            %s,
            %s
        )
    """

    parametros = (
        datos["id_socio"],
        datos["id_cancha"],
        datos["fecha_hora_inicio"].replace(tzinfo=None),
        datos["fecha_hora_fin"].replace(tzinfo=None),
        datos["precio_hora"],
        datos["precio_total"]
    )

    return ejecutar_consulta(
        sql,
        parametros,
        modificar=True
    )


def actualizar_estado(id, estado):
    sql = """
        UPDATE reservas
        SET estado = %s
        WHERE id = %s
    """

    ejecutar_consulta(
        sql,
        (estado, id),
        modificar=True
    )
