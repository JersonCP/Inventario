from inventario import cargar_inventario, guardar_inventario


def registrar_producto():
    while True:
        inventario = cargar_inventario()
        print("\n--- REGISTRAR PRODUCTO ---")

        codigo = input("Codigo: ").strip().upper()
        if not codigo:
            print("Error: el codigo no puede estar vacio.")
        elif codigo in inventario:
            print(f"Error: ya existe un producto con el codigo '{codigo}'.")
        else:
            nombre = input("Nombre: ").strip()
            if not nombre:
                print("Error: el nombre no puede estar vacio.")
            else:
                try:
                    precio = float(input("Precio (S/): ").strip())
                    if precio < 0:
                        raise ValueError
                except ValueError:
                    print("Error: ingresa un precio valido (numero positivo).")
                else:
                    try:
                        stock = int(input("Stock inicial: ").strip())
                        if stock < 0:
                            raise ValueError
                    except ValueError:
                        print("Error: ingresa un stock valido (numero entero positivo).")
                    else:
                        inventario[codigo] = {
                            "nombre": nombre,
                            "precio": precio,
                            "stock": stock
                        }
                        guardar_inventario(inventario)
                        print(f"Producto '{nombre}' registrado correctamente.")

        print("\n[1] Registrar otro producto")
        print("[0] Volver al inicio")
        opcion = input("Opcion: ").strip()
        if opcion == "0":
            break
        elif opcion != "1":
            print("Opcion no valida.")
