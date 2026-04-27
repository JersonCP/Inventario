from inventario import cargar_inventario
from registrar import registrar_producto
from buscar import buscar_producto
from actualizar import actualizar_stock


def menu():
    while True:
        inventario = cargar_inventario()

        print("\n=============================")
        print("  INVENTARIO - GRUPO B")
        print(f"  Productos: {len(inventario)}")
        print("=============================")
        print("[1] Registrar producto")
        print("[2] Buscar producto")
        print("[3] Actualizar stock")
        print("[0] Salir")
        print("=============================")

        opcion = input("Opcion: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            buscar_producto()
        elif opcion == "3":
            actualizar_stock()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu()
