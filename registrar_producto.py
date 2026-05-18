"""
registrar_producto.py - T01: Registro de producto
Permite registrar un nuevo producto en el inventario con validaciones.
"""

from datos import cargar_inventario, guardar_inventario, generar_codigo
import math

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

    errores = []

    # --- Validaciones ---
    nombre = nombre.strip() if isinstance(nombre, str) else ""

    if not nombre:
        errores.append("• El nombre del producto no puede estar vacío.")

    if len(nombre) > 20:
        errores.append("• El nombre no puede superar los 20 caracteres.")

    try:
        precio = float(precio)
    except (ValueError, TypeError):
        errores.append("• El precio debe ser un número válido.")
        precio = None

    if precio is not None:

        if math.isinf(precio) or math.isnan(precio): #BUG11 Y 12 CORREGIDO
            errores.append("• Precio inválido.")
    
        if precio <= 0: #BUG03 CORREGIDO
            errores.append("• El precio debe ser mayor a 0.")
    
        if precio > 20000: #BUG09  CORREGIDO
            errores.append("• El precio no puede superar S/. 20000.")

    try:
        cantidad = float(cantidad) #BUG02 Y 04 CORREGIDO
    except (ValueError, TypeError):
        errores.append("• La cantidad es inválida.")
        cantidad = None

    if cantidad is not None:

        if cantidad <= 0 or cantidad != int(cantidad):
            errores.append("• La cantidad debe ser un entero positivo.")

        if cantidad > 10000: #BUG09 CORREGIDO
            errores.append("• El stock no puede superar 10000.")

    # Mostrar todos los errores juntos
    if errores:
        return {
            "exito": False,
            "mensaje": "\n".join(errores),
            "codigo": None
        }

    cantidad = int(cantidad)

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
