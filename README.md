# 📊 Simulador de Modelos Matemáticos y Algoritmos

Este proyecto es una aplicación de escritorio interactiva desarrollada en **Python** con **CustomTkinter**. Su objetivo es simular y visualizar diversos modelos matemáticos, epidemiológicos, económicos y algorítmicos de forma visual y didáctica. 

Cada simulación incluye un panel de control con parámetros configurables en tiempo real, representaciones gráficas interactivas y una **Guía Didáctica** integrada que detalla los fundamentos matemáticos de cada modelo.

---

## 🚀 Características Principales

### 1. 🎲 Generadores Pseudoaleatorios
Implementa y compara los cuatro algoritmos clásicos de generación de números aleatorios por computadora:
* **Cuadrados Medios:** Método de John von Neumann que extrae dígitos centrales del cuadrado de la semilla.
* **Productos Medios:** Utiliza la multiplicación de dos semillas consecutivas.
* **Multiplicador Constante:** Utiliza el producto de una constante fija por la semilla.
* **Congruencial Lineal (LCG):** Algoritmo de Lehmer basado en aritmética modular ($X_{i+1} = (aX_i + c) \pmod m$).
* **Visualización:** Gráfica lineal del comportamiento de la secuencia e histograma para verificar visualmente la **Distribución Uniforme ($U[0,1]$)**.

### 🎰 2. Simulación de Ruleta (Monte Carlo)
Estudio empírico de probabilidades aplicadas al juego de la ruleta europea:
* Demostración práctica de la **Ley de los Grandes Números** y la ventaja matemática de la casa (2.70% debido al cero).
* Gráfica en tiempo real del capital del jugador para evidenciar el fenómeno de la **Ruina del Jugador**.
* **Marcador de Casino:** Panel dinámico que muestra la última tirada con su color correspondiente (Rojo, Negro o Cero) y un historial de los últimos 6 giros.

### 🦠 3. Simulación Epidemiológica COVID (SIR 2D)
Autómata celular bidimensional en cuadrícula que modela la dispersión de patógenos en el espacio físico:
* Clasificación de estados **SIR**: Sano (Susceptible), Infectado, Recuperado (Inmune) y Muerto.
* Reglas de contagio basadas en el **Vecindario de Moore** (8 vecinos adyacentes).
* Sliders para ajustar en tiempo real la tasa de contagio, recuperación, mortalidad y velocidad del ciclo.
* Visualización en modo neón futurista con estadísticas de población activa.

### 🧬 4. Autómatas Celulares 1D (Wolfram)
Simulador de los 256 autómatas celulares unidimensionales definidos por Stephen Wolfram:
* Opciones para elegir reglas destacadas (como la Regla 30 caótica, Regla 90 fractal o la Regla 110 Turing completa).
* Ajuste de dimensiones de la rejilla, generaciones de tiempo e inicialización (celda única o aleatoria).
* Renderizado instantáneo de la historia completa o modo de simulación animado paso a paso.

### 📈 5. Modelo Depredador-Presa de Lotka-Volterra
Resolución numérica de ecuaciones diferenciales ordinarias acopladas:
* Motor de cálculo basado en el método de **Runge-Kutta de 4to orden (RK4)** para garantizar estabilidad numérica.
* Gráfica dual: **Evolución Temporal** (Poblaciones vs Tiempo) y **Plano de Fase** (Presas vs Depredadores) para visualizar las órbitas y puntos de equilibrio.
* Presets integrados para ciclos estables, explosiones demográficas y extinción ecológica.

### 🌾 6. Simulación de Producción de Quinua
Modelo ecofisiológico y financiero de un cultivo de quinua (*Chenopodium quinoa*) a lo largo de un ciclo agrícola de 150 días:
* Simulación del crecimiento de biomasa y llenado de grano afectados por temperatura (acumulación de GDD base 3°C), disponibilidad de agua en suelo (evapotranspiración y riegos), fertilización NPK y densidad de siembra.
* **Balance Financiero:** Cálculo automático de la inversión (semilla, agua, NPK, mano de obra) frente a ingresos brutos según el precio internacional del mercado, mostrando la ganancia neta y el **Retorno de Inversión (ROI)**.
* Escenarios de clima preconfigurados: Altiplano Templado, Seco/Frío y Valles Interandinos.

---

## 📂 Estructura del Proyecto

```text
Simulacion/
│
├── main.py                 # Punto de entrada de la aplicación
├── app.py                  # Inicialización y configuración de la app
├── config.py               # Configuración de apariencia, dimensiones y paleta de colores
├── requirements.txt        # Dependencias de librerías del proyecto
│
├── simulaciones/           # Motores de cálculo de cada simulación
│   ├── automata.py
│   ├── covid.py
│   ├── grid_engine.py
│   ├── lotka.py
│   ├── pseudoaleatorios.py
│   ├── quinua.py
│   └── ruleta.py
│
├── ui/                     # Vistas y componentes del entorno gráfico (GUI)
│   ├── main_window.py      # Estructura principal (Sidebar + Navbar + Contenido)
│   ├── sidebar.py          # Barra lateral de navegación
│   ├── navbar.py           # Cabecera con fecha y usuario
│   ├── dashboard.py        # Panel de inicio con accesos directos dinámicos
│   ├── pseudoaleatorios_page.py
│   ├── ruleta_page.py
│   ├── covid_page.py
│   ├── automata_page.py
│   ├── lotka_page.py
│   └── quinua_page.py
│
└── components/             # Widgets y lienzos personalizados reutilizables
    ├── grid_canvas.py      # Grid gráfico para autómata de contagios
    └── table.py            # Tabla estilizada oscura para visualización de datos
```

---

## 🛠️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

### 1. Clonar el repositorio
Si aún no has clonado el repositorio, ejecuta en la terminal:
```bash
git clone https://github.com/AlainPH/Simulacion.git
cd Simulacion
```

### 2. Instalar dependencias
Asegúrate de tener Python 3.8 o superior instalado. Instala las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
Para iniciar el simulador, simplemente ejecuta el archivo principal:
```bash
python main.py
```

---

## 💡 Tecnologías Utilizadas
* **Python 3** (Lenguaje principal)
* **CustomTkinter** (Diseño moderno e interactivo de la interfaz de usuario en modo oscuro)
* **Matplotlib** (Generación de gráficos científicos en tiempo real)
* **Pandas** y **NumPy** (Manipulación eficiente de datos y vectores matemáticos)

---
Desarrollado con fines educativos y de simulación científica por **Alain Puente**.
