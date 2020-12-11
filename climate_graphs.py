import csv
import tkinter as tk
from matplotlib.axes import Axes
from matplotlib import pyplot as plt


def convert_to_plot_data(filename: str) -> tuple:
    """Returns list of tuples consisting of 3 elements.
    
    For each tuple called tup,
    tup[0] is the year
    tup[1] is number of articles that tested climate-change positive, on that year
    tup[2] is the Climate Awareness Index (CAI) on that year
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        yrs, num_articles, cai   = [], [], []
        for row in reader:
            yrs.append(int(row[0]))
            num_articles.append(int(row[1]))
            cai.append(float(row[2]))
    return yrs, num_articles, cai


def show_line_graph(ax: Axes, dataset_name: str, show_cai: bool = True):
    """Plots a line graph, with years on the x-axis and either the CAI or the
    number of articles that tested climate-change positive.
    """
    yrs, nums, cai = convert_to_plot_data(f'climate_data/{dataset_name}_climate_change_data.txt')
    if show_cai:
        ax.plot(yrs, cai, marker = 'o')
        ax.set(title = f'{dataset_name.upper()}', xlim = (yrs[0], yrs[-1]))
        # ax.set_xlim(xmin=yrs[0], xmax=yrs[-1])
    else:
        ax.plot(yrs, nums, marker = 'o')
        ax.set_xlim(xmin=yrs[0], xmax=yrs[-1])


# def embed_line_graph(dataset_name: str, window: tk.Tk, placement: tuple):  # show_cai: bool = True):
#     """Creates a graph to be embed in tkinter application.
    
#     Instance Attributes:
#         - dataset_name: the name of the dataset
#         - window: an instance of tk.Tk class
#         - placement: a tuple representing the placement of the graph
    
#     placement[0] is passed to the x parameter of widget.place in Tkinter
#     placement[1] is passed to the y parameter of widget.place in Tkinter
#     placement[2] is passed to the height parameter of widget.place in Tkinter
#     placement[3] is passed to the width parameter of widget.place in Tkinter
#     """
#     # This figure will contain the plot
#     fig = Figure(figsize = (5, 5), dpi = 100)
#     yrs, nums, cai = convert_to_plot_data(f'climate_data/{dataset_name}_climate_change_data.txt')
#     plot1 = fig.add_subplot(1, 1, 1)
#     plot1.plot(yrs, nums)

#     canvas = FigureCanvasTkAgg(fig, master = window)
#     canvas.draw()
#     canvas.get_tk_widget().pack()
#     # canvas.get_tk_widget().place(
#     #     x = placement[0], y = placement[1], height = placement[2], width = placement[3]
#     # )
    
#     toolbar = NavigationToolbar2Tk(canvas, window)
#     toolbar.update()
#     canvas.get_tk_widget().pack()
#     # canvas.get_tk_widget().place(
#     #     x = placement[0], y = placement[1] + placement[2], height = placement[2] // 4,
#     #     width = placement[3]
#     # )


if __name__ == "__main__":
    # show_line_graph('nytimes')
    # rng = np.arange(50)
    # rnd = np.random.randint(0, 10, size=(3, rng.size))
    # yrs = 1950 + rng
    # print(rng, rnd, yrs, sep='\n')

    # fig, ax = plt.subplots(figsize=(5, 3))
    # ax.stackplot(yrs, rng + rnd, labels=['Eastasia', 'Eurasia', 'Oceania'])
    # ax.set_title('Combined debt growth over time')
    # ax.legend(loc='upper left')
    # ax.set_ylabel('Total debt')
    # ax.set_xlim(xmin=yrs[0], xmax=yrs[-1])
    # fig.tight_layout()
    # plt.show()
    pass