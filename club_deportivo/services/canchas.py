from ..repositories.canchas import (obtener_todas, obtener_por_id, 
contar_canchas, existe_deporte, crear_cancha, actualizar_cancha, 
tiene_reservas, eliminar_cancha, obtener_disponibles, contar_disponibles)

def listar_canchas(filtros):

    canchas = obtener_todas(filtros)
    total = contar_canchas(filtros)
    return {
        "canchas": canchas,
        "total": total
    }

def listar_canchas_disponibles(filtros):
    canchas = obtener_disponibles(
        filtros["fecha"],
        filtros["hora_inicio"],
        filtros["hora_fin"],
        filtros
    )

    total = contar_disponibles(
        filtros["fecha"],
        filtros["hora_inicio"],
        filtros["hora_fin"],
        filtros
    )

    return {
        "canchas": canchas,
        "total": total
    }

def buscar_cancha(id):
    return obtener_por_id(id)

def crear_canchas(datos):
    if not existe_deporte(datos["id_deporte"]):
        raise LookupError("El deporte no existe")
    return crear_cancha(datos)

def actualizar_cancha_service(id, datos):

    if buscar_cancha(id) is None:
        raise LookupError("La cancha no existe")

    actualizar_cancha(id, datos)

def eliminar_cancha_service(id):

    if buscar_cancha(id) is None:
        raise LookupError("La cancha no existe")

    if tiene_reservas(id):
        raise ValueError("La cancha tiene reservas")

    eliminar_cancha(id)


