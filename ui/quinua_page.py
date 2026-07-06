import customtkinter as ctk


class QuinuaPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        titulo = ctk.CTkLabel(
            self,
            text="🌾 Simulación de Producción de Quinua",
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(pady=30)

        descripcion = ctk.CTkLabel(
            self,
            text="Modelo de simulación del crecimiento y producción de quinua.",
            font=("Segoe UI", 15)
        )
        descripcion.pack()