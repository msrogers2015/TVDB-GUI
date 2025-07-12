import json
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.widgets = {}
        self.configure_gui()
        self.create_gui()

    def configure_gui(self):
        """Base application configurations including sizing, appearance, applicaiton title, etc."""
        self.title("TVDB GUI")
        self.resizable(width=False, height=False)
        width = 600
        height = 400
        x_pos = (self.winfo_screenwidth() // 2) - (width // 2)
        y_pos = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    def create_gui(self):
        """Create GUI widgets via parsing a json file with widget parameters."""
        with open("layout.json", "r") as file:
            data = json.load(file)
            for item in data:
                match data[item]["type"]:
                    case "label":
                        self.parse_gui.parse_label(data[item], item)
                    case "frame":
                        self.parse_gui.parse_frame(data[item], item)


if __name__ == "__main__":
    app = App()
    app.mainloop()
