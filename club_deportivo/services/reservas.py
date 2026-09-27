from datetime import datetime, timezone, timedelta

from ..repositories.reservas import (
    obtener_todas,
    contar_reservas,
    obtener_por_id,
    obtener_socio,
    obtener_cancha,
    existe_superposicion_cancha,
    existe_superposicion_socio,
    crear_reserva,
    actualizar_estado
)


GMT_MENOS_3 = timezone(timedelta(hours=-3))


def listar_reservas(filtros):
    reservas = obtener_todas(filtros)
    total = contar_reservas(filtros)

    return {
        "reservas": reservas,
        "total": total
    }


def buscar_reserva(id):
    return obtener_por_id(id)


def crear_reserva_service(datos):

    socio = obtener_socio(
        datos["id_socio"]
    )

    if socio is None:
        raise LookupError(
            "El socio no existe"
        )

    if not socio["activo"]:
        raise ValueError(
            "El socio está inactivo"
        )

    cancha = obtener_cancha(
        datos["id_cancha"]
    )

    if cancha is None:
        raise LookupError(
            "La cancha no existe"
        )

    if not cancha["activa"]:
        raise ValueError(
            "La cancha está inactiva"
        )

    inicio = datos["fecha_hora_inicio"].replace(
        tzinfo=None
    )

    fin = datos["fecha_hora_fin"].replace(
        tzinfo=None
    )

    if existe_superposicion_cancha(
        datos["id_cancha"],
        inicio,
        fin
    ):
        raise ValueError(
            "La cancha ya tiene una reserva superpuesta"
        )

    if existe_superposicion_socio(
        datos["id_socio"],
        inicio,
        fin
    ):
        raise ValueError(
            "El socio ya tiene una reserva superpuesta"
        )

    horas = (
        fin - inicio
    ).total_seconds() / 3600

    precio_hora = cancha["precio_hora"]
    precio_total = int(
        horas * precio_hora
    )

    datos["precio_hora"] = precio_hora
    datos["precio_total"] = precio_total

    return crear_reserva(datos)


def actualizar_estado_service(id, nuevo_estado):

    reserva = buscar_reserva(id)

    if reserva is None:
        raise LookupError(
            "La reserva no existe"
        )

    estado_actual = reserva["estado"]

    # Repetir el estado actual es válido.
    if estado_actual == nuevo_estado:
        return reserva

    ahora = datetime.now(GMT_MENOS_3).replace(
        tzinfo=None
    )

    inicio = reserva["fecha_hora_inicio"]
    fin = reserva["fecha_hora_fin"]

    if estado_actual != "confirmada":
        raise ValueError(
            "La transición de estado no está permitida"
        )

    if nuevo_estado == "cancelada":

        if ahora >= inicio:
            raise ValueError(
                "No se puede cancelar una reserva cuyo inicio ya llegó"
            )

        actualizar_estado(
            id,
            "cancelada"
        )

    elif nuevo_estado == "finalizada":

        if ahora < fin:
            raise ValueError(
                "No se puede finalizar una reserva antes de su horario de fin"
            )

        actualizar_estado(
            id,
            "finalizada"
        )

    else:
        raise ValueError(
            "La transición de estado no está permitida"
        )

    return buscar_reserva(id)
