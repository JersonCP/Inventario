import json
import os

ARCHIVO = "inventario.json"


def cargar_inventario():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_inventario(inventario):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)
