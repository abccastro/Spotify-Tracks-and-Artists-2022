from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.pyplot as plt


def showBarGraph(x_val, y_val, x_label=None, y_label=None, title=None, add_val=None):

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

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_val, y_val)
    ax.set_xticks(x_val)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
