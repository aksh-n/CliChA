import csv
import tkinter as tk
import numpy as np
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
        ax.plot(yrs, cai, marker = 'o', color = 'crimson')
        ax.set(
            title = f'{dataset_name.upper()} Climate Awareness Index Graph',
            xlabel = 'Years', ylabel = 'Climate Awareness Index (CAI)',
            ylim = (0, max(cai) + 1))
    else:
        ax.plot(yrs, nums, marker = 'o', color = 'forestgreen')
        ax.set(
            title = f'{dataset_name.upper()} Climate Change Aware Articles Graph',
            xlabel = 'Years', ylabel = 'Number of Climate Change Aware Articles',
            ylim = (0, max(nums) + 1))


def show_bar_graph(ax: Axes, dataset_1: str, dataset_2: str, show_cai: bool = True):
    """Plots a bar graph, with years on the x-axis and either the absolute difference of CAI or the
    number of articles that tested climate-change positive between the two datasets.
    """
    yrs_1, nums_1, cai_1 = convert_to_plot_data(f'climate_data/{dataset_1}_climate_change_data.txt')
    yrs_2, nums_2, cai_2 = convert_to_plot_data(f'climate_data/{dataset_2}_climate_change_data.txt')
    
    if len(yrs_2) < len(yrs_1):
        yrs, yrs_diff = yrs_2, len(yrs_1) - len(yrs_2)
        nums_1, cai_1 = nums_1[yrs_diff:], cai_1[yrs_diff:]
    else:
        yrs, yrs_diff = yrs_1, len(yrs_2) - len(yrs_1)
        nums_2, cai_2 = nums_2[yrs_diff:], cai_2[yrs_diff:]
    
    nums = [abs(nums_1[i] - nums_2[i]) for i in range(len(nums_1))]
    cai = [abs(cai_1[i] - cai_2[i]) for i in range(len(cai_1))]
    if show_cai:
        ax.bar(yrs, cai, color = 'dodgerblue')
        ax.set(
            title = f'{dataset_1.upper()} vs {dataset_2.upper()} Climate Awareness Index Graph',
            xlabel = 'Years', ylabel = 'Climate Awareness Index (CAI)',
            ylim = (0, max(cai) + 1))
    else:
        ax.bar(yrs, nums, color = 'darkviolet')
        ax.set(
            title = f'{dataset_1.upper()} vs {dataset_2.upper()} Climate Change Aware Articles Graph',
            xlabel = 'Years', ylabel = 'Number of Climate Change Aware Articles',
            ylim = (0, max(nums) + 1))

if __name__ == "__main__":
    pass