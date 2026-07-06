import customtkinter as ctk


class LotkaPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        titulo = ctk.CTkLabel(
            self,
            text="📈 Modelo Lotka-Volterra",
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(pady=30)

        descripcion = ctk.CTkLabel(
            self,
            text="Modelo dinámico de interacción entre variables.",
            font=("Segoe UI", 15)
        )
        descripcion.pack()