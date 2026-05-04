"""
buscar_producto.py - T02: Búsqueda de producto
Permite buscar productos por código exacto o por nombre (búsqueda parcial).
"""

from datos import cargar_inventario


def buscar_por_codigo(codigo: str) -> dict:
    """
    Busca un producto por su código exacto.

    Args:
        codigo: Código del producto (ej. "P001").

    Returns:
        dict con claves:
            "exito"    (bool)        – True si se encontró.
            "mensaje"  (str)         – Descripción del resultado.
            "producto" (dict | None) – Datos del producto encontrado o None.
    """
    codigo = codigo.strip().upper() if isinstance(codigo, str) else ""

    if not codigo:
        return {"exito": False, "mensaje": "El código no puede estar vacío.", "producto": None}

    inventario = cargar_inventario()

    if codigo not in inventario:
        return {"exito": False, "mensaje": f"No se encontró ningún producto con código '{codigo}'.", "producto": None}

    producto = inventario[codigo].copy()
    producto["codigo"] = codigo
    return {"exito": True, "mensaje": "Producto encontrado.", "producto": producto}


def buscar_por_nombre(nombre: str) -> dict:
    """
    Busca productos cuyo nombre contenga el texto indicado (búsqueda parcial,
    insensible a mayúsculas).

    Args:
        nombre: Texto a buscar dentro del nombre del producto.

    Returns:
        dict con claves:
            "exito"     (bool)       – True si se encontró al menos uno.
            "mensaje"   (str)        – Descripción del resultado.
            "productos" (list[dict]) – Lista de productos que coinciden.
    """
    nombre = nombre.strip() if isinstance(nombre, str) else ""

    if not nombre:
        return {"exito": False, "mensaje": "El término de búsqueda no puede estar vacío.", "productos": []}

    inventario = cargar_inventario()
    resultados = []

    for codigo, datos in inventario.items():
        if nombre.lower() in datos["nombre"].lower():
            item = datos.copy()
            item["codigo"] = codigo
            resultados.append(item)

    if not resultados:
        return {
            "exito": False,
            "mensaje": f"No se encontraron productos con '{nombre}' en el nombre.",
            "productos": [],
        }

    return {
        "exito": True,
        "mensaje": f"Se encontraron {len(resultados)} producto(s).",
        "productos": resultados,
    }

