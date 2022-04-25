from copy_rasters import main as cr_main
from create_mosaics import main as cm_main
from publish_layers import main as pl_main


def main():
    cr_input_dir = r'C:\CWR\srcSpeciesLevelData'
    cr_output_dir = r'C:\CWR\stagingSpeciesLevelData'
    cr_main(cr_input_dir, cr_output_dir)

    cm_input_dir = r'C:\CWR\stagingSpeciesLevelData'
    cm_main(cm_input_dir)

    cl_workspace = r'C:\CWR\CWR.gdb'
    pl_main(cl_workspace)


if __name__ == '__main__':
    main()
