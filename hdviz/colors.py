import seaborn as sns
import numpy as np


def keys_to_colors(keys):
    uk = np.unique(keys)
    n_colors = len(uk)
    if n_colors <= 10:
        pal = sns.color_palette("tab10")[0:n_colors]
    elif n_colors <= 20:
        pal = sns.color_palette("tab20")[0:n_colors]
    else:
        raise RuntimeError("not enough colors to plot > 20 categories!")
    color_dict = dict(zip(uk, pal))
    colors = [color_dict[key] for key in keys]
    return colors
