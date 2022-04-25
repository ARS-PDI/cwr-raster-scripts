import os
import sys
import xml.dom.minidom as dom

import arcpy


def update_xml_kv(sd_draft, tag_name, tag_data, value):
    doc = dom.parse(sd_draft)
    keys = doc.getElementsByTagName(tag_name)

    for key in keys:
        if key.firstChild.data == tag_data:
            # This assumes that the Value node is the second child of the PropertySetProperty node.
            key.parentNode.childNodes[1].firstChild.data = value

    with open(sd_draft, 'w') as xml:
        doc.writexml(xml)


def set_resampling_method(sd_draft):
    # Sets the default resampling method to Nearest Neighbor (option 0)
    update_xml_kv(sd_draft, 'Key', 'DefaultResamplingMethod', '0')


def set_override(sd_draft):
    with open(sd_draft, 'r') as file:
        file_data = file.read()

    file_data = file_data.replace(
        'esriServiceDefinitionType_New', 'esriServiceDefinitionType_Replacement')

    with open(sd_draft, 'w') as file:
        file.write(file_data)


def set_public(sd_draft):
    update_xml_kv(sd_draft, 'Key', 'PackageIsPublic', 'true')


def set_properties(sd_draft):
    set_resampling_method(sd_draft)
    set_override(sd_draft)
    set_public(sd_draft)


def publish_layers():
    mosaics = arcpy.ListDatasets(feature_type='Mosaic')

    for mosaic in mosaics:
        print('Publishing', mosaic)

        sd_draft = f'{mosaic}.sddraft'
        sd = f'{mosaic}.sd'

        try:
            arcpy.CreateImageSDDraft(mosaic,
                                     sd_draft,
                                     f'test_{mosaic}',
                                     'ARCGIS_SERVER',
                                     copy_data_to_server=True,
                                     folder_name='CWR',
                                     summary=mosaic,
                                     tags=f'CWR,{mosaic},ARS,PDI')
            set_properties(sd_draft)
            arcpy.StageService_server(sd_draft, os.path.join(os.getcwd(), sd))
            arcpy.UploadServiceDefinition_server(sd,
                                                 'https://pdiimagery.azurecloudgov.us/arcgis')
        except arcpy.ExecuteError as e:
            raise e
        finally:
            os.remove(os.path.join(os.getcwd(), sd_draft))
            os.remove(os.path.join(os.getcwd(), sd))


def main(workspace):
    arcpy.SignInToPortal('https://pdienterprise.azurecloudgov.us/portal',
                         os.environ.get('AG_USERNM'),
                         os.environ.get('AG_PASSWD'))
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    publish_layers()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: python3 publish_layers.py [GDBs folder]')

    main(sys.argv[1])
