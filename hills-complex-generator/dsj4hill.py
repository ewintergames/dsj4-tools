from hill import Hill, eps
import xml.etree.ElementTree as ET
import numpy as np
import copy


def x_shifter_name(hill_id):
    return f'x-shift-hill{hill_id}'


def y_shifter_name(hill_id):
    return f'y-shift-hill{hill_id}'


def z_shifter_name(hill_id):
    return f'z-shift-hill{hill_id}'


def inrun_name(hill_id):
    return f'inrun{hill_id}'


def inrun_top_name(hill_id):
    return f'inrun{hill_id}-top'


def inrun_left_name(hill_id):
    return f'inrun{hill_id}-left'


def inrun_right_name(hill_id):
    return f'inrun{hill_id}-right'


def dhill_name(hill_id):
    return f'dhill{hill_id}'


def dhill_u_name(hill_id):
    return f'dhill{hill_id}-u'

def dhill_end_name(hill_id):
    return f'dhill{hill_id}-end'


def dhill_top_name(hill_id):
    return f'dhill{hill_id}-top'


def dhill_left_name(hill_id):
    return f'dhill{hill_id}-left'


def dhill_right_name(hill_id):
    return f'dhill{hill_id}-right'


def hill_y_name(hill_id):
    return f'hill{hill_id}-y'


def hill_y0_name(hill_id):
    return f'hill{hill_id}-y0'


def hill_z_name(hill_id):
    return f'hill{hill_id}-z'


def profile_name_y(old_name, hill_id):
    return f'{old_name}-hill{hill_id}-refy'


def profile_name_z(old_name, hill_id):
    return f'{old_name}-hill{hill_id}-refz'


def element_name(old_name, hill_id):
    return f'{old_name}-hill{hill_id}'


unused_names = {'terrain', 'time', 'location',
                'weather', 'inrun', 'dhill', 'terrain'}

builtin_profiles = {'inrun', 'inrun-top', 'dhill',
                    'dhill-top', 'dhill-left', 'dhill-right'}
required_profiles = {'inrun-left', 'inrun-right'}
persistent_profiles = {'terrain'}

refy_attribs = {'refy', 'trefy', 'brefy', 'texture-refy'}
refz_attribs = {'refz', 'reflz', 'refrz'}


def get_line(elem_id, y, refx=None, refy=None):
    node = ET.Element('profile')
    node.attrib['id'] = elem_id

    tmp = ET.SubElement(node, 'start')
    tmp.attrib['x'] = '-1000'
    tmp.attrib['y'] = str(y)
    if refx is not None:
        tmp.attrib['refx'] = refx
    if refy is not None:
        tmp.attrib['refy'] = refy

    tmp = ET.SubElement(node, 'line')
    tmp.attrib['x'] = '1000'
    tmp.attrib['y'] = str(y)
    if refx is not None:
        tmp.attrib['refx'] = refx
    if refy is not None:
        tmp.attrib['refy'] = refy

    return node


def get_refx(elem_id, x, refx=None):
    node = ET.Element('refx')
    node.attrib['id'] = elem_id
    node.attrib['value'] = str(x)
    if refx is not None:
        node.attrib['refx'] = refx
    return node


def get_shifters(x, y, z, hill_id):
    return [get_refx(x_shifter_name(hill_id), x),
            get_line(y_shifter_name(hill_id), y),
            get_line(z_shifter_name(hill_id), z)]


def profile_from_xml(elem):
    inrun_dict = elem.find('inrun').find('profile').attrib
    guardrail_dict = elem.find('inrun').find('guardrail').attrib
    dhill_dict = elem.find('dhill').find('profile').attrib
    r2 = float(dhill_dict['r2']) if 'r2' in dhill_dict else None
    r2x = float(dhill_dict['r2x'])if 'r2x' in dhill_dict else None
    r2y = float(dhill_dict['r2y']) if 'r2y' in dhill_dict else None

    return Hill(e=float(inrun_dict['e']),
                es=float(inrun_dict['es']),
                gates=float(2),
                t=float(inrun_dict['t']),
                gamma=float(inrun_dict['gamma']),
                alpha=float(inrun_dict['alpha']),
                r1=float(inrun_dict['r1']),
                s=float(inrun_dict['s']),
                l=float(inrun_dict['l']),
                f=float(inrun_dict['f']),
                alpha_dhill=float(dhill_dict['alpha']),
                h=float(dhill_dict['h']),
                n=float(dhill_dict['n']),
                l1=float(dhill_dict['l1']),
                l2=float(dhill_dict['l2']),
                a=float(dhill_dict['a']),
                betap=float(dhill_dict['beta-p']),
                beta=float(dhill_dict['beta']),
                betal=float(dhill_dict['beta-l']),
                r2=r2,
                r2x=r2x,
                r2y=r2y,
                k=float(dhill_dict['k']),
                hs=float(dhill_dict['hs']),
                b1=float(inrun_dict['b1']),
                b0=float(dhill_dict['b0']),
                bk=float(dhill_dict['bk']),
                ba=float(dhill_dict['ba']),
                guardrail_z1=float(guardrail_dict['z1']),
                guardrail_z2=float(guardrail_dict['z2']))


