import customtkinter as ctk

from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from simulaciones.ruleta import SimuladorRuleta

from components.table import DataTable


class RuletaPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.modelo = SimuladorRuleta()

        self.df = None

        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.crear_panel()

        self.crear_tabla()
    def crear_panel(self):

        panel = ctk.CTkFrame(self,width=280)

        panel.grid(row=0,column=0,sticky="ns",padx=15,pady=15)

        panel.grid_propagate(False)

        ctk.CTkLabel(
            panel,
            text="Ruleta",
            font=("Segoe UI",22,"bold")
        ).pack(pady=20)

        self.tipo = ctk.CTkComboBox(

            panel,

            values=[

                "Rojo",

                "Negro",

                "Par",

                "Impar"

            ]

        )

        self.tipo.pack(fill="x",padx=20,pady=10)

        self.capital = ctk.CTkEntry(panel,placeholder_text="Capital")

        self.capital.insert(0,"1000")

        self.capital.pack(fill="x",padx=20,pady=10)

        self.apuesta = ctk.CTkEntry(panel,placeholder_text="Apuesta")

        self.apuesta.insert(0,"20")

        self.apuesta.pack(fill="x",padx=20,pady=10)

        self.tiradas = ctk.CTkEntry(panel,placeholder_text="Tiradas")

        self.tiradas.insert(0,"100")

        self.tiradas.pack(fill="x",padx=20,pady=10)

        ctk.CTkButton(

            panel,

            text="Simular",

            command=self.simular

        ).pack(fill="x",padx=20,pady=20)
    def crear_tabla(self):

        derecha = ctk.CTkFrame(self)

        derecha.grid(row=0,column=1,sticky="nsew",padx=15,pady=15)

        derecha.grid_rowconfigure(1,weight=1)

        derecha.grid_columnconfigure(0,weight=1)

        self.figura = Figure(figsize=(7,3),dpi=100)

        self.ax = self.figura.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figura,derecha)

        self.canvas.get_tk_widget().grid(row=0,column=0,sticky="ew")

        self.tabla = DataTable(

            derecha,

            (

                "Tirada",

                "Número",

                "Ganó",

                "Capital"

            )

        )

        self.tabla.grid(

            row=1,

            column=0,

            sticky="nsew"

        )
    def simular(self):

        try:

            self.df = self.modelo.simular(

                self.tipo.get(),

                float(self.capital.get()),

                float(self.apuesta.get()),

                int(self.tiradas.get())

            )

            datos = []

            for _, fila in self.df.iterrows():

                datos.append(

                    (

                        fila["Tirada"],

                        fila["Número"],

                        fila["Ganó"],

                        round(fila["Capital"],2)

                    )

                )

            self.tabla.insertar(datos)

            self.ax.clear()

            self.ax.plot(self.df["Capital"])

            self.ax.set_title("Capital durante la simulación")

            self.canvas.draw()

        except Exception as e:

            messagebox.showerror(

                "Error",

                str(e)

            )