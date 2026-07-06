import customtkinter as ctk

from simulaciones.grid_engine import GridEngine
from components.grid_canvas import GridCanvas


class CovidPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.motor = GridEngine(120, 120)

        self.running = False
        self.delay = 40

        self.crear_interfaz()

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def crear_interfaz(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= PANEL IZQUIERDO =================
        panel = ctk.CTkFrame(self, width=300)
        panel.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        panel.grid_propagate(False)

        titulo = ctk.CTkLabel(
            panel,
            text="SIMULACIÓN COVID",
            font=("Segoe UI", 24, "bold")
        )
        titulo.pack(pady=(20, 15))

        # -------------------------------------------------
        ctk.CTkLabel(panel, text="Número de iteraciones").pack(anchor="w", padx=20)
        self.entry_iteraciones = ctk.CTkEntry(panel)
        self.entry_iteraciones.insert(0, "500")
        self.entry_iteraciones.pack(fill="x", padx=20, pady=(0, 10))

        # -------------------------------------------------
        ctk.CTkLabel(panel, text="Infectados iniciales").pack(anchor="w", padx=20)
        self.entry_infectados = ctk.CTkEntry(panel)
        self.entry_infectados.insert(0, "20")
        self.entry_infectados.pack(fill="x", padx=20, pady=(0, 10))

        # -------------------------------------------------
        ctk.CTkLabel(panel, text="Probabilidad de contagio").pack(anchor="w", padx=20)
        self.entry_contagio = ctk.CTkEntry(panel)
        self.entry_contagio.insert(0, "0.35")
        self.entry_contagio.pack(fill="x", padx=20, pady=(0, 10))

        # -------------------------------------------------
        ctk.CTkLabel(panel, text="Probabilidad de recuperación").pack(anchor="w", padx=20)
        self.entry_recuperacion = ctk.CTkEntry(panel)
        self.entry_recuperacion.insert(0, "0.02")
        self.entry_recuperacion.pack(fill="x", padx=20, pady=(0, 10))

        # -------------------------------------------------
        ctk.CTkLabel(panel, text="Probabilidad de muerte").pack(anchor="w", padx=20)
        self.entry_muerte = ctk.CTkEntry(panel)
        self.entry_muerte.insert(0, "0.01")
        self.entry_muerte.pack(fill="x", padx=20, pady=(0, 10))

        # -------------------------------------------------
        ctk.CTkLabel(panel, text="Velocidad (ms)").pack(anchor="w", padx=20)
        self.slider = ctk.CTkSlider(
            panel,
            from_=5,
            to=150,
            number_of_steps=145,
            command=self.cambiar_velocidad
        )
        self.slider.set(40)
        self.slider.pack(fill="x", padx=20)

        # -------------------------------------------------
        ctk.CTkButton(
            panel,
            text="▶ Iniciar",
            height=40,
            command=self.iniciar
        ).pack(fill="x", padx=20, pady=(25, 8))

        ctk.CTkButton(
            panel,
            text="⏸ Pausar",
            height=40,
            command=self.pausar
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            panel,
            text="⟳ Reiniciar",
            height=40,
            command=self.reiniciar
        ).pack(fill="x", padx=20, pady=8)

        # ====================================================
        self.lblIteracion = ctk.CTkLabel(panel, text="Iteración: 0")
        self.lblIteracion.pack(pady=(20, 5))

        self.lblSanos = ctk.CTkLabel(panel, text="Sanos: 0")
        self.lblSanos.pack()

        self.lblInfectados = ctk.CTkLabel(panel, text="Infectados: 0")
        self.lblInfectados.pack()

        self.lblRecuperados = ctk.CTkLabel(panel, text="Recuperados: 0")
        self.lblRecuperados.pack()

        self.lblMuertos = ctk.CTkLabel(panel, text="Muertos: 0")
        self.lblMuertos.pack()

        # ================= PANEL DERECHO =================
        derecha = ctk.CTkFrame(self)
        derecha.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

        # Tabview didáctico
        self.tabview = ctk.CTkTabview(derecha)
        self.tabview.pack(fill="both", expand=True)

        self.tab_visual = self.tabview.add("📊 Visualización 2D")
        self.tab_teoria = self.tabview.add("📖 Guía Didáctica")

        # Configurar canvas dentro de tab_visual
        self.canvas = GridCanvas(
            self.tab_visual,
            filas=120,
            columnas=120,
            tam=5
        )
        self.canvas.pack(expand=True)
        self.canvas.dibujar(self.motor.grid)

        # Texto explicativo enriquecido en tab_teoria
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
        self.txt_teoria.insert("end", "MODELO EPIDEMIOLÓGICO SIR EN CUADRÍCULA 2D\n\n", "title")
        self.txt_teoria.insert("end", "Esta simulación recrea de forma gráfica y espacial cómo se propaga una enfermedad infecciosa en una población distribuida sobre un plano bidimensional, imitando el comportamiento de las epidemias reales.\n\n", "body")

        self.txt_teoria.insert("end", "1. ESTADOS DE LA POBLACIÓN (Modelo SIR ampliado)\n", "subtitle")
        self.txt_teoria.insert("end", "• Susceptible (Sano - Gris Oscuro): Individuos sanos que no tienen el virus pero pueden contagiarse si entran en contacto físico directo con un infectado.\n", "body")
        self.txt_teoria.insert("end", "• Infectado (Enfermo - Rojo Neón): Celdas activas que albergan la enfermedad. Intentan transmitir el virus a todos sus vecinos directos en cada paso.\n", "body")
        self.txt_teoria.insert("end", "• Recuperado (Inmune - Verde Neón): Individuos que superaron la infección. Poseen anticuerpos y no pueden contraer el virus de nuevo ni propagarlo.\n", "body")
        self.txt_teoria.insert("end", "• Muerto (Fallecido - Gris Claro): Celdas inactivas que representan las bajas a causa de la letalidad del virus. Ya no interactúan con el sistema.\n\n", "body")

        self.txt_teoria.insert("end", "2. MECÁNICA Y REGLAS DE TRANSICIÓN\n", "subtitle")
        self.txt_teoria.insert("end", "En cada ciclo de tiempo discreto (un día virtual), se evalúan las celdas bajo los siguientes criterios:\n", "body")
        self.txt_teoria.insert("end", "• Contagio: Una celda Sana se infecta con probabilidad 'p_contagio' si tiene al menos un vecino en estado Infectado dentro de su Vecindario de Moore (los 8 bloques que la rodean).\n", "body")
        self.txt_teoria.insert("end", "• Recuperación: Una celda Infectada sana y pasa a Recuperada con probabilidad 'p_recuperacion'.\n", "body")
        self.txt_teoria.insert("end", "• Deceso: Una celda Infectada fallece y pasa a Muerta con probabilidad 'p_muerte'.\n\n", "body")

        self.txt_teoria.insert("end", "💡 GUÍA DIDÁCTICA Y DE EXPERIMENTACIÓN:\n", "tip")
        self.txt_teoria.insert("end", "• Aplanar la Curva: Modifica los parámetros a un escenario de 'cuarentena' (ej: baja el contagio a 0.12 e incrementa la recuperación a 0.05). Observarás que el virus avanza lento, en pequeños focos locales, y la cantidad máxima de infectados simultáneos disminuye drásticamente, previniendo el colapso.\n", "body")
        self.txt_teoria.insert("end", "• Brote Exponencial: Si estableces el contagio alto (> 0.40) y una recuperación lenta (0.01), la mancha roja invadirá el mapa completo de forma explosiva, dejando un rastro de inmunidad (verde) y decesos (gris).\n", "body")

        self.txt_teoria.configure(state="disabled")

    # ==========================================================

    def cambiar_velocidad(self, valor):
        self.delay = int(valor)

    # ==========================================================

    def iniciar(self):
        self.motor.max_iteraciones = int(self.entry_iteraciones.get())
        self.motor.contagio = float(self.entry_contagio.get())
        self.motor.recuperacion = float(self.entry_recuperacion.get())
        self.motor.muerte = float(self.entry_muerte.get())
        
        infectados = int(self.entry_infectados.get())
        self.motor.reiniciar(infectados)

        self.running = True
        self.actualizar()

    # ==========================================================

    def pausar(self):
        self.running = False

    # ==========================================================

    def reiniciar(self):
        self.running = False
        infectados = int(self.entry_infectados.get())
        self.motor.reiniciar(infectados)
        self.canvas.dibujar(self.motor.grid)
        self.actualizar_labels()

    # ==========================================================

    def actualizar(self):
        if not self.running:
            return

        self.motor.paso()
        self.canvas.dibujar(self.motor.grid)
        self.actualizar_labels()

        if self.motor.iteracion < self.motor.max_iteraciones:
            self.after(self.delay, self.actualizar)
        else:
            self.running = False

    # ==========================================================

    def actualizar_labels(self):
        datos = self.motor.estadisticas()
        self.lblIteracion.configure(text=f"Iteración: {datos['iteracion']}")
        self.lblSanos.configure(text=f"Sanos: {datos['sanos']}")
        self.lblInfectados.configure(text=f"Infectados: {datos['infectados']}")
        self.lblRecuperados.configure(text=f"Recuperados: {datos['recuperados']}")
        self.lblMuertos.configure(text=f"Muertos: {datos['muertos']}")