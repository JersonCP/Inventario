"""
principal.py - Módulo de Inventario (Grupo B)
Interfaz gráfica con tkinter. Menú principal con pestañas para cada funcionalidad.
Ejecutar directamente: python principal.py
"""

import tkinter as tk
from tkinter import messagebox, ttk

from actualizar_stock import actualizar_stock
from buscar_producto import buscar_por_codigo, buscar_por_nombre
from eliminar_producto import eliminar_producto
from listar_productos import listar_productos

# Importar las funcionalidades
from registrar_producto import registrar_producto

# ─────────────────────────────────────────────
#  Paleta de colores
# ─────────────────────────────────────────────
COLOR_FONDO = "#1e1e2e"
COLOR_PANEL = "#2a2a3e"
COLOR_ACENTO = "#7c6af7"
COLOR_ACENTO2 = "#5adecd"
COLOR_TEXTO = "#e0e0f0"
COLOR_TEXTO_DIM = "#888899"
COLOR_EXITO = "#4caf50"
COLOR_ERROR = "#f44336"
COLOR_ENTRADA = "#33334d"
COLOR_BORDE = "#44446a"
FUENTE_TITULO = ("Segoe UI", 20, "bold")
FUENTE_SECCION = ("Segoe UI", 13, "bold")
FUENTE_LABEL = ("Segoe UI", 10)
FUENTE_BOTON = ("Segoe UI", 10, "bold")
FUENTE_MONO = ("Consolas", 10)


def estilo_entry(parent, **kwargs) -> tk.Entry:
    """Crea un Entry con estilo consistente."""
    e = tk.Entry(
        parent,
        bg=COLOR_ENTRADA,
        fg=COLOR_TEXTO,
        insertbackground=COLOR_TEXTO,
        relief="flat",
        font=FUENTE_MONO,
        highlightthickness=1,
        highlightcolor=COLOR_ACENTO,
        highlightbackground=COLOR_BORDE,
        **kwargs,
    )
    return e


def estilo_boton(parent, texto, comando, color=None) -> tk.Button:
    """Crea un Button con estilo consistente."""
    c = color or COLOR_ACENTO
    b = tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=c,
        fg="#ffffff",
        relief="flat",
        font=FUENTE_BOTON,
        padx=14,
        pady=6,
        cursor="hand2",
        activebackground=COLOR_ACENTO2,
        activeforeground="#1e1e2e",
    )
    return b


def estilo_label(parent, texto, bold=False, dim=False, **kwargs) -> tk.Label:
    """Crea un Label con estilo consistente."""
    fuente = ("Segoe UI", 10, "bold") if bold else FUENTE_LABEL
    color = COLOR_TEXTO_DIM if dim else COLOR_TEXTO
    return tk.Label(parent, text=texto, bg=COLOR_PANEL, fg=color, font=fuente, **kwargs)


def resultado_label(parent) -> tk.Label:
    """Label para mostrar mensajes de resultado (éxito/error)."""
    return tk.Label(
        parent,
        text="",
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        font=FUENTE_LABEL,
        wraplength=480,
        justify="left",
    )


def limpiar_hijos(frame):
    """Elimina todos los widgets hijos de un frame."""
    for widget in frame.winfo_children():
        widget.destroy()


# ═══════════════════════════════════════════════════════════
#  TAB 1 – REGISTRAR PRODUCTO
# ═══════════════════════════════════════════════════════════