def inrun_top_from_hill(hill, hill_id):
    a = ET.Element('profile')
    a.attrib['id'] = inrun_top_name(hill_id)

    b = ET.SubElement(a, 'start')
    b.attrib['x'] = str(hill.A[0] - hill.f)
    b.attrib['y'] = str(hill.A[1])
    b.attrib['refx'] = dhill_name(hill_id)
    b.attrib['refy'] = hill_y_name(hill_id)

    b = ET.SubElement(a, 'line')
    b.attrib['x'] = str(hill.A[0])
    b.attrib['y'] = str(hill.A[1])
    b.attrib['refx'] = dhill_name(hill_id)
    b.attrib['refy'] = hill_y_name(hill_id)

    b = ET.SubElement(a, 'line')
    b.attrib['x'] = str(hill.E1[0])
    b.attrib['y'] = str(hill.E1[1])
    b.attrib['refx'] = dhill_name(hill_id)
    b.attrib['refy'] = hill_y_name(hill_id)

    b = ET.SubElement(a, 'polynom3')
    b.attrib['x'] = str(hill.E2[0])
    b.attrib['y'] = str(hill.E2[1])
    b.attrib['k1'] = str(np.tan(-hill.gamma))
    b.attrib['k2'] = str(np.tan(-hill.alpha))
    b.attrib['refx'] = dhill_name(hill_id)
    b.attrib['refy'] = hill_y_name(hill_id)

    b = ET.SubElement(a, 'line')
    b.attrib['x'] = str(hill.T[0])
    b.attrib['y'] = str(hill.T[1])
    b.attrib['refx'] = dhill_name(hill_id)
    b.attrib['refy'] = hill_y_name(hill_id)
    return a


def dhill_top_from_hill(hill, hill_id):
    a = ET.Element('profile')
    a.attrib['id'] = dhill_top_name(hill_id)

    b = ET.SubElement(a, 'start')
    b.attrib['x'] = str(hill.F[0])
    b.attrib['y'] = str(hill.F[1])
    b.attrib['refy'] = hill_y_name(hill_id)
    b.attrib['refx'] = dhill_name(hill_id)

    c = ET.SubElement(a, 'polynom3')
    c.attrib['x'] = str(hill.P[0])
    c.attrib['y'] = str(hill.P[1])
    c.attrib['k1'] = str(np.tan(-hill.beta0))
    c.attrib['k2'] = str(np.tan(-hill.betaP))
    c.attrib['refx'] = dhill_name(hill_id)
    c.attrib['refy'] = hill_y_name(hill_id)

    if hill.rL1 < eps:
        d = ET.SubElement(a, 'line')
    else:
        d = ET.SubElement(a, 'polynom3')
        d.attrib['k1'] = str(np.tan(-hill.betaP))
        d.attrib['k2'] = str(np.tan(-hill.betaK))
    d.attrib['x'] = str(hill.K[0])
    d.attrib['y'] = str(hill.K[1])
    d.attrib['refx'] = dhill_name(hill_id)
    d.attrib['refy'] = hill_y_name(hill_id)

    if hill.rL2 < eps:
        e = ET.SubElement(a, 'line')
    else:
        e = ET.SubElement(a, 'polynom3')
        e.attrib['k1'] = str(np.tan(-hill.betaK))
        e.attrib['k2'] = str(np.tan(-hill.betaL))
    e.attrib['x'] = str(hill.L[0])
    e.attrib['y'] = str(hill.L[1])
    e.attrib['refx'] = dhill_name(hill_id)
    e.attrib['refy'] = hill_y_name(hill_id)

    f = ET.SubElement(a, 'polynom3')
    f.attrib['x'] = str(hill.U[0])
    f.attrib['y'] = str(hill.U[1])
    f.attrib['k1'] = str(np.tan(-hill.betaL))
    f.attrib['k2'] = str(0)
    f.attrib['refx'] = dhill_name(hill_id)
    f.attrib['refy'] = hill_y_name(hill_id)
    return a


