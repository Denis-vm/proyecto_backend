from flask import Blueprint
from mysql.connector import Error
from ..services.deportes import listar_deportes

deportes_bp = Blueprint(
    "deportes",
    __name__
)

#TODOS LOS DEPORTES
@deportes_bp.route("/deportes", methods=["GET"])
def lista_deporte():
    try:
        deportes = listar_deportes()
    except Error:
        return {
            "errors": [{
                "code": "ERROR_BASE_DATOS",
                "message": "Error interno",
                "level": "error",
                "description": "Ocurrió un error al acceder a la base de datos"
            }]
        }, 500

    if not deportes:
        return "", 204

    return {
        "deportes": deportes
    }, 200