def construir_tab_registrar(tab):
    tab.configure(bg=COLOR_PANEL)
    pad = {"padx": 20, "pady": 6}

    estilo_label(tab, "Registrar nuevo producto", bold=True).grid(
        row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="w"
    )

    # 🔹 Código (solo mostrar)
    estilo_label(tab, "Código del producto").grid(row=1, column=0, sticky="w", **pad)
    lbl_codigo = estilo_label(tab, "---", bold=True)
    lbl_codigo.grid(row=1, column=1, sticky="w", **pad)

    # Nombre
    estilo_label(tab, "Nombre del producto *").grid(row=2, column=0, sticky="w", **pad)
    ent_nombre = estilo_entry(tab, width=40)
    ent_nombre.grid(row=2, column=1, sticky="w", **pad)

    # Precio
    estilo_label(tab, "Precio unitario (S/.) *").grid(
        row=3, column=0, sticky="w", **pad
    )
    ent_precio = estilo_entry(tab, width=20)
    ent_precio.grid(row=3, column=1, sticky="w", **pad)

    # Cantidad
    estilo_label(tab, "Cantidad inicial *").grid(row=4, column=0, sticky="w", **pad)
    ent_cantidad = estilo_entry(tab, width=20)
    ent_cantidad.grid(row=4, column=1, sticky="w", **pad)

    lbl_resultado = resultado_label(tab)
    lbl_resultado.grid(row=6, column=0, columnspan=2, padx=20, pady=4, sticky="w")

    def limpiar():
        ent_nombre.delete(0, tk.END)
        ent_precio.delete(0, tk.END)
        ent_cantidad.delete(0, tk.END)
        lbl_resultado.config(text="", fg=COLOR_TEXTO)
        ent_nombre.focus()

    def registrar():
        resultado = registrar_producto(
            ent_nombre.get(),
            ent_precio.get(),
            ent_cantidad.get(),
        )

        if resultado["exito"]:
            # 🔹 mostrar código generado
            lbl_codigo.config(text=resultado["codigo"])

            lbl_resultado.config(text=f"✔  {resultado['mensaje']}", fg=COLOR_EXITO)

        else:
            lbl_resultado.config(text=f"✘  {resultado['mensaje']}", fg=COLOR_ERROR)

    frame_botones = tk.Frame(tab, bg=COLOR_PANEL)
    frame_botones.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="w")

    estilo_boton(frame_botones, "Registrar", registrar).pack(side="left", padx=(0, 10))
    estilo_boton(frame_botones, "Limpiar", limpiar, color="#555577").pack(side="left")

    estilo_label(tab, "* Campos obligatorios", dim=True).grid(
        row=7, column=0, columnspan=2, padx=20, sticky="w"
    )


# ═══════════════════════════════════════════════════════════
#  TAB 2 – BUSCAR PRODUCTO
# ═══════════════════════════════════════════════════════════


