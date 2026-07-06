import customtkinter as ctk
import config

from ui.sidebar import Sidebar
from ui.navbar import Navbar
from ui.dashboard import Dashboard
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

        # 4. Dashboard
        self.dashboard = Dashboard(self.content)
        self.dashboard.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=20,
    pady=20
)

    # =====================================================

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