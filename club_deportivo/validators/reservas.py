from datetime import datetime, timezone, timedelta


GMT_MENOS_3 = timezone(timedelta(hours=-3))

FORMATO_FECHA_HORA = "%Y-%m-%dT%H:%M:%S.%f-03:00"


def validar_paginacion(limite, offset):
    if limite < 1 or limite > 100:
        raise ValueError({
            "error": "El parámetro _limit debe estar entre 1 y 100"
        })

    if offset < 0:
        raise ValueError({
            "error": "El parámetro _offset debe ser mayor o igual a 0"
        })


def validar_id(valor, nombre):
    try:
        valor = int(valor)
    except (ValueError, TypeError):
        raise ValueError({
            "error": f"El parámetro {nombre} debe ser un entero"
        })

    if valor <= 0:
        raise ValueError({
            "error": f"El parámetro {nombre} debe ser mayor a 0"
        })

    return valor


def validar_fecha_hora(valor, nombre):
    if not isinstance(valor, str):
        raise ValueError({
            "error": f"{nombre} debe ser un texto"
        })

    try:
        fecha_hora = datetime.strptime(
            valor,
            FORMATO_FECHA_HORA
        )
    except ValueError:
        raise ValueError({
            "error": (
                f"{nombre} debe tener formato "
                "YYYY-MM-DDTHH:MM:SS.ffffff-03:00"
            )
        })

    return fecha_hora.replace(tzinfo=GMT_MENOS_3)


def validar_intervalo(fecha_hora_inicio, fecha_hora_fin):
    if fecha_hora_inicio >= fecha_hora_fin:
        raise ValueError({
            "error": "fecha_hora_fin debe ser posterior a fecha_hora_inicio"
        })

    if fecha_hora_inicio.date() != fecha_hora_fin.date():
        raise ValueError({
            "error": "La reserva no puede atravesar la medianoche"
        })

    if fecha_hora_inicio.hour < 8:
        raise ValueError({
            "error": "La reserva debe comenzar a partir de las 08:00"
        })

    if fecha_hora_fin.hour > 23 or (
        fecha_hora_fin.hour == 23
        and (
            fecha_hora_fin.minute > 0
            or fecha_hora_fin.second > 0
            or fecha_hora_fin.microsecond > 0
        )
    ):
        raise ValueError({
            "error": "La reserva debe finalizar como máximo a las 23:00"
        })

    if fecha_hora_inicio.minute != 0 or fecha_hora_inicio.second != 0:
        raise ValueError({
            "error": "La hora de inicio debe ser una hora exacta"
        })

    if fecha_hora_fin.minute != 0 or fecha_hora_fin.second != 0:
        raise ValueError({
            "error": "La hora de fin debe ser una hora exacta"
        })

    horas = (
        fecha_hora_fin - fecha_hora_inicio
    ).total_seconds() / 3600

    if horas < 1 or horas > 3:
        raise ValueError({
            "error": "La duración debe ser de entre 1 y 3 horas"
        })


def validar_filtros_reservas(args):
    permitidos = {
        "_limit",
        "_offset",
        "id_cancha",
        "id_socio",
        "estado",
        "fecha_desde",
        "fecha_hasta"
    }

    for parametro in args:
        if parametro not in permitidos:
            raise ValueError({
                "error": f"El parámetro {parametro} no está permitido"
            })

    try:
        limite = int(args.get("_limit", "10"))
        offset = int(args.get("_offset", "0"))
    except ValueError:
        raise ValueError({
            "error": "_limit y _offset deben ser enteros"
        })

    validar_paginacion(limite, offset)

    id_cancha = args.get("id_cancha")
    if id_cancha is not None:
        id_cancha = validar_id(id_cancha, "id_cancha")

    id_socio = args.get("id_socio")
    if id_socio is not None:
        id_socio = validar_id(id_socio, "id_socio")

    estado = args.get("estado")

    if estado is not None and estado not in {
        "confirmada",
        "cancelada",
        "finalizada"
    }:
        raise ValueError({
            "error": "El estado no es válido"
        })

    fecha_desde = args.get("fecha_desde")
    fecha_hasta = args.get("fecha_hasta")

    if fecha_desde:
        try:
            datetime.strptime(fecha_desde, "%Y-%m-%d")
        except ValueError:
            raise ValueError({
                "error": "fecha_desde debe tener formato YYYY-MM-DD"
            })

    if fecha_hasta:
        try:
            datetime.strptime(fecha_hasta, "%Y-%m-%d")
        except ValueError:
            raise ValueError({
                "error": "fecha_hasta debe tener formato YYYY-MM-DD"
            })

    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        raise ValueError({
            "error": "fecha_desde debe ser menor o igual a fecha_hasta"
        })

    return {
        "limite": limite,
        "offset": offset,
        "id_cancha": id_cancha,
        "id_socio": id_socio,
        "estado": estado,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    }


def validar_creacion_reserva(data):
    if not isinstance(data, dict):
        raise ValueError({
            "error": "El cuerpo debe ser un objeto JSON"
        })

    if not data:
        raise ValueError({
            "error": "El cuerpo no puede estar vacío"
        })

    campos_permitidos = {
        "id_socio",
        "id_cancha",
        "fecha_hora_inicio",
        "fecha_hora_fin"
    }

    if set(data.keys()) - campos_permitidos:
        raise ValueError({
            "error": "Se recibieron campos desconocidos"
        })

    for campo in campos_permitidos:
        if campo not in data:
            raise ValueError({
                "error": f"El campo {campo} es obligatorio"
            })

    id_socio = validar_id(
        data["id_socio"],
        "id_socio"
    )

    id_cancha = validar_id(
        data["id_cancha"],
        "id_cancha"
    )

    inicio = validar_fecha_hora(
        data["fecha_hora_inicio"],
        "fecha_hora_inicio"
    )

    fin = validar_fecha_hora(
        data["fecha_hora_fin"],
        "fecha_hora_fin"
    )

    ahora = datetime.now(GMT_MENOS_3)

    if inicio <= ahora:
        raise ValueError({
            "error": "La reserva debe comenzar en el futuro"
        })

    validar_intervalo(inicio, fin)

    return {
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin
    }


def validar_estado(data):
    if not isinstance(data, dict):
        raise ValueError({
            "error": "El cuerpo debe ser un objeto JSON"
        })

    if not data:
        raise ValueError({
            "error": "El cuerpo no puede estar vacío"
        })

    if set(data.keys()) != {"estado"}:
        raise ValueError({
            "error": "El cuerpo solo debe contener el campo estado"
        })

    if data["estado"] not in {
        "confirmada",
        "cancelada",
        "finalizada"
    }:
        raise ValueError({
            "error": "El estado no es válido"
        })

    return data["estado"]
