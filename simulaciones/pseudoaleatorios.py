import pandas as pd


class GeneradorPseudoaleatorio:

    # ==============================================
    # Cuadrados Medios
    # ==============================================

    def cuadrados_medios(self, semilla, cantidad):

        resultados = []

        x = int(semilla)

        for _ in range(cantidad):

            cuadrado = str(x ** 2).zfill(8)

            medio = cuadrado[2:6]

            x = int(medio)

            ri = x / 10000

            resultados.append({
                "Semilla": x,
                "Ri": ri
            })

        return pd.DataFrame(resultados)

    # ==============================================
    # Productos Medios
    # ==============================================

    def productos_medios(self, x1, x2, cantidad):

        resultados = []

        a = int(x1)
        b = int(x2)

        for _ in range(cantidad):

            producto = str(a * b).zfill(8)

            medio = producto[2:6]

            nuevo = int(medio)

            ri = nuevo / 10000

            resultados.append({
                "Semilla": nuevo,
                "Ri": ri
            })

            a = b
            b = nuevo

        return pd.DataFrame(resultados)

    # ==============================================
    # Multiplicador Constante
    # ==============================================

    def multiplicador_constante(self, semilla, constante, cantidad):

        resultados = []

        x = int(semilla)

        for _ in range(cantidad):

            producto = str(x * constante).zfill(8)

            medio = producto[2:6]

            x = int(medio)

            ri = x / 10000

            resultados.append({
                "Semilla": x,
                "Ri": ri
            })

        return pd.DataFrame(resultados)

    # ==============================================
    # Congruencial Lineal
    # ==============================================

    def congruencial(self, x0, a, c, m, cantidad):

        resultados = []

        x = int(x0)

        for _ in range(cantidad):

            x = (a * x + c) % m

            ri = x / m

            resultados.append({
                "Semilla": x,
                "Ri": ri
            })

        return pd.DataFrame(resultados)