def dhill_side_from_hill(hill, side, hill_id, z_shift):
    a = ET.Element('profile')
    a.attrib['id'] = dhill_right_name(
        hill_id) if side == -1 else dhill_left_name(hill_id)

    b = ET.SubElement(a, 'start')
    b.attrib['x'] = str(hill.F[0])
    b.attrib['y'] = str(side * hill.b2 * 0.5 + z_shift)
    b.attrib['refx'] = dhill_name(hill_id)

    c = ET.SubElement(a, 'line')
    c.attrib['x'] = str(hill.K[0])
    c.attrib['y'] = str(side * hill.bK * 0.5 + z_shift)
    c.attrib['refx'] = dhill_name(hill_id)

    d = ET.SubElement(a, 'line')
    d.attrib['x'] = str(hill.U[0])
    d.attrib['y'] = str(side * hill.bU * 0.5 + z_shift)
    d.attrib['refx'] = dhill_name(hill_id)

    d = ET.SubElement(a, 'line')
    d.attrib['x'] = str(hill.U[0] + hill.a - hill.bU * 0.5)
    d.attrib['y'] = str(side * hill.bU * 0.5 + z_shift)
    d.attrib['refx'] = dhill_name(hill_id)

    d = ET.SubElement(a, 'line')
    d.attrib['x'] = str(hill.U[0] + hill.a)
    d.attrib['y'] = str(z_shift)
    d.attrib['refx'] = dhill_name(hill_id)
    return a


def hill_alignment(mh_profile, sh_profile, hill_id, x_shift, y_shift, z_shift):
    delta = mh_profile.U - sh_profile.U
    dhill_x = delta[0] + x_shift
    inrun_x = sh_profile.A[0] - sh_profile.f + delta[0] + x_shift
    dhill_ux = dhill_x + sh_profile.U[0]
    dhill_end = dhill_x + sh_profile.U[0] + sh_profile.a
    hill_y = delta[1] + y_shift + sh_profile.s
    hill_y0 = hill_y
    hill_z = z_shift

    return [get_refx(inrun_name(hill_id), inrun_x),
            get_refx(dhill_name(hill_id), dhill_x),
            get_refx(dhill_u_name(hill_id), dhill_ux),
            get_refx(dhill_end_name(hill_id), dhill_ux),
            get_line(hill_y_name(hill_id), hill_y),
            get_line(hill_y0_name(hill_id), hill_y0),
            get_line(hill_z_name(hill_id), hill_z)]


