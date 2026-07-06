import customtkinter as ctk
import config


class Sidebar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=config.SIDEBAR_WIDTH,
            fg_color=config.SIDEBAR_COLOR,
            corner_radius=0
        )

        self.pack_propagate(False)

        self.crear_componentes()

    def crear_componentes(self):

        # ==========================
        # Logo
        # ==========================

        logo = ctk.CTkLabel(
            self,
            text="📊",
            font=("Segoe UI Emoji", 40)
        )

        logo.pack(pady=(25, 5))

        titulo = ctk.CTkLabel(
            self,
            text="SIMULADOR",
            font=config.TITLE_FONT
        )

        titulo.pack()

        subtitulo = ctk.CTkLabel(
            self,
            text="Modelos Matemáticos",
            font=("Segoe UI", 13),
            text_color=config.TEXT_SECONDARY
        )

        subtitulo.pack(pady=(0, 25))

        # ==========================
        # Botones del menú
        # ==========================

        botones = [

            ("🏠 Dashboard"),

            ("🎲 Pseudoaleatorios"),

            ("🎰 Ruleta"),

            ("🦠 COVID"),

            ("🧬 Autómatas"),

            ("📈 Lotka Volterra"),

            ("🌾 Quinua")

        ]

        self.lista_botones = []

        for texto in botones:

            boton = ctk.CTkButton(

                self,

                text=texto,

                height=45,

                anchor="w",

                font=config.BUTTON_FONT,

                fg_color="transparent",

                hover_color="#3A3F55",

                corner_radius=10

            )

            boton.pack(

                fill="x",

                padx=15,

                pady=5

            )

            self.lista_botones.append(boton)

        # ==========================
        # Espacio inferior
        # ==========================

        ctk.CTkLabel(
            self,
            text="Versión 1.0",
            text_color=config.TEXT_SECONDARY
        ).pack(side="bottom", pady=20)