def construir_tab_buscar(tab):
    tab.configure(bg=COLOR_PANEL)
    pad = {"padx": 20, "pady": 6}

    estilo_label(tab, "Buscar producto", bold=True).grid(
        row=0, column=0, columnspan=3, pady=(20, 10), padx=20, sticky="w"
    )

    # Modo de búsqueda
    var_modo = tk.StringVar(value="codigo")
    frame_radio = tk.Frame(tab, bg=COLOR_PANEL)
    frame_radio.grid(row=1, column=0, columnspan=3, padx=20, sticky="w")

    def estilo_radio(parent, texto, valor):
        return tk.Radiobutton(
            parent,
            text=texto,
            variable=var_modo,
            value=valor,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            selectcolor=COLOR_ACENTO,
            activebackground=COLOR_PANEL,
            activeforeground=COLOR_ACENTO2,
            font=FUENTE_LABEL,
            command=lambda: cambiar_modo(),
        )

    estilo_radio(frame_radio, "Buscar por Código", "codigo").pack(
        side="left", padx=(0, 20)
    )
    estilo_radio(frame_radio, "Buscar por Nombre", "nombre").pack(side="left")

    lbl_campo = estilo_label(tab, "Código del producto:")
    lbl_campo.grid(row=2, column=0, sticky="w", **pad)
    ent_busqueda = estilo_entry(tab, width=35)
    ent_busqueda.grid(row=2, column=1, sticky="w", **pad)

    def cambiar_modo():
        if var_modo.get() == "codigo":
            lbl_campo.config(text="Código del producto:")
        else:
            lbl_campo.config(text="Nombre (parcial):")
        ent_busqueda.delete(0, tk.END)
        limpiar_resultados()

    # Frame resultados
    frame_res = tk.Frame(tab, bg=COLOR_PANEL)
    frame_res.grid(row=4, column=0, columnspan=3, padx=20, pady=(10, 0), sticky="nsew")
    tab.rowconfigure(4, weight=1)
    tab.columnconfigure(1, weight=1)

    lbl_estado = resultado_label(tab)
    lbl_estado.grid(row=3, column=0, columnspan=3, padx=20, sticky="w")

    def limpiar_resultados():
        limpiar_hijos(frame_res)
        lbl_estado.config(text="", fg=COLOR_TEXTO)

    def mostrar_producto(producto):
        """Muestra un producto como tarjeta."""
        tarjeta = tk.Frame(frame_res, bg=COLOR_ENTRADA, padx=12, pady=8)
        tarjeta.pack(fill="x", pady=4)

        tk.Label(
            tarjeta,
            text=f"[{producto['codigo']}] {producto['nombre']}",
            bg=COLOR_ENTRADA,
            fg=COLOR_ACENTO2,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")
        tk.Label(
            tarjeta,
            text=f"Precio: S/. {producto['precio']:.2f}   |   Stock: {producto['stock']} unid.",
            bg=COLOR_ENTRADA,
            fg=COLOR_TEXTO,
            font=FUENTE_LABEL,
        ).pack(anchor="w", pady=(2, 0))

    def buscar():
        limpiar_resultados()
        termino = ent_busqueda.get()

        if var_modo.get() == "codigo":
            resultado = buscar_por_codigo(termino)
            if resultado["exito"]:
                lbl_estado.config(text="✔  Producto encontrado.", fg=COLOR_EXITO)
                mostrar_producto(resultado["producto"])
            else:
                lbl_estado.config(text=f"✘  {resultado['mensaje']}", fg=COLOR_ERROR)
        else:
            resultado = buscar_por_nombre(termino)
            if resultado["exito"]:
                lbl_estado.config(text=f"✔  {resultado['mensaje']}", fg=COLOR_EXITO)
                for p in resultado["productos"]:
                    mostrar_producto(p)
            else:
                lbl_estado.config(text=f"✘  {resultado['mensaje']}", fg=COLOR_ERROR)

    estilo_boton(tab, "Buscar", buscar).grid(row=2, column=2, padx=(0, 20), pady=6)

    # Búsqueda al presionar Enter
    ent_busqueda.bind("<Return>", lambda e: buscar())


# ═══════════════════════════════════════════════════════════
#  TAB 3 – ACTUALIZAR STOCK
# ═══════════════════════════════════════════════════════════


def construir_tab_stock(tab):
    tab.configure(bg=COLOR_PANEL)
    pad = {"padx": 20, "pady": 6}

    estilo_label(tab, "Actualizar stock", bold=True).grid(
        row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="w"
    )

    estilo_label(tab, "Código del producto *").grid(row=1, column=0, sticky="w", **pad)
    ent_codigo = estilo_entry(tab, width=20)
    ent_codigo.grid(row=1, column=1, sticky="w", **pad)

    estilo_label(tab, "Cantidad *").grid(row=2, column=0, sticky="w", **pad)
    ent_cantidad = estilo_entry(tab, width=15)
    ent_cantidad.grid(row=2, column=1, sticky="w", **pad)

    estilo_label(tab, "Tipo de operación *").grid(row=3, column=0, sticky="w", **pad)
    var_op = tk.StringVar(value="entrada")
    frame_op = tk.Frame(tab, bg=COLOR_PANEL)
    frame_op.grid(row=3, column=1, sticky="w", padx=20)

    for texto, valor in [("Entrada (+)", "entrada"), ("Salida (−)", "salida")]:
        tk.Radiobutton(
            frame_op,
            text=texto,
            variable=var_op,
            value=valor,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            selectcolor=COLOR_ACENTO,
            activebackground=COLOR_PANEL,
            font=FUENTE_LABEL,
        ).pack(side="left", padx=(0, 15))

    lbl_resultado = resultado_label(tab)
    lbl_resultado.grid(row=5, column=0, columnspan=2, padx=20, pady=4, sticky="w")
    lbl_stock = estilo_label(tab, "")
    lbl_stock.grid(row=6, column=0, columnspan=2, padx=20, sticky="w")

    def actualizar():
        resultado = actualizar_stock(ent_codigo.get(), ent_cantidad.get(), var_op.get())
        if resultado["exito"]:
            lbl_resultado.config(text=f"✔  {resultado['mensaje']}", fg=COLOR_EXITO)
            lbl_stock.config(
                text=f"Stock nuevo: {resultado['stock_nuevo']} unidades",
                fg=COLOR_ACENTO2,
            )
            ent_cantidad.delete(0, tk.END)
        else:
            lbl_resultado.config(text=f"✘  {resultado['mensaje']}", fg=COLOR_ERROR)
            lbl_stock.config(text="")

    def limpiar():
        ent_codigo.delete(0, tk.END)
        ent_cantidad.delete(0, tk.END)
        var_op.set("entrada")
        lbl_resultado.config(text="")
        lbl_stock.config(text="")

    frame_botones = tk.Frame(tab, bg=COLOR_PANEL)
    frame_botones.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="w")
    estilo_boton(frame_botones, "Actualizar", actualizar).pack(
        side="left", padx=(0, 10)
    )
    estilo_boton(frame_botones, "Limpiar", limpiar, color="#555577").pack(side="left")


