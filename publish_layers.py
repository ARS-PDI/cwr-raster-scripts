import arcpy
import os
import sys
from time import gmtime, strftime

img_types = ['ersEx', 'ersIn', 'ga50', 'grsEx', 'grsIn', 'thrsld']

def _get_img_type(mos):
    for img_type in img_types:
        if img_type in mos:
            return img_type

    raise ValueError('Unknown image type')

def create_name(mos):
    img_type = _get_img_type(mos)
    datetime = strftime('%m%d%y%H%M', gmtime())

    return f'{img_type}_{datetime}'

def create_tags(mos):
    return f'CWR,Imagery,{_get_img_type(mos)},ARS,PDI'

def publish_layers(workspace):
    """
    workspace: Folder containg GDB(s)
    """
    for gdb in os.listdir(workspace):
        arcpy.env.workspace = gdb_path = os.path.join(workspace, gdb)
        arcpy.env.overwriteOutput = False

        max_tries = 3
        mos_datasets = arcpy.ListDatasets(feature_type='Mosaic')
        mos_datasets_len = 0

        try:
            mos_datasets_len = len(mos_datasets)
        except:
            continue

        for i in range(mos_datasets_len):
            mos = mos_datasets[i]
            sd_draft = os.path.join(workspace, mos + '.sddraft')
            sd = os.path.join(workspace, mos + '.sd')

            for curr_try in range(max_tries):
                try:
                    arcpy.CreateImageSDDraft(
                        os.path.join(gdb_path, mos),
                        sd_draft,
                        create_name(mos),
                        'ARCGIS_SERVER',
                        copy_data_to_server=True,
                        folder_name='CWR',
                        summary=mos,
                        tags=create_tags(mos)
                    )

                    break
                except:
                    pass

            for curr_try in range(max_tries):
                try:
                    arcpy.StageService_server(sd_draft, sd)

                    break
                except:
                    pass

            success = False

            for curr_try in range(max_tries):
                try:
                    print(f'[{curr_try + 1}] Uploading the service definition for', mos)

                    arcpy.UploadServiceDefinition_server(
                        sd,
                        'https://pdiimagery.azurecloudgov.us/arcgis',
                        in_my_contents=True,
                        in_public=True,
                        in_organization='SHARE_ORGANIZATION'
                    )

                    print(f'{mos} successfully published')
                    success = True
                    
                    break
                except:
                    pass

            if not success:
                with open('publish_log.txt', 'a') as f:
                    f.write(f'{mos}\n')

            try:
                os.remove(os.path.join(workspace, f'{mos}.sddraft'))
                os.remove(os.path.join(workspace, f'{mos}.sd'))
    
                print('Cleaned', mos, 'service definitions')
            except FileNotFoundError:
                pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: python3 publish_layers.py [GDBs folder]')

    arcpy.SignInToPortal(
        'https://pdienterprise.azurecloudgov.us/portal',
        os.environ.get('AG_USERNM'),
        os.environ.get('AG_PASSWD')
    )

    workspace = sys.argv[1]

    publish_layers(workspace)
