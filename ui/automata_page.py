import customtkinter as ctk


class AutomataPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        titulo = ctk.CTkLabel(
            self,
            text="🧬 Autómatas Celulares",
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(pady=30)

        descripcion = ctk.CTkLabel(
            self,
            text="Simulación de autómatas celulares unidimensionales.",
            font=("Segoe UI", 15)
        )
        descripcion.pack()