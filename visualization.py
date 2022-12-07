"""
Project Fall 2022 (BDM-11123)
Submitted by:
- Auradee Castro
- Olivia Deguit
"""
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.pyplot as plt


def showBarGraph(x_val, y_val, x_label=None, y_label=None, title=None, add_val=None):
    """
    The function that displays the bar graph
    :param list x_val: List of elements for x-axis
    :param list y_val: List of elements for y-axis
    :param str x_label: Text label on x-axis
    :param str y_label: Text label on y-axis
    :param str title: Title of the graph
    :param bool add_val: True to show category value. Default value is None.
    """

    y_pos = np.arange(len(y_val))
    plt.figure(figsize=(10, 6))
    plt.barh(y_pos, x_val, align='center', alpha=0.5)

    if add_val:
        for i, v in enumerate(x_val):
            plt.text(v + .5, i - .25, str(v), color='grey')

    plt.yticks(y_pos, y_val)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def showLineGraph(x_val, y_val, x_label=None, y_label=None, title=None):
    """
    The function that displays the line graph
    :param list x_val: List of elements for x-axis
    :param list y_val: List of elements for y-axis
    :param str x_label: Text label on x-axis
    :param str y_label: Text label on y-axis
    :param str title: Title of the graph
    """

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_val, y_val)
    ax.set_xticks(x_val)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
