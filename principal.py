import tkinter as tk
from tkinter import ttk, messagebox

from registrar_producto import registrar_producto
from buscar_producto import buscar_por_codigo, buscar_por_nombre
from actualizar_stock import actualizar_stock
from eliminar_producto import eliminar_producto
from listar_productos import listar_productos


def tab_registrar(tab):
    import tkinter as tk
    from registrar_producto import registrar_producto

    tk.Label(tab, text="Registrar producto", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    # 🔹 Codigo (solo mostrar)
    tk.Label(tab, text="Codigo del producto").grid(row=1, column=0)
    lbl_codigo = tk.Label(tab, text="---", fg="blue", font=("Arial", 10, "bold"))
    lbl_codigo.grid(row=1, column=1)

    # 🔹 Nombre
    tk.Label(tab, text="Nombre").grid(row=2, column=0)
    ent_nombre = tk.Entry(tab)
    ent_nombre.grid(row=2, column=1)

    # 🔹 Precio
    tk.Label(tab, text="Precio").grid(row=3, column=0)
    ent_precio = tk.Entry(tab)
    ent_precio.grid(row=3, column=1)

    # 🔹 Cantidad
    tk.Label(tab, text="Cantidad").grid(row=4, column=0)
    ent_cantidad = tk.Entry(tab)
    ent_cantidad.grid(row=4, column=1)

    # 🔹 Resultado
    lbl_resultado = tk.Label(tab, text="")
    lbl_resultado.grid(row=6, column=0, columnspan=2)

    # 🔹 Función registrar
    def registrar():
        r = registrar_producto(
            ent_nombre.get(),
            ent_precio.get(),
            ent_cantidad.get()
        )

        if r["exito"]:
            # Mostrar codigo generado
            lbl_codigo.config(text=r["codigo"])
            lbl_resultado.config(text=r["mensaje"], fg="green")
        else:
            lbl_resultado.config(text=r["mensaje"], fg="red")

    # 🔹 Función limpiar
    def limpiar():
        ent_nombre.delete(0, tk.END)
        ent_precio.delete(0, tk.END)
        ent_cantidad.delete(0, tk.END)
        lbl_codigo.config(text="---")
        lbl_resultado.config(text="")

    # 🔹 Botones
    tk.Button(tab, text="Registrar", command=registrar).grid(row=5, column=0)
    tk.Button(tab, text="Limpiar", command=limpiar).grid(row=5, column=1)



def tab_buscar(tab):
    tk.Label(tab, text="Buscar producto", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    # Campo codigo
    tk.Label(tab, text="Codigo").grid(row=1, column=0)
    ent_codigo = tk.Entry(tab)
    ent_codigo.grid(row=1, column=1)

    # Campo nombre
    tk.Label(tab, text="Nombre").grid(row=2, column=0)
    ent_nombre = tk.Entry(tab)
    ent_nombre.grid(row=2, column=1)

    txt = tk.Text(tab, height=10)
    txt.grid(row=4, column=0, columnspan=2)

    lbl = tk.Label(tab, text="")
    lbl.grid(row=3, column=0, columnspan=2)

    def buscar():
        txt.delete("1.0", tk.END)

        codigo = ent_codigo.get().strip()
        nombre = ent_nombre.get().strip()

        # ambos llenos (opcional)
        if codigo and nombre:
            lbl.config(text="Ingresa solo codigo o nombre", fg="red")
            return

        #  buscar por codigo
        if codigo:
            r = buscar_por_codigo(codigo)
            if r["exito"]:
                p = r["producto"]
                txt.insert(tk.END, f"{p['codigo']} | {p['nombre']} | {p['precio']} | {p['stock']}")
                lbl.config(text="Encontrado", fg="green")
            else:
                lbl.config(text=r["mensaje"], fg="red")

        #  buscar por nombre
        elif nombre:
            r = buscar_por_nombre(nombre)
            if r["exito"]:
                for p in r["productos"]:
                    txt.insert(tk.END, f"{p['codigo']} | {p['nombre']} | {p['precio']} | {p['stock']}\n")
                lbl.config(text=f"{len(r['productos'])} resultado(s)", fg="green")
            else:
                lbl.config(text=r["mensaje"], fg="red")

        else:
            lbl.config(text="Ingresa codigo o nombre", fg="red")

    tk.Button(tab, text="Buscar", command=buscar).grid(row=5, column=0, columnspan=2)


def tab_stock(tab):
    tk.Label(tab, text="Actualizar stock").pack(pady=10)

    ent_codigo = tk.Entry(tab)
    ent_codigo.pack()

    ent_cant = tk.Entry(tab)
    ent_cant.pack()

    lbl = tk.Label(tab, text="")
    lbl.pack()

    def entrada():
        r = actualizar_stock(ent_codigo.get(), ent_cant.get(), "entrada")
        lbl.config(text=r["mensaje"], fg="green" if r["exito"] else "red")

    def salida():
        r = actualizar_stock(ent_codigo.get(), ent_cant.get(), "salida")
        lbl.config(text=r["mensaje"], fg="green" if r["exito"] else "red")

    tk.Button(tab, text="Entrada", command=entrada).pack()
    tk.Button(tab, text="Salida", command=salida).pack()


def tab_eliminar(tab):
    tk.Label(tab, text="Eliminar producto").pack(pady=10)

    ent = tk.Entry(tab)
    ent.pack()

    lbl = tk.Label(tab, text="")
    lbl.pack()

    def eliminar():
        if messagebox.askyesno("Confirmar", "¿Eliminar producto?"):
            r = eliminar_producto(ent.get())
            lbl.config(text=r["mensaje"], fg="green" if r["exito"] else "red")

    tk.Button(tab, text="Eliminar", command=eliminar).pack()


def tab_listar(tab):
    txt = tk.Text(tab)
    txt.pack(fill="both", expand=True)

    def cargar():
        txt.delete("1.0", tk.END)
        r = listar_productos()
        if r["exito"]:
            for p in r["productos"]:
                txt.insert(tk.END, f"{p['codigo']} {p['nombre']} {p['precio']} {p['stock']}\n")

    tk.Button(tab, text="Actualizar", command=cargar).pack()
    cargar()


def main():
    root = tk.Tk()
    root.title("Inventario")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tabs = [
        ("Registrar", tab_registrar),
        ("Buscar", tab_buscar),
        ("Stock", tab_stock),
        ("Eliminar", tab_eliminar),
        ("Listar", tab_listar),
    ]

    for nombre, func in tabs:
        frame = tk.Frame(notebook)
        notebook.add(frame, text=nombre)
        func(frame)

    root.mainloop()


if __name__ == "__main__":
    main()
