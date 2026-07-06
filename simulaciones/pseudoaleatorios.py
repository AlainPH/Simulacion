import pandas as pd


class GeneradorPseudoaleatorio:

    # ==============================================
    # Cuadrados Medios
    # ==============================================

    def cuadrados_medios(self, semilla, cantidad):

        resultados = []

        x = int(semilla)

        d = len(str(semilla).strip())

        for i in range(1, cantidad + 1):

            cuadrado = x ** 2

            cuadrado_str = str(cuadrado).zfill(2 * d)

            start_idx = d // 2

            medio_str = cuadrado_str[start_idx : start_idx + d]

            x_anterior = x

            x = int(medio_str)

            ri = x / (10 ** d)

            resultados.append({

                "i": i,

                "Xi": x_anterior,

                "Xi^2": cuadrado,

                "Xi+1": x,

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

        d = len(str(x1).strip())

        for i in range(1, cantidad + 1):

            producto = a * b

            producto_str = str(producto).zfill(2 * d)

            start_idx = d // 2

            medio_str = producto_str[start_idx : start_idx + d]

            nuevo = int(medio_str)

            ri = nuevo / (10 ** d)

            resultados.append({

                "i": i,

                "Xi-1": a,

                "Xi": b,

                "Producto": producto,

                "Xi+1": nuevo,

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

        const = int(constante)

        d = len(str(semilla).strip())

        for i in range(1, cantidad + 1):

            producto = x * const

            producto_str = str(producto).zfill(2 * d)

            start_idx = d // 2

            medio_str = producto_str[start_idx : start_idx + d]

            x_anterior = x

            x = int(medio_str)

            ri = x / (10 ** d)

            resultados.append({

                "i": i,

                "a": const,

                "Xi": x_anterior,

                "Producto": producto,

                "Xi+1": x,

                "Ri": ri

            })

        return pd.DataFrame(resultados)

    # ==============================================
    # Congruencial Lineal
    # ==============================================

    def congruencial(self, x0, a, c, m, cantidad):

        resultados = []

        x = int(x0)

        for i in range(1, cantidad + 1):

            operacion = a * x + c

            siguiente = operacion % m

            ri = siguiente / m

            resultados.append({

                "i": i,

                "Xi": x,

                "a * Xi + c": operacion,

                "Xi+1": siguiente,

                "Ri": ri

            })

            x = siguiente

        return pd.DataFrame(resultados)