import customtkinter as ctk


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.crear_tarjetas()

    def crear_tarjetas(self):

        datos = [
            ("🎲", "Pseudoaleatorios", "Generadores"),
            ("🎰", "Ruleta", "Monte Carlo"),
            ("🦠", "COVID", "Simulación"),
            ("🧬", "Autómatas", "Celulares"),
            ("📈", "Lotka Volterra", "Modelo"),
            ("🌾", "Quinua", "Producción")
        ]

        fila = 0
        columna = 0

        for icono, titulo, subtitulo in datos:

            tarjeta = ctk.CTkFrame(self, corner_radius=15)

            tarjeta.grid(
                row=fila,
                column=columna,
                padx=20,
                pady=20,
                sticky="nsew"
            )

            ctk.CTkLabel(
                tarjeta,
                text=icono,
                font=("Segoe UI Emoji", 45)
            ).pack(pady=(20, 5))

            ctk.CTkLabel(
                tarjeta,
                text=titulo,
                font=("Segoe UI", 18, "bold")
            ).pack()

            ctk.CTkLabel(
                tarjeta,
                text=subtitulo,
                font=("Segoe UI", 13)
            ).pack(pady=(0, 20))

            columna += 1

            if columna == 3:
                columna = 0
                fila += 1