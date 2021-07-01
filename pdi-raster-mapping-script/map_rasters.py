import os
import sys
import arcpy

def map_rasters(input_dir, workspace, rast_func, fgdb):
    for file in os.listdir(input_dir):
        if os.path.isdir(os.path.join(input_dir, file)):
            map_rasters(os.path.join(input_dir, file), workspace, rast_func, fgdb)
        elif file.endswith('.mrf'):
            input_rast_path = os.path.join(input_dir, file)
            print('Processing', input_rast_path)

            mosaic = file
            mosaic = mosaic.replace('.mrf', '')
            mosaic = mosaic.replace(' ', '_')
            mosaic = mosaic.replace('-', '_')
            mosaic = mosaic.replace('.', '')

            # Create new mosaic dataset in file Geodatabase
            arcpy.CreateMosaicDataset_management(
                os.path.join(arcpy.env.workspace, fgdb),          # Path to new mosaic
                mosaic,                                           # Mosaic name
                arcpy.SpatialReference('WGS 1984 UTM Zone 14N')   # Coordinate system
            )

            mosaic_path = os.path.join(arcpy.env.workspace, fgdb, mosaic)
            arcpy.AddRastersToMosaicDataset_management(
                mosaic_path,                                      # Target mosaic dataset
                'Raster Dataset',                                 # Raster type
                input_rast_path                                   # Path to input raster
            )

            rast_func_path = os.path.join(workspace, rast_func)
            arcpy.SetMosaicDatasetProperties_management(
                mosaic_path,                                      # Target mosaic dataset
                processing_templates=rast_func_path,              # Processing templates
                default_processing_template=rast_func_path        # Default template
            )

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 map_rasters.py [root folder] [raster function file]')
        exit()

    root_dir = sys.argv[1]
    rast_func = sys.argv[2]
    fgdb = 'mosaics.gdb'

    # Set environment variables
    arcpy.env.workspace = os.getcwd()
    arcpy.env.overwriteOutput = False

    # Create new file Geodatabase in current directory and set environment variables
    try:
        arcpy.CreateFileGDB_management(os.getcwd(), fgdb)
    except:
        pass

    # Map rasters using custom raster function file and put them into file geodatabase
    map_rasters(root_dir, arcpy.env.workspace, rast_func, fgdb)