# ═══════════════════════════════════════════════════════════
#  TAB 4 – ELIMINAR PRODUCTO
# ═══════════════════════════════════════════════════════════


def construir_tab_eliminar(tab):
    tab.configure(bg=COLOR_PANEL)
    pad = {"padx": 20, "pady": 6}

    estilo_label(tab, "Eliminar producto", bold=True).grid(
        row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="w"
    )
    estilo_label(
        tab, "Ingresa el código del producto que deseas eliminar.", dim=True
    ).grid(row=1, column=0, columnspan=2, padx=20, sticky="w")

    estilo_label(tab, "Código del producto *").grid(row=2, column=0, sticky="w", **pad)
    ent_codigo = estilo_entry(tab, width=20)
    ent_codigo.grid(row=2, column=1, sticky="w", **pad)

    lbl_resultado = resultado_label(tab)
    lbl_resultado.grid(row=4, column=0, columnspan=2, padx=20, pady=4, sticky="w")

    def intentar_eliminar():
        codigo = ent_codigo.get().strip().upper()
        if not codigo:
            lbl_resultado.config(text="✘  Debes ingresar un código.", fg=COLOR_ERROR)
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el producto con código '{codigo}'?\nEsta acción no se puede deshacer.",
        )
        if not confirmar:
            lbl_resultado.config(text="Operación cancelada.", fg=COLOR_TEXTO_DIM)
            return

        resultado = eliminar_producto(codigo)
        if resultado["exito"]:
            lbl_resultado.config(text=f"✔  {resultado['mensaje']}", fg=COLOR_EXITO)
            ent_codigo.delete(0, tk.END)
        else:
            lbl_resultado.config(text=f"✘  {resultado['mensaje']}", fg=COLOR_ERROR)

    estilo_boton(tab, "Eliminar", intentar_eliminar, color="#c0392b").grid(
        row=3, column=0, columnspan=2, padx=20, pady=10, sticky="w"
    )


# ═══════════════════════════════════════════════════════════
#  TAB 5 – LISTAR PRODUCTOS
# ═══════════════════════════════════════════════════════════


