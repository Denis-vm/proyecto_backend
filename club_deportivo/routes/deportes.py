from flask import Blueprint
from ..services.deportes import listar_deportes as listar_deportes_service, buscar_deporte

deportes_bp = Blueprint(
    "deportes",
    __name__,
    url_prefix="/deportes"
)

""" TODOS LOS DEPORTES """
@deportes_bp.get("")
def listar_deportes():
    deportes = listar_deportes_service()

    if deportes is None:
        return{
            "error": "No se pudo conectar la base de datos"
        }, 500
    if not deportes:
        return "",204

    return{
        "deportes": deportes
    }, 200
