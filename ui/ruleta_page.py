import customtkinter as ctk
import tkinter as tk
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
        panel = ctk.CTkFrame(self, width=280)
        panel.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        panel.grid_propagate(False)

        ctk.CTkLabel(
            panel,
            text="Simulador Ruleta",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(panel, text="Tipo de Apuesta").pack(anchor="w", padx=20)
        self.tipo = ctk.CTkComboBox(
            panel,
            values=["Rojo", "Negro", "Par", "Impar"]
        )
        self.tipo.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(panel, text="Capital Inicial ($)").pack(anchor="w", padx=20)
        self.capital = ctk.CTkEntry(panel, placeholder_text="Capital")
        self.capital.insert(0, "1000")
        self.capital.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(panel, text="Monto de Apuesta ($)").pack(anchor="w", padx=20)
        self.apuesta = ctk.CTkEntry(panel, placeholder_text="Apuesta")
        self.apuesta.insert(0, "20")
        self.apuesta.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(panel, text="Número de Tiradas").pack(anchor="w", padx=20)
        self.tiradas = ctk.CTkEntry(panel, placeholder_text="Tiradas")
        self.tiradas.insert(0, "100")
        self.tiradas.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkButton(
            panel,
            text="Simular Ruleta",
            command=self.simular
        ).pack(fill="x", padx=20, pady=10)

    def crear_tabla(self):
        derecha = ctk.CTkFrame(self)
        derecha.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        derecha.grid_rowconfigure(0, weight=1)
        derecha.grid_columnconfigure(0, weight=1)

        # Tabview para hacer el diseño didáctico
        self.tabview = ctk.CTkTabview(derecha)
        self.tabview.pack(fill="both", expand=True)

        self.tab_sim = self.tabview.add("📊 Simulación")
        self.tab_teoria = self.tabview.add("📖 Guía Didáctica")

        self.tab_sim.grid_rowconfigure(1, weight=1)
        self.tab_sim.grid_columnconfigure(0, weight=1)

        # Contenedor superior para Gráfica y Scoreboard
        top_frame = ctk.CTkFrame(self.tab_sim, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # GRAFICA
        self.figura = Figure(figsize=(5, 2.5), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_facecolor('#1E1F29')
        self.figura.patch.set_facecolor('#1E1F29')

        self.canvas = FigureCanvasTkAgg(self.figura, top_frame)
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        # SCOREBOARD (Panel de casino real)
        self.scoreboard = ctk.CTkFrame(
            top_frame,
            width=200,
            fg_color="#252836",
            border_color="#3E4256",
            border_width=1,
            corner_radius=12
        )
        self.scoreboard.pack(side="right", fill="y", padx=(10, 0))
        self.scoreboard.pack_propagate(False)

        ctk.CTkLabel(
            self.scoreboard,
            text="ÚLTIMO NÚMERO",
            font=("Segoe UI", 11, "bold"),
            text_color="#BBBBBB"
        ).pack(pady=(12, 5))

        self.lbl_big_number = ctk.CTkLabel(
            self.scoreboard,
            text="-",
            font=("Segoe UI", 36, "bold"),
            text_color="white",
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#2F3242"
        )
        self.lbl_big_number.pack(pady=5)

        self.lbl_number_details = ctk.CTkLabel(
            self.scoreboard,
            text="",
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        )
        self.lbl_number_details.pack(pady=(0, 10))

        # Historial horizontal
        ctk.CTkLabel(
            self.scoreboard,
            text="HISTORIAL RECIENTE",
            font=("Segoe UI", 9, "bold"),
            text_color="#BBBBBB"
        ).pack(pady=(5, 3))

        self.history_row = ctk.CTkFrame(self.scoreboard, fg_color="transparent")
        self.history_row.pack(fill="x", padx=10)

        self.history_labels = []
        for _ in range(6):
            lbl = ctk.CTkLabel(
                self.history_row,
                text="-",
                font=("Segoe UI", 11, "bold"),
                text_color="white",
                width=24,
                height=24,
                corner_radius=12,
                fg_color="#2F3242"
            )
            lbl.pack(side="left", padx=2, expand=True)
            self.history_labels.append(lbl)

        # TABLA
        self.tabla = DataTable(
            self.tab_sim,
            ("Tirada", "Número", "Ganó", "Capital")
        )
        self.tabla.grid(row=1, column=0, sticky="nsew")

        # CONTENIDO DIDÁCTICO
        self.txt_teoria = ctk.CTkTextbox(self.tab_teoria, wrap="word", font=("Segoe UI", 13))
        self.txt_teoria.pack(fill="both", expand=True, padx=10, pady=10)

        teoria_texto = (
            "SIMULACIÓN DE RULETA Y EL MÉTODO MONTE CARLO\n\n"
            "El método de Monte Carlo utiliza el muestreo aleatorio repetido para obtener resultados "
            "numéricos estimativos. La ruleta es una excelente herramienta física para ilustrar "
            "este concepto matemático.\n\n"
            "1. LEY DE LOS GRANDES NÚMEROS\n"
            "• Esta ley indica que a medida que aumenta la cantidad de ensayos (tiradas de ruleta), la "
            "frecuencia observada de victorias y pérdidas converge hacia su valor de probabilidad matemática real.\n"
            "• Si simulas 10 tiradas, podrías ganar el 80% de las veces debido a la varianza a corto plazo. Pero "
            "si simulas 10,000 tiradas, verás cómo tu tasa de aciertos se acerca inevitablemente al valor teórico (48.6%).\n\n"
            "2. LA VENTAJA DE LA CASA (El Cero)\n"
            "• En la ruleta europea hay 37 casillas: del 1 al 36 (mitad rojos, mitad negros) y el 0 (verde).\n"
            "• Si apuestas a Rojo, ganas si cae en las 18 casillas rojas. Pierdes si cae en las 18 negras o en el 0.\n"
            "• Probabilidad de ganar: 18 / 37 = 48.65%.\n"
            "• Probabilidad de perder: 19 / 37 = 51.35%.\n"
            "• La ventaja matemática del casino es del 2.70%. A largo plazo, el capital del jugador decrece de forma continua "
            "debido a este pequeño sesgo en la probabilidad.\n\n"
            "3. LA RUINA DEL JUGADOR\n"
            "• Es el fenómeno matemático donde un jugador que juega con capital finito contra un oponente de capital "
            "infinito (el casino) que posee una ventaja matemática, eventualmente irá a la quiebra independientemente de "
            "su estrategia de apuestas."
        )
        self.txt_teoria.insert("0.0", teoria_texto)
        self.txt_teoria.configure(state="disabled")

    def simular(self):
        try:
            cap = float(self.capital.get())
            ap = float(self.apuesta.get())
            tir = int(self.tiradas.get())

            if cap <= 0 or ap <= 0 or tir <= 0:
                raise ValueError("Todos los valores numéricos deben ser mayores a 0")
            if ap > cap:
                raise ValueError("El monto de la apuesta no puede ser mayor que tu capital inicial")

            self.df = self.modelo.simular(self.tipo.get(), cap, ap, tir)

            datos = []
            for _, fila in self.df.iterrows():
                datos.append((
                    int(fila["Tirada"]),
                    int(fila["Número"]),
                    "Sí" if fila["Ganó"] == "Sí" else "No",
                    round(fila["Capital"], 2)
                ))

            self.tabla.insertar(datos)

            # Actualizar gráfico
            self.ax.clear()
            self.ax.plot(self.df["Tirada"], self.df["Capital"], color="#E74C3C", linewidth=2)
            self.ax.axhline(y=cap, color="white", linestyle="--", alpha=0.5, label="Capital Inicial")
            self.ax.set_title("Capital durante la simulación", color="white")
            self.ax.set_xlabel("Número de Tirada", color="white")
            self.ax.set_ylabel("Capital ($)", color="white")
            self.ax.tick_params(colors="white")
            self.ax.grid(True, color="#2D2F3F", linestyle=":")
            self.ax.legend(facecolor="#252836", labelcolor="white")
            self.canvas.draw()

            # Actualizar Scoreboard
            if not self.df.empty:
                rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
                
                # Último número
                ultimo_num = int(self.df.iloc[-1]["Número"])
                if ultimo_num == 0:
                    bg_col = "#2ecc71"  # Verde
                    lbl_col = "Verde"
                    lbl_par = "Cero"
                else:
                    bg_col = "#e74c3c" if ultimo_num in rojos else "#1A1A1A"
                    lbl_col = "Rojo" if ultimo_num in rojos else "Negro"
                    lbl_par = "Par" if ultimo_num % 2 == 0 else "Impar"
                
                self.lbl_big_number.configure(text=str(ultimo_num), fg_color=bg_col)
                self.lbl_number_details.configure(text=f"{lbl_col} | {lbl_par}")

                # Historial reciente (últimos 6 números)
                historial = self.df.tail(6)["Número"].tolist()
                while len(historial) < 6:
                    historial.insert(0, None)
                
                for idx, num in enumerate(historial):
                    lbl = self.history_labels[idx]
                    if num is None:
                        lbl.configure(text="-", fg_color="#2F3242")
                    else:
                        num = int(num)
                        if num == 0:
                            lbl.configure(text="0", fg_color="#2ecc71")
                        else:
                            bg_h = "#e74c3c" if num in rojos else "#1A1A1A"
                            lbl.configure(text=str(num), fg_color=bg_h)

        except ValueError as ve:
            messagebox.showerror("Parámetros Inválidos", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))