"""
registrar_producto.py - T01: Registro de producto
Permite registrar un nuevo producto en el inventario con validaciones.
"""

from datos import cargar_inventario, guardar_inventario, generar_codigo


def registrar_producto(nombre: str, precio: float, cantidad: int) -> dict:
    """
    Registra un nuevo producto en el inventario.

    Args:
        nombre:   Nombre del producto (no vacío, máx. 100 caracteres).
        precio:   Precio unitario (debe ser >= 0).
        cantidad: Cantidad inicial en stock (debe ser >= 0).

    Returns:
        dict con claves:
            "exito"   (bool)  – True si se registró correctamente.
            "mensaje" (str)   – Descripción del resultado.
            "codigo"  (str)   – Código asignado al producto (si exito=True).

    Raises:
        No lanza excepciones; los errores se devuelven en el campo "mensaje".
    """
    # --- Validaciones ---
    nombre = nombre.strip() if isinstance(nombre, str) else ""

    if not nombre:
        return {"exito": False, "mensaje": "El nombre del producto no puede estar vacío.", "codigo": None}

    if len(nombre) > 100:
        return {"exito": False, "mensaje": "El nombre no puede superar los 100 caracteres.", "codigo": None}

    try:
        precio = float(precio)
    except (ValueError, TypeError):
        return {"exito": False, "mensaje": "El precio debe ser un número válido.", "codigo": None}

    if precio < 0:
        return {"exito": False, "mensaje": "El precio no puede ser negativo.", "codigo": None}

    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return {"exito": False, "mensaje": "La cantidad debe ser un número entero válido.", "codigo": None}

    if cantidad < 0:
        return {"exito": False, "mensaje": "La cantidad no puede ser negativa.", "codigo": None}

    # --- Registro ---
    inventario = cargar_inventario()

    # Verificar nombre duplicado (ignorar mayúsculas)
    for prod in inventario.values():
        if prod["nombre"].lower() == nombre.lower():
            return {
                "exito": False,
                "mensaje": f"Ya existe un producto con el nombre '{nombre}'.",
                "codigo": None,
            }

    codigo = generar_codigo(inventario)

    inventario[codigo] = {
        "nombre": nombre,
        "precio": round(precio, 2),
        "stock": cantidad,
    }

    guardar_inventario(inventario)

    return {
        "exito": True,
        "mensaje": f"Producto registrado exitosamente con código {codigo}.",
        "codigo": codigo,
    }

