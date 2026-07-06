import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from simulaciones.pseudoaleatorios import GeneradorPseudoaleatorio
from components.table import DataTable


class PseudoaleatoriosPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.generador = GeneradorPseudoaleatorio()
        self.df = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_panel()
        self.crear_tabla()

    # ==================================================

    def crear_panel(self):

        panel = ctk.CTkFrame(self, width=280)
        panel.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        panel.grid_propagate(False)

        ctk.CTkLabel(
            panel,
            text="Pseudoaleatorios",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=20)

        self.algoritmo = ctk.CTkComboBox(
            panel,
            values=[
                "Cuadrados Medios",
                "Productos Medios",
                "Multiplicador Constante",
                "Congruencial Lineal"
            ]
        )
        self.algoritmo.pack(fill="x", padx=20, pady=10)

        self.semilla = ctk.CTkEntry(panel, placeholder_text="Semilla")
        self.semilla.pack(fill="x", padx=20, pady=8)

        self.semilla2 = ctk.CTkEntry(panel, placeholder_text="Segunda semilla")
        self.semilla2.pack(fill="x", padx=20, pady=8)

        self.constante = ctk.CTkEntry(panel, placeholder_text="Constante")
        self.constante.pack(fill="x", padx=20, pady=8)

        self.cantidad = ctk.CTkEntry(panel, placeholder_text="Cantidad")
        self.cantidad.insert(0, "20")
        self.cantidad.pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            panel,
            text="Generar",
            command=self.generar
        ).pack(fill="x", padx=20, pady=20)

        self.lblMin = ctk.CTkLabel(panel, text="Mínimo:")
        self.lblMin.pack()

        self.lblMax = ctk.CTkLabel(panel, text="Máximo:")
        self.lblMax.pack()

        self.lblProm = ctk.CTkLabel(panel, text="Promedio:")
        self.lblProm.pack()

    # ==================================================

    def crear_tabla(self):

        derecha = ctk.CTkFrame(self)
        derecha.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        derecha.grid_rowconfigure(1, weight=1)
        derecha.grid_columnconfigure(0, weight=1)

        # GRAFICA
        self.figura = Figure(figsize=(7, 3), dpi=100)
        self.ax = self.figura.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figura, derecha)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="ew")

        # TABLA (solo DataTable, sin Treeview duplicado)
        self.tabla = DataTable(derecha, ("Semilla", "Ri"))
        self.tabla.grid(row=1, column=0, sticky="nsew")

    # ==================================================

    def generar(self):

        try:
            algoritmo = self.algoritmo.get()
            cantidad = int(self.cantidad.get())

            sem1 = self.semilla.get().strip()
            sem2 = self.semilla2.get().strip()

            if not sem1:
                raise ValueError("Semilla vacía")

            if algoritmo == "Cuadrados Medios":

                self.df = self.generador.cuadrados_medios(
                    sem1,
                    cantidad
                )

            elif algoritmo == "Productos Medios":

                if not sem2:
                    raise ValueError("Segunda semilla requerida")

                self.df = self.generador.productos_medios(
                    sem1,
                    sem2,
                    cantidad
                )

            elif algoritmo == "Multiplicador Constante":

                self.df = self.generador.multiplicador_constante(
                    sem1,
                    int(self.constante.get()),
                    cantidad
                )

            else:

                self.df = self.generador.congruencial(
                    int(sem1),
                    5,
                    7,
                    16,
                    cantidad
                )

            self.actualizar_tabla()
            self.actualizar_grafica()
            self.actualizar_estadisticas()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================================================

    def actualizar_tabla(self):

        datos = [
            (fila["Semilla"], round(fila["Ri"], 4))
            for _, fila in self.df.iterrows()
        ]

        self.tabla.insertar(datos)

    # ==================================================

    def actualizar_grafica(self):

        self.ax.clear()
        self.ax.plot(self.df["Ri"])
        self.ax.set_title("Números Pseudoaleatorios")
        self.canvas.draw()

    # ==================================================

    def actualizar_estadisticas(self):

        self.lblMin.configure(
            text=f"Mínimo: {self.df['Ri'].min():.4f}"
        )

        self.lblMax.configure(
            text=f"Máximo: {self.df['Ri'].max():.4f}"
        )

        self.lblProm.configure(
            text=f"Promedio: {self.df['Ri'].mean():.4f}"
        )