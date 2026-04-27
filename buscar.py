from inventario import cargar_inventario


def buscar_producto():
    while True:
        inventario = cargar_inventario()
        print("\n--- BUSCAR PRODUCTO ---")

        codigo = input("Codigo: ").strip().upper()

        if codigo not in inventario:
            print(f"Error: no se encontro el producto con codigo '{codigo}'.")
        else:
            p = inventario[codigo]
            print(f"\nCodigo : {codigo}")
            print(f"Nombre : {p['nombre']}")
            print(f"Precio : S/ {p['precio']:.2f}")
            print(f"Stock  : {p['stock']} unidades")

        print("\n[1] Buscar otro producto")
        print("[0] Volver al inicio")
        opcion = input("Opcion: ").strip()
        if opcion == "0":
            break
        elif opcion != "1":
            print("Opcion no valida.")
