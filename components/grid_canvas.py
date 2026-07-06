import tkinter as tk


class GridCanvas(tk.Canvas):

    def __init__(self, master, filas=120, columnas=120, tam=5):
        super().__init__(master, bg="#1E1F29", highlightthickness=0)

        self.filas = filas
        self.columnas = columnas
        self.tam = tam

        self.rectangulos = []

        self.config(
            width=columnas * tam,
            height=filas * tam
        )

        self._crear_cuadricula()

    # ======================================================

    def _crear_cuadricula(self):

        self.rectangulos = []

        for i in range(self.filas):
            fila = []

            for j in range(self.columnas):

                x1 = j * self.tam
                y1 = i * self.tam
                x2 = x1 + self.tam
                y2 = y1 + self.tam

                rect = self.create_rectangle(
                    x1, y1, x2, y2,
                    fill="#2F3242",
                    outline="#1E1F29"
                )

                fila.append(rect)

            self.rectangulos.append(fila)

    # ======================================================

    def dibujar(self, grid):

        # Colores del sistema epidemiológico (Estilo Neón Premium)
        colores = {
            0: "#1E1F29",   # vacío
            1: "#2F3242",   # sano (color de tarjeta)
            2: "#FF4757",   # infectado (rojo neón)
            3: "#2ED573",   # recuperado (verde neón)
            4: "#747D8C"    # muerto (gris pizarra)
        }

        for i in range(self.filas):
            for j in range(self.columnas):

                estado = grid[i][j]

                self.itemconfig(
                    self.rectangulos[i][j],
                    fill=colores.get(estado, "#2F3242")
                )