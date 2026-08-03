# %%
"""
File name       : report_writer.py
Author(s)       : Ken Ely
Institution     : Monash University
Last modified   : 27 July 2026
Licence         : All rights reserved

Description:
Converts 2D displacement and strain field data (formatted as CSV files) into a 
LaTeX report.

"""

# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from pathlib import Path
import csv
import shutil
import time

# %%
# For timing run time
start_time = time.time()

# %%
print(os.getcwd())

# %%
def plot_csv(csv_path, save_path, title, vmin=None, vmax=None):
    """
    Loads a 2D numeric grid from a CSV file and saves it as a colormap image.
 
    Parameters:
    ----------
    csv_path : str
        The file path to the input CSV file containing numeric data.
    save_path : str
        The file path where the generated plot image will be saved.
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
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Print
    print(save_path+" successfully exported.")

# %%
def norm(data, data_range):
    """Normalizes a data point to a 0-1 scale based on a specified range.

    Args:
        data (float or int): The data point to normalize.
        data_range (tuple or list): A sequence containing the (min, max) values
            of the range.

    Returns:
        float: The normalized value.

    Raises:
        ValueError: If the min and max values in data_range are equal.
    """
    min = data_range[0]
    max = data_range[1]
    
    if max == min:
        raise ValueError(
            f"Invalid range: [{min}, {max}]. Min and max values cannot be equal."
        )
    
    norm_data = (data - min) / (max - min)
    return norm_data

# %%
def ssim_psnr(ref_path, test_path, range):
    """
    Compute SSIM and PSNR between two datasets loaded from CSV files.

    This function reads two numeric datasets, normalizes them to a target range, 
    cleans missing values, and evaluates their Structural Similarity Index (SSIM) 
    and Peak Signal-to-Noise Ratio (PSNR).

    Parameters
    ----------
    ref_path : str
        File path to the ground truth reference CSV data.
    test_path : str
        File path to the degraded or processed test CSV data.
    range : tuple or numeric
        The data range configuration used by the normalization helper.

    Returns
    -------
    ssim_value : float
        The Structural Similarity Index, typically ranging from -1 to 1.
    psnr_value : float
        The Peak Signal-to-Noise Ratio value in decibels (dB).
    """
    # Load numeric data directly
    ref_data = np.genfromtxt(ref_path, delimiter=',', dtype=None, encoding='utf-8')
    test_data = np.genfromtxt(test_path, delimiter=',', dtype=None, encoding='utf-8')

    # Normalise arrays and replace nans with zeroes
    new_ref_data = np.nan_to_num(norm(ref_data, range))
    new_test_data = np.nan_to_num(norm(test_data, range))

    # Evaluate SSIM
    ssim_value = ssim(new_ref_data, new_test_data, data_range=1.0)
    
    # Evaluate PSNR
    psnr_value = psnr(new_ref_data, new_test_data, data_range=1.0)

    return ssim_value, psnr_value

# %%
## INPUT PARAMETERS
# Directory containing CSV files
in_dir = './bin/outputs/'

# Reference dataset
ref_base = 'ohtcfrp_00_vs_ohtcfrp_11_'

# Export plots
export_plots = False

# Directory for output plots
out_dir = './report/dic-plots/'

# Path of output TEX file
tex_path = './report/report.tex'

# Path of output CSV file
csv_path = './report/output.csv'

# Standard ranges
u_range = (-0.25, 0)
v_range = (-2, -1)
exx_range = (-2e-3, 0)
exy_range = (-2e-3, 2e-3)
eyy_range = (5e-3, 10e-3)

PARAMS = ('u', 'v', 'exx', 'exy', 'eyy')
TITLES = ('u displacement', 'v displacement', 'exx strain', 'exy strain', 'eyy strain')
LATEX_TITLES = ('$u$ displacement', '$v$ displacement', '$e_{xx}$ strain', '$e_{xy}$ strain', '$e_{yy}$ strain')
RANGES = (u_range, v_range, exx_range, exy_range, eyy_range)

# %%
# Create output folders if they don't already exist
Path("report").mkdir(parents=True, exist_ok=True)
Path("report/dic-plots").mkdir(parents=True, exist_ok=True)

# %%
# LaTeX output string
out_str = r"""\documentclass[a4paper, 8pt, twoside]{article}
\usepackage[left=1in, top=1in, bottom=1in, right=1in]{geometry}
\usepackage{graphicx}
\usepackage{siunitx}
\usepackage{subcaption}
\title{DIC Report---Blurry Reference vs Blurry Current, 90 Degrees}
\author{Ken Ely}
\date{27 July 2026}

\begin{document}

\maketitle

\tableofcontents
\newpage

"""

# %%
# Include true plots
# Export plots as PNGs
if export_plots:
    for i in range(5):
        plot_csv(in_dir+ref_base+PARAMS[i]+'.csv', 
                out_dir+ref_base+PARAMS[i]+'.png', 
                TITLES[i], 
                RANGES[i][0], 
                RANGES[i][1])

# Write LaTeX code for including plots
out_str += r"""\section{Unblurred Reference vs Unblurred Current (True Plots)}
\begin{minipage}{\textwidth}
"""
for i in range(5):
    out_str += r"\includegraphics[height=125pt]{"
    out_str += "dic-plots/"+ref_base+PARAMS[i]+".png}\n"

out_str += r"""\end{minipage}

"""


# %%
"""ref_m = np.arange(5, 105, 5)
ref_t = np.full(20, 90)
cur_m = np.arange(5, 105, 5)
cur_t = np.full(20, 90)"""

# Load the entire CSV file
df = pd.read_csv('image_paths.csv', usecols=['output_prefix'])

# CSV file values
csv_values = []

for j in range(len(df)):
    # Target dataset
    base = df.loc[j, 'output_prefix']

    # Progress
    print(f"[{j+1}/{len(df)}] Processing {base[:-1]}")
    