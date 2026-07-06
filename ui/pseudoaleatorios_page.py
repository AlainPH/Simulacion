import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from simulaciones.pseudoaleatorios import GeneradorPseudoaleatorio


class PseudoaleatoriosPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.generador = GeneradorPseudoaleatorio()

        self.df = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_panel()
        self.crear_tabla()