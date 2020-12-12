#!/usr/bin/env python3
import tkinter as tk
from climate_graphs import show_line_graph, show_bar_graph

# Importing matplotlib and required classes and functions to integrate graphs into tkinter GUI.
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
matplotlib.use("TkAgg")


WIDTH = 1250
HEIGHT= 800
HEIGHT_WIDGET = 30
MENU = [ 
    '1. miniature scraping and processing + show graph',
    '2. A "Climate Awareness Index (CAI) vs Years" line graph for New York Times and Science Daily',
    '3. A "Number of Climate Aware Articles vs Years" line graph for New York Times and Science Daily',
    '4. A Comparison of Nytimes and Science Daily 1998-2020',
    '5. co2 graph'
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
        self.Frame2 = tk.Frame(self.master, bg = "pink1")
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
            self.show_graph_1, self.nytimes_cai, self.nytimes_num_articles, self.comparison_cai, self.show_graph_5
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
        print('hello')
    
    def nytimes_cai(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        self.button_switch["command"] = self.science_daily_cai
        show_line_graph(self.ax, 'nytimes')
        self.canvas.draw()
    
    def science_daily_cai(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        self.button_switch["command"] = self.nytimes_cai
        show_line_graph(self.ax, 'science_daily_small')
        self.canvas.draw()
    
    def nytimes_num_articles(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        self.button_switch["command"] = self.science_daily_num_articles
        show_line_graph(self.ax, 'nytimes', False)
        self.canvas.draw()
    
    def science_daily_num_articles(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        self.button_switch["command"] = self.nytimes_num_articles
        show_line_graph(self.ax, 'science_daily_small', False)
        self.canvas.draw()
    
    def comparison_cai(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        self.button_switch["command"] = self.comparison_num_articles
        show_bar_graph(self.ax, 'nytimes', 'science_daily_small')
        self.canvas.draw()
    
    def comparison_num_articles(self):
        if not self.graph_drawn:
            self.draw_graph()
        self.ax.clear() # clear current axes
        self.button_switch["command"] = self.comparison_cai
        show_bar_graph(self.ax, 'nytimes', 'science_daily_small', False)
        self.canvas.draw()

    def show_graph_5(self):
        if not self.graph_drawn:
            self.draw_graph()
        print("5")

    def _quit(self):
        self.Frame2.quit()

create_app()