class GeneradorLotkaVolterra:

    def __init__(self):
        pass

    def simular(self, x0, y0, alpha, beta, gamma, delta, dt, pasos):
        """
        Simula el modelo de depredador-presa Lotka-Volterra usando el método de Runge-Kutta de 4to orden (RK4).
        
        Parámetros:
        - x0: Población inicial de presas
        - y0: Población inicial de depredadores
        - alpha: Tasa de crecimiento de las presas (nacimientos)
        - beta: Tasa de depredación (encuentros mortales para las presas)
        - gamma: Tasa de mortalidad natural de depredadores
        - delta: Tasa de incremento/crecimiento de depredadores por presa consumida
        - dt: Paso de tiempo
        - pasos: Número total de pasos a simular
        """
        t = [0.0]
        x = [float(x0)]
        y = [float(y0)]

        curr_x = float(x0)
        curr_y = float(y0)

        for i in range(1, pasos + 1):
            # RK4: k1
            dx1 = alpha * curr_x - beta * curr_x * curr_y
            dy1 = delta * curr_x * curr_y - gamma * curr_y

            # RK4: k2
            tx2_x = curr_x + 0.5 * dt * dx1
            tx2_y = curr_y + 0.5 * dt * dy1
            dx2 = alpha * tx2_x - beta * tx2_x * tx2_y
            dy2 = delta * tx2_x * tx2_y - gamma * tx2_y

            # RK4: k3
            tx3_x = curr_x + 0.5 * dt * dx2
            tx3_y = curr_y + 0.5 * dt * dy2
            dx3 = alpha * tx3_x - beta * tx3_x * tx3_y
            dy3 = delta * tx3_x * tx3_y - gamma * tx3_y

            # RK4: k4
            tx4_x = curr_x + dt * dx3
            tx4_y = curr_y + dt * dy3
            dx4 = alpha * tx4_x - beta * tx4_x * tx4_y
            dy4 = delta * tx4_x * tx4_y - gamma * tx4_y

            # Actualizar valores
            curr_x = curr_x + (dt / 6.0) * (dx1 + 2.0 * dx2 + 2.0 * dx3 + dx4)
            curr_y = curr_y + (dt / 6.0) * (dy1 + 2.0 * dy2 + 2.0 * dy3 + dy4)

            # Evitar poblaciones negativas
            if curr_x < 0.0:
                curr_x = 0.0
            if curr_y < 0.0:
                curr_y = 0.0

            t.append(i * dt)
            x.append(curr_x)
            y.append(curr_y)

        return t, x, y
