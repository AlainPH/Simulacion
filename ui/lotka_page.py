import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from simulaciones.lotka import GeneradorLotkaVolterra


class LotkaPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.generador = GeneradorLotkaVolterra()
        
        self.crear_interfaz()

    def crear_interfaz(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= PANEL IZQUIERDO =================
        panel = ctk.CTkFrame(self, width=320)
        panel.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        panel.grid_propagate(False)

        titulo = ctk.CTkLabel(
            panel,
            text="MODELO LOTKA-VOLTERRA",
            font=("Segoe UI", 18, "bold")
        )
        titulo.pack(pady=(20, 15))

        # ---------------- Presas Iniciales (X0) ----------------
        ctk.CTkLabel(panel, text="Población inicial de Presas (X0)").pack(anchor="w", padx=20)
        self.entry_x0 = ctk.CTkEntry(panel)
        self.entry_x0.insert(0, "40.0")
        self.entry_x0.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Depredadores Iniciales (Y0) ----------------
        ctk.CTkLabel(panel, text="Población inicial de Depredadores (Y0)").pack(anchor="w", padx=20)
        self.entry_y0 = ctk.CTkEntry(panel)
        self.entry_y0.insert(0, "9.0")
        self.entry_y0.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Alpha (Crecimiento Presas) ----------------
        ctk.CTkLabel(panel, text="Crecimiento de Presas (\u03b1)").pack(anchor="w", padx=20)
        self.entry_alpha = ctk.CTkEntry(panel)
        self.entry_alpha.insert(0, "0.1")
        self.entry_alpha.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Beta (Tasa de Depredación) ----------------
        ctk.CTkLabel(panel, text="Tasa de Depredación (\u03b2)").pack(anchor="w", padx=20)
        self.entry_beta = ctk.CTkEntry(panel)
        self.entry_beta.insert(0, "0.02")
        self.entry_beta.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Gamma (Muerte Depredadores) ----------------
        ctk.CTkLabel(panel, text="Mortalidad Depredadores (\u03b3)").pack(anchor="w", padx=20)
        self.entry_gamma = ctk.CTkEntry(panel)
        self.entry_gamma.insert(0, "0.3")
        self.entry_gamma.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Delta (Eficiencia Depredadores) ----------------
        ctk.CTkLabel(panel, text="Crecimiento Depredadores (\u03b4)").pack(anchor="w", padx=20)
        self.entry_delta = ctk.CTkEntry(panel)
        self.entry_delta.insert(0, "0.01")
        self.entry_delta.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Configuración Simulación ----------------
        ctk.CTkLabel(panel, text="Paso de tiempo (dt) / Pasos").pack(anchor="w", padx=20)
        config_frame = ctk.CTkFrame(panel, fg_color="transparent")
        config_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.entry_dt = ctk.CTkEntry(config_frame, placeholder_text="dt", width=70)
        self.entry_dt.insert(0, "0.1")
        self.entry_dt.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.entry_pasos = ctk.CTkEntry(config_frame, placeholder_text="pasos", width=120)
        self.entry_pasos.insert(0, "1000")
        self.entry_pasos.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # ---------------- Botones ----------------
        self.btn_generar = ctk.CTkButton(
            panel,
            text="📈 Graficar Modelo",
            height=35,
            command=self.simular
        )
        self.btn_generar.pack(fill="x", padx=20, pady=5)

        self.btn_presets = ctk.CTkComboBox(
            panel,
            values=["Preset: Ciclo Estable", "Preset: Extinción Depredador", "Preset: Explosión de Población"],
            command=self.aplicar_preset
        )
        self.btn_presets.set("Cargar Preset...")
        self.btn_presets.pack(fill="x", padx=20, pady=5)

        # Info del estado
        self.lbl_stats = ctk.CTkLabel(
            panel, 
            text="Presas máx: -\nDepredadores máx: -", 
            justify="left", 
            font=("Segoe UI", 12, "italic")
        )
        self.lbl_stats.pack(pady=15)

        # ================= PANEL DERECHO =================
        self.derecha = ctk.CTkFrame(self)
        self.derecha.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.derecha.grid_rowconfigure(0, weight=1)
        self.derecha.grid_columnconfigure(0, weight=1)

        # Tabview didáctico
        self.tabview = ctk.CTkTabview(self.derecha)
        self.tabview.pack(fill="both", expand=True)

        self.tab_visual = self.tabview.add("📊 Simulación y Órbitas")
        self.tab_teoria = self.tabview.add("📖 Guía Didáctica")

        # Matplotlib Figure dentro del tab_visual
        self.figura = Figure(figsize=(8, 6), dpi=100)
        self.ax1 = self.figura.add_subplot(211)  # Series temporales
        self.ax2 = self.figura.add_subplot(212)  # Plano de fase

        self.ax1.set_facecolor("#1E1F29")
        self.ax2.set_facecolor("#1E1F29")
        self.figura.patch.set_facecolor("#1E1F29")
        self.figura.subplots_adjust(hspace=0.4, top=0.92, bottom=0.15)

        self.canvas_matplotlib = FigureCanvasTkAgg(self.figura, self.tab_visual)
        self.canvas_matplotlib.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Texto didáctico en tab_teoria
        self.txt_teoria = ctk.CTkTextbox(self.tab_teoria, wrap="word", font=("Segoe UI", 13))
        self.txt_teoria.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_guia_didactica()
        self.limpiar_graficos()

    def cargar_guia_didactica(self):
        self.txt_teoria.configure(state="normal")
        self.txt_teoria.delete("1.0", "end")

        txt = self.txt_teoria._textbox
        txt.tag_config("title", font=("Segoe UI", 16, "bold"), foreground="#4F8EF7", spacing1=10, spacing3=10)
        txt.tag_config("subtitle", font=("Segoe UI", 13, "bold"), foreground="#2ECC71", spacing1=12, spacing3=4)
        txt.tag_config("code", font=("Consolas", 11), foreground="#F1C40F", background="#1E1F29", spacing1=6, spacing3=6, lmargin1=15, lmargin2=15)
        txt.tag_config("body", font=("Segoe UI", 11), foreground="#E0E0E0", spacing1=3, spacing3=3)
        txt.tag_config("tip", font=("Segoe UI", 11, "italic"), foreground="#E67E22", spacing1=6, spacing3=6, lmargin1=10)

        self.txt_teoria.insert("end", "MODELO PREDADOR-PRESA DE LOTKA-VOLTERRA\n\n", "title")
        self.txt_teoria.insert("end", "El modelo de Lotka-Volterra es un sistema acoplado de ecuaciones diferenciales de primer orden no lineales. Describe la relación poblacional de dos especies biológicas en interacción recíproca (presa y depredador).\n\n", "body")
        
        self.txt_teoria.insert("end", "1. LAS ECUACIONES DE CAMBIO DINÁMICO\n", "subtitle")
        self.txt_teoria.insert("end", "• Ecuación de Presas (X):\n", "body")
        self.txt_teoria.insert("end", "  dX / dt = alpha * X  -  beta * X * Y\n\n", "code")
        self.txt_teoria.insert("end", "  - alpha: Tasa natural de reproducción de las presas en ausencia de predadores.\n  - beta: Tasa de encuentros destructivos entre presas y depredadores.\n\n• Ecuación de Depredadores (Y):\n", "body")
        self.txt_teoria.insert("end", "  dY / dt = delta * X * Y  -  gamma * Y\n\n", "code")
        self.txt_teoria.insert("end", "  - delta: Eficiencia alimenticia (nacimientos de depredadores basados en presas consumidas).\n  - gamma: Tasa natural de mortalidad de depredadores si no hay alimento.\n\n", "body")

        self.txt_teoria.insert("end", "2. INTERPRETACIÓN DE LOS RESULTADOS GRÁFICOS\n", "subtitle")
        self.txt_teoria.insert("end", "• Evolución Temporal (Arriba):\n  Muestra oscilaciones periódicas continuas. Observa que el pico de la población de depredadores (línea roja) ocurre desfasado (más tarde) que el de presas (línea verde), ya que el depredador solo prospera tras el incremento de su alimento.\n\n• Plano de Fase (Abajo):\n  Grafica Presas (X) frente a Depredadores (Y) eliminando la variable tiempo. Dibuja órbitas cerradas estables. El centro geométrico de estas órbitas representa el punto de equilibrio estacionario del sistema ecológico.\n\n", "body")

        self.txt_teoria.insert("end", "💡 ANÁLISIS PRÁCTICO:\n", "tip")
        self.txt_teoria.insert("end", "• Carga el preset 'Extinción Depredador' para simular un escenario donde la baja población inicial y alta mortalidad del depredador hace que desaparezcan, ocasionando que la población de presas (verde) se dispare sin límites biológicos.\n", "body")

        self.txt_teoria.configure(state="disabled")

    def aplicar_preset(self, preset):
        if preset == "Preset: Ciclo Estable":
            self.entry_x0.delete(0, tk.END); self.entry_x0.insert(0, "40.0")
            self.entry_y0.delete(0, tk.END); self.entry_y0.insert(0, "9.0")
            self.entry_alpha.delete(0, tk.END); self.entry_alpha.insert(0, "0.1")
            self.entry_beta.delete(0, tk.END); self.entry_beta.insert(0, "0.02")
            self.entry_gamma.delete(0, tk.END); self.entry_gamma.insert(0, "0.3")
            self.entry_delta.delete(0, tk.END); self.entry_delta.insert(0, "0.01")
            self.entry_dt.delete(0, tk.END); self.entry_dt.insert(0, "0.1")
            self.entry_pasos.delete(0, tk.END); self.entry_pasos.insert(0, "1000")
        elif preset == "Preset: Extinción Depredador":
            self.entry_x0.delete(0, tk.END); self.entry_x0.insert(0, "15.0")
            self.entry_y0.delete(0, tk.END); self.entry_y0.insert(0, "0.5")
            self.entry_alpha.delete(0, tk.END); self.entry_alpha.insert(0, "0.2")
            self.entry_beta.delete(0, tk.END); self.entry_beta.insert(0, "0.05")
            self.entry_gamma.delete(0, tk.END); self.entry_gamma.insert(0, "0.8")
            self.entry_delta.delete(0, tk.END); self.entry_delta.insert(0, "0.01")
            self.entry_dt.delete(0, tk.END); self.entry_dt.insert(0, "0.1")
            self.entry_pasos.delete(0, tk.END); self.entry_pasos.insert(0, "600")
        elif preset == "Preset: Explosión de Población":
            self.entry_x0.delete(0, tk.END); self.entry_x0.insert(0, "80.0")
            self.entry_y0.delete(0, tk.END); self.entry_y0.insert(0, "30.0")
            self.entry_alpha.delete(0, tk.END); self.entry_alpha.insert(0, "0.5")
            self.entry_beta.delete(0, tk.END); self.entry_beta.insert(0, "0.03")
            self.entry_gamma.delete(0, tk.END); self.entry_gamma.insert(0, "0.2")
            self.entry_delta.delete(0, tk.END); self.entry_delta.insert(0, "0.005")
            self.entry_dt.delete(0, tk.END); self.entry_dt.insert(0, "0.05")
            self.entry_pasos.delete(0, tk.END); self.entry_pasos.insert(0, "1500")

    def limpiar_graficos(self):
        self.ax1.clear()
        self.ax2.clear()

        self.ax1.text(0.5, 0.5, "Presiona 'Graficar Modelo' para iniciar la simulación", 
                      color="white", ha="center", va="center", transform=self.ax1.transAxes)
        self.ax1.axis('off')
        
        self.ax2.text(0.5, 0.5, "Espacio de fases (Depredador vs Presa)", 
                      color="white", ha="center", va="center", transform=self.ax2.transAxes)
        self.ax2.axis('off')

        self.canvas_matplotlib.draw()

    def simular(self):
        try:
            x0 = float(self.entry_x0.get())
            y0 = float(self.entry_y0.get())
            alpha = float(self.entry_alpha.get())
            beta = float(self.entry_beta.get())
            gamma = float(self.entry_gamma.get())
            delta = float(self.entry_delta.get())
            dt = float(self.entry_dt.get())
            pasos = int(self.entry_pasos.get())

            if min(x0, y0, alpha, beta, gamma, delta, dt) < 0 or pasos <= 0:
                raise ValueError("Todos los valores numéricos deben ser no-negativos y pasos > 0")

            t, x, y = self.generador.simular(x0, y0, alpha, beta, gamma, delta, dt, pasos)

            # Graficar series temporales
            self.ax1.clear()
            self.ax1.axis('on')
            self.ax1.plot(t, x, color="#2ecc71", label="Presas (X)", linewidth=2)
            self.ax1.plot(t, y, color="#e74c3c", label="Depredadores (Y)", linewidth=2)
            self.ax1.set_title("Evolución Temporal de las Poblaciones", color="white", fontsize=11)
            self.ax1.set_xlabel("Tiempo", color="white")
            self.ax1.set_ylabel("Población", color="white")
            self.ax1.tick_params(colors="white")
            self.ax1.legend(facecolor="#252836", labelcolor="white")
            self.ax1.grid(True, linestyle="--", alpha=0.3)

            # Graficar espacio de fases
            self.ax2.clear()
            self.ax2.axis('on')
            self.ax2.plot(x, y, color="#4f8ef7", linewidth=2)
            self.ax2.scatter([x0], [y0], color="yellow", label="Inicio (x0, y0)", zorder=5)
            self.ax2.set_title("Plano de Fase (Órbita de Interacción)", color="white", fontsize=11)
            self.ax2.set_xlabel("Población de Presas (X)", color="white")
            self.ax2.set_ylabel("Población de Depredadores (Y)", color="white")
            self.ax2.tick_params(colors="white")
            self.ax2.legend(facecolor="#252836", labelcolor="white")
            self.ax2.grid(True, linestyle="--", alpha=0.3)

            self.canvas_matplotlib.draw()

            # Mostrar estadísticas
            self.lbl_stats.configure(
                text=f"Presas Máx: {max(x):.1f}\nDepredadores Máx: {max(y):.1f}\nÚltimo estado: Presas={x[-1]:.1f}, Depredadores={y[-1]:.1f}"
            )

        except ValueError as ve:
            messagebox.showerror("Error en Parámetros", f"Por favor verifica los datos ingresados: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en la simulación: {str(e)}")