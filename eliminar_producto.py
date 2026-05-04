"""
eliminar_producto.py - T04: Eliminación de producto
Permite eliminar un producto del inventario por su código.
"""

from datos import cargar_inventario, guardar_inventario


def eliminar_producto(codigo: str) -> dict:
    """
    Elimina un producto del inventario.

    Args:
        codigo: Código del producto a eliminar (ej. "P001").

    Returns:
        dict con claves:
            "exito"   (bool) – True si se eliminó correctamente.
            "mensaje" (str)  – Descripción del resultado.
            "nombre"  (str)  – Nombre del producto eliminado (si exito=True).
    """
    codigo = codigo.strip().upper() if isinstance(codigo, str) else ""

    if not codigo:
        return {"exito": False, "mensaje": "El código no puede estar vacío.", "nombre": None}

    inventario = cargar_inventario()

    if codigo not in inventario:
        return {"exito": False, "mensaje": f"No existe ningún producto con código '{codigo}'.", "nombre": None}

    nombre = inventario[codigo]["nombre"]
    del inventario[codigo]
    guardar_inventario(inventario)

    return {
        "exito": True,
        "mensaje": f"Producto '{nombre}' (código {codigo}) eliminado correctamente.",
        "nombre": nombre,
    }
