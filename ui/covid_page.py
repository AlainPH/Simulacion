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

        ctk.CTkLabel(panel, text="Velocidad").pack(anchor="w", padx=20)

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

        derecha.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 15),
            pady=15
        )

        self.canvas = GridCanvas(
            derecha,
            filas=120,
            columnas=120,
            tam=5
        )

        self.canvas.pack(expand=True)

        self.canvas.dibujar(self.motor.grid)

    # ==========================================================

    def cambiar_velocidad(self, valor):

        self.delay = int(valor)

    # ==========================================================

    def iniciar(self):

        self.motor.max_iteraciones = int(
            self.entry_iteraciones.get()
        )

        self.motor.contagio = float(
            self.entry_contagio.get()
        )

        self.motor.recuperacion = float(
            self.entry_recuperacion.get()
        )

        self.motor.muerte = float(
            self.entry_muerte.get()
        )

        infectados = int(
            self.entry_infectados.get()
        )

        self.motor.reiniciar(infectados)

        self.running = True

        self.actualizar()

    # ==========================================================

    def pausar(self):

        self.running = False

    # ==========================================================

    def reiniciar(self):

        self.running = False

        infectados = int(
            self.entry_infectados.get()
        )

        self.motor.reiniciar(infectados)

        self.canvas.dibujar(self.motor.grid)

        self.actualizar_labels()

    # ==========================================================

    def actualizar(self):

        if not self.running:
            return

        self.motor.paso()

        self.canvas.dibujar(
            self.motor.grid
        )

        self.actualizar_labels()

        if self.motor.iteracion < self.motor.max_iteraciones:

            self.after(
                self.delay,
                self.actualizar
            )

        else:

            self.running = False

    # ==========================================================

    def actualizar_labels(self):

        datos = self.motor.estadisticas()

        self.lblIteracion.configure(
            text=f"Iteración: {datos['iteracion']}"
        )

        self.lblSanos.configure(
            text=f"Sanos: {datos['sanos']}"
        )

        self.lblInfectados.configure(
            text=f"Infectados: {datos['infectados']}"
        )

        self.lblRecuperados.configure(
            text=f"Recuperados: {datos['recuperados']}"
        )

        self.lblMuertos.configure(
            text=f"Muertos: {datos['muertos']}"
        )