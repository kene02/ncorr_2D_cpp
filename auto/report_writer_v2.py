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
ref_base = 'reference-focus-bw_vs_current-focus-bw_'

# Export plots
export_plots = True

# Directory for output plots
out_dir = './report/dic-plots/'

# Path of output TEX file
tex_path = './report/report.tex'

# Path of output CSV file
csv_path = './report/output.csv'

# Standard ranges
u_range = (0, 0.5)
v_range = (0, 0.1)
exx_range = (-3e-2, 3e-2)
exy_range = (-2e-2, 2e-2)
eyy_range = (-2e-2, 2e-2)

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
\title{DIC Report---Experimental Data}
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

ref = ["Blurred", "Blurred", "Focused"]
cur = ["Blurred", "Focused", "Blurred"]
for j in range(len(df)-1):
    # Target dataset
    base = df.loc[j, 'output_prefix']

    # Progress
    print(f"[{j+1}/{len(df)}] Processing {base[:-1]}")
    
    # Export plots as PNGs
    if export_plots:
        for i in range(5):
            plot_csv(in_dir+base+PARAMS[i]+'.csv', 
                    out_dir+base+PARAMS[i]+'.png', 
                    TITLES[i], 
                    RANGES[i][0], 
                    RANGES[i][1])

    # Write LaTeX code for including plots
    out_str += rf"""\section{{Reference (${ref[j]}) vs Current (${cur[j]})}}
\begin{{minipage}}{{\textwidth}}
"""
    for i in range(5):
        out_str += r"\includegraphics[height=125pt]{"
        out_str += "dic-plots/"+base+PARAMS[i]+".png}\n"

    out_str += r"""
\vspace{12pt}

"""

    ssims = []
    psnrs = []
    for i in range(5):
        # Evaluate SSIM and PSNR
        ssim_val, psnr_val = ssim_psnr(in_dir+ref_base+PARAMS[i]+'.csv', 
                                    in_dir+base+PARAMS[i]+'.csv', 
                                    u_range)
        
        # Put SSIM and PSNR into lists
        ssims.append(ssim_val)
        psnrs.append(psnr_val)
        
    # Add new row to CSV values
    csv_values.append([ref[j], cur[j]]+ssims+psnrs)
        
    # Generate LaTeX table
    out_str += r"""\centering
\begin{tabular}{|l|S[table-format=1.4]|S|}
\hline
\textbf{Plot} & {\textbf{SSIM}} & {\textbf{PSNR} (dB)} \\ \hline
"""
    
    # Put SSIM and PSNR values into the LaTeX table
    for i in range(5):
        out_str += f"{LATEX_TITLES[i]} & {ssims[i]:.4f} & {psnrs[i]:.4f} \\\\"
        if i != 4:
            out_str += "\n"
            
    out_str += r""" \hline
\end{tabular}
\end{minipage}

"""

# End LaTeX document
out_str += r"\end{document}"


# %%
# Write .tex file
with open(tex_path, "w", encoding="utf-8") as file:
    file.write(out_str)

print("Successfully created "+tex_path)

# %%
# Write .csv file
header = ["Reference", "Current",
    "SSIM_u", "SSIM_v", "SSIM_exx", "SSIM_exy", "SSIM_eyy", 
    "PSNR_u", "PSNR_v", "PSNR_exx", "PSNR_exy", "PSNR_eyy"]

with open(csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(header)
    
    # Write multiple data rows at once
    writer.writerows(csv_values)
    
print("Successfully created "+csv_path)

# %%
# Zip report folder
shutil.make_archive("report", "zip", "report/")
print("Successfully created report.zip")

# %%
# Time elapsed
print("--- %s seconds ---" % (time.time() - start_time))