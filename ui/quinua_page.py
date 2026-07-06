import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from simulaciones.quinua import SimuladorQuinua


class QuinuaPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.simulador = SimuladorQuinua()
        
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
            text="SIMULACIÓN DE QUINUA",
            font=("Segoe UI", 18, "bold")
        )
        titulo.pack(pady=(20, 15))

        # ---------------- Área Sembrada ----------------
        ctk.CTkLabel(panel, text="Área de cultivo (hectáreas)").pack(anchor="w", padx=20)
        self.entry_area = ctk.CTkEntry(panel)
        self.entry_area.insert(0, "5.0")
        self.entry_area.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Densidad de Semilla ----------------
        ctk.CTkLabel(panel, text="Densidad de semilla (kg/ha)").pack(anchor="w", padx=20)
        self.entry_semilla = ctk.CTkEntry(panel)
        self.entry_semilla.insert(0, "10.0")
        self.entry_semilla.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Frecuencia de Riego ----------------
        ctk.CTkLabel(panel, text="Frecuencia de riego (días)").pack(anchor="w", padx=20)
        self.entry_riego = ctk.CTkEntry(panel)
        self.entry_riego.insert(0, "10")
        self.entry_riego.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Fertilizante NPK ----------------
        ctk.CTkLabel(panel, text="Fertilizante NPK aplicado (kg/ha)").pack(anchor="w", padx=20)
        self.entry_npk = ctk.CTkEntry(panel)
        self.entry_npk.insert(0, "100.0")
        self.entry_npk.pack(fill="x", padx=20, pady=(0, 8))

        # ---------------- Temperatura Media ----------------
        ctk.CTkLabel(panel, text="Temperatura media del ciclo (°C)").pack(anchor="w", padx=20)
        self.entry_temp = ctk.CTkEntry(panel)
        self.entry_temp.insert(0, "14.0")
        self.entry_temp.pack(fill="x", padx=20, pady=(0, 15))

        # ---------------- Botón Simular ----------------
        self.btn_simular = ctk.CTkButton(
            panel,
            text="🌾 Simular Ciclo Agrícola",
            height=35,
            command=self.simular
        )
        self.btn_simular.pack(fill="x", padx=20, pady=5)

        # Presets de Clima/Suelo
        self.combo_presets = ctk.CTkComboBox(
            panel,
            values=["Clima: Altiplano Templado", "Clima: Altiplano Seco/Frío", "Clima: Valle Interandino"],
            command=self.aplicar_preset
        )
        self.combo_presets.set("Elegir Escenario...")
        self.combo_presets.pack(fill="x", padx=20, pady=5)

        # ================= PANEL DERECHO =================
        self.derecha = ctk.CTkFrame(self)
        self.derecha.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.derecha.grid_rowconfigure(0, weight=1)
        self.derecha.grid_columnconfigure(0, weight=1)

        # Tabview didáctico
        self.tabview = ctk.CTkTabview(self.derecha)
        self.tabview.pack(fill="both", expand=True)

        self.tab_visual = self.tabview.add("📊 Rendimiento y Finanzas")
        self.tab_teoria = self.tabview.add("📖 Guía Didáctica")

        # Configurar elementos dentro de tab_visual
        self.tab_visual.grid_rowconfigure(0, weight=3)  # Gráfico
        self.tab_visual.grid_rowconfigure(1, weight=2)  # Balances
        self.tab_visual.grid_columnconfigure(0, weight=1)

        # Gráfico Matplotlib
        self.figura = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_facecolor("#1E1F29")
        self.figura.patch.set_facecolor("#1E1F29")

        self.canvas_matplotlib = FigureCanvasTkAgg(self.figura, self.tab_visual)
        self.canvas_matplotlib.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Panel de balances financieros y de rendimiento
        self.balance_panel = ctk.CTkFrame(self.tab_visual)
        self.balance_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.balance_panel.grid_columnconfigure((0, 1), weight=1)
        self.balance_panel.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.lbl_rendimiento = ctk.CTkLabel(self.balance_panel, text="Rendimiento: -", font=("Segoe UI", 13, "bold"), anchor="w")
        self.lbl_rendimiento.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.lbl_produccion = ctk.CTkLabel(self.balance_panel, text="Producción Total: -", font=("Segoe UI", 13, "bold"), anchor="w")
        self.lbl_produccion.grid(row=0, column=1, padx=20, pady=5, sticky="w")

        self.lbl_costo_total = ctk.CTkLabel(self.balance_panel, text="Costos Operativos Totales: -", font=("Segoe UI", 13), anchor="w")
        self.lbl_costo_total.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.lbl_ingreso_total = ctk.CTkLabel(self.balance_panel, text="Ingresos Totales: -", font=("Segoe UI", 13), anchor="w")
        self.lbl_ingreso_total.grid(row=1, column=1, padx=20, pady=5, sticky="w")

        self.lbl_ganancia = ctk.CTkLabel(self.balance_panel, text="Ganancia Neta: -", font=("Segoe UI", 14, "bold"), anchor="w")
        self.lbl_ganancia.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.lbl_roi = ctk.CTkLabel(self.balance_panel, text="Retorno de Inversión (ROI): -", font=("Segoe UI", 14, "bold"), anchor="w")
        self.lbl_roi.grid(row=2, column=1, padx=20, pady=5, sticky="w")

        self.lbl_desglose = ctk.CTkLabel(self.balance_panel, text="Desglose: Semillas: $0 | Fertilizante: $0 | Agua: $0", font=("Segoe UI", 11, "italic"))
        self.lbl_desglose.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        # Texto didáctico en tab_teoria
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

        self.txt_teoria.insert("end", "MODELO FISIOLÓGICO Y FINANCIERO DE LA QUINUA\n\n", "title")
        self.txt_teoria.insert("end", "Este simulador dinámico modela el crecimiento diario de la biomasa de la planta y el peso final del grano de quinua (Chenopodium quinoa) a lo largo de un ciclo agrícola de 150 días, en base a factores climáticos y de manejo agronómico.\n\n", "body")
        
        self.txt_teoria.insert("end", "1. ECOFISIOLOGÍA Y FACTORES LIMITANTES\n", "subtitle")
        self.txt_teoria.insert("end", "• Tiempo Térmico (GDD - Growing Degree Days):\n", "body")
        self.txt_teoria.insert("end", "  GDD_diario = max( Temp_media - 3.0°C, 0 )\n\n", "code")
        self.txt_teoria.insert("end", "  La planta necesita acumular calor para desarrollarse. La temperatura óptima es ~18°C. Temperaturas muy frías (heladas) o excesivo calor frenan la fotosíntesis.\n\n• Estrés Hídrico:\n  La humedad del suelo se agota por evapotranspiración (ET) diaria. Si la humedad disminuye por debajo del 30% de la capacidad del suelo, se activa el factor de estrés hídrico f_agua < 1.0, reduciendo el crecimiento.\n\n• Nutrientes (NPK):\n  La fertilización ideal es de 120 kg/ha de NPK. Una fertilización pobre restringe el potencial de biomasa de las hojas.\n\n• Densidad de siembra:\n  Densidades fuera del rango óptimo (8-12 kg/ha) causan un menor rendimiento (poca cobertura si es menor, o competencia autodestructiva si es mayor).\n\n", "body")

        self.txt_teoria.insert("end", "2. ETAPAS DE DESARROLLO (150 días)\n", "subtitle")
        self.txt_teoria.insert("end", "• Germinación (Días 1-10): Establecimiento y emergencia inicial.\n• Fase Vegetativa (Días 11-90): Crecimiento rápido de tallos y hojas.\n• Llenado de Grano (Días 91-140): El 45% de la energía de crecimiento se transloca a la panoja.\n• Madurez (Días 141-150): Secado del grano previo a la cosecha.\n\n", "body")

        self.txt_teoria.insert("end", "💡 ANÁLISIS FINANCIERO Y RENDIMIENTO:\n", "tip")
        self.txt_teoria.insert("end", "• Evalúa el Retorno de Inversión (ROI). El simulador calcula egresos por semilla ($4.5/kg), NPK ($1.2/kg), agua ($25 por riego) y un costo operativo fijo de preparación de tierra y labranza de $600/ha.\n• Los ingresos brutos se obtienen vendiendo el grano cosechado al precio promedio de exportación ($2.80/kg).\n", "body")

        self.txt_teoria.configure(state="disabled")

    def aplicar_preset(self, escenario):
        if escenario == "Clima: Altiplano Templado":
            self.entry_temp.delete(0, tk.END); self.entry_temp.insert(0, "15.0")
            self.entry_riego.delete(0, tk.END); self.entry_riego.insert(0, "8")
            self.entry_npk.delete(0, tk.END); self.entry_npk.insert(0, "120.0")
        elif escenario == "Clima: Altiplano Seco/Frío":
            self.entry_temp.delete(0, tk.END); self.entry_temp.insert(0, "9.0")
            self.entry_riego.delete(0, tk.END); self.entry_riego.insert(0, "15")
            self.entry_npk.delete(0, tk.END); self.entry_npk.insert(0, "60.0")
        elif escenario == "Clima: Valle Interandino":
            self.entry_temp.delete(0, tk.END); self.entry_temp.insert(0, "19.0")
            self.entry_riego.delete(0, tk.END); self.entry_riego.insert(0, "6")
            self.entry_npk.delete(0, tk.END); self.entry_npk.insert(0, "140.0")

    def limpiar_grafico(self):
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Presiona 'Simular Ciclo Agrícola' para graficar el crecimiento", 
                     color="white", ha="center", va="center", transform=self.ax.transAxes)
        self.ax.axis('off')
        self.canvas_matplotlib.draw()

    def simular(self):
        try:
            area = float(self.entry_area.get())
            semilla = float(self.entry_semilla.get())
            riego = int(self.entry_riego.get())
            npk = float(self.entry_npk.get())
            temp = float(self.entry_temp.get())

            if min(area, semilla, riego, npk, temp) <= 0:
                raise ValueError("Todos los parámetros deben ser mayores a 0")

            dias, biomasa, grano, balance = self.simulador.simular(area, semilla, riego, npk, temp)

            # Graficar curvas de crecimiento
            self.ax.clear()
            self.ax.axis('on')
            self.ax.plot(dias, biomasa, color="#2ecc71", label="Biomasa Total (kg/ha)", linewidth=2.5)
            self.ax.plot(dias, grano, color="#f1c40f", label="Rendimiento del Grano (kg/ha)", linewidth=2.5)
            self.ax.set_title("Curva de Crecimiento de la Quinua (150 días)", color="white", fontsize=12, pad=10)
            self.ax.set_xlabel("Días desde la Siembra", color="white")
            self.ax.set_ylabel("Rendimiento (kg/ha)", color="white")
            self.ax.tick_params(colors="white")
            self.ax.legend(facecolor="#252836", labelcolor="white", loc="upper left")
            self.ax.grid(True, linestyle="--", alpha=0.3)
            self.canvas_matplotlib.draw()

            # Actualizar interfaz de balances
            self.lbl_rendimiento.configure(text=f"Rendimiento Promedio: {balance['rendimiento_ha']:.1f} kg/ha")
            self.lbl_produccion.configure(text=f"Producción Total: {balance['produccion_total']:.2f} Toneladas")
            
            self.lbl_costo_total.configure(text=f"Costos Operativos: ${balance['costo_total']:,.2f} USD")
            self.lbl_ingreso_total.configure(text=f"Ventas Brutas: ${balance['ingresos_totales']:,.2f} USD")
            
            neto = balance['ganancia_neta']
            color_ganancia = "#2ecc71" if neto >= 0 else "#e74c3c"
            self.lbl_ganancia.configure(
                text=f"Ganancia Neta: ${neto:,.2f} USD",
                text_color=color_ganancia
            )
            
            self.lbl_roi.configure(
                text=f"Retorno de Inversión (ROI): {balance['roi']:.1f}%",
                text_color=color_ganancia
            )

            self.lbl_desglose.configure(
                text=f"Desglose de Costos: Semillas: ${balance['costo_semillas']:,.1f} | Fertilizante: ${balance['costo_fertilizantes']:,.1f} | Agua: ${balance['costo_agua']:,.1f} | Operación: ${balance['costo_operativo']:,.1f}"
            )

        except ValueError as ve:
            messagebox.showerror("Error en Parámetros", f"Por favor verifica los datos ingresados: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en la simulación: {str(e)}")