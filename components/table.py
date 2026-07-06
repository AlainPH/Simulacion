import tkinter as tk
from tkinter import ttk


class DataTable(ttk.Frame):

    def __init__(self, master, columnas):

        super().__init__(master)

        self.columnas = columnas

        # ===========================
        # Scroll vertical
        # ===========================

        self.scroll_y = ttk.Scrollbar(
            self,
            orient="vertical"
        )

        self.scroll_y.pack(
            side="right",
            fill="y"
        )

        # ===========================
        # Scroll horizontal
        # ===========================

        self.scroll_x = ttk.Scrollbar(
            self,
            orient="horizontal"
        )

        self.scroll_x.pack(
            side="bottom",
            fill="x"
        )

        # ===========================
        # Tabla
        # ===========================

        self.tree = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        self.scroll_y.config(command=self.tree.yview)
        self.scroll_x.config(command=self.tree.xview)

        for columna in columnas:

            self.tree.heading(columna, text=columna)

            self.tree.column(
                columna,
                width=140,
                anchor="center"
            )

    # =====================================

    def limpiar(self):

        self.tree.delete(*self.tree.get_children())

    # =====================================

    def insertar(self, datos):

        self.limpiar()

        for fila in datos:

            self.tree.insert(
                "",
                tk.END,
                values=fila
            )

    # =====================================

    def obtener_tree(self):

        return self.tree