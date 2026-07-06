import customtkinter as ctk
import config
from datetime import datetime


class Navbar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            height=config.NAVBAR_HEIGHT,
            fg_color=config.NAVBAR_COLOR,
            corner_radius=0
        )

        self.grid_propagate(False)

        self.crear_componentes()

        self.actualizar_hora()

    # =====================================

    def crear_componentes(self):

        # Columna izquierda
        self.left = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.left.pack(
            side="left",
            padx=20,
            fill="y"
        )

        self.titulo = ctk.CTkLabel(
            self.left,
            text="Dashboard",
            font=("Segoe UI", 24, "bold")
        )

        self.titulo.pack(anchor="w")

        # Columna derecha
        self.right = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.right.pack(
            side="right",
            padx=20
        )

        self.fecha = ctk.CTkLabel(
            self.right,
            text="",
            font=("Segoe UI", 13)
        )

        self.fecha.pack(anchor="e")

        self.usuario = ctk.CTkLabel(
            self.right,
            text="Usuario: Alain",
            font=("Segoe UI", 14, "bold")
        )

        self.usuario.pack(anchor="e")

    # =====================================

    def actualizar_hora(self):

        ahora = datetime.now()

        texto = ahora.strftime("%d/%m/%Y  %H:%M:%S")

        self.fecha.configure(text=texto)

        self.after(1000, self.actualizar_hora)

    # =====================================

    def cambiar_titulo(self, texto):

        self.titulo.configure(text=texto)