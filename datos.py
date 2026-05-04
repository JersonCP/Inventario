"""
datos.py - Gestión de persistencia del inventario
Carga y guarda el inventario desde/hacia inventario.json
"""

import json
import os

ARCHIVO = os.path.join(os.path.dirname(__file__), "inventario.json")


def cargar_inventario() -> dict:
    """Carga el inventario desde el archivo JSON. Retorna dict vacío si no existe."""
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_inventario(inventario: dict) -> None:
    """Guarda el inventario en el archivo JSON."""
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)


def generar_codigo(inventario: dict) -> str:
    """
    Genera un código autoincremental tipo P001, P002, ...
    Busca el mayor número existente y suma 1.
    """
    numeros = []
    for codigo in inventario.keys():
        if codigo.startswith("P") and codigo[1:].isdigit():
            numeros.append(int(codigo[1:]))
    siguiente = max(numeros) + 1 if numeros else 1
    return f"P{siguiente:03d}"
