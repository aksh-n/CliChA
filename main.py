#!/usr/bin/env python3
import tkinter as tk
from climate_graphs import show_line_graph

# Importing matplotlib and required classes and functions to integrate graphs into tkinter GUI.
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
matplotlib.use("TkAgg")


WIDTH = 800
HEIGHT= 800
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


def config_plot():
    fig, ax = matplotlib.pyplot.subplots()
    ax.set(xlabel = 'Year', ylabel = 'Climate Awareness Index (CAI)', title = 'Graph 1')
    return (fig, ax)


class Application(tk.Frame):
    def __init__(self, master=None):
        """Initializes the main frame of the application.
        
        Instance Attributes:
            - master: an instance of tk.Tk
        """
        super().__init__(master)
        master.protocol('WM_DELETE_WINDOW', self._quit)
        self.master = master
        self.place(x=0, y=0, w=WIDTH, h=HEIGHT)
        self.create_widgets()
        self.graph_drawn = False
    

    def create_widgets(self):
        self.create_menu_and_buttons()
        self.Frame2 = tk.Frame(self.master, bg = "pink")
        self.Frame2.place(
            x = 0, y = HEIGHT_WIDGET * (len(MENU) + 1),
            height = HEIGHT - HEIGHT_WIDGET * (len(MENU) + 1), width = WIDTH
        )

    def create_menu_and_buttons(self):
        Frame1 = tk.Frame(self.master, bg = "pink")
        Frame1.place(x = 0, y = 0, height = HEIGHT_WIDGET * (len(MENU) + 1), width = WIDTH)
        self.intro = tk.Label(
            Frame1, text = "WELCOME! Here are a few options:", fg="white", bg="MediumPurple4",
            anchor="w", justify="left"
        )
        self.intro.place(x = 0, y = 0, height=HEIGHT_WIDGET, width=WIDTH)
        self.intro.config(font=("Courier", 20))

        self.options = [None] * len(MENU)
        self.buttons = [None] * len(MENU)

        show_graphs = [
            self.show_graph_1, self.show_graph_2, self.show_graph_3, self.show_graph_4, self.show_graph_5
        ]
        for i in range(len(MENU)):
            self.options[i] = tk.Label(
                Frame1, text=MENU[i], fg="white", bg="VioletRed3", anchor='w', justify='left'
            )
            self.options[i].place(
                x = 50, y = (i + 1) * HEIGHT_WIDGET, height=HEIGHT_WIDGET, width=WIDTH
            )
            self.buttons[i] = tk.Button(Frame1, text=f"B{i + 1}", fg="white", bg="black")
            self.buttons[i].place(
                x = 0, y = (i + 1) * HEIGHT_WIDGET, height=HEIGHT_WIDGET, width=50
            )
            self.options[i].config(font=("Courier", 15))
            self.buttons[i].config(font=("Courier", 15), command=show_graphs[i])
    
    def draw_graph(self):
        self.graph_drawn = True
        self.fig, self.ax = config_plot()
        self.graphIndex = 0
        self.canvas = FigureCanvasTkAgg(self.fig, self.Frame2)
        self.config_window()
    
    def config_window(self):
        toolbar = NavigationToolbar2Tk(self.canvas, self.Frame2)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.button = tk.Button(self.Frame2, text="Quit", command=self._quit)
        self.button.pack(side=tk.BOTTOM)
        self.button_switch = tk.Button(self.Frame2, text="Switch Graphs") #, command=self.switch_graphs)
        self.button_switch.pack(side=tk.BOTTOM)

    def show_graph_1(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        print('hello')
    
    def show_graph_2(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        show_line_graph(self.ax, 'nytimes')
        self.canvas.draw()
    
    def show_graph_3(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        show_line_graph(self.ax, 'science_daily_small')
        self.canvas.draw()
    
    def show_graph_4(self):
        if not self.graph_drawn:
            self.draw_graph()
        print("4")
    
    def show_graph_5(self):
        if not self.graph_drawn:
            self.draw_graph()
        print("5")

    def _quit(self):
        self.Frame2.quit()

create_app()