def adjust_attribs(substitutions, node, x_shift=0, y_shift=0, z_shift=0, adjust_x=False, adjust_y=False, adjust_z=False, node_type=-1):
    for k, v in node.attrib.items():
        if v in substitutions:
            if type(substitutions[v]) is tuple:
                if k in refy_attribs:
                    node.attrib[k] = substitutions[v][0]
                elif k in refz_attribs:
                    node.attrib[k] = substitutions[v][1]
                elif k == 'id':
                    node.attrib[k] = substitutions[v][node_type]
            else:
                node.attrib[k] = substitutions[v]

    if 'refx' not in node.attrib:
        node.attrib['refx'] = substitutions['dhill']
    if 'refx' in node.attrib:
        if 'x1' in node.attrib and 'refx1' not in node.attrib:
            node.attrib['refx1'] = node.attrib['refx']
        if 'x2' in node.attrib and 'refx2' not in node.attrib:
            node.attrib['refx2'] = node.attrib['refx']
    elif adjust_x:
        node.attrib['refx'] = substitutions['dhill']
        if 'x1' in node.attrib and 'refx1' not in node.attrib:
            node.attrib['refx1'] = substitutions['dhill']
        if 'x2' in node.attrib and 'refx2' not in node.attrib:
            node.attrib['refx2'] = substitutions['dhill']

    if adjust_y:
        if 'y' in node.attrib and 'refy' not in node.attrib:
            node.attrib['refy'] = substitutions['hill-y0']
        if 'ty' in node.attrib and 'trefy' not in node.attrib:
            node.attrib['trefy'] = substitutions['hill-y0']
        if 'by' in node.attrib and 'brefy' not in node.attrib:
            node.attrib['brefy'] = substitutions['hill-y0']
        if 'tly1' in node.attrib and 'trefly1' not in node.attrib:
            node.attrib['trefly1'] = substitutions['hill-y0']
        if 'bly1' in node.attrib and 'brefly1' not in node.attrib:
            node.attrib['brefly1'] = substitutions['hill-y0']
        if 'tly2' in node.attrib and 'trefly2' not in node.attrib:
            node.attrib['trefly2'] = substitutions['hill-y0']
        if 'bly2' in node.attrib and 'brefly2' not in node.attrib:
            node.attrib['brefly2'] = substitutions['hill-y0']

    if adjust_z and node_type == 1:
        if 'y' in node.attrib and 'refy' not in node.attrib:
            node.attrib['refy'] = substitutions['hill-z']
    if adjust_z:
        if 'z' in node.attrib and 'refz' not in node.attrib:
            node.attrib['refz'] = substitutions['hill-z']
    if 'refz' in node.attrib:
        if 'rz' in node.attrib and 'refrz' not in node.attrib:
            node.attrib['refrz'] = node.attrib['refz']
        if 'lz' in node.attrib and 'reflz' not in node.attrib:
            node.attrib['reflz'] = node.attrib['refz']
        if 'trz' in node.attrib and 'trefrz' not in node.attrib:
            node.attrib['trefrz'] = node.attrib['refz']
        if 'brz' in node.attrib and 'brefrz' not in node.attrib:
            node.attrib['brefrz'] = node.attrib['refz']
        if 'tlz' in node.attrib and 'treflz' not in node.attrib:
            node.attrib['treflz'] = node.attrib['refz']
        if 'blz' in node.attrib and 'breflz' not in node.attrib:
            node.attrib['breflz'] = node.attrib['refz']
    elif adjust_z:
        node.attrib['refz'] = substitutions['hill-z']
        if 'rz' in node.attrib and 'refrz' not in node.attrib:
            node.attrib['refrz'] = substitutions['hill-z']
        if 'lz' in node.attrib and 'reflz' not in node.attrib:
            node.attrib['reflz'] = substitutions['hill-z']
        if 'trz' in node.attrib and 'trefrz' not in node.attrib:
            node.attrib['trefrz'] = substitutions['hill-z']
        if 'brz' in node.attrib and 'brefrz' not in node.attrib:
            node.attrib['brefrz'] = substitutions['hill-z']
        if 'tlz' in node.attrib and 'treflz' not in node.attrib:
            node.attrib['treflz'] = substitutions['hill-z']
        if 'blz' in node.attrib and 'breflz' not in node.attrib:
            node.attrib['breflz'] = substitutions['hill-z']


def adjust_inrun_sides(substitutions, node, side, b1, z_shift):
    adjust_attribs(substitutions, node)

    for p in node:
        adjust_attribs(substitutions, p)
        y = float(p.attrib['y']) + z_shift
        p.attrib['y'] = str(y)


