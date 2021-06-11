# Double checks that for every TIF there is a corresponding MRF in all the root
# directory's (folder of folders of folders) subdirectories

import os
import sys

if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_folder  = sys.argv[1]
        output_folder = sys.argv[2]
    else:
        print('Usage: python3 doublecheck.py "C:/Users/.../Input Folder" "C:/Users/.../Output Folder"')
        exit(1)

    no_match = []

    for folder in os.listdir(input_folder):
        for subfolder in os.listdir(f'{input_folder}/{folder}'):
            for file in os.listdir(f'{input_folder}/{folder}/{subfolder}'):
                if file.endswith('.tif'):
                    if file.replace('.tif', '.mrf.aux.xml') not in os.listdir(f'{output_folder}/{folder}/{subfolder}'):
                        no_match.append(f'{folder}/{subfolder}/{file}')

    if no_match:
        print('The following rasters do not have no match:')
        for raster in no_match:
            print(raster)
    else:
        print('All TIFs have a matching MRF')
