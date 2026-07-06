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

        self.master = master

        self.pack_propagate(False)

        self.crear_componentes()

    # =========================================

    def crear_componentes(self):

        logo = ctk.CTkLabel(
            self,
            text="📊",
            font=("Segoe UI Emoji", 42)
        )
        logo.pack(pady=(25,5))

        titulo = ctk.CTkLabel(
            self,
            text="SIMULADOR",
            font=("Segoe UI",22,"bold")
        )
        titulo.pack()

        subtitulo = ctk.CTkLabel(
            self,
            text="Modelos Matemáticos",
            font=("Segoe UI",13)
        )
        subtitulo.pack(pady=(0,25))

        self.crear_boton("🏠 Dashboard","dashboard")
        self.crear_boton("🎲 Pseudoaleatorios","pseudo")
        self.crear_boton("🎰 Ruleta","ruleta")
        self.crear_boton("🦠 COVID","covid")
        self.crear_boton("🧬 Autómatas","automata")
        self.crear_boton("📈 Lotka Volterra","lotka")
        self.crear_boton("🌾 Quinua","quinua")

        ctk.CTkLabel(
            self,
            text="Versión 1.0",
            text_color="gray"
        ).pack(side="bottom",pady=20)

    # =========================================

    def crear_boton(self,texto,pagina):

        boton = ctk.CTkButton(

            self,

            text=texto,

            anchor="w",

            height=45,

            fg_color="transparent",

            hover_color="#3A3F55",

            command=lambda:self.master.mostrar_pagina(pagina)

        )

        boton.pack(fill="x",padx=15,pady=5)