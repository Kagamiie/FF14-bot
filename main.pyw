import tkinter as tk
from tkinter import ttk
import threading
import time

from fishing_macro import macro_loop as fishing_macro  # Ton script principal
from combat_macro import run_macro as simple_macro    # Le script qui fait 1-2-3

class FFXIVMacroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV Macro Controller")
        # self.root.geometry("200x50")
        self.root.resizable(False, False)

        self.fishing_var = tk.BooleanVar()
        self.simple_var = tk.BooleanVar()

        self.root.attributes('-topmost', True)

        # Création des boutons de sélection
        ttk.Checkbutton(
            root, text="Fishing Macro", variable=self.fishing_var,
            command=lambda: self.toggle_macro('fishing')
        ).pack(padx=5)

        ttk.Checkbutton(
            root, text="Simple Macro (1-2-3 Loop)", variable=self.simple_var,
            command=lambda: self.toggle_macro('simple')
        ).pack(padx=5)

        # Variables pour les threads et événements
        self.threads = {}
        self.events = {'fishing': threading.Event(), 'simple': threading.Event()}

    def toggle_macro(self, macro_type):
        if getattr(self, f'{macro_type}_var').get():
            if macro_type not in self.threads or not self.threads[macro_type].is_alive():
                self.events[macro_type].clear()  # Réinitialise l'événement
                thread = threading.Thread(target=self.run_macro, args=(macro_type,), daemon=True)
                self.threads[macro_type] = thread
                thread.start()
        else:
            self.events[macro_type].set()  # Signale au thread de s'arrêter

    def run_macro(self, macro_type):
        while not self.events[macro_type].is_set():
            if macro_type == 'fishing':
                fishing_macro()
            elif macro_type == 'simple':
                simple_macro()

if __name__ == "__main__":
    root = tk.Tk()
    app = FFXIVMacroGUI(root)
    root.mainloop()
