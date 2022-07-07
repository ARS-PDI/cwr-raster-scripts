# Crop Wild Relatives Scripts

## What It Does

There are 4 CWR scripts. The first ([copy_rasters.py](copy_rasters.py)) copies the rasters to a flat directory and renames them to the naming conventions that the CWR web app uses. It also automatically does transformations on some of the images before copying them over. The second ([create_mosaics.py](create_mosaics.py)) creates mosaics using the images that the first script put out. The third ([publish_layers.py](publish_layers.py)) publishes these mosaics to ArcGIS Enterprise as image layers. The fourth script ([run_all.py](run_all.py)) will automatically run these scripts in order as long as the environment has been set up. Instructions for environment setup are below.

## Environment Setup

### Python Runtime

First, you will need to make sure you are using the Python runtime that comes with ArcGIS Pro (The executable can be found at `C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe`).

To be able to publish layers in publish_layers.py or run_all.py, which uses the code in publish_layers, then you either need to set environment variables or replace some lines in the publish_layers.py.

### Update Lines

Towards the bottom of publish_layers.py, there are some lines that say `os.environ.get('AG_USERNM')` and `os.environ.get('AG_PASSWD')`. Replace these lines with an ArcGIS Enterprise username and password credentials in quotations (e.g. `'first.last_USDAARS'`, `'arcgis_password'`).

If you choose to edit these lines, avoid committing and pushing these changes.

### Set Environment Variables

As mentioned before, this is not necessary if you followed the instructions in the previous section. This route is safer if you are just using the script and not changing it.

1. Open Windows Search and type in "environment variables" and press enter.
1. Select "Environment Variables..." in the window that pops up.
1. Under the user variables section at the top, click "New..."
1. Create a variable with the name `'AG_USERNM'` with an ArcGIS Enterprise username.
1. Create another variable with the name `'AG_PASSWD'` with an ArcGIS Enterprise password.

If you’re getting an error when attempting to run the scripts using this method, try closing the Python runtime you’re using and reopening it.

### Populate Directories

Create a directory called `C:\CWR` and then put in a folder named `speciesLevelData` containing the original TIFF images. The original should still be separated into folders and not be stored in a flat directory. The final product should be `C:\CWR\speciesLevelData` which folders named by genera, and each genus folder should contain a set of species. Each species folder should contain several TIFF images for each species.

## Running the Script

After your environment has been set up, then you can run through all the steps with `python3 run_all.py`. To run an individual script, use `python3 [script] <args>`. To figure out the arguments needed for the script, run `python3 [script]` to see a usage message or examine the script’s code.
