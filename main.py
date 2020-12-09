#!/usr/bin/env python3
import tkinter as tk
# from tkinter.ttk import E

WIDTH = 1000
HEIGHT= 300
HEIGHT_WIDGET = 30
MENU = [ 
    "1. miniature scraping and processing + show graph",
    "2. nytimes: number of articles and CAI",
    "3. science daily: number of articles and CAI",
    "4. comparison of nytimes and science daily 1998-2020",
    "5. co2 graph"
]

def create_app():
    root = tk.Tk()
    root.title("Climate Change Awareness")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(width=False, height=False)
    app = Application(master=root)
    app.mainloop()


class Application(tk.Frame):
    def __init__(self, master=None):
        """Initializes the main frame of the application.
        
        Instance Attributes:
            - master: an instance of tk.Tk
        """
        super().__init__(master)
        self.master = master
        self.place(x=0, y=0, w=WIDTH, h=HEIGHT)
        self.create_widgets()
    

    def create_widgets(self):
        # self.intro = tk.Label(self, text=MENU, fg="white", bg="VioletRed3", anchor='w', justify='left')
        # self.intro.place(x=0, y=0, height=HEIGHT_WIDGET * 4, width=WIDTH)
        # self.intro.config(font=("Courier", 15))
        self.create_menu_and_buttons()

    def create_menu_and_buttons(self):
        self.intro = tk.Label(
            self, text = "WELCOME! Here are a few options:", fg="white", bg="maroon4",
            anchor="w", justify="left"
        )
        self.intro.place(x = 0, y = 0, height=HEIGHT_WIDGET, width=WIDTH)
        self.intro.config(font=("Courier", 20))

        self.options = [None] * len(MENU)
        self.buttons = [None] * len(MENU)
        for i in range(len(MENU)):
            self.options[i] = tk.Label(
                self, text=MENU[i], fg="white", bg="VioletRed3", anchor='w', justify='left'
            )
            self.options[i].place(
                x = 50, y = (i + 1) * HEIGHT_WIDGET, height=HEIGHT_WIDGET, width=WIDTH
            )
            self.buttons[i] = tk.Button(self, text=f"Button {i + 1}", )
            self.buttons[i].place(
                x = 0, y = (i + 1) * HEIGHT_WIDGET, height=HEIGHT_WIDGET, width=50
            )
            self.options[i].config(font=("Courier", 15))
        
    def print_desc(self, event):
        pass

create_app()