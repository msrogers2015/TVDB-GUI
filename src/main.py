import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog


class App(tk.Tk):
    def __init__(self):
        """Creation of the base application. The App class inherits from tk.Tk so that 'self' can be used instead of
        'self.root' allowing a more streamlined approach for the gui. Upon initialization, the gui engine is ran and
        creates all widgets within the provided layout.json file."""
        super().__init__()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.widgets = {}
        self.functions = {}
        self.parse_gui = GUIParser(self, self.widgets, self.functions, self.base_dir)
        self.configure_gui()
        self.create_gui()

    def configure_gui(self):
        """Base application configurations including sizing, appearance, application title, etc."""
        self.title("TVDB GUI")
        self.resizable(width=False, height=False)
        width = 800
        height = 600
        x_pos = (self.winfo_screenwidth() // 2) - (width // 2)
        y_pos = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    def create_gui(self):
        """Create GUI widgets via parsing a json file with widget parameters."""
        json_path = os.path.join(self.base_dir, "layout.json")

        with open(json_path, "r") as file:
            data = json.load(file)
            for item in data:
                match data[item]["type"]:
                    case "label":
                        self.parse_gui.parse_label(data[item], item)
                    case "button":
                        self.parse_gui.parse_button(data[item], item)
                    case "frame":
                        self.parse_gui.parse_frame(data[item], item)
                    case "treeview":
                        self.parse_gui.parse_treeview(data[item], item)
                    case "menu":
                        self.parse_gui.parse_menu(data[item], item)
                    case "dropdown":
                        self.parse_gui.parse_dropdown(data[item], item)
                    case "image":
                        self.parse_gui.parse_image(data[item], item)


class GUIParser:
    def __init__(self, root: tk.Tk, widgets: dict, functions: dict,base_dir: str):
        """Assign base references for gui engine.
            Args:
            Root: The base of the application, the tk root object.
            Widgets: A dictionary of widgets that can be referenced when a widget needs to be udpdated e.g. update
                the string within a label or disable/enable buttons.
            Functions: A dictionary of functions from the base application that can be assigned to widgets based on
                the data from the json dump.
            Base_Dir: The base directory of the application.
        """
        self.root = root
        self.widgets = widgets
        self.functions = functions
        self.base_dir = base_dir

    def parse_label(self, data: dict, item: str) -> None:
        """Creates a ttk.Label using data passed from the json dump. The item name is widget dict reference point for
        any required in-process configuration updates. Currently supported arguments are:Placement (either the root
        application or another widget), Anchor (or placement of the text within the label), Font Infromation
        (font-family and font-size)"""
        self.widgets[item] = ttk.Label(
            self.root if data['location'] == "root" else self.widgets[data['location']],
            text=data["text"],
            anchor=data["anchor"],
            font=(data["font"]["family"], data["font"]["size"]),
        )
        self.widgets[item].place(
            x=data["x"], y=data["y"], width=data["width"], height=data["height"]
        )

    def parse_frame(self, data: dict, item: str) -> None:
        """Creates a ttk.Frame using data passed from the json dump. The item name is widget dict reference point for
        any required in-process configuration updates. Currently supported arguments are:Placement (either the root
        application or another widget, Borderwidth, Height/Width, Relief"""
        self.widgets[item] = ttk.Frame(
            self.root if data['location'] == "root" else self.widgets[data['location']],
            borderwidth=data["borderwidth"],
            height=data["height"],
            width=data["width"],
            relief=data["relief"],
        )
        self.widgets[item].place(x=data["x"], y=data["y"])

    def parse_treeview(self, data: dict, item: str) -> None:
        """Creates a ttk.Treeview using data passed from the json dump. The item name is widget dict reference point for
        any required in-process configuration updates. Currently supported arguments are: Placement (either the root
        application or another widget, Vertical Scroll Bar, Horizontal Scroll Bar, and Dynamic Column Creation"""
        self.widgets[item] = ttk.Treeview(
            self.root if data['location'] == "root" else self.widgets[data['location']],
        )
        self.widgets[item]['columns'] = list(data['columns'].keys())
        self.widgets[item].column('#0', width=0, minwidth=0, stretch='no')
        self.widgets[item].heading('#0', text='')
        # Create columns
        for col in data['columns']:
            col_data = data['columns'][col]
            self.widgets[item].column(col, width=col_data['width'], minwidth=col_data['width'])
            self.widgets[item].heading(col, text=col)
        # PLace treeview so that scroll bars can be added as needed.
        self.widgets[item].place(x=data["x"], y=data["y"], width=data["width"], height=data["height"])

        if data['xscroll'] != "":
            x_scroll_bar = ttk.Scrollbar(self.widgets[item], orient='horizontal')
            x_scroll_bar.config(command=self.widgets[item].xview)
            self.widgets[item].config(xscrollcommand=x_scroll_bar.set, selectmode='extended')
            x_scroll_bar.pack(side=data['xscroll']['location'], fill='x')

        if data['yscroll'] != "":
            y_scroll_bar = ttk.Scrollbar(self.widgets[item], orient='vertical')
            y_scroll_bar.config(command=self.widgets[item].yview)
            self.widgets[item].config(yscrollcommand=y_scroll_bar.set, selectmode='extended')
            y_scroll_bar.pack(side=data['yscroll']['location'], fill='y')

    def parse_button(self, data: dict, item: str) -> None:
        """Creates a ttk.Button using data passed from the json dump. The item name is widget dict reference point for
        any required in-process configuration updates. Currently supported arguments are: Placement (either the root
        application or another widget, Text within the button, Function to be ran (command), and intital active state"""
        self.widgets[item] = ttk.Button(
            self.root if data['location'] == "root" else self.widgets[data['location']],
            text=data["text"], command=self.functions[data["command"]] if data['command'] is not None else None,
        )
        if data['state'] != '':
            self.widgets[item].configure(state=data['state'])

        self.widgets[item].place(x=data["x"], y=data["y"], width=data["width"], height=data["height"])

    def parse_menu(self, data: dict, item: str) -> None:
        """Creates a tk.Menu using data passed from the json dump. The item name is widget dict reference point for
        any required in-process configuration updates. Currently supported arguments are: Placement (either the root
        application or another widget, specifically the sub-menus), items within each sub-menu, and the function of
        each item within a sub-menu."""
        self.widgets[item] = tk.Menu(self.root)
        for submenu in list(data['sub_menus'].keys()):
            sub_data = data['sub_menus'][submenu]
            self.widgets[submenu] = tk.Menu(self.widgets[item], tearoff=False)
            for command in sub_data['commands']:
                self.widgets[submenu].add_command(label=command, command=lambda : print(command))
            self.widgets[item].add_cascade(label=sub_data['name'], menu = self.widgets[submenu])

        self.root.config(menu = self.widgets[item])

    def parse_dropdown(self, data: dict, item: str) -> None:
        """Creates a ttk.OptionMenu using data passed from the json dump. The item name is widget dict reference point
        for any required in-process configuration updates. Currently supported arguments are: Placement (either the root
        application or another widget), the StringVar displaying the current option within the option menu, list of
        intial options to provide, and the default option to display."""
        self.widgets[data['variable']] = tk.StringVar()
        self.widgets[data['variable']].set(data['default'])
        self.widgets[item] = ttk.OptionMenu(
            self.root if data['location'] == "root" else self.widgets[data['location']],
            self.widgets[data['variable']],
            *data['options']
        )
        self.widgets[item].place(x=data["x"], y=data["y"], width=data["width"], height=data["height"])

    def parse_image(self, data: dict, item: str) -> None:
        """Creates an image using data passed from the json dump. The item name is widget dict reference point for
        any required in-process configuration updates. Currently supported arguments are: Placement (either the root
        application or another widget), location of the image via a path join, and a name for the ttk.lable hosting
        and displaying the image (which is what is saved to the widgets dict)."""
        img_path = os.path.join(self.base_dir, data['sub_directory'], data['image_path'])
        self.widgets[item] = tk.PhotoImage(file=img_path)

        self.widgets[item] = tk.PhotoImage(file=img_path, width=data["width"], height=data["height"])
        self.widgets[data['label_name']] = ttk.Label(
            self.root if data['location'] == "root" else self.widgets[data['location']],
            image = self.widgets[item]
        )
        self.widgets[data['label_name']].place(x=data["x"], y=data["y"], width=data["width"], height=data["height"])

if __name__ == "__main__":
    app = App()
    app.mainloop()
