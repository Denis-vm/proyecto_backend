from flask import Blueprint, jsonify, request
from mysql.connector import Error
from urllib.parse import urlencode

from ..services.socios import (
    listar_socios,
    buscar_socio,
    crear_socio_service,
    actualizar_socio_service
)

from ..validators.socios import (
    validar_filtros_socios,
    validar_creacion_socio,
    validar_actualizacion_socio
)


socios_bp = Blueprint(
    "socios",
    __name__
)


def construir_enlaces_socios(filtros, total):
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

        if filtros["nombre"] is not None:
            parametros["nombre"] = filtros["nombre"]

        if filtros["activo"] is not None:
            parametros["activo"] = str(
                filtros["activo"]
            ).lower()

        return f"{request.base_url}?{urlencode(parametros)}"

    return {
        "_first": {
            "href": crear_url(0)
        },
        "_prev": {
            "href": crear_url(max(0, offset - limite))
        } if offset > 0 else None,
        "_next": {
            "href": crear_url(offset + limite)
        } if offset + limite < total else None,
        "_last": {
            "href": crear_url(ultimo_offset)
        }
    }


@socios_bp.route("/socios", methods=["GET"])
def obtener_socios():

    try:
        filtros = validar_filtros_socios(request.args)
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
        resultado = listar_socios(filtros)
    except Error:
        return jsonify({
            "errors": [{
                "code": "ERROR_BASE_DATOS",
                "message": "Error interno",
                "level": "error",
                "description": "Ocurrió un error al acceder a la base de datos"
            }]
        }), 500

    return jsonify({
        "socios": resultado["socios"],
        "_links": construir_enlaces_socios(
            filtros,
            resultado["total"]
        )
    }), 200


@socios_bp.route("/socios/<int:id>", methods=["GET"])
def obtener_socio(id):

    try:
        socio = buscar_socio(id)
    except Error:
        return jsonify({
            "errors": [{
                "code": "ERROR_BASE_DATOS",
                "message": "Error interno",
                "level": "error",
                "description": "Ocurrió un error al acceder a la base de datos"
            }]
        }), 500

    if socio is None:
        return jsonify({
            "errors": [{
                "code": "SOCIO_NO_EXISTE",
                "message": "El socio no existe",
                "level": "error",
                "description": "No se encontró un socio con el identificador indicado"
            }]
        }), 404

    return jsonify(socio), 200


@socios_bp.route("/socios", methods=["POST"])
def registrar_socio():

    try:
        datos = validar_creacion_socio(
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
        crear_socio_service(datos)
    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "EMAIL_YA_REGISTRADO",
                "message": "El email ya está registrado",
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

    return "", 201


@socios_bp.route("/socios/<int:id>", methods=["PATCH"])
def actualizar_socio(id):

    try:
        datos = validar_actualizacion_socio(
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
        actualizar_socio_service(id, datos)
    except LookupError as e:
        return jsonify({
            "errors": [{
                "code": "SOCIO_NO_EXISTE",
                "message": "El socio no existe",
                "level": "error",
                "description": str(e)
            }]
        }), 404
    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "EMAIL_YA_REGISTRADO",
                "message": "El email ya está registrado",
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

    return "", 200
