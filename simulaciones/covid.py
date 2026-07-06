import numpy as np


class SimuladorCovid:

    VACIO = 0
    SANO = 1
    INFECTADO = 2
    RECUPERADO = 3

    def __init__(
        self,
        filas=120,
        columnas=180,
        prob_inicial=0.01,
        prob_contagio=0.35,
        prob_recuperacion=0.02
    ):

        self.filas = filas
        self.columnas = columnas

        self.prob_contagio = prob_contagio
        self.prob_recuperacion = prob_recuperacion

        self.matriz = np.ones((filas, columnas), dtype=int)

        infectados = np.random.rand(filas, columnas) < prob_inicial

        self.matriz[infectados] = self.INFECTADO

    def paso(self):

        nueva = self.matriz.copy()

        for i in range(self.filas):

            for j in range(self.columnas):

                if self.matriz[i, j] == self.INFECTADO:

                    if np.random.random() < self.prob_recuperacion:

                        nueva[i, j] = self.RECUPERADO

                    for di in (-1, 0, 1):

                        for dj in (-1, 0, 1):

                            if di == 0 and dj == 0:
                                continue

                            ni = i + di
                            nj = j + dj

                            if (
                                0 <= ni < self.filas and
                                0 <= nj < self.columnas
                            ):

                                if self.matriz[ni, nj] == self.SANO:

                                    if np.random.random() < self.prob_contagio:

                                        nueva[ni, nj] = self.INFECTADO

        self.matriz = nueva

        return self.matriz