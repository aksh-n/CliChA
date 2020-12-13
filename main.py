#!/usr/bin/env python3
"""Climate Change Awareness (CliChA), Main Module

This module provides a graphical user interface (GUI) using tkinter.
Runs a demo and provides visualizations relevant to the project.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
import tkinter as tk
import threading
from climate_graphs import show_line_graph, show_bar_graph, demo_graph, co2_comparison_graph
from main_backend import run_demo_nytimes, demo_processing_cai

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
    '5. A Comparison of Climate Awareness Index of Nytimes/Science Daily and CO2 concentration'
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
        self.Frame1 = tk.Frame(self.master, bg = "pink")
        self.Frame1.place(x = 0, y = 0, height = HEIGHT_WIDGET * (len(MENU) + 2), width = WIDTH)
        self.create_menu_and_buttons()
        self.demo_message = tk.Label(self.Frame1, text = "", fg="white", bg="MediumPurple4")
        self.demo_message.place(
            x = 0, y = (len(MENU) + 1) * HEIGHT_WIDGET, height = HEIGHT_WIDGET, width = WIDTH
        )
        self.Frame2 = tk.Frame(self.master, bg = "pink1")
        self.Frame2.place(
            x = 0, y = HEIGHT_WIDGET * (len(MENU) + 2),
            height = HEIGHT - HEIGHT_WIDGET * (len(MENU) + 2), width = WIDTH
        )

    def create_menu_and_buttons(self):
        self.intro = tk.Label(
            self.Frame1, text = "WELCOME! Here are a few options:", fg="white", bg="black",
            anchor="w", justify="left"
        )
        self.intro.place(x = 0, y = 0, height=HEIGHT_WIDGET, width=WIDTH)
        self.intro.config(font=("Courier", 20))

        self.options = [None] * len(MENU)
        self.buttons = [None] * len(MENU)

        show_graphs = [
            self.demo_start, self.nytimes_cai, self.nytimes_num_articles,
            self.comparison_cai, self.co2_comparison_nytimes
        ]
        for i in range(len(MENU)):
            self.options[i] = tk.Label(
                self.Frame1, text=MENU[i], fg="white", bg="VioletRed3", anchor='w', justify='left'
            )
            self.options[i].place(
                x = 50, y = (i + 1) * HEIGHT_WIDGET, height=HEIGHT_WIDGET, width=WIDTH
            )
            self.buttons[i] = tk.Button(self.Frame1, text=f"B{i + 1}", fg="white", bg="black")
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

    def demo_start(self):
        print("ZZZZZZZZZZZZZZZZZZZZZZZZ")
    #     if not self.graph_drawn:
    #         self.draw_graph()
    #     self.ax.clear() # clear current axes
    #     self.button_switch["text"] = "Start Demo!"
    #     self.button_switch["command"] = threading.Thread(target=self.demo_scraping_processing_graph)
    
    # def demo_scraping_processing_graph(self):
    #     self.demo_message["text"] = "Now Scraping, Please Wait."
    #     threading.Thread(target=run_demo_nytimes()).start()
    #     self.demo_message["text"] = "Now Processing, Please Wait."
    #     threading.Thread(target=demo_graph(self.ax, demo_processing_cai())).start()
    #     self.demo_message["text"] = ""
    #     print("Done!")
    
    def nytimes_cai(self):
        if not self.graph_drawn:
            self.draw_graph()
        self._clear()
        self.button_switch["text"] = "Switch Graphs"
        self.button_switch["command"] = self.science_daily_cai
        show_line_graph(self.ax, 'nytimes')
        self.canvas.draw()
    
    def science_daily_cai(self):
        if not self.graph_drawn:
            self.draw_graph()
        self._clear()
        self.button_switch["text"] = "Switch Graphs"
        self.button_switch["command"] = self.nytimes_cai
        show_line_graph(self.ax, 'science_daily_small')
        self.canvas.draw()
    
    def nytimes_num_articles(self):
        if not self.graph_drawn:
            self.draw_graph()
        self._clear()
        self.button_switch["text"] = "Switch Graphs"
        self.button_switch["command"] = self.science_daily_num_articles
        show_line_graph(self.ax, 'nytimes', False)
        self.canvas.draw()
    
    def science_daily_num_articles(self):
        if not self.graph_drawn:
            self.draw_graph()
        self._clear()
        self.button_switch["text"] = "Switch Graphs"
        self.button_switch["command"] = self.nytimes_num_articles
        show_line_graph(self.ax, 'science_daily_small', False)
        self.canvas.draw()
    
    def comparison_cai(self):
        if not self.graph_drawn:
            self.draw_graph()
        self._clear()
        self.button_switch["text"] = "Switch Graphs"
        self.button_switch["command"] = self.comparison_num_articles
        show_bar_graph(self.ax, 'science_daily_small', 'nytimes')
        self.canvas.draw()
    
    def comparison_num_articles(self):
        if not self.graph_drawn:
            self.draw_graph()
        self._clear()
        self.button_switch["text"] = "Switch Graphs"
        self.button_switch["command"] = self.comparison_cai
        show_bar_graph(self.ax, 'science_daily_small', 'nytimes', False)
        self.canvas.draw()

    def co2_comparison_nytimes(self):
        if not self.graph_drawn:
            self.draw_graph()
        self._clear()
        self.button_switch["text"] = "Switch Graphs"
        self.button_switch["command"] = self.co2_comparison_science_daily
        self.ax2 = self.ax.twinx()
        co2_comparison_graph(self.ax, self.ax2, 'nytimes')
        self.canvas.draw()
    
    def co2_comparison_science_daily(self):
        if not self.graph_drawn:
            self.draw_graph()
        self._clear()
        self.button_switch["text"] = "Switch Graphs"
        self.button_switch["command"] = self.co2_comparison_nytimes
        self.ax2 = self.ax.twinx()
        co2_comparison_graph(self.ax, self.ax2, 'science_daily_small')
        self.canvas.draw()

    def _clear(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
    
    def _quit(self):
        self.Frame2.quit()

create_app()