def make_hill(substitutions, node, hill, z_shift):
    '''
    <railing refx="inrun0" x1="0.2" x2="6.75" z="2.75" refy="platform1-top" 
    h="1.0" h2="0.85" w="0.05" t="Textures\\wood1b.png" 
    m="Materials\\material1.xml" c="0x5a464e"/>
    '''

    mat = 'Materials\\snow.xml'
    tex = ''
    scl = '1000'
    col = '0xe3e3e3'  # '0xffffff'

    # inrun
    a = ET.SubElement(node, 'pillar')
    a.attrib['refx'] = substitutions['dhill']
    a.attrib['refx1'] = substitutions['inrun']
    a.attrib['refx2'] = substitutions['dhill']
    a.attrib['x1'] = '0'
    a.attrib['x2'] = '0'

    a.attrib['reflz'] = substitutions['hill-z']
    a.attrib['refrz'] = substitutions['hill-z']
    a.attrib['lz'] = str(hill.guardrail_z2)
    a.attrib['rz'] = str(hill.guardrail_z1)

    a.attrib['trefy'] = substitutions['inrun-top']
    a.attrib['brefy'] = substitutions['inrun-top']
    a.attrib['ty'] = '0.02'
    a.attrib['by'] = '-0.02'
    a.attrib['t'] = tex
    a.attrib['m'] = mat
    a.attrib['scale'] = scl
    a.attrib['c'] = col

    # dhill
    a = ET.SubElement(node, 'pillar')
    a.attrib['refx'] = substitutions['dhill']
    a.attrib['refx1'] = substitutions['dhill']
    a.attrib['refx2'] = substitutions['dhill-u']
    a.attrib['x1'] = '0'
    a.attrib['x2'] = '0'

    a.attrib['reflz'] = substitutions['dhill-left']
    a.attrib['refrz'] = substitutions['dhill-right']
    a.attrib['lz'] = '0'
    a.attrib['rz'] = '0'

    a.attrib['trefy'] = substitutions['dhill-top']
    a.attrib['brefy'] = substitutions['dhill-top']
    a.attrib['ty'] = '0.02'
    a.attrib['by'] = '-0.02'
    a.attrib['t'] = tex
    a.attrib['m'] = mat
    a.attrib['scale'] = scl
    a.attrib['c'] = col

    # dhill-fence
    a = ET.SubElement(node, 'railing')
    a.attrib['refx'] = substitutions['dhill']
    a.attrib['refx1'] = substitutions['dhill']
    a.attrib['refx2'] = substitutions['dhill-u']
    a.attrib['x1'] = '0'
    a.attrib['x2'] = '0'
    a.attrib['refy'] = substitutions['dhill-top']
    a.attrib['refz'] = substitutions['dhill-left']
    a.attrib['h'] = '1'
    a.attrib['w'] = '0.1'
    a.attrib['t'] = tex
    a.attrib['m'] = mat
    a.attrib['scale'] = scl
    a.attrib['c'] = col

    a = ET.SubElement(node, 'railing')
    a.attrib['refx'] = substitutions['dhill']
    a.attrib['refx1'] = substitutions['dhill']
    a.attrib['refx2'] = substitutions['dhill-u']
    a.attrib['x1'] = '0'
    a.attrib['x2'] = '0'
    a.attrib['refy'] = substitutions['dhill-top']
    a.attrib['refz'] = substitutions['dhill-right']
    a.attrib['h'] = '1'
    a.attrib['w'] = '0.1'
    a.attrib['t'] = tex
    a.attrib['m'] = mat
    a.attrib['scale'] = scl
    a.attrib['c'] = col


def convert_profile(substitutions, node, type):
    adjust_attribs(substitutions, node, True)
    refx = node.attrib['refx']
    for p in node:
        if 'refx' not in p.attrib:
            p.attrib['refx'] = refx
        if p.tag == 'profile':
            if 'x' not in p.attrib:
                p.attrib['x'] = '0'
            if 'refy' not in p.attrib:
                p.attrib['refy'] = substitutions['hill-y0'] if type == 'y' else substitutions['hill-z']
            adjust_attribs(substitutions, p, True, type == 'y',
                           type == 'z', 0 if type == 'y' else 1)
        else:
            adjust_attribs(substitutions, p, False, type == 'y',
                           type == 'z', 0 if type == 'y' else 1)


