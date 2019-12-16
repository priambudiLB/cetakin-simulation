from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
import math

def pie(title, datas, labels, row):
    explode = (0,0.3)

    fig, axes = plt.subplots(int(len(datas)/row),row)
    fig.tight_layout()
    for i, ax in enumerate(axes.flatten()):
        if math.floor(i/row) < 2:
            a = datas[i]*100
            ax.pie([100-a,a],
                labels=labels[math.floor(i/3)],
                autopct='%.2f',
                explode=explode)
        ax.set_title(title[i])

    plt.show()

def bar(title, datas, labels, ylabel):
    y_pos = np.arange(len(labels))
    plt.bar(
        y_pos,
        datas,
        )
    plt.xticks(y_pos, labels)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()
