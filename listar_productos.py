"""
listar_productos.py - T05: Listado de productos
Permite obtener todos los productos registrados en el inventario.
"""

from datos import cargar_inventario


def listar_productos() -> dict:
    """
    Retorna todos los productos registrados en el inventario.

    Returns:
        dict con claves:
            "exito"     (bool)       – True si hay al menos un producto.
            "mensaje"   (str)        – Descripción del resultado.
            "productos" (list[dict]) – Lista de productos con su código incluido.
                                       Ordenada por código alfanumérico.
    """
    inventario = cargar_inventario()

    if not inventario:
        return {
            "exito": False,
            "mensaje": "No hay productos registrados en el inventario.",
            "productos": [],
        }

    productos = []
    for codigo, datos in inventario.items():
        item = datos.copy()
        item["codigo"] = codigo
        productos.append(item)

    # Ordenar por código
    productos.sort(key=lambda p: p["codigo"])

    return {
        "exito": True,
        "mensaje": f"Se encontraron {len(productos)} producto(s).",
        "productos": productos,
    }
