import customtkinter as ctk


class RuletaPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        titulo = ctk.CTkLabel(
            self,
            text="🎰 Simulación de Ruleta",
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(pady=30)

        descripcion = ctk.CTkLabel(
            self,
            text="Aquí se realizará la simulación mediante Monte Carlo.",
            font=("Segoe UI", 15)
        )
        descripcion.pack()