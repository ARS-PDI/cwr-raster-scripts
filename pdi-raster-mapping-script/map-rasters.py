import sys
import arcpy
from os import path

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 map-rasters.py [workspace] [folder with MRF files]')
        exit()

    workspace = sys.argv[1]
    mrf_folder = sys.argv[2]
    test_mosaic = 'test_mosaic'
    fgdb = 'workspace.gdb'

    # Create new file Geodatabase in project
    arcpy.CreateFileGDB_management(workspace, fgdb)

    # Create new mosaic dataset in file Geodatabase
    arcpy.env.workspace = path.join(workspace, fgdb)
    coord_sys = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
    arcpy.CreateMosaicDataset_management(arcpy.env.workspace, test_mosaic, coord_sys, 1)

    # Add raster file to dataset
    dataset_path = path.join(arcpy.env.workspace, test_mosaic)
    input_path = path.join(workspace, mrf_folder)
    arcpy.AddRastersToMosaicDataset_management(dataset_path, 'Raster Dataset', input_path)

    # Raster -> Remap
    input_ranges = []
    for i in range(-4500, 5000, 500):
        input_ranges.append(i)
        input_ranges.append(i + 500)
        
    output_ranges = list(range(1, 20))
    curr_rast = path.join(arcpy.env.workspace, test_mosaic)
    new_rast = arcpy.sa.Remap(curr_rast, input_ranges, output_ranges)
    new_rast.save(path.join(workspace, 'test_mosaic_output'))

    # TODO: Remap -> Attribute table (Page 8)
