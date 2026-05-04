"""
actualizar_stock.py - T03: Actualización de stock
Permite incrementar o disminuir el stock de un producto existente.
"""

from datos import cargar_inventario, guardar_inventario


def actualizar_stock(codigo: str, cantidad: int, operacion: str) -> dict:
    """
    Actualiza el stock de un producto.

    Args:
        codigo:    Código del producto (ej. "P001").
        cantidad:  Cantidad a agregar o retirar (debe ser > 0).
        operacion: "entrada" para incrementar, "salida" para disminuir.

    Returns:
        dict con claves:
            "exito"        (bool)     – True si se actualizó correctamente.
            "mensaje"      (str)      – Descripción del resultado.
            "stock_nuevo"  (int|None) – Stock resultante, o None si hubo error.
    """
    # --- Validaciones ---
    codigo = codigo.strip().upper() if isinstance(codigo, str) else ""

    if not codigo:
        return {"exito": False, "mensaje": "El código no puede estar vacío.", "stock_nuevo": None}

    operacion = operacion.strip().lower() if isinstance(operacion, str) else ""

    if operacion not in ("entrada", "salida"):
        return {"exito": False, "mensaje": "La operación debe ser 'entrada' o 'salida'.", "stock_nuevo": None}

    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return {"exito": False, "mensaje": "La cantidad debe ser un número entero válido.", "stock_nuevo": None}

    if cantidad <= 0:
        return {"exito": False, "mensaje": "La cantidad debe ser mayor a cero.", "stock_nuevo": None}

    # --- Actualización ---
    inventario = cargar_inventario()

    if codigo not in inventario:
        return {"exito": False, "mensaje": f"No se encontró ningún producto con código '{codigo}'.", "stock_nuevo": None}

    stock_actual = inventario[codigo]["stock"]

    if operacion == "entrada":
        nuevo_stock = stock_actual + cantidad
    else:  # salida
        if cantidad > stock_actual:
            return {
                "exito": False,
                "mensaje": f"Stock insuficiente. Stock actual: {stock_actual}, cantidad solicitada: {cantidad}.",
                "stock_nuevo": None,
            }
        nuevo_stock = stock_actual - cantidad

    inventario[codigo]["stock"] = nuevo_stock
    guardar_inventario(inventario)

    accion = "agregadas" if operacion == "entrada" else "retiradas"
    nombre = inventario[codigo]["nombre"]

    return {
        "exito": True,
        "mensaje": f"{cantidad} unidad(es) {accion} correctamente de '{nombre}'. Stock actual: {nuevo_stock}.",
        "stock_nuevo": nuevo_stock,
    }
