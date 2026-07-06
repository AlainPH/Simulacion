import customtkinter as ctk


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.crear_tarjetas()

    def crear_tarjetas(self):
        # Datos: (Ícono, Título, Subtítulo, ID de Página)
        datos = [
            ("🎲", "Pseudoaleatorios", "Generadores Matemáticos", "pseudo"),
            ("🎰", "Ruleta", "Simulación de Monte Carlo", "ruleta"),
            ("🦠", "COVID", "Propagación en Cuadrícula 2D", "covid"),
            ("🧬", "Autómatas Celulares", "Reglas Unidimensionales", "automata"),
            ("📈", "Lotka Volterra", "Modelo Depredador-Presa", "lotka"),
            ("🌾", "Quinua", "Crecimiento y Costos Agrícolas", "quinua")
        ]

        fila = 0
        columna = 0

        for icono, titulo, subtitulo, page_id in datos:
            # Crear la tarjeta como un frame interactivo
            tarjeta = ctk.CTkFrame(
                self, 
                corner_radius=15, 
                fg_color="#2F3242",
                border_color="#3E4256",
                border_width=1
            )
            tarjeta.grid(
                row=fila,
                column=columna,
                padx=20,
                pady=20,
                sticky="nsew"
            )

            # Contenido de la tarjeta
            lbl_icono = ctk.CTkLabel(
                tarjeta,
                text=icono,
                font=("Segoe UI Emoji", 55)
            )
            lbl_icono.pack(pady=(25, 5))

            lbl_titulo = ctk.CTkLabel(
                tarjeta,
                text=titulo,
                font=("Segoe UI", 18, "bold"),
                text_color="#FFFFFF"
            )
            lbl_titulo.pack()

            lbl_subtitulo = ctk.CTkLabel(
                tarjeta,
                text=subtitulo,
                font=("Segoe UI", 12),
                text_color="#BBBBBB"
            )
            lbl_subtitulo.pack(pady=(5, 10))

            lbl_accion = ctk.CTkLabel(
                tarjeta,
                text="Hacer clic para entrar →",
                font=("Segoe UI", 11, "italic"),
                text_color="#4F8EF7"
            )
            lbl_accion.pack(pady=(0, 20))

            # Hacer que la tarjeta sea interactiva con efectos hover y click
            self.hacer_interactiva(tarjeta, page_id)

            columna += 1
            if columna == 3:
                columna = 0
                fila += 1

    def hacer_interactiva(self, frame, page_id):
        normal_color = "#2F3242"
        hover_color = "#3A3F54"
        border_normal = "#3E4256"
        border_hover = "#4F8EF7"

        # Función para cambiar apariencia al pasar el cursor
        def al_entrar(e):
            frame.configure(fg_color=hover_color, border_color=border_hover)

        def al_salir(e):
            frame.configure(fg_color=normal_color, border_color=border_normal)

        # Función al hacer click
        def al_hacer_click(e):
            # Acceder a MainWindow para cambiar de página
            main_window = self.master.master
            if hasattr(main_window, "mostrar_pagina"):
                main_window.mostrar_pagina(page_id)

        # Vincular eventos a la tarjeta
        frame.bind("<Enter>", al_entrar)
        frame.bind("<Leave>", al_salir)
        frame.bind("<Button-1>", al_hacer_click)

        # Vincular también a cada uno de sus widgets hijos para que toda la tarjeta responda
        for hijo in frame.winfo_children():
            hijo.bind("<Enter>", al_entrar)
            hijo.bind("<Leave>", al_salir)
            hijo.bind("<Button-1>", al_hacer_click)