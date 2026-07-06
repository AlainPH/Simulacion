import numpy as np


class AutomataCelular:

    def __init__(self):
        pass

    def simular(self, regla, columnas, generaciones, estado_inicial="single"):
        """
        Simula un autómata celular 1D según una regla de Wolfram (0-255).
        
        Regla en binario de 8 bits (ej. Regla 30 -> 00011110)
        Los índices corresponden a los vecinos (izq, centro, der) en binario:
        7: 111, 6: 110, 5: 101, 4: 100, 3: 011, 2: 010, 1: 001, 0: 000
        """
        # Convertir la regla a su representación binaria de 8 bits (lista de 8 elementos)
        # regla_bin[i] representa el estado siguiente para la configuración i
        regla_bin = [(regla >> i) & 1 for i in range(8)]
        
        # Grid para almacenar la historia (filas = generaciones, columnas = tamaño del grid)
        grid = np.zeros((generaciones, columnas), dtype=np.uint8)
        
        # Inicialización
        if estado_inicial == "single":
            grid[0, columnas // 2] = 1
        else:
            grid[0] = np.random.choice([0, 1], size=columnas, p=[0.5, 0.5])
            
        for g in range(1, generaciones):
            for c in range(columnas):
                # Vecinos con condiciones de frontera periódicas (toroidal)
                izq = grid[g - 1, (c - 1) % columnas]
                cen = grid[g - 1, c]
                der = grid[g - 1, (c + 1) % columnas]
                
                # Calcular el índice del estado de los vecinos
                estado_vecinos = (izq << 2) | (cen << 1) | der
                
                # Asignar el nuevo estado según la regla de Wolfram
                grid[g, c] = regla_bin[estado_vecinos]
                
        return grid
