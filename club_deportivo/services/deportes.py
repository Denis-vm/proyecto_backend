from ..repositories.deportes import obtener_todos


def listar_deportes():
    return obtener_todos()