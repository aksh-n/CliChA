"""Climate Change Awareness (CliChA), Climate Change Awareness Graphs

This module provides graphing functions, to be used in the GUI of main.py.
They are not meant for standalone purposes.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
import csv
from collections import defaultdict
from matplotlib.axes import Axes
# from matplotlib import pyplot as plt
# from main_backend import run_demo_nytimes, demo_processing_cai


def convert_to_plot_data(filename: str) -> tuple:
    """Converts the files generated by find_climate_articles.py to plottable data.
    Returns three lists.

    The first list consists of the years
    The second list consists of number of articles that tested climate-change positive, per year
    The third list consists of the Climate Awareness Index (CAI), per year

    Instance Attributes:
        - filename: the name of the file
    """
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        yrs, num_articles, cai = [], [], []
        for row in reader:
            yrs.append(int(row[0]))
            num_articles.append(int(row[1]))
            cai.append(float(row[2]))
    return yrs, num_articles, cai


def convert_keeling_data() -> tuple:
    """Converts the Keeling data in monthly_in_situ_co2_mlo.csv to plottable data.
    Returns two lists.

    The first list consists of the years
    The second list consists of CO2 concentrations in micro-mol CO2 per mole (ppm)
    """
    keeling_file = 'climate_data/monthly_in_situ_co2_mlo.csv'
    with open(keeling_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for _ in range(57):
            next(reader)
        co2_dict = defaultdict(lambda: [0, 0])
        for row in reader:
            yr, _, _, _, _, _, co2_ppm, *_ = row
            yr, co2_ppm = int(yr), float(co2_ppm)
            if co2_ppm != -99.99:
                co2_dict[yr] = co2_dict[yr][0] + 1, co2_dict[yr][1] + co2_ppm

        yrs = list(range(1958, 2021))
        co2_ppm = [co2_dict[y][1] / co2_dict[y][0] for y in yrs]
        return yrs, co2_ppm


def show_line_graph(ax: Axes, dataset_name: str, show_cai: bool = True) -> None:
    """Plots a line graph, with years on the x-axis and either the CAI or the
    number of articles that tested climate-change positive.

    Instance Attributes:
    - ax: an instance of Axes
    - dataset_name: the name of the dataset
    - show_cai: a bool representing whether to show CAI graph or number of articles graph
    """
    yrs, nums, cai = convert_to_plot_data(f'climate_data/{dataset_name}_climate_change_data.txt')
    if show_cai:
        ax.plot(yrs, cai, marker='o', color='crimson')
        ax.set(
            title=f'{dataset_name.upper()} Climate Awareness Index Graph',
            xlabel='Years', ylabel='Climate Awareness Index (CAI)',
            ylim=(0, max(cai) + 1)
        )
    else:
        ax.plot(yrs, nums, marker='o', color='forestgreen')
        ax.set(
            title=f'{dataset_name.upper()} Climate Change Aware Articles Graph',
            xlabel='Years', ylabel='Number of Climate Change Aware Articles',
            ylim=(0, max(nums) + 1)
        )


def show_bar_graph(ax: Axes, dataset_1: str, dataset_2: str, show_cai: bool = True) -> None:
    """Plots a bar graph, with years on the x-axis and either the ratio of CAI or the
    number of articles that tested climate-change positive between the two datasets.

    Instance Attributes:
        - ax: an instance of Axes
        - dataset_1: the name of the first dataset
        - dataset_2: the name of the second dataset
        - show_cai: a bool representing whether to show CAI graph or number of articles graph
    """
    yrs_1, nums_1, cai_1 = convert_to_plot_data(f'climate_data/{dataset_1}_climate_change_data.txt')
    yrs_2, nums_2, cai_2 = convert_to_plot_data(f'climate_data/{dataset_2}_climate_change_data.txt')

    if len(yrs_2) < len(yrs_1):
        yrs, yrs_diff = yrs_2, len(yrs_1) - len(yrs_2)
        nums_1, cai_1 = nums_1[yrs_diff:], cai_1[yrs_diff:]
    else:
        yrs, yrs_diff = yrs_1, len(yrs_2) - len(yrs_1)
        nums_2, cai_2 = nums_2[yrs_diff:], cai_2[yrs_diff:]

    nums = [nums_1[i] / nums_2[i] for i in range(len(nums_1))]
    cai = [cai_1[i] / cai_2[i] for i in range(len(cai_1))]
    if show_cai:
        ax.bar(yrs, cai, color='dodgerblue')
        ax.set(
            title=f'{dataset_1.upper()} vs {dataset_2.upper()} Climate Awareness Index Graph',
            xlabel='Years', ylabel='Ratio of Climate Awareness Index (CAI)',
            ylim=(0, max(cai) + 1))
    else:
        ax.bar(yrs, nums, color='darkviolet')
        ax.set(
            title=f'{dataset_1.upper()} vs {dataset_2.upper()} Climate Change Aware Articles Graph',
            xlabel='Years', ylabel='Ratio of Number of Climate Change Aware Articles',
            ylim=(0, max(nums) + 1))


def demo_graph(ax: Axes, list_cai: list) -> None:
    """Plots a bar graph showing the Climate Awareness Index (CAI) of each article
    scraped in the demo.

    Instance Attributes:
        - ax: an instance of Axes
        - list_cai: a list of CAI values
    """
    ax.bar(range(len(list_cai)), list_cai, color='gold')
    ax.set(
        title='Demo Climate Awareness Index Graph',
        xlabel='Articles Index', ylabel='Climate Awareness Index (CAI)'
    )


def co2_comparison_graph(ax: Axes, ax2: Axes, dataset_name: str) -> None:
    """Plots a dual line graph showing the comparision between CO2 emissions and the
    Climate Awareness Index (CAI) of either of the datasets.

    Instance Attribute:
        - ax: and instance of Axes
        - ax2: an instance of Axes, shares the same x-axis as ax
        - dataset_name: the name of the dataset
    """
    yrs_1, co2_ppm = convert_keeling_data()
    yrs_2, _, cai = convert_to_plot_data(f'climate_data/{dataset_name}_climate_change_data.txt')
    if len(yrs_1) > len(yrs_2):
        yrs, yrs_diff = yrs_2, len(yrs_1) - len(yrs_2)
        co2_ppm = co2_ppm[yrs_diff:]
    else:
        yrs, yrs_diff = yrs_1, len(yrs_2) - len(yrs_1)
        cai = cai[yrs_diff:]

    ax.plot(yrs, cai, color='navy')
    name = f'Comparison of Climate Awareness Index of {dataset_name.upper()} and CO2 concentration'
    ax.set(title=name, xlabel='Years')
    ax.set_ylabel("Climate Awareness Index (CAI)", color='navy')
    ax2.plot(yrs, co2_ppm, color='darkgoldenrod')
    ax2.set_ylabel('CO2 concentrations in micro-mol CO2 per mole (ppm)', color='darkgoldenrod')


if __name__ == "__main__":
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # demo_graph(ax, demo_processing_cai())
    # plt.show()
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': [
            'collections',
            'csv',
            'matplotlib',
            'matplotlib.axes',
            'main_backend',
            'python-ta.contracts'
        ],
        'allowed-io': ['convert_to_plot_data', 'convert_keeling_data'],
        'max-line-length': 100,
        'max-locals': 25,
        'disable': ['R1705', 'C0200']
    })

    # there seems to be a bug that is not allowing this to be executed properly
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
