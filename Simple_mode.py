import logging
import cimpy
from pathlib import Path

logging.basicConfig(filename='importCIGREMV.log',
                    level=logging.INFO, filemode='w')


def import_cim(input_path, output_path, sincal2pf, profile_list):
    example = Path(input_path).resolve()
    xml_files = []
    for file in example.glob('*.xml'):
        xml_files.append(str(file.absolute()))
    import_result = cimpy.cim_import(xml_files, "cgmes_v2_4_15")
    activeProfileList = map(lambda x: x.upper(), profile_list)
    if sincal2pf:
        cimpy.sincal_Pf(import_result)
    cimpy.cim_export(import_result, output_path,
                     "cgmes_v2_4_15", activeProfileList)
