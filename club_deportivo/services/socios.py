from ..repositories.socios import (
    obtener_todos,
    contar_socios,
    obtener_por_id,
    existe_email,
    crear_socio,
    actualizar_socio
)


def listar_socios(filtros):
    socios = obtener_todos(filtros)
    total = contar_socios(filtros)

    return {
        "socios": socios,
        "total": total
    }


def buscar_socio(id):
    return obtener_por_id(id)


def crear_socio_service(datos):
    if existe_email(datos["email"]):
        raise ValueError("El email ya está registrado")

    return crear_socio(datos)


def actualizar_socio_service(id, datos):
    if buscar_socio(id) is None:
        raise LookupError("El socio no existe")

    if "email" in datos:
        if existe_email(datos["email"], id):
            raise ValueError("El email ya está registrado")

    actualizar_socio(id, datos)
