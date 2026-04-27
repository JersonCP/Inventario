from inventario import cargar_inventario, guardar_inventario


def actualizar_stock():
    while True:
        inventario = cargar_inventario()
        print("\n--- ACTUALIZAR STOCK ---")

        codigo = input("Codigo: ").strip().upper()

        if codigo not in inventario:
            print(f"Error: no se encontro el producto con codigo '{codigo}'.")
        else:
            p = inventario[codigo]
            print(f"Producto     : {p['nombre']}")
            print(f"Stock actual : {p['stock']} unidades")
            print("[1] Agregar unidades")
            print("[2] Retirar unidades")

            opcion = input("Opcion: ").strip()
            if opcion not in ("1", "2"):
                print("Error: opcion no valida.")
            else:
                try:
                    cantidad = int(input("Cantidad: ").strip())
                    if cantidad <= 0:
                        raise ValueError
                except ValueError:
                    print("Error: ingresa un numero entero mayor a 0.")
                else:
                    if opcion == "1":
                        p["stock"] += cantidad
                        print(f"Se agregaron {cantidad} unidades. Stock actual: {p['stock']}")
                        guardar_inventario(inventario)
                    else:
                        if cantidad > p["stock"]:
                            print(f"Error: stock insuficiente. Disponible: {p['stock']} unidades.")
                        else:
                            p["stock"] -= cantidad
                            print(f"Se retiraron {cantidad} unidades. Stock actual: {p['stock']}")
                            guardar_inventario(inventario)

        print("\n[1] Actualizar otro producto")
        print("[0] Volver al inicio")
        opcion = input("Opcion: ").strip()
        if opcion == "0":
            break
        elif opcion != "1":
            print("Opcion no valida.")
