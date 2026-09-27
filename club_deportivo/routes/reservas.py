from flask import Blueprint, jsonify, request
from mysql.connector import Error
from urllib.parse import urlencode

from ..services.reservas import (
    listar_reservas,
    buscar_reserva,
    crear_reserva_service,
    actualizar_estado_service
)

from ..validators.reservas import (
    validar_filtros_reservas,
    validar_creacion_reserva,
    validar_estado
)


reservas_bp = Blueprint(
    "reservas",
    __name__
)


def construir_enlaces_reservas(filtros, total):

    limite = filtros["limite"]
    offset = filtros["offset"]

    ultimo_offset = (
        ((total - 1) // limite) * limite
        if total > 0
        else 0
    )

    def crear_url(nuevo_offset):

        parametros = {
            "_limit": limite,
            "_offset": nuevo_offset
        }

        if filtros["id_cancha"] is not None:
            parametros["id_cancha"] = filtros["id_cancha"]

        if filtros["id_socio"] is not None:
            parametros["id_socio"] = filtros["id_socio"]

        if filtros["estado"] is not None:
            parametros["estado"] = filtros["estado"]

        if filtros["fecha_desde"] is not None:
            parametros["fecha_desde"] = filtros["fecha_desde"]

        if filtros["fecha_hasta"] is not None:
            parametros["fecha_hasta"] = filtros["fecha_hasta"]

        return f"{request.base_url}?{urlencode(parametros)}"

    return {
        "_first": {
            "href": crear_url(0)
        },
        "_prev": {
            "href": crear_url(
                max(0, offset - limite)
            )
        } if offset > 0 else None,
        "_next": {
            "href": crear_url(
                offset + limite
            )
        } if offset + limite < total else None,
        "_last": {
            "href": crear_url(
                ultimo_offset
            )
        }
    }


def serializar_reserva(reserva):

    if reserva is None:
        return None

    resultado = dict(reserva)

    if resultado["fecha_hora_inicio"] is not None:
        resultado["fecha_hora_inicio"] = (
            resultado["fecha_hora_inicio"]
            .strftime("%Y-%m-%dT%H:%M:%S.000000-03:00")
        )

    if resultado["fecha_hora_fin"] is not None:
        resultado["fecha_hora_fin"] = (
            resultado["fecha_hora_fin"]
            .strftime("%Y-%m-%dT%H:%M:%S.000000-03:00")
        )

    return resultado


@reservas_bp.route("/reservas", methods=["GET"])
def obtener_reservas():

    try:
        filtros = validar_filtros_reservas(
            request.args
        )
    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "ERROR_VALIDACION",
                "message": "Los parámetros de la solicitud son inválidos",
                "level": "error",
                "description": e.args[0]["error"]
            }]
        }), 400

    try:
        resultado = listar_reservas(filtros)
    except Error:
        return jsonify({
            "errors": [{
                "code": "ERROR_BASE_DATOS",
                "message": "Error interno",
                "level": "error",
                "description": "Ocurrió un error al acceder a la base de datos"
            }]
        }), 500

    reservas = [
        serializar_reserva(reserva)
        for reserva in resultado["reservas"]
    ]

    return jsonify({
        "reservas": reservas,
        "_links": construir_enlaces_reservas(
            filtros,
            resultado["total"]
        )
    }), 200


@reservas_bp.route("/reservas/<int:id>", methods=["GET"])
def obtener_reserva(id):

    try:
        reserva = buscar_reserva(id)
    except Error:
        return jsonify({
            "errors": [{
                "code": "ERROR_BASE_DATOS",
                "message": "Error interno",
                "level": "error",
                "description": "Ocurrió un error al acceder a la base de datos"
            }]
        }), 500

    if reserva is None:
        return jsonify({
            "errors": [{
                "code": "RESERVA_NO_EXISTE",
                "message": "La reserva no existe",
                "level": "error",
                "description": "No se encontró una reserva con el identificador indicado"
            }]
        }), 404

    return jsonify(
        serializar_reserva(reserva)
    ), 200


@reservas_bp.route("/reservas", methods=["POST"])
def registrar_reserva():

    try:
        datos = validar_creacion_reserva(
            request.get_json()
        )
    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "ERROR_VALIDACION",
                "message": "El cuerpo de la solicitud es inválido",
                "level": "error",
                "description": e.args[0]["error"]
            }]
        }), 400

    try:
        id_reserva = crear_reserva_service(
            datos
        )
    except LookupError as e:

        codigo = (
            "SOCIO_NO_EXISTE"
            if "socio" in str(e)
            else "CANCHA_NO_EXISTE"
        )

        return jsonify({
            "errors": [{
                "code": codigo,
                "message": str(e),
                "level": "error",
                "description": str(e)
            }]
        }), 404

    except ValueError as e:

        mensaje = str(e)

        if "superpuesta" in mensaje:
            codigo = "RESERVA_SUPERPUESTA"
        elif "inactivo" in mensaje:
            codigo = "ENTIDAD_INACTIVA"
        else:
            codigo = "ERROR_VALIDACION"

        return jsonify({
            "errors": [{
                "code": codigo,
                "message": mensaje,
                "level": "error",
                "description": mensaje
            }]
        }), 409

    except Error:
        return jsonify({
            "errors": [{
                "code": "ERROR_BASE_DATOS",
                "message": "Error interno",
                "level": "error",
                "description": "Ocurrió un error al acceder a la base de datos"
            }]
        }), 500

    reserva = buscar_reserva(id_reserva)

    return jsonify(
        serializar_reserva(reserva)
    ), 201


@reservas_bp.route(
    "/reservas/<int:id>/estado",
    methods=["PUT"]
)
def cambiar_estado_reserva(id):

    try:
        estado = validar_estado(
            request.get_json()
        )
    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "ERROR_VALIDACION",
                "message": "El cuerpo de la solicitud es inválido",
                "level": "error",
                "description": e.args[0]["error"]
            }]
        }), 400

    try:
        reserva = actualizar_estado_service(
            id,
            estado
        )
    except LookupError:
        return jsonify({
            "errors": [{
                "code": "RESERVA_NO_EXISTE",
                "message": "La reserva no existe",
                "level": "error",
                "description": "No se encontró una reserva con el identificador indicado"
            }]
        }), 404

    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "TRANSICION_NO_PERMITIDA",
                "message": str(e),
                "level": "error",
                "description": str(e)
            }]
        }), 409

    except Error:
        return jsonify({
            "errors": [{
                "code": "ERROR_BASE_DATOS",
                "message": "Error interno",
                "level": "error",
                "description": "Ocurrió un error al acceder a la base de datos"
            }]
        }), 500

    return jsonify(
        serializar_reserva(reserva)
    ), 200
