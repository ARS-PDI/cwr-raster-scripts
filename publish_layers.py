import os
import sys

import arcpy


def publish_layers():
    mosaics = arcpy.ListDatasets(feature_type='Mosaic')

    for mosaic in mosaics:
        sd_draft = f'{mosaic}.sddraft'
        sd = f'{mosaic}.sd'

        arcpy.CreateImageSDDraft(mosaic,
                                 sd_draft,
                                 f'cwr_{mosaic}',
                                 'ARCGIS_SERVER',
                                 copy_data_to_server=True,
                                 folder_name='CWR',
                                 summary=mosaic,
                                 tags=f'CWR,{mosaic},ARS,PDI')

        arcpy.StageService_server(sd_draft, sd)

        arcpy.UploadServiceDefinition_server(sd,
                                             'https://pdiimagery.azurecloudgov.us/arcgis',
                                             in_my_contents=True,
                                             in_public=True,
                                             in_organization='SHARE_ORGANIZATION')

        os.remove(os.path.join(os.getcwd(), sd_draft))
        os.remove(os.path.join(os.getcwd(), sd))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: python3 publish_layers.py [GDBs folder]')

    arcpy.SignInToPortal('https://pdienterprise.azurecloudgov.us/portal',
                         os.environ.get('AG_USERNM'),
                         os.environ.get('AG_PASSWD'))
    arcpy.env.workspace = sys.argv[1]

    publish_layers()
