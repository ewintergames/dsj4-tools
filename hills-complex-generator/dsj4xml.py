import xml.etree.ElementTree as ET
from dsj4hill import append_converted_nodes, get_shifters


def parse_dsj4_xml(main_hill_path, *hills):
    mh_tree = ET.parse(main_hill_path)
    mh_root = mh_tree.getroot()

    for hill_id, (second_hill_path, x, y, z) in enumerate(hills):
        sh_tree = ET.parse(second_hill_path)
        sh_root = sh_tree.getroot()
        append_converted_nodes(mh_root, sh_root, hill_id, x, y, z)

    return mh_tree


if __name__ == '__main__':
    # tree = parse_dsj4_xml('Harrachov-HS142-CZE-92-v1.xml',
    #                       'Harrachov-HS250-CZE-15-v1.xml', 0, 0, 40)
    # tree.write('Harrachov-HS142-CZE-j1.xml')
        # 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Harrachov-HS142-CZE-j1.xml')
    
    # pleso = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Strbske_Pleso-HS125-SVK-v0.xml'
    # pleso_target = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Strbske_Pleso-HS125-SVK-j0.xml'
    # tree = parse_dsj4_xml(pleso, pleso, 0, 0, 5)
    # tree.write(pleso_target)

    mat22 = 'C:/Users/jonat/Documents/dsj4-hill-generator/Matysówka-K22-POL-8-v2.xml'
    mat43 = 'C:/Users/jonat/Documents/dsj4-hill-generator/Matysówka-K43-POL-9-v2.xml'
    mat77 = 'C:/Users/jonat/Documents/dsj4-hill-generator/Matysówka-HS77-POL-10-v3.xml'
    mat104 = 'C:/Users/jonat/Documents/dsj4-hill-generator/Matysówka-HS104-POL-11-v2.xml'
    mat150 = 'C:/Users/jonat/Documents/dsj4-hill-generator/Matysówka-HS150-POL-12-v2.xml'
    mat250 = 'C:/Users/jonat/Documents/dsj4-hill-generator/Matysówka-HS250-POL-13-v2.xml'
    mat375 = 'C:/Users/jonat/Documents/dsj4-hill-generator/Matysówka-HS375-POL-14-v2.xml'

    mat22_target = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Matysówka-K22-POL-8-v2-complex.xml'
    mat43_target = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Matysówka-K43-POL-9-v2-complex.xml'
    mat77_target = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Matysówka-HS77-POL-10-v3-complex.xml'


    # wh_l = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Whistler-HS142-CAN.xml'
    # wh_n = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Whistler-HS104-CAN.xml'
    # wh_l_target = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Whistler-HS142-CAN-complex.xml'
    # wh_n_target = 'C:/Users/jonat/Documents/Deluxe Ski Jump 4/Custom Hills/Whistler-HS104-CAN-complex.xml'

    tree = parse_dsj4_xml(mat22, (mat43, 0, 0, -14.5), (mat77, 0, 0, 40), (mat104, 0, 0, 60), (mat150, 0, 0, 87), (mat250, 0, 0, -90), (mat375, 0, 0, -150))
    tree.write(mat22_target)

    # tree = parse_dsj4_xml(mat43, mat43, 0, 0, -10)
    # tree.write(mat43_target)

    # tree = parse_dsj4_xml(mat77, mat77, 0, 0, -10)
    # tree.write(mat77_target)


    print('Done!')
