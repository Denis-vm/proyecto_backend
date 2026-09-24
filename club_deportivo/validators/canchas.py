from datetime import datetime



# Valida los parametros de paginación
def validar_paginacion(limite, offset):

    if limite < 1 or limite > 100:
        raise ValueError({
            "error": "El parámetro _limit debe estar entre 1 y 100"
        })

    if offset < 0:
        raise ValueError({
            "error": "El parámetro _offset debe ser mayor o igual a 0"
        })

    return limite, offset


#Techada va a ser true o false
def validar_booleano(valor, nombre):
    
    if valor is None:
        return None

    if valor == "true":
        return True

    if valor == "false":
        return False

    raise ValueError({
        "error": f"El parámetro {nombre} debe ser true o false"
    })


#Valida el identificador del deporte
def validar_id_deporte(id_deporte):

    if id_deporte is None:
        return None

    try:
        id_deporte = int(id_deporte)
    except ValueError:
        raise ValueError({
            "error": "El parámetro id_deporte debe ser un entero"
        })

    if id_deporte <= 0:
        raise ValueError({
            "error": "El parámetro id_deporte debe ser mayor a 0"
        })

    return id_deporte



#Valida los parámetros recibidos por GET /canchas
def validar_filtros_canchas(args):
    parametros_permitidos = {
        "_limit",
        "_offset",
        "id_deporte",
        "nombre",
        "techada",
        "activa"
    }

    for parametro in args:
        if parametro not in parametros_permitidos:
            raise ValueError({
                "error": f"El parámetro {parametro} no está permitido"
            })

    limite = args.get("_limit", "10")
    offset = args.get("_offset", "0")

    try:
        limite = int(limite)
        offset = int(offset)
    except ValueError:
        raise ValueError({
            "error": "_limit y _offset deben ser enteros"
        })

    validar_paginacion(limite, offset)

    id_deporte = validar_id_deporte(
        args.get("id_deporte")
    )

    nombre = args.get("nombre")

    techada = validar_booleano(
        args.get("techada"),
        "techada"
    )

    activa = validar_booleano(
        args.get("activa"),
        "activa"
    )

    return {
        "limite": limite,
        "offset": offset,
        "id_deporte": id_deporte,
        "nombre": nombre,
        "techada": techada,
        "activa": activa
    }


# Valida los datos necesarios para crear una cancha    

def validar_nombre(nombre):

    if not isinstance(nombre, str):
        raise ValueError({
            "error": "El nombre debe ser un texto"
        })

    nombre = nombre.strip()

    if not nombre:
        raise ValueError({
            "error": "El nombre no puede estar vacío"
        })

    return nombre

def validar_precio(precio):

    if not isinstance(precio, int) or isinstance(precio, bool):
        raise ValueError({
            "error": "El precio_hora debe ser un entero"
        })

    if precio <= 0:
        raise ValueError({
            "error": "El precio_hora debe ser mayor a 0"
        })

def validar_booleano_body(valor, nombre):

    if not isinstance(valor, bool):
        raise ValueError({
            "error": f"El campo {nombre} debe ser true o false"
        })

def validar_creacion_cancha(data):


    if not isinstance(data, dict):
        raise ValueError({
            "error": "El cuerpo debe ser un objeto JSON"
        })

    campos_permitidos = {
        "nombre",
        "id_deporte",
        "precio_hora",
        "techada",
        "activa"
    }

    campos_desconocidos = set(data.keys()) - campos_permitidos

    if campos_desconocidos:
        raise ValueError({
            "error": "Se recibieron campos desconocidos"
        })

    if not data:
        raise ValueError({
            "error": "El cuerpo no puede estar vacío"
        })

    if "nombre" not in data:
        raise ValueError({
            "error": "El campo nombre es obligatorio"
        })

    if "id_deporte" not in data:
        raise ValueError({
            "error": "El campo id_deporte es obligatorio"
        })

    if "precio_hora" not in data:
        raise ValueError({
            "error": "El campo precio_hora es obligatorio"
        })

    
    nombre = validar_nombre(data["nombre"])

    id_deporte = validar_id_deporte(data["id_deporte"])

    precio_hora = data["precio_hora"]
    validar_precio(precio_hora)

    techada = data.get("techada", False)
    activa = data.get("activa", True)

    validar_booleano_body(techada, "techada")
    validar_booleano_body(activa, "activa")

    return {
        "nombre": nombre,
        "id_deporte": id_deporte,
        "precio_hora": precio_hora,
        "techada": techada,
        "activa": activa
    }



