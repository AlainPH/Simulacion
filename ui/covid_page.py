import customtkinter as ctk


class CovidPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        titulo = ctk.CTkLabel(
            self,
            text="🦠 Simulación COVID",
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(pady=30)

        descripcion = ctk.CTkLabel(
            self,
            text="Modelo epidemiológico SIR para la propagación del COVID.",
            font=("Segoe UI", 15)
        )
        descripcion.pack()