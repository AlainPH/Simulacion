import random
import pandas as pd


class SimuladorRuleta:

    def __init__(self):

        self.historial = []

    # ==========================================
    # Simulación
    # ==========================================

    def simular(self, apuesta, capital, apuesta_fija, tiradas):

        dinero = float(capital)

        resultados = []

        for i in range(int(tiradas)):

            numero = random.randint(0, 36)

            gano = False

            premio = 0

            # -------------------------
            # Color
            # -------------------------

            rojos = [
                1,3,5,7,9,12,14,16,18,
                19,21,23,25,27,30,32,34,36
            ]

            if apuesta == "Rojo":

                if numero in rojos:

                    gano = True

                    premio = apuesta_fija

            elif apuesta == "Negro":

                if numero != 0 and numero not in rojos:

                    gano = True

                    premio = apuesta_fija

            elif apuesta == "Par":

                if numero != 0 and numero % 2 == 0:

                    gano = True

                    premio = apuesta_fija

            elif apuesta == "Impar":

                if numero % 2 == 1:

                    gano = True

                    premio = apuesta_fija

            if gano:

                dinero += premio

            else:

                dinero -= apuesta_fija

            resultados.append({

                "Tirada": i + 1,

                "Número": numero,

                "Ganó": "Sí" if gano else "No",

                "Capital": dinero

            })

        return pd.DataFrame(resultados)