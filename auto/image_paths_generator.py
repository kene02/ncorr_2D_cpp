"""
File name       : image_paths_generator.py
Author(s)       : Ken Ely
Institution     : Monash University
Last modified   : 28 July 2026
Licence         : All rights reserved

Description:
Generates image_paths.csv (file that specifies which images auto ncorr_test 
should perform digital image correlation between).

"""
import csv

# Inputs
ref_images = ["reference-blurred-bw", "reference-focus-bw"]
cur_images = ["current-blurred-bw", "current-focus-bw"]
roi = "current-focus-roi"
in_path = "./images/"
out_path = "./outputs/"
ext = ".jpg"

# Generate table
csv_values = []
for ref_image in ref_images:
    for cur_image in cur_images:
        output_prefix = f"{ref_image}_vs_{cur_image}_"
        csv_values.append([in_path+ref_image+ext, 
                           in_path+cur_image+ext, 
                           in_path+roi+ext, 
                           out_path+output_prefix])

# Save to CSV file
CSV_PATH = "image_paths.csv"
HEADER = ["ref_image", "cur_image", "roi_path", "output_prefix"]
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as file:
    # Force Unix line endings (\n) so C++ parses it cleanly
    writer = csv.writer(file, lineterminator='\n')
    
    # Write the header row
    writer.writerow(HEADER)
    
    # Write multiple data rows at once
    writer.writerows(csv_values)
print("Successfully created "+CSV_PATH)