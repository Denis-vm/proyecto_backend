from ..repositories.deportes import obtener_todos, obtener_por_id


def listar_deportes():
    return obtener_todos()