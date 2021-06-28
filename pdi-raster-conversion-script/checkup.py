# Double checks that for every TIF there is a corresponding MRF in all the root
# directory's (folder of folders of folders) subdirectories

import os
import sys

def checkup(input_dir, output_dir, no_match):
    for file in os.listdir(input_dir):
        if file.endswith('.tif'):
            if file.replace('.tif', '.mrf.aux.xml') not in os.listdir(output_dir):
                no_match.append(f'{input_dir}/{file}')
        elif os.path.isdir(f'{input_dir}/{file}'):
            checkup(f'{input_dir}/{file}', f'{output_dir}/{file}', no_match)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_dir  = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        print('Usage: python3 checkup.py [input folder] [output_folder]')
        exit(1)

    no_match = []
    checkup(input_dir, output_dir, no_match)

    if no_match:
        print('The following rasters do not have no match:')
        for raster in no_match:
            print(raster)
    else:
        print('All TIFs have a matching MRF')
