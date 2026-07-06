import tkinter as tk


class GridCanvas(tk.Canvas):

    def __init__(self, master, filas=120, columnas=120, tam=5):
        super().__init__(master, bg="white", highlightthickness=0)

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
                    fill="white",
                    outline=""
                )

                fila.append(rect)

            self.rectangulos.append(fila)

    # ======================================================

    def dibujar(self, grid):

        # Colores del sistema epidemiológico
        colores = {
            0: "white",   # vacío
            1: "#e0e0e0", # sano
            2: "#e74c3c", # infectado
            3: "#2ecc71", # recuperado
            4: "#2c3e50"  # muerto
        }

        for i in range(self.filas):
            for j in range(self.columnas):

                estado = grid[i][j]

                self.itemconfig(
                    self.rectangulos[i][j],
                    fill=colores.get(estado, "white")
                )