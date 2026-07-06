import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from simulaciones.automata import AutomataCelular


class AutomataPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.generador = AutomataCelular()
        
        # Variables de control de simulación
        self.grid_history = None
        self.running = False
        self.current_gen = 0
        self.delay = 30
        self.regla_seleccionada = 30
        self.columnas = 151
        self.generaciones = 100
        self.estado_inicial = "single"

        self.crear_interfaz()

    def crear_interfaz(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= PANEL IZQUIERDO =================
        panel = ctk.CTkFrame(self, width=300)
        panel.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        panel.grid_propagate(False)

        titulo = ctk.CTkLabel(
            panel,
            text="AUTÓMATAS CELULARES",
            font=("Segoe UI", 20, "bold")
        )
        titulo.pack(pady=(20, 15))

        # ---------------- Regla de Wolfram ----------------
        ctk.CTkLabel(panel, text="Regla de Wolfram (0-255)").pack(anchor="w", padx=20)
        self.combo_regla = ctk.CTkComboBox(
            panel,
            values=["30", "90", "110", "150", "184", "250"]
        )
        self.combo_regla.set("30")
        self.combo_regla.pack(fill="x", padx=20, pady=(0, 10))

        # ---------------- Columnas (Ancho) ----------------
        ctk.CTkLabel(panel, text="Ancho de la cuadrícula (celdas)").pack(anchor="w", padx=20)
        self.entry_columnas = ctk.CTkEntry(panel)
        self.entry_columnas.insert(0, "151")
        self.entry_columnas.pack(fill="x", padx=20, pady=(0, 10))

        # ---------------- Generaciones (Alto) ----------------
        ctk.CTkLabel(panel, text="Generaciones (tiempo)").pack(anchor="w", padx=20)
        self.entry_generaciones = ctk.CTkEntry(panel)
        self.entry_generaciones.insert(0, "100")
        self.entry_generaciones.pack(fill="x", padx=20, pady=(0, 10))

        # ---------------- Estado Inicial ----------------
        ctk.CTkLabel(panel, text="Estado inicial").pack(anchor="w", padx=20)
        self.combo_inicial = ctk.CTkComboBox(
            panel,
            values=["Celda única al centro", "Estado aleatorio"]
        )
        self.combo_inicial.set("Celda única al centro")
        self.combo_inicial.pack(fill="x", padx=20, pady=(0, 10))

        # ---------------- Velocidad de animación ----------------
        ctk.CTkLabel(panel, text="Velocidad de animación (ms)").pack(anchor="w", padx=20)
        self.slider_velocidad = ctk.CTkSlider(
            panel,
            from_=5,
            to=200,
            number_of_steps=40,
            command=self.cambiar_velocidad
        )
        self.slider_velocidad.set(30)
        self.slider_velocidad.pack(fill="x", padx=20, pady=(0, 20))

        # ---------------- Botones de acción ----------------
        self.btn_generar = ctk.CTkButton(
            panel,
            text="⚡ Generar Completo",
            height=35,
            command=self.generar_completo
        )
        self.btn_generar.pack(fill="x", padx=20, pady=5)

        self.btn_animar = ctk.CTkButton(
            panel,
            text="▶ Animar Simulación",
            height=35,
            command=self.iniciar_animacion
        )
        self.btn_animar.pack(fill="x", padx=20, pady=5)

        self.btn_pausar = ctk.CTkButton(
            panel,
            text="⏸ Pausar",
            height=35,
            state="disabled",
            command=self.pausar
        )
        self.btn_pausar.pack(fill="x", padx=20, pady=5)

        self.btn_reiniciar = ctk.CTkButton(
            panel,
            text="⟳ Limpiar",
            height=35,
            command=self.reiniciar
        )
        self.btn_reiniciar.pack(fill="x", padx=20, pady=5)

        # Info del estado
        self.lbl_info = ctk.CTkLabel(panel, text="Generación actual: 0 / 0", font=("Segoe UI", 12, "italic"))
        self.lbl_info.pack(pady=15)

        # ================= PANEL DERECHO =================
        self.derecha = ctk.CTkFrame(self)
        self.derecha.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.derecha.grid_rowconfigure(0, weight=1)
        self.derecha.grid_columnconfigure(0, weight=1)

        # Tabview didáctico
        self.tabview = ctk.CTkTabview(self.derecha)
        self.tabview.pack(fill="both", expand=True)

        self.tab_visual = self.tabview.add("📊 Visualización")
        self.tab_teoria = self.tabview.add("📖 Guía Didáctica")

        # Matplotlib Figure dentro del tab de visualización
        self.figura = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_facecolor("#1E1F29")
        self.figura.patch.set_facecolor("#1E1F29")
        
        self.canvas_matplotlib = FigureCanvasTkAgg(self.figura, self.tab_visual)
        self.canvas_matplotlib.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Texto explicativo en el tab de teoría
        self.txt_teoria = ctk.CTkTextbox(self.tab_teoria, wrap="word", font=("Segoe UI", 13))
        self.txt_teoria.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_guia_didactica()
        self.limpiar_grafico()

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
        self.txt_teoria.insert("end", "AUTÓMATAS CELULARES 1D (REGLAS DE WOLFRAM)\n\n", "title")
        self.txt_teoria.insert("end", "Un autómata celular es un modelo dinámico y matemático compuesto por una rejilla de celdas cuyos estados se actualizan en pasos discretos de tiempo de acuerdo con reglas lógicas de vecindario.\n\n", "body")
        
        self.txt_teoria.insert("end", "1. MECÁNICA Y VECINDARIO DE WOLFRAM\n", "subtitle")
        self.txt_teoria.insert("end", "• En un autómata 1D, el nuevo estado de una celda depende de su estado actual y del de sus dos vecinas inmediatas (izquierda y derecha). Existen 8 posibles configuraciones iniciales para este trío:\n", "body")
        self.txt_teoria.insert("end", "  [111, 110, 101, 100, 011, 010, 001, 000]\n\n", "code")
        self.txt_teoria.insert("end", "• Una regla de Wolfram es simplemente un número del 0 al 255. La representación binaria de este número de 8 bits especifica el resultado (0 o 1) para cada uno de los 8 vecindarios anteriores en orden inverso.\n", "body")
        self.txt_teoria.insert("end", "Ejemplo: Regla 30 = 00011110 en binario. Indica que una celda se activará en el paso siguiente solo si su vecindario coincide con los estados 100, 011, 010 o 001.\n\n", "body")

        self.txt_teoria.insert("end", "2. LAS 4 CLASES DE WOLFRAM PARA LA COMPLEJIDAD\n", "subtitle")
        self.txt_teoria.insert("end", "Stephen Wolfram clasificó los autómatas celulares en 4 grupos según su evolución a largo plazo:\n", "body")
        self.txt_teoria.insert("end", "• Clase 1: Colapso rápido hacia un estado homogéneo uniforme (todas las celdas apagadas o encendidas. Ej: Regla 0 o 250).\n", "body")
        self.txt_teoria.insert("end", "• Clase 2: Convergencia a estructuras periódicas, repetitivas o estables en el tiempo (Ej: Regla 90, Regla 184).\n", "body")
        self.txt_teoria.insert("end", "• Clase 3: Comportamiento completamente caótico, aperiódico y pseudoaleatorio (Ej: Regla 30, utilizada para la generación de ruido y llaves criptográficas).\n", "body")
        self.txt_teoria.insert("end", "• Clase 4: Autoorganización compleja. Aparecen estructuras locales estables que se desplazan e interactúan de forma lógica (Ej: Regla 110).\n\n", "body")

        self.txt_teoria.insert("end", "💡 REGLAS QUE TIENES QUE PROBAR:\n", "tip")
        self.txt_teoria.insert("end", "• Regla 90: Crea la estructura del famoso Triángulo de Sierpinski, un patrón fractal autosemejante de gran belleza geométrica.\n", "body")
        self.txt_teoria.insert("end", "• Regla 110: ¡Es universalmente Turing completa! Puede emular cualquier programa de computadora si se diseña el estado inicial adecuado, demostrando que sistemas hiper-simples pueden computar información compleja.\n", "body")

        self.txt_teoria.configure(state="disabled")

    def cambiar_velocidad(self, valor):
        self.delay = int(valor)

    def validar_parametros(self):
        try:
            regla = int(self.combo_regla.get())
            if not (0 <= regla <= 255):
                raise ValueError("La regla debe estar entre 0 y 255")
            
            columnas = int(self.entry_columnas.get())
            if columnas <= 2 or columnas % 2 == 0:
                columnas = columnas + 1 if columnas % 2 == 0 else columnas
                self.entry_columnas.delete(0, tk.END)
                self.entry_columnas.insert(0, str(columnas))
                
            generaciones = int(self.entry_generaciones.get())
            if generaciones <= 0:
                raise ValueError("Las generaciones deben ser mayores a 0")
            
            estado = "single" if "centro" in self.combo_inicial.get().lower() else "random"
            
            self.regla_seleccionada = regla
            self.columnas = columnas
            self.generaciones = generaciones
            self.estado_inicial = estado
            return True
        except ValueError as ve:
            messagebox.showerror("Parámetros Inválidos", str(ve))
            return False

    def limpiar_grafico(self):
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Haz clic en 'Generar' para iniciar la simulación\no 'Animar' para verla paso a paso", 
                     color="white", ha="center", va="center", transform=self.ax.transAxes, fontsize=12)
        self.ax.axis('off')
        self.canvas_matplotlib.draw()

    def generar_completo(self):
        self.running = False
        self.btn_pausar.configure(state="disabled")
        self.btn_animar.configure(state="normal")
        
        if not self.validar_parametros():
            return
            
        self.grid_history = self.generador.simular(
            self.regla_seleccionada,
            self.columnas,
            self.generaciones,
            self.estado_inicial
        )
        
        self.actualizar_grafica_completa()
        self.lbl_info.configure(text=f"Generación actual: {self.generaciones} / {self.generaciones}")

    def iniciar_animacion(self):
        if not self.validar_parametros():
            return

        self.running = True
        self.btn_pausar.configure(state="normal")
        self.btn_animar.configure(state="disabled")
        self.btn_generar.configure(state="disabled")
        
        self.grid_history = self.generador.simular(
            self.regla_seleccionada,
            self.columnas,
            self.generaciones,
            self.estado_inicial
        )
        
        self.current_gen = 1
        self.animar_paso()

    def animar_paso(self):
        if not self.running:
            return

        if self.current_gen > self.generaciones:
            self.running = False
            self.btn_pausar.configure(state="disabled")
            self.btn_animar.configure(state="normal")
            self.btn_generar.configure(state="normal")
            return

        sub_grid = self.grid_history[:self.current_gen]
        full_display_grid = np.zeros((self.generaciones, self.columnas), dtype=np.uint8)
        full_display_grid[:self.current_gen] = sub_grid

        self.ax.clear()
        self.ax.imshow(full_display_grid, cmap="Blues", interpolation="nearest", aspect="auto")
        self.ax.set_title(f"Autómata Celular - Regla {self.regla_seleccionada} (Gen {self.current_gen}/{self.generaciones})", color="white")
        self.ax.axis("off")
        self.canvas_matplotlib.draw()
        
        self.lbl_info.configure(text=f"Generación actual: {self.current_gen} / {self.generaciones}")
        self.current_gen += 1

        self.after(self.delay, self.animar_paso)

    def pausar(self):
        self.running = False
        self.btn_pausar.configure(state="disabled")
        self.btn_animar.configure(state="normal")
        self.btn_generar.configure(state="normal")

    def reiniciar(self):
        self.running = False
        self.grid_history = None
        self.current_gen = 0
        self.btn_pausar.configure(state="disabled")
        self.btn_animar.configure(state="normal")
        self.btn_generar.configure(state="normal")
        self.lbl_info.configure(text="Generación actual: 0 / 0")
        self.limpiar_grafico()

    def actualizar_grafica_completa(self):
        self.ax.clear()
        self.ax.imshow(self.grid_history, cmap="Blues", interpolation="nearest", aspect="auto")
        self.ax.set_title(f"Autómata Celular - Regla {self.regla_seleccionada}", color="white")
        self.ax.axis("off")
        self.canvas_matplotlib.draw()