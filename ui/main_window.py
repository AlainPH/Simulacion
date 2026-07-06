import customtkinter as ctk
import config

from ui.sidebar import Sidebar
from ui.navbar import Navbar
from ui.dashboard import Dashboard
from ui.pseudoaleatorios_page import PseudoaleatoriosPage
from ui.ruleta_page import RuletaPage
from ui.covid_page import CovidPage
from ui.automata_page import AutomataPage
from ui.lotka_page import LotkaPage
from ui.quinua_page import QuinuaPage
class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =============================
        # Configuración de la ventana
        # =============================

        self.title(config.APP_NAME)

        self.geometry(
            f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}"
        )

        self.minsize(
            config.MIN_WIDTH,
            config.MIN_HEIGHT
        )

        self.configure(
            fg_color=config.BACKGROUND
        )

        # =============================
        # Grid principal
        # =============================

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Crear interfaz
       # 1. Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # 2. Navbar
        self.navbar = Navbar(self)
        self.navbar.grid(row=0, column=1, sticky="ew")

        # 3. Contenido
        self.crear_contenido()

        self.mostrar_pagina("dashboard")

    # =====================================================

    def crear_contenido(self):

        self.content = ctk.CTkFrame(
            self,
            fg_color=config.CONTENT_COLOR
        )

        self.content.grid(
            row=1,
            column=1,
            sticky="nsew"
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
    
    def limpiar_contenido(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ===============================================

    def mostrar_pagina(self, pagina):
        self.limpiar_contenido()

        if pagina == "dashboard":
            Dashboard(self.content).pack(fill="both", expand=True, padx=20, pady=20)
            self.navbar.cambiar_titulo("Dashboard")
        elif pagina == "pseudo":
            PseudoaleatoriosPage(self.content).pack(fill="both", expand=True)
            self.navbar.cambiar_titulo("Pseudoaleatorios")
        elif pagina == "ruleta":
            RuletaPage(self.content).pack(fill="both", expand=True)
            self.navbar.cambiar_titulo("Ruleta")
        elif pagina == "covid":
            CovidPage(self.content).pack(fill="both", expand=True)
            self.navbar.cambiar_titulo("COVID")
        elif pagina == "automata":
            AutomataPage(self.content).pack(fill="both", expand=True)
            self.navbar.cambiar_titulo("Autómatas")
        elif pagina == "lotka":
            LotkaPage(self.content).pack(fill="both", expand=True)
            self.navbar.cambiar_titulo("Lotka Volterra")
        elif pagina == "quinua":
            QuinuaPage(self.content).pack(fill="both", expand=True)
            self.navbar.cambiar_titulo("Quinua")