import customtkinter as ctk

import config

from ui.main_window import MainWindow


class SimuladorApp:

    def __init__(self):

        ctk.set_appearance_mode(config.THEME)

        ctk.set_default_color_theme(config.COLOR_THEME)

        self.window = MainWindow()

    def run(self):

        self.window.mainloop()