def construir_tab_listar(tab):
    tab.configure(bg=COLOR_PANEL)

    encabezado = tk.Frame(tab, bg=COLOR_PANEL)
    encabezado.pack(fill="x", padx=20, pady=(20, 10))
    estilo_label(encabezado, "Listado de productos", bold=True).pack(side="left")
    estilo_boton(
        encabezado, "↻ Actualizar", lambda: cargar_lista(), color="#555577"
    ).pack(side="right")

    lbl_estado = tk.Label(
        tab, text="", bg=COLOR_PANEL, fg=COLOR_TEXTO_DIM, font=FUENTE_LABEL
    )
    lbl_estado.pack(padx=20, anchor="w")

    # Tabla con Treeview
    frame_tabla = tk.Frame(tab, bg=COLOR_PANEL)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    cols = ("codigo", "nombre", "precio", "stock")
    tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=15)

    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview",
        background=COLOR_ENTRADA,
        foreground=COLOR_TEXTO,
        rowheight=28,
        fieldbackground=COLOR_ENTRADA,
        font=FUENTE_LABEL,
    )
    style.configure(
        "Treeview.Heading",
        background=COLOR_ACENTO,
        foreground="#ffffff",
        font=("Segoe UI", 10, "bold"),
    )
    style.map("Treeview", background=[("selected", COLOR_ACENTO)])

    encab = {
        "codigo": "Código",
        "nombre": "Nombre",
        "precio": "Precio (S/.)",
        "stock": "Stock",
    }
    anchos = {"codigo": 90, "nombre": 250, "precio": 120, "stock": 80}
    for col in cols:
        tree.heading(col, text=encab[col])
        tree.column(col, width=anchos[col], anchor="center" if col != "nombre" else "w")

    scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    def cargar_lista():
        for row in tree.get_children():
            tree.delete(row)
        resultado = listar_productos()
        if resultado["exito"]:
            lbl_estado.config(text=resultado["mensaje"], fg=COLOR_ACENTO2)
            for p in resultado["productos"]:
                tree.insert(
                    "",
                    "end",
                    values=(
                        p["codigo"],
                        p["nombre"],
                        f"{p['precio']:.2f}",
                        p["stock"],
                    ),
                )
        else:
            lbl_estado.config(text=resultado["mensaje"], fg=COLOR_TEXTO_DIM)

    cargar_lista()


# ═══════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════


def main():
    root = tk.Tk()
    root.title("Sistema de Inventario – Grupo B")
    root.geometry("720x560")
    root.minsize(680, 480)
    root.configure(bg=COLOR_FONDO)

    # Encabezado
    header = tk.Frame(root, bg=COLOR_ACENTO, height=56)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(
        header,
        text="📦  Módulo de Inventario",
        bg=COLOR_ACENTO,
        fg="#ffffff",
        font=FUENTE_TITULO,
    ).pack(side="left", padx=20)
    tk.Label(
        header,
        text="Grupo B · UCSM",
        bg=COLOR_ACENTO,
        fg="#d0c8ff",
        font=("Segoe UI", 10),
    ).pack(side="right", padx=20)

    # Notebook (pestañas)
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook", background=COLOR_FONDO, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=COLOR_FONDO,
        foreground=COLOR_TEXTO_DIM,
        padding=[14, 8],
        font=("Segoe UI", 10),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLOR_PANEL)],
        foreground=[("selected", COLOR_ACENTO2)],
    )

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=0, pady=0)

    tabs_config = [
        ("➕ Registrar", construir_tab_registrar),
        ("🔍 Buscar", construir_tab_buscar),
        ("🔄 Stock", construir_tab_stock),
        ("🗑 Eliminar", construir_tab_eliminar),
        ("📋 Listar", construir_tab_listar),
    ]

    for nombre_tab, constructor in tabs_config:
        frame = tk.Frame(notebook, bg=COLOR_PANEL)
        notebook.add(frame, text=nombre_tab)
        constructor(frame)

    root.mainloop()


if __name__ == "__main__":
    main()
