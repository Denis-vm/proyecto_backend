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


def validar_email(email):
    if not isinstance(email, str):
        raise ValueError({
            "error": "El email debe ser un texto"
        })

    email = email.strip().lower()

    if not email:
        raise ValueError({
            "error": "El email no puede estar vacío"
        })

    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError({
            "error": "El email no tiene un formato válido"
        })

    return email


def validar_filtros_socios(args):
    parametros_permitidos = {
        "_limit",
        "_offset",
        "nombre",
        "activo"
    }

    for parametro in args:
        if parametro not in parametros_permitidos:
            raise ValueError({
                "error": f"El parámetro {parametro} no está permitido"
            })

    try:
        limite = int(args.get("_limit", "10"))
        offset = int(args.get("_offset", "0"))
    except ValueError:
        raise ValueError({
            "error": "_limit y _offset deben ser enteros"
        })

    validar_paginacion(limite, offset)

    return {
        "limite": limite,
        "offset": offset,
        "nombre": args.get("nombre"),
        "activo": validar_booleano(
            args.get("activo"),
            "activo"
        )
    }


def validar_creacion_socio(data):
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
        "email"
    }

    if set(data.keys()) - campos_permitidos:
        raise ValueError({
            "error": "Se recibieron campos desconocidos"
        })

    if "nombre" not in data:
        raise ValueError({
            "error": "El campo nombre es obligatorio"
        })

    if "email" not in data:
        raise ValueError({
            "error": "El campo email es obligatorio"
        })

    return {
        "nombre": validar_nombre(data["nombre"]),
        "email": validar_email(data["email"])
    }


def validar_actualizacion_socio(data):
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
        "email",
        "activo"
    }

    if set(data.keys()) - campos_permitidos:
        raise ValueError({
            "error": "Se recibieron campos desconocidos"
        })

    datos = {}

    if "nombre" in data:
        datos["nombre"] = validar_nombre(data["nombre"])

    if "email" in data:
        datos["email"] = validar_email(data["email"])

    if "activo" in data:
        if not isinstance(data["activo"], bool):
            raise ValueError({
                "error": "El campo activo debe ser true o false"
            })

        datos["activo"] = data["activo"]

    return datos