def append_converted_nodes(mh_root, sh_root, hill_id, x_shift, y_shift, z_shift):
    mh_profile = profile_from_xml(mh_root)
    sh_profile = profile_from_xml(sh_root)

    # inrun, dhill, hill-y
    mh_root.extend(hill_alignment(
        mh_profile, sh_profile, hill_id, x_shift, y_shift, z_shift))

    mh_root.append(inrun_top_from_hill(sh_profile, hill_id))
    mh_root.append(dhill_top_from_hill(sh_profile, hill_id))
    mh_root.append(dhill_side_from_hill(sh_profile, 1, hill_id, z_shift))
    mh_root.append(dhill_side_from_hill(sh_profile, -1, hill_id, z_shift))

    substitutions = {'inrun': inrun_name(hill_id),
                     'inrun-top': inrun_top_name(hill_id),
                     'inrun-left': inrun_left_name(hill_id),
                     'inrun-right': inrun_right_name(hill_id),
                     'dhill': dhill_name(hill_id),
                     'dhill-u': dhill_u_name(hill_id),
                     'dhill-top': dhill_top_name(hill_id),
                     'dhill-left': dhill_left_name(hill_id),
                     'dhill-right': dhill_right_name(hill_id),
                     'hill-y': hill_y_name(hill_id),
                     'hill-y0': hill_y0_name(hill_id),
                     'hill-z': hill_z_name(hill_id)}

    make_hill(substitutions, mh_root, sh_profile, z_shift)

    for node in sh_root:
        if node.tag in unused_names:
            continue

        mh_root.append(node)

        if node.tag == 'profile':
            if 'id' in node.attrib and node.attrib['id'] not in substitutions:
                substitutions[node.attrib['id']] = (profile_name_y(node.attrib['id'], hill_id),
                                                    profile_name_z(node.attrib['id'], hill_id))

            # inrun-left & inrun-right
            if node.attrib['id'] == 'inrun-left':
                adjust_inrun_sides(substitutions, node, 1,
                                   sh_profile.b1, z_shift)
            elif node.attrib['id'] == 'inrun-right':
                adjust_inrun_sides(substitutions, node, -1,
                                   sh_profile.b1, z_shift)
            else:
                node2 = copy.deepcopy(node)
                mh_root.append(node2)

                node.attrib['id'] = profile_name_y(node.attrib['id'], hill_id)
                node2.attrib['id'] = profile_name_z(
                    node2.attrib['id'], hill_id)

                convert_profile(substitutions, node, 'y')
                convert_profile(substitutions, node2, 'z')
        elif node.tag == 'stairs':
            if 'id' in node.attrib and node.attrib['id'] not in substitutions:
                substitutions[node.attrib['id']] = element_name(
                    node.attrib['id'], hill_id)
            # if 'rz' in node.attrib and not 'refrz' in node.attrib:
            #     node.attrib['rz'] = str(float(node.attrib['rz']) + z_shift)
            # if 'lz' in node.attrib and not 'reflz' in node.attrib:
            #     node.attrib['lz'] = str(float(node.attrib['lz']) + z_shift)
            adjust_attribs(substitutions, node, adjust_z=True)
            if 'refy' not in node.attrib:
                node.attrib['refy'] = substitutions['inrun-top']
        elif node.tag == 'beamgroup' or node.tag == 'beam':
            if 'id' in node.attrib and node.attrib['id'] not in substitutions:
                substitutions[node.attrib['id']] = element_name(
                    node.attrib['id'], hill_id)
            adjust_attribs(substitutions, node, adjust_z=True)
            if 'refx' not in node.attrib:
                node.attrib['refx'] = substitutions['inrun']
            if 'refy' not in node.attrib:
                node.attrib['refy'] = substitutions['inrun-top']
            if 'refz' not in node.attrib:
                node.attrib['refz'] = substitutions['hill-z']
            if 'z' not in node.attrib:
                node.attrib['z'] = '0'
        elif node.tag == 'railing':
            if 'id' in node.attrib and node.attrib['id'] not in substitutions:
                substitutions[node.attrib['id']] = element_name(
                    node.attrib['id'], hill_id)
            if 'z' in node.attrib:
                node.attrib['z'] = str(float(node.attrib['z']) + z_shift)
                adjust_attribs(substitutions, node)
            elif 'z1' in node.attrib and 'z2' in node.attrib:
                node.attrib['z1'] = str(float(node.attrib['z1']) + z_shift)
                node.attrib['z2'] = str(float(node.attrib['z2']) + z_shift)
                adjust_attribs(substitutions, node)
            elif 'w' in node.attrib:
                node.attrib['z'] = str(z_shift)
                adjust_attribs(substitutions, node)
            else:
                adjust_attribs(substitutions, node, adjust_z=True)
            if 'refx' not in node.attrib:
                node.attrib['refx'] = substitutions['inrun']
            # if 'refx1' not in node.attrib:
            #     node.attrib['refx1'] = substitutions['inrun']
            # if 'refx2' not in node.attrib:
            #     node.attrib['refx2'] = substitutions['inrun']                            
            if 'refy' not in node.attrib:
                node.attrib['refy'] = substitutions['inrun-top']
        elif node.tag == 'pillar':
            if 'id' in node.attrib and node.attrib['id'] not in substitutions:
                substitutions[node.attrib['id']] = element_name(
                    node.attrib['id'], hill_id)
            elif 'z1' in node.attrib and 'z2' in node.attrib:
                node.attrib['z1'] = str(float(node.attrib['z1']) + z_shift)
                node.attrib['z2'] = str(float(node.attrib['z2']) + z_shift)
            adjust_attribs(substitutions, node, adjust_y = True, adjust_z=True)
            if 'refx' not in node.attrib:
                node.attrib['refx'] = substitutions['inrun']
        else:
            if 'id' in node.attrib and node.attrib['id'] not in substitutions:
                substitutions[node.attrib['id']] = element_name(
                    node.attrib['id'], hill_id)
            adjust_attribs(substitutions, node, adjust_z=True)
