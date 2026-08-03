import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def show_csv(csv_path, title, vmin=None, vmax=None):
    """
    Loads a 2D numeric grid from a CSV file and plots it as a colormap image.
 
    Parameters:
    ----------
    csv_path : str
        The file path to the input CSV file containing numeric data.
    title : str
        The title displayed at the top of the plot.
    vmin : float, optional
        The minimum data value that maps to the bottom of the color scale.
        Defaults to None (scaled to data minimum).
    vmax : float, optional
        The maximum data value that maps to the top of the color scale.
        Defaults to None (scaled to data maximum).
    """
    # Load numeric data directly
    data = np.genfromtxt(csv_path, delimiter=',', dtype=None, encoding='utf-8')
    
    # Plot the 2D grid directly with a colormap
    plt.figure()
    plt.imshow(data, cmap='viridis', aspect='equal', vmin=vmin, vmax=vmax)
    plt.title(title)
    plt.colorbar()

base = "./bin/outputs/reference-focus-bw_vs_current-focus-bw_"

PARAMS = ('u', 'v', 'exx', 'exy', 'eyy')
TITLES = ('u displacement', 'v displacement', 'exx strain', 'exy strain', 'eyy strain')

for i in range(5):
    show_csv(base+PARAMS[i]+'.csv', TITLES[i])
    
plt.show()