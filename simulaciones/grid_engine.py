import numpy as np


class GridEngine:

    VACIO = 0
    SANO = 1
    INFECTADO = 2
    RECUPERADO = 3
    MUERTO = 4

    def __init__(self, filas=120, columnas=120):

        self.filas = filas
        self.columnas = columnas

        self.grid = np.full(
            (filas, columnas),
            self.SANO,
            dtype=np.uint8
        )

        self.contagio = 0.35
        self.recuperacion = 0.02
        self.muerte = 0.01

        self.iteracion = 0
        self.max_iteraciones = 500

    # =====================================================

    def reiniciar(self, infectados=20):

        self.grid.fill(self.SANO)

        infectados = max(
            1,
            min(
                infectados,
                self.filas * self.columnas
            )
        )

        posiciones = np.random.choice(
            self.filas * self.columnas,
            infectados,
            replace=False
        )

        for p in posiciones:

            fila = p // self.columnas
            columna = p % self.columnas

            self.grid[fila, columna] = self.INFECTADO

        self.iteracion = 0

    # =====================================================

    def vecinos(self, i, j):

        for di in (-1, 0, 1):

            for dj in (-1, 0, 1):

                if di == 0 and dj == 0:
                    continue

                ni = i + di
                nj = j + dj

                if (
                    0 <= ni < self.filas
                    and
                    0 <= nj < self.columnas
                ):

                    yield ni, nj

    # =====================================================

    def paso(self):

        if self.iteracion >= self.max_iteraciones:
            return

        nueva = self.grid.copy()

        for i in range(self.filas):

            for j in range(self.columnas):

                if self.grid[i, j] != self.INFECTADO:
                    continue

                # ---------------- MUERTE ----------------

                if np.random.random() < self.muerte:

                    nueva[i, j] = self.MUERTO
                    continue

                # ------------ RECUPERACIÓN -------------

                if np.random.random() < self.recuperacion:

                    nueva[i, j] = self.RECUPERADO
                    continue

                # --------------- CONTAGIO --------------

                for ni, nj in self.vecinos(i, j):

                    if nueva[ni, nj] != self.SANO:
                        continue

                    if np.random.random() < self.contagio:

                        nueva[ni, nj] = self.INFECTADO

        self.grid = nueva

        self.iteracion += 1

    # =====================================================

    def estadisticas(self):

        return {

            "sanos": int(
                np.sum(
                    self.grid == self.SANO
                )
            ),

            "infectados": int(
                np.sum(
                    self.grid == self.INFECTADO
                )
            ),

            "recuperados": int(
                np.sum(
                    self.grid == self.RECUPERADO
                )
            ),

            "muertos": int(
                np.sum(
                    self.grid == self.MUERTO
                )
            ),

            "iteracion": self.iteracion

        }