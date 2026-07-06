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

        self.on_algoritmo_cambiado(self.algoritmo.get())

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
            ],
            command=self.on_algoritmo_cambiado
        )
        self.algoritmo.pack(fill="x", padx=20, pady=10)

        self.inputs_container = ctk.CTkFrame(panel, fg_color="transparent")
        self.inputs_container.pack(fill="x", padx=20, pady=5)

        self.entry_semilla = ctk.CTkEntry(self.inputs_container, placeholder_text="Semilla (X0)")
        self.entry_semilla2 = ctk.CTkEntry(self.inputs_container, placeholder_text="Segunda semilla (X1)")
        self.entry_constante = ctk.CTkEntry(self.inputs_container, placeholder_text="Constante (a)")
        self.entry_multiplicador = ctk.CTkEntry(self.inputs_container, placeholder_text="Multiplicador (a)")
        self.entry_incremento = ctk.CTkEntry(self.inputs_container, placeholder_text="Incremento (c)")
        self.entry_modulo = ctk.CTkEntry(self.inputs_container, placeholder_text="Módulo (m)")
        self.entry_cantidad = ctk.CTkEntry(self.inputs_container, placeholder_text="Cantidad de números")
        
        self.entry_cantidad.insert(0, "20")

        ctk.CTkButton(
            panel,
            text="Generar",
            command=self.generar
        ).pack(fill="x", padx=20, pady=20)

        self.lblMin = ctk.CTkLabel(panel, text="Mínimo: -")
        self.lblMin.pack()

        self.lblMax = ctk.CTkLabel(panel, text="Máximo: -")
        self.lblMax.pack()

        self.lblProm = ctk.CTkLabel(panel, text="Promedio: -")
        self.lblProm.pack()

    # ==================================================

    def on_algoritmo_cambiado(self, algoritmo):
        self.entry_semilla.pack_forget()
        self.entry_semilla2.pack_forget()
        self.entry_constante.pack_forget()
        self.entry_multiplicador.pack_forget()
        self.entry_incremento.pack_forget()
        self.entry_modulo.pack_forget()
        self.entry_cantidad.pack_forget()

        if algoritmo == "Cuadrados Medios":
            self.entry_semilla.configure(placeholder_text="Semilla (X0)")
            self.entry_semilla.pack(fill="x", pady=6)
            self.entry_cantidad.pack(fill="x", pady=6)

        elif algoritmo == "Productos Medios":
            self.entry_semilla.configure(placeholder_text="Semilla 1 (X0)")
            self.entry_semilla.pack(fill="x", pady=6)
            self.entry_semilla2.configure(placeholder_text="Semilla 2 (X1)")
            self.entry_semilla2.pack(fill="x", pady=6)
            self.entry_cantidad.pack(fill="x", pady=6)

        elif algoritmo == "Multiplicador Constante":
            self.entry_semilla.configure(placeholder_text="Semilla (X0)")
            self.entry_semilla.pack(fill="x", pady=6)
            self.entry_constante.configure(placeholder_text="Constante (a)")
            self.entry_constante.pack(fill="x", pady=6)
            self.entry_cantidad.pack(fill="x", pady=6)

        elif algoritmo == "Congruencial Lineal":
            self.entry_semilla.configure(placeholder_text="Semilla (X0)")
            self.entry_semilla.pack(fill="x", pady=6)
            self.entry_multiplicador.configure(placeholder_text="Multiplicador (a)")
            self.entry_multiplicador.pack(fill="x", pady=6)
            self.entry_incremento.configure(placeholder_text="Incremento (c)")
            self.entry_incremento.pack(fill="x", pady=6)
            self.entry_modulo.configure(placeholder_text="Módulo (m)")
            self.entry_modulo.pack(fill="x", pady=6)
            self.entry_cantidad.pack(fill="x", pady=6)

    # ==================================================

    def crear_tabla(self):
        derecha = ctk.CTkFrame(self)
        derecha.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        derecha.grid_rowconfigure(0, weight=1)
        derecha.grid_columnconfigure(0, weight=1)

        # Tabview
        self.tabview = ctk.CTkTabview(derecha)
        self.tabview.pack(fill="both", expand=True)

        self.tab_sim = self.tabview.add("📊 Simulación")
        self.tab_teoria = self.tabview.add("📖 Guía Didáctica")

        self.tab_sim.grid_rowconfigure(1, weight=1)
        self.tab_sim.grid_columnconfigure(0, weight=1)

        # GRAFICA CON DOBLE SUBPLOT (Secuencia + Histograma)
        self.figura = Figure(figsize=(7, 2.5), dpi=100)
        self.ax1 = self.figura.add_subplot(121)
        self.ax2 = self.figura.add_subplot(122)
        self.figura.subplots_adjust(wspace=0.35, bottom=0.22, top=0.85)

        self.canvas = FigureCanvasTkAgg(self.figura, self.tab_sim)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="ew")

        # TABLA
        self.tabla = DataTable(self.tab_sim, ("i", "Semilla", "Ri"))
        self.tabla.grid(row=1, column=0, sticky="nsew")

        # TEXTO DIDÁCTICO CON ESTILOS
        self.txt_teoria = ctk.CTkTextbox(self.tab_teoria, wrap="word", font=("Segoe UI", 13))
        self.txt_teoria.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_guia_didactica()

    def cargar_guia_didactica(self):
        self.txt_teoria.configure(state="normal")
        self.txt_teoria.delete("1.0", "end")

        txt = self.txt_teoria._textbox
        txt.tag_config("title", font=("Segoe UI", 16, "bold"), foreground="#4F8EF7", spacing1=10, spacing3=10)
        txt.tag_config("subtitle", font=("Segoe UI", 13, "bold"), foreground="#2ECC71", spacing1=12, spacing3=4)
        txt.tag_config("code", font=("Consolas", 11), foreground="#F1C40F", background="#1E1F29", spacing1=6, spacing3=6, lmargin1=15, lmargin2=15)
        txt.tag_config("body", font=("Segoe UI", 11), foreground="#E0E0E0", spacing1=3, spacing3=3)
        txt.tag_config("tip", font=("Segoe UI", 11, "italic"), foreground="#E67E22", spacing1=6, spacing3=6, lmargin1=10)

        # Inserción estructurada
        self.txt_teoria.insert("end", "MÉTODOS DE GENERACIÓN DE NÚMEROS PSEUDOALEATORIOS\n\n", "title")
        self.txt_teoria.insert("end", "Los números pseudoaleatorios son secuencias calculadas mediante algoritmos matemáticos deterministas. Aunque no son verdaderamente aleatorios, imitan con gran precisión sus propiedades estadísticas y son la base de la simulación de sistemas.\n\n", "body")
        
        self.txt_teoria.insert("end", "1. CUADRADOS MEDIOS (John von Neumann, 1946)\n", "subtitle")
        self.txt_teoria.insert("end", "• Método: Se eleva una semilla inicial de d dígitos al cuadrado. Si el resultado tiene menos de 2d dígitos, se añaden ceros a la izquierda. Luego, se extraen los d dígitos del centro como la nueva semilla.\n", "body")
        self.txt_teoria.insert("end", "Fórmula:  Xi+1 = Dígitos_Centrales( Xi^2 )  |  Ri = Xi+1 / 10^d\n\n", "code")

        self.txt_teoria.insert("end", "2. PRODUCTOS MEDIOS\n", "subtitle")
        self.txt_teoria.insert("end", "• Método: Similar al anterior, pero utiliza dos semillas iniciales (X0 y X1). En cada paso se multiplican las dos últimas semillas y se extraen los d dígitos del medio.\n", "body")
        self.txt_teoria.insert("end", "Fórmula:  Xi+1 = Dígitos_Centrales( Xi * Xi-1 )  |  Ri = Xi+1 / 10^d\n\n", "code")

        self.txt_teoria.insert("end", "3. MULTIPLICADOR CONSTANTE\n", "subtitle")
        self.txt_teoria.insert("end", "• Método: Multiplica la semilla actual por una constante constante fija 'a' y extrae los d dígitos centrales del producto para obtener la nueva semilla.\n", "body")
        self.txt_teoria.insert("end", "Fórmula:  Xi+1 = Dígitos_Centrales( a * Xi )  |  Ri = Xi+1 / 10^d\n\n", "code")

        self.txt_teoria.insert("end", "4. CONGRUENCIAL LINEAL (D. H. Lehmer, 1951)\n", "subtitle")
        self.txt_teoria.insert("end", "• Método: Es el algoritmo más utilizado comercialmente. Produce una secuencia basada en la aritmética modular.\n", "body")
        self.txt_teoria.insert("end", "Fórmula:  Xi+1 = (a * Xi + c) mod m  |  Ri = Xi+1 / m\n\n", "code")
        self.txt_teoria.insert("end", "Parámetros del modelo:\n  - X0: Semilla inicial (X0 >= 0)\n  - a: Multiplicador (a > 0)\n  - c: Incremento aditivo (c >= 0)\n  - m: Módulo (m > X0, a, c)\n\n", "body")

        self.txt_teoria.insert("end", "💡 CÓMO MEDIR LA CALIDAD DEL GENERADOR:\n", "tip")
        self.txt_teoria.insert("end", "• Observa la gráfica de Distribución (el Histograma de la izquierda). Un buen generador de números pseudoaleatorios debe distribuir sus números de forma uniforme entre 0 y 1. Si generas suficientes números (ej: 500 o 1,000) utilizando el Congruencial Lineal, el histograma debería verse plano y equilibrado, demostrando una distribución uniforme (U[0,1]).\n", "body")
        self.txt_teoria.insert("end", "• Para que el Congruencial Lineal alcance su periodo completo (es decir, genere 'm' números distintos antes de repetirse), debe cumplir las tres condiciones del Teorema de Hull-Dobell:\n  1. c y m son primos relativos (mcd(c, m) = 1).\n  2. a-1 es divisible por todos los factores primos de m.\n  3. Si m es divisible por 4, a-1 también debe serlo.\n", "body")

        self.txt_teoria.configure(state="disabled")

    # ==================================================

    def generar(self):
        try:
            algoritmo = self.algoritmo.get()
            
            cant_str = self.entry_cantidad.get().strip()
            if not cant_str:
                raise ValueError("La cantidad de números es requerida")
            cantidad = int(cant_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
                
            sem_str = self.entry_semilla.get().strip()
            if not sem_str:
                raise ValueError("La Semilla (X0) es requerida")
            semilla = int(sem_str)

            if algoritmo == "Cuadrados Medios":
                if len(sem_str) < 3:
                    raise ValueError("La semilla debe tener al menos 3 dígitos")
                self.df = self.generador.cuadrados_medios(semilla, cantidad)

            elif algoritmo == "Productos Medios":
                sem2_str = self.entry_semilla2.get().strip()
                if not sem2_str:
                    raise ValueError("La Segunda Semilla (X1) es requerida")
                if len(sem_str) != len(sem2_str):
                    raise ValueError("Ambas semillas deben tener la misma longitud")
                if len(sem_str) < 3:
                    raise ValueError("Las semillas deben tener al menos 3 dígitos")
                semilla2 = int(sem2_str)
                self.df = self.generador.productos_medios(semilla, semilla2, cantidad)

            elif algoritmo == "Multiplicador Constante":
                const_str = self.entry_constante.get().strip()
                if not const_str:
                    raise ValueError("La constante (a) es requerida")
                if len(sem_str) < 3:
                    raise ValueError("La semilla debe tener al menos 3 dígitos")
                constante = int(const_str)
                self.df = self.generador.multiplicador_constante(semilla, constante, cantidad)

            elif algoritmo == "Congruencial Lineal":
                mult_str = self.entry_multiplicador.get().strip()
                inc_str = self.entry_incremento.get().strip()
                mod_str = self.entry_modulo.get().strip()
                
                if not mult_str or not inc_str or not mod_str:
                    raise ValueError("Se requieren Multiplicador (a), Incremento (c) y Módulo (m)")
                
                a = int(mult_str)
                c = int(inc_str)
                m = int(mod_str)
                
                if m <= 0:
                    raise ValueError("El módulo (m) debe ser mayor a 0")
                
                self.df = self.generador.congruencial(semilla, a, c, m, cantidad)

            columnas_nuevas = list(self.df.columns)
            self.tabla.actualizar_columnas(columnas_nuevas)

            self.actualizar_tabla()
            self.actualizar_grafica()
            self.actualizar_estadisticas()

        except ValueError as ve:
            messagebox.showerror("Error de Validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar números: {str(e)}")

    # ==================================================

    def actualizar_tabla(self):
        datos = []
        for _, fila in self.df.iterrows():
            valores_fila = []
            for col in self.df.columns:
                val = fila[col]
                if isinstance(val, float):
                    valores_fila.append(round(val, 4))
                else:
                    valores_fila.append(val)
            datos.append(tuple(valores_fila))

        self.tabla.insertar(datos)

    # ==================================================

    def actualizar_grafica(self):
        # Grafico 1: Línea temporal
        self.ax1.clear()
        self.ax1.plot(self.df["i"], self.df["Ri"], marker='o', color='#4F8EF7', linewidth=1, markersize=3)
        self.ax1.set_title("Secuencia de Valores (Ri)", color="white", fontsize=10)
        self.ax1.set_xlabel("Iteración (i)", color="white", fontsize=8)
        self.ax1.set_ylabel("Ri", color="white", fontsize=8)
        self.ax1.tick_params(colors="white", labelsize=8)
        self.ax1.grid(True, color="#2D2F3F", linestyle=":")
        self.ax1.set_facecolor('#1E1F29')

        # Grafico 2: Histograma de frecuencia para ver Uniformidad
        self.ax2.clear()
        self.ax2.hist(self.df["Ri"], bins=10, range=(0.0, 1.0), color='#2ECC71', edgecolor='#1E1F29', alpha=0.8)
        self.ax2.set_title("Distribución (Frecuencia)", color="white", fontsize=10)
        self.ax2.set_xlabel("Intervalo Ri", color="white", fontsize=8)
        self.ax2.set_ylabel("Frecuencia", color="white", fontsize=8)
        self.ax2.tick_params(colors="white", labelsize=8)
        self.ax2.grid(True, color="#2D2F3F", linestyle=":", axis="y")
        self.ax2.set_facecolor('#1E1F29')

        self.figura.patch.set_facecolor('#1E1F29')
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