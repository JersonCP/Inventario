"""
datos.py - Gestión de persistencia del inventario
Carga y guarda el inventario desde/hacia inventario.json
"""

import json
import os

ARCHIVO = os.path.join(os.path.dirname(__file__), "inventario.json")


def cargar_inventario() -> dict:
    """Carga el inventario desde el archivo JSON."""

    if not os.path.exists(ARCHIVO):
        guardar_inventario({})
        return {}

    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)

    except (json.JSONDecodeError, OSError):
        # BUG01 CORREGIDO
        inventario_vacio = {}

        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(inventario_vacio, f, indent=4, ensure_ascii=False)

        return inventario_vacio


def guardar_inventario(inventario: dict) -> None:
    """Guarda el inventario en el archivo JSON."""
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)


def generar_codigo(inventario: dict) -> str: #BUG07 CORREGIDO
    numeros = set()

    for codigo in inventario.keys():
        if codigo.startswith("P") and codigo[1:].isdigit():
            numeros.add(int(codigo[1:]))

    i = 1
    while i in numeros:
        i += 1

    return f"P{i:03d}"
