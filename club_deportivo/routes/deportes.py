from flask import Blueprint
from ..services.deportes import listar_deportes

deportes_bp = Blueprint(
    "deportes",
    __name__
)

#TODOS LOS DEPORTES
@deportes_bp.route("/deportes", methods=["GET"])
def lista_deporte():
    deportes = listar_deportes()

    if deportes is None:
        return{
            "error": "No se pudo conectar la base de datos"
        }, 500
    if not deportes:
        return "",204

    return{
        "deportes": deportes
    }, 200