# Valida los datos para actualizar parcialmente una cancha
def validar_actualizacion_cancha(data):

    if not isinstance(data, dict):
        raise ValueError({
            "error": "El cuerpo debe ser un objeto JSON"
        })

    if not data:
        raise ValueError({
            "error": "El cuerpo no puede estar vacío"
        })

    campos_permitidos = {
        "nombre",
        "precio_hora",
        "techada",
        "activa"
    }

    campos_desconocidos = set(data.keys()) - campos_permitidos

    if campos_desconocidos:
        raise ValueError({
            "error": "Se recibieron campos desconocidos"
        })

    if "nombre" in data:
        data["nombre"] = validar_nombre(data["nombre"])

    if "precio_hora" in data:
        validar_precio(data["precio_hora"])

    if "techada" in data:
        validar_booleano_body(data["techada"], "techada")

    if "activa" in data:
        validar_booleano_body(data["activa"], "activa")

    return data







def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        raise ValueError({
            "error": "La fecha debe tener formato YYYY-MM-DD"
        })
    return fecha


def validar_hora(hora, nombre):
    try:
        datetime.strptime(hora, "%H:%M:%S")
    except ValueError:
        raise ValueError({
            "error": f"El parámetro {nombre} debe tener formato HH:MM:SS"
        })

    if not hora.endswith(":00"):
        raise ValueError({
            "error": f"El parámetro {nombre} debe estar en una hora exacta"
        })

    hora_entero = int(hora[:2])

    if hora_entero < 8 or hora_entero > 23:
        raise ValueError({
            "error": f"El parámetro {nombre} debe estar entre las 08:00 y las 23:00"
        })

    return hora


def validar_disponibilidad(args):
    parametros_permitidos = {
        "fecha",
        "hora_inicio",
        "hora_fin",
        "id_deporte",
        "techada",
        "_limit",
        "_offset"
    }

    for parametro in args:
        if parametro not in parametros_permitidos:
            raise ValueError({
                "error": f"El parámetro {parametro} no está permitido"
            })

    fecha = args.get("fecha")
    hora_inicio = args.get("hora_inicio")
    hora_fin = args.get("hora_fin")

    if fecha is None:
        raise ValueError({
            "error": "El parámetro fecha es obligatorio"
        })

    if hora_inicio is None:
        raise ValueError({
            "error": "El parámetro hora_inicio es obligatorio"
        })

    if hora_fin is None:
        raise ValueError({
            "error": "El parámetro hora_fin es obligatorio"
        })

    fecha = validar_fecha(fecha)
    hora_inicio = validar_hora(hora_inicio, "hora_inicio")
    hora_fin = validar_hora(hora_fin, "hora_fin")

    if hora_fin <= hora_inicio:
        raise ValueError({
            "error": "hora_fin debe ser posterior a hora_inicio"
        })

    inicio = datetime.strptime(hora_inicio, "%H:%M:%S")
    fin = datetime.strptime(hora_fin, "%H:%M:%S")

    duracion = fin - inicio
    horas = duracion.total_seconds() / 3600

    if horas < 1 or horas > 3:
        raise ValueError({
            "error": "La duración debe ser de entre 1 y 3 horas"
        })

    limite = args.get("_limit", "10")
    offset = args.get("_offset", "0")

    try:
        limite = int(limite)
        offset = int(offset)
    except ValueError:
        raise ValueError({
            "error": "_limit y _offset deben ser enteros"
        })

    validar_paginacion(limite, offset)

    id_deporte = validar_id_deporte(args.get("id_deporte"))
    techada = validar_booleano(args.get("techada"), "techada")

    return {
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "id_deporte": id_deporte,
        "techada": techada,
        "limite": limite,
        "offset": offset
    }