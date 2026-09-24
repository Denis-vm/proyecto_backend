from flask import Blueprint, jsonify, request
from mysql.connector import Error
from urllib.parse import urlencode
from ..services.canchas import (listar_canchas,listar_canchas_disponibles , buscar_cancha, crear_canchas, 
actualizar_cancha_service, eliminar_cancha_service)

from ..validators.canchas import (validar_filtros_canchas,validar_disponibilidad , validar_creacion_cancha, 
validar_actualizacion_cancha)


canchas_bp = Blueprint(
    "canchas",
    __name__
)

#FUNCION PARA implementar HATEOAS
def construir_enlaces_canchas(filtros, total):
    limite = filtros["limite"]
    offset = filtros["offset"]

    ultimo_offset = ((total - 1) // limite) * limite if total > 0 else 0

    def crear_url(nuevo_offset):
        parametros = {
            "_limit": limite,
            "_offset": nuevo_offset
        }

        if filtros["id_deporte"] is not None:
            parametros["id_deporte"] = filtros["id_deporte"]

        if filtros["nombre"] is not None:
            parametros["nombre"] = filtros["nombre"]

        if filtros["techada"] is not None:
            parametros["techada"] = str(
                filtros["techada"]
            ).lower()

        if filtros["activa"] is not None:
            parametros["activa"] = str(
                filtros["activa"]
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

# GET / CANCHAS

@canchas_bp.route("/canchas", methods=["GET"])
def obtener_canchas():

    try:
        filtros = validar_filtros_canchas(request.args)
    except ValueError as e:
        return jsonify({
            "errors": [
                {
                "code": "ERROR_VALIDACION",
                "message": "Los parámetros de la solicitud son inválidos",
                "level": "error",
                "description": e.args[0]["error"]
                }
            ]
        }), 400

    try:
        resultado = listar_canchas(filtros)
    except Error:
        return jsonify({
            "errors": [
                {
                    "code": "ERROR_BASE_DATOS",
                    "message": "Error interno",
                    "level": "error",
                    "description": "Ocurrió un error al acceder a la base de datos"
                }
            ]
        }), 500

    enlaces = construir_enlaces_canchas(filtros, resultado["total"])

    return jsonify({
        "canchas": resultado["canchas"],
        "_links": enlaces
    }), 200


# GET / CANCHAS / ID
@canchas_bp.route("/canchas/<int:id>", methods=["GET"])
def obtener_cancha(id):

    try:
        cancha = buscar_cancha(id)
    except Error:
        return jsonify({
            "errors": [
                {
                    "code": "ERROR_BASE_DATOS",
                    "message": "Error interno",
                    "level": "error",
                    "description": "Ocurrió un error al acceder a la base de datos"
                }
            ]
        }), 500

    if cancha is None:
        return jsonify({
            "errors": [
                {
                    "code": "CANCHA_NO_EXISTE",
                    "message": "La cancha no existe",
                    "level": "error",
                    "description": "No se encontró una cancha con el identificador indicado"
                }
            ]
        }), 404

    return jsonify(cancha), 200


#FUNCION PARA implementar HATEOAS
def construir_enlaces_disponibles(filtros, total):
    limite = filtros["limite"]
    offset = filtros["offset"]

    ultimo_offset = ((total - 1) // limite) * limite if total > 0 else 0

    def crear_url(nuevo_offset):
        parametros = {
            "fecha": filtros["fecha"],
            "hora_inicio": filtros["hora_inicio"],
            "hora_fin": filtros["hora_fin"],
            "_limit": limite,
            "_offset": nuevo_offset
        }

        if filtros["id_deporte"] is not None:
            parametros["id_deporte"] = filtros["id_deporte"]

        if filtros["techada"] is not None:
            parametros["techada"] = str(filtros["techada"]).lower()

        return f"{request.base_url}?{urlencode(parametros)}"

    return {
        "_first": {"href": crear_url(0)},
        "_prev": {"href": crear_url(max(0, offset - limite))} if offset > 0 else None,
        "_next": {"href": crear_url(offset + limite)} if offset + limite < total else None,
        "_last": {"href": crear_url(ultimo_offset)}
    }

#GET CANCHAS DISPONIBLES
@canchas_bp.route("/canchas/disponibles", methods=["GET"])
def obtener_canchas_disponibles():
    try:
        filtros = validar_disponibilidad(request.args)
    except ValueError as e:
        return jsonify({
            "errors": [
                {
                    "code": "ERROR_VALIDACION",
                    "message": "Los parámetros de la solicitud son inválidos",
                    "level": "error",
                    "description": e.args[0]["error"]
                }
            ]
        }), 400

    try:
        resultado = listar_canchas_disponibles(filtros)
    except Error:
        return jsonify({
            "errors": [
                {
                    "code": "ERROR_BASE_DATOS",
                    "message": "Error interno",
                    "level": "error",
                    "description": "Ocurrió un error al acceder a la base de datos"
                }
            ]
        }), 500

    enlaces = construir_enlaces_disponibles(
    filtros,
    resultado["total"]
    )

    return jsonify({
        "canchas": resultado["canchas"],
        "_links": enlaces
    }), 200

#///////////////////////////////////////////



# POST / CANCHAS
@canchas_bp.route("/canchas", methods=["POST"])
def crear_nueva_cancha():

    try:
        datos = validar_creacion_cancha(request.get_json())
    except ValueError as e:
        return jsonify({
        "errors": [
            {
                "code": "ERROR_VALIDACION",
                "message": "El cuerpo de la solicitud es inválido",
                "level": "error",
                "description": e.args[0]["error"]
            }
        ]
      }), 400

    try:
        id_cancha = crear_canchas(datos)
    except LookupError as e:
       return jsonify({
        "errors": [
            {
                "code": "DEPORTE_NO_EXISTE",
                "message": "El deporte no existe",
                "level": "error",
                "description": str(e)
            }
        ]
       }), 404
    except Error:
        return jsonify({
            "errors": [
            {
                "code": "ERROR_BASE_DATOS",
                "message": "Error interno",
                "level": "error",
                "description": "Ocurrió un error al acceder a la base de datos"
            }
          ]
        }), 500

    return "", 201


# PATCH CANCHAS ID
@canchas_bp.route("/canchas/<int:id>", methods=["PATCH"])
def actualizar_cancha(id):

    try:
        datos = validar_actualizacion_cancha(request.get_json())
    except ValueError as e:
        return jsonify({
            "errors": [
                {
                    "code": "ERROR_VALIDACION",
                    "message": "El cuerpo de la solicitud es inválido",
                    "level": "error",
                    "description": e.args[0]["error"]
                }
            ]
        }), 400

    try:
        actualizar_cancha_service(id, datos)
    except LookupError as e:
        return jsonify({
            "errors": [
                {
                    "code": "CANCHA_NO_EXISTE",
                    "message": "La cancha no existe",
                    "level": "error",
                    "description": str(e)
                }
            ]
        }), 404
    except Error:
        return jsonify({
            "errors": [
                {
                    "code": "ERROR_BASE_DATOS",
                    "message": "Error interno",
                    "level": "error",
                    "description": "Ocurrió un error al acceder a la base de datos"
                }
            ]
        }), 500

    return "", 204

#ELIMINAR 
@canchas_bp.route("/canchas/<int:id>", methods=["DELETE"])
def eliminar_cancha(id):

    try:
        eliminar_cancha_service(id)

    except LookupError as e:
        return jsonify({
            "errors": [
                {
                    "code": "CANCHA_NO_EXISTE",
                    "message": "La cancha no existe",
                    "level": "error",
                    "description": str(e)
                }
            ]
        }), 404

    except ValueError as e:
        return jsonify({
            "errors": [
                {
                    "code": "CANCHA_CON_RESERVAS",
                    "message": "La cancha tiene reservas",
                    "level": "error",
                    "description": str(e)
                }
            ]
        }), 409

    except Error:
        return jsonify({
            "errors": [
                {
                    "code": "ERROR_BASE_DATOS",
                    "message": "Error interno",
                    "level": "error",
                    "description": "Ocurrió un error al acceder a la base de datos"
                }
            ]
        }), 500

    return "", 204

