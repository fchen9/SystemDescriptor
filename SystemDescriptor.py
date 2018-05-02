import argparse
import logging
import os
from lxml import etree
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from xml.dom.minidom import parseString


def arg_parse(parser):
    parser.add_argument('-config', '--config', help="configuration file location", required=True, default="")
    parser.add_argument('-system', '--system', help="system name", required=False, default="")
    parser.add_argument('-mapping', '--mapping', help="mapping name", required=False, default="")
    parser.add_argument('-compo', '--compo', help="composition name", required=False, default="")
    parser.add_argument('-modularity', action="store_const", const="-modularity", required=False)


def new_prettify(elem):
    rough_string = etree.tostring(elem, pretty_print=True)
    reparsed = parseString(rough_string)
    return '\n'.join([line for line in reparsed.toprettyxml(indent=' '*4).split('\n') if line.strip()])


def remove_duplicates(list_to_be_checked):
    found = set()
    for item in list_to_be_checked:
        if item['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text not in found:
            yield item
            found.add(item['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text)


# check compatibility between interfaces or types
def check_compatibility(recursive_dico, simple_dico, logger):
    # parse all input files to get all interfaces and types
    sr_interfaces = []
    cs_interfaces = []
    nv_interfaces = []
    p_interfaces = []
    ms_interfaces = []
    types = []
    logger.info('=================Parsing information=================')
    for each_path in recursive_dico:
        for directory, directories, files in os.walk(each_path):
            for file in files:
                if file.endswith('.dico'):
                    fullname = os.path.join(directory, file)
                    try:
                        check_xml_wellformed(fullname)
                        logger.info(' The file '+fullname+' is well-formed')
                    except Exception as e:
                        logger.error(' The file '+fullname+' is not well-formed: '+str(e))
                        return
                    tree = etree.parse(fullname)
                    root = tree.getroot()
                    sender_receiver_interface = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-INTERFACE")
                    client_server_interface = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-INTERFACE")
                    nv_data_interface = root.findall(".//{http://autosar.org/schema/r4.0}NV-DATA-INTERFACE")
                    parameter_interface = root.findall(".//{http://autosar.org/schema/r4.0}PARAMETER-INTERFACE")
                    mode_switch_interface = root.findall(".//{http://autosar.org/schema/r4.0}MODE-SWITCH-INTERFACE")
                    data_types = root.findall(".//{http://autosar.org/schema/r4.0}IMPLEMENTATION-DATA-TYPE")
                    for elemSR in sender_receiver_interface:
                        objElement = {}
                        objElement['SHORT-NAME'] = elemSR.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                        objElement['VERSION'] = elemSR.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        sr_interfaces.append(objElement)
                    for elemCS in client_server_interface:
                        objElement = {}
                        objElement['SHORT-NAME'] = elemCS.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                        objElement['VERSION'] = elemCS.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        cs_interfaces.append(objElement)
                    for elemNV in nv_data_interface:
                        objElement = {}
                        objElement['SHORT-NAME'] = elemNV.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                        objElement['VERSION'] = elemNV.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        nv_interfaces.append(objElement)
                    for elemP in parameter_interface:
                        objElement = {}
                        objElement['SHORT-NAME'] = elemP.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                        objElement['VERSION'] = elemP.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        p_interfaces.append(objElement)
                    for elemMS in mode_switch_interface:
                        objElement = {}
                        objElement['SHORT-NAME'] = elemMS.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                        objElement['VERSION'] = elemMS.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        ms_interfaces.append(objElement)
                    for elemType in data_types:
                        objElement = {}
                        objElement['SHORT-NAME'] = elemType.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                        if elemType.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL") is not None:
                            objElement['VERSION'] = elemType.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        types.append(objElement)
    for each_path in simple_dico:
        for file in os.listdir(each_path):
            if file.endswith('.dico'):
                fullname = os.path.join(each_path, file)
                try:
                    check_xml_wellformed(fullname)
                    logger.info(' The file ' + fullname + ' is well-formed')
                except Exception as e:
                    logger.error(' The file ' + fullname + ' is not well-formed: ' + str(e))
                    return
                tree = etree.parse(fullname)
                root = tree.getroot()
                sender_receiver_interface = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-INTERFACE")
                client_server_interface = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-INTERFACE")
                nv_data_interface = root.findall(".//{http://autosar.org/schema/r4.0}NV-DATA-INTERFACE")
                parameter_interface = root.findall(".//{http://autosar.org/schema/r4.0}PARAMETER-INTERFACE")
                mode_switch_interface = root.findall(".//{http://autosar.org/schema/r4.0}MODE-SWITCH-INTERFACE")
                data_types = root.findall(".//{http://autosar.org/schema/r4.0}IMPLEMENTATION-DATA-TYPE")
                for elemSR in sender_receiver_interface:
                    objElement = {}
                    objElement['SHORT-NAME'] = elemSR.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    objElement['VERSION'] = elemSR.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                    sr_interfaces.append(objElement)
                for elemCS in client_server_interface:
                    objElement = {}
                    objElement['SHORT-NAME'] = elemCS.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    objElement['VERSION'] = elemCS.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                    cs_interfaces.append(objElement)
                for elemNV in nv_data_interface:
                    objElement = {}
                    objElement['SHORT-NAME'] = elemNV.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    objElement['VERSION'] = elemNV.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                    nv_interfaces.append(objElement)
                for elemP in parameter_interface:
                    objElement = {}
                    objElement['SHORT-NAME'] = elemP.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    objElement['VERSION'] = elemP.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                    p_interfaces.append(objElement)
                for elemMS in mode_switch_interface:
                    objElement = {}
                    objElement['SHORT-NAME'] = elemMS.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    objElement['VERSION'] = elemMS.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                    ms_interfaces.append(objElement)
                for elemType in data_types:
                    objElement = {}
                    objElement['SHORT-NAME'] = elemType.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text
                    if elemType.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL") is not None:
                        objElement['VERSION'] = elemType.find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                    types.append(objElement)
    # check compatibility between different types of data
    error_found = False
    for index1 in range(len(sr_interfaces)):
        for index2 in range(len(sr_interfaces)):
            if index1 != index2:
                if sr_interfaces[index1]['SHORT-NAME'] == sr_interfaces[index2]['SHORT-NAME']:
                    if sr_interfaces[index1]['VERSION'][-12:] != sr_interfaces[index2]['VERSION'][-12:]:
                        logger.error('The interface: '+sr_interfaces[index1]['SHORT-NAME']+' has different versions:'+sr_interfaces[index1]['VERSION']+' and '+sr_interfaces[index2]['VERSION'])
                        error_found = True
    for index1 in range(len(cs_interfaces)):
        for index2 in range(len(cs_interfaces)):
            if index1 != index2:
                if cs_interfaces[index1]['SHORT-NAME'] == cs_interfaces[index2]['SHORT-NAME']:
                    if cs_interfaces[index1]['VERSION'][-12:] != cs_interfaces[index2]['VERSION'][-12:]:
                        logger.error('The interface: '+cs_interfaces[index1]['SHORT-NAME']+' has different versions:'+cs_interfaces[index1]['VERSION']+' and '+cs_interfaces[index2]['VERSION'])
                        error_found = True
    for index1 in range(len(nv_interfaces)):
        for index2 in range(len(nv_interfaces)):
            if index1 != index2:
                if nv_interfaces[index1]['SHORT-NAME'] == nv_interfaces[index2]['SHORT-NAME']:
                    if nv_interfaces[index1]['VERSION'][-12:] != nv_interfaces[index2]['VERSION'][-12:]:
                        logger.error('The interface: '+nv_interfaces[index1]['SHORT-NAME']+' has different versions:'+nv_interfaces[index1]['VERSION']+' and '+nv_interfaces[index2]['VERSION'])
                        error_found = True
    for index1 in range(len(p_interfaces)):
        for index2 in range(len(p_interfaces)):
            if index1 != index2:
                if p_interfaces[index1]['SHORT-NAME'] == p_interfaces[index2]['SHORT-NAME']:
                    if p_interfaces[index1]['VERSION'][-12:] != p_interfaces[index2]['VERSION'][-12:]:
                        logger.error('The interface: '+p_interfaces[index1]['SHORT-NAME']+' has different versions:'+p_interfaces[index1]['VERSION']+' and '+p_interfaces[index2]['VERSION'])
                        error_found = True
    for index1 in range(len(ms_interfaces)):
        for index2 in range(len(ms_interfaces)):
            if index1 != index2:
                if ms_interfaces[index1]['SHORT-NAME'] == ms_interfaces[index2]['SHORT-NAME']:
                    if ms_interfaces[index1]['VERSION'][-12:] != ms_interfaces[index2]['VERSION'][-12:]:
                        logger.error('The interface: '+ms_interfaces[index1]['SHORT-NAME']+' has different versions:'+ms_interfaces[index1]['VERSION']+' and '+ms_interfaces[index2]['VERSION'])
                        error_found = True
    for index1 in range(len(types)):
        for index2 in range(len(types)):
            if index1 != index2:
                if types[index1]['SHORT-NAME'] == types[index2]['SHORT-NAME']:
                    if types[index1]['VERSION'][-12:] != types[index2]['VERSION'][-12:]:
                        logger.error('The interface: '+types[index1]['SHORT-NAME']+' has different versions:'+types[index1]['VERSION']+' and '+types[index2]['VERSION'])
                        error_found = True
    if error_found:
        return False
    else:
        return True


def generate_system(recursive_arxml, recursive_dico, simple_arxml, simple_dico, output_path, xsd_path, system_name, mapping_name, composition_name, modularity, logger):
    NSMAP = {None: 'http://autosar.org/schema/r4.0',
             "xsi": 'http://www.w3.org/2001/XMLSchema-instance'}
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    interfaces = []
    final_interfaces = []
    m_interfaces = []
    types = []
    final_types = []
    m_types = []
    data_constr = []
    final_data_constr = []
    m_data_constr = []
    arxml_interfaces = []
    arxml_types = []
    arxml_data_constr = []
    system_signals = []
    provided_ports = []
    client_server_signal_group_mapping = []
    client_server_signal_mapping = []
    sender_receiver_composite_element = []
    sender_receiver_signal_group_mapping = []
    sender_receiver_signal_mapping = []
    trigger_signal_mapping = []
    component_clustering = []
    component_separation = []
    sw_ecu_mapping_constraint = []
    pnc_mapping = []
    ecu_mapping = []
    ecu_resource_estimation = []
    common_signal_path = []
    forbidden_signal_path = []
    permissible_signal_path = []
    separate_signal_path = []
    sw_impl_mappings = []
    swc_ecu_mapping = []
    data_mappings_name = []
    software_composition = []
    system_version = []
    root_software_composition = []
    fibex_elements = []
    compu_methods = []
    arxml_compu_methods = []
    xmlschema_xsd_arxml = etree.parse(xsd_path)
    xmlschema_arxml = etree.XMLSchema(xmlschema_xsd_arxml)
    for each_path in recursive_dico:
        for directory, directories, files in os.walk(each_path):
            for file in files:
                if file.endswith('.dico'):
                    fullname = os.path.join(directory, file)
                    tree = etree.parse(fullname)
                    if xmlschema_arxml.validate(tree) is not True:
                        logger.warning('The file: ' + fullname + ' is NOT valid with the provided xsd schema')
                    else:
                        logger.info('The file: ' + fullname + ' is valid with the provided xsd schema')
                    root = tree.getroot()
                    pports = root.findall(".//{http://autosar.org/schema/r4.0}P-PORT-PROTOTYPE")
                    prports = root.findall(".//{http://autosar.org/schema/r4.0}PR-PORT-PROTOTYPE")
                    for elem in pports:
                        provided_ports.append(elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text)
                    for elem in prports:
                        provided_ports.append(elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text)
                    sender_receiver_interface = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-INTERFACE")
                    for elem in sender_receiver_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getprevious().text
                        objElem['DATA'] = elem
                        interfaces.append(objElem)
                    client_server_interface = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-INTERFACE")
                    for elem in client_server_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getprevious().text
                        objElem['DATA'] = elem
                        interfaces.append(objElem)
                    nv_data_interface = root.findall(".//{http://autosar.org/schema/r4.0}NV-DATA-INTERFACE")
                    for elem in nv_data_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getprevious().text
                        objElem['DATA'] = elem
                        interfaces.append(objElem)
                    parameter_interface = root.findall(".//{http://autosar.org/schema/r4.0}PARAMETER-INTERFACE")
                    for elem in parameter_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getprevious().text
                        objElem['DATA'] = elem
                        interfaces.append(objElem)
                    mode_switch_interface = root.findall(".//{http://autosar.org/schema/r4.0}MODE-SWITCH-INTERFACE")
                    for elem in mode_switch_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getprevious().text
                        objElem['DATA'] = elem
                        interfaces.append(objElem)
                    data_types = root.findall(".//{http://autosar.org/schema/r4.0}IMPLEMENTATION-DATA-TYPE")
                    for elem in data_types:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getprevious().text
                        objElem['DATA'] = elem
                        types.append(objElem)
                    computational_methods = root.findall(".//{http://autosar.org/schema/r4.0}COMPU-METHOD")
                    for elem in computational_methods:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getprevious().text
                        objElem['DATA'] = elem
                        compu_methods.append(objElem)
                    data_constraints = root.findall(".//{http://autosar.org/schema/r4.0}DATA-CONSTR")
                    for elem in data_constraints:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getprevious().text
                        objElem['DATA'] = elem
                        data_constr.append(objElem)
                    # data mappings
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-TO-SIGNAL-GROUP-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        client_server_signal_group_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-TO-SIGNAL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        client_server_signal_group_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-COMPOSITE-ELEMENT-TO-SIGNAL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sender_receiver_composite_element.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-GROUP-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sender_receiver_signal_group_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sender_receiver_signal_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}TRIGGER-TO-SIGNAL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        trigger_signal_mapping.append(objElem)
                    # ECU-RESOURCE-MAPPINGS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}ECU-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        trigger_signal_mapping.append(objElem)
                    # MAPPING-CONSTRAINT
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}COMPONENT-CLUSTERING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        component_clustering.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}COMPONENT-SEPARATION")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        component_separation.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-ECU-MAPPING-CONSTRAINT")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sw_ecu_mapping_constraint.append(objElem)
                    # PNC-MAPPINGS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}PNC-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        pnc_mapping.append(objElem)
                    # RESOURCE-ESTIMATIONS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}ECU-RESOURCE-ESTIMATION")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        ecu_resource_estimation.append(objElem)
                    # SIGNAL-PATH-CONSTRAINTS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}COMMON-SIGNAL-PATH")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        common_signal_path.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}FORBIDDEN-SIGNAL-PATH")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        forbidden_signal_path.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}PERMISSIBLE-SIGNAL-PATH")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        permissible_signal_path.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SEPARATE-SIGNAL-PATH")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        separate_signal_path.append(objElem)
                    # SW-IMPL-MAPPINGS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-IMPL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sw_impl_mappings.append(objElem)
                    # software mappings
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-ECU-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        swc_ecu_mapping.append(objElem)
                    # composition mapping
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SW-COMPONENT-PROTOTYPE")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        software_composition.append(objElem)
                    # fibex_elements
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}FIBEX-ELEMENTS")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        fibex_elements.append(objElem)
                    # root software compositions
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}ROOT-SW-COMPOSITION-PROTOTYPE")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        root_software_composition.append(objElem)
                    # system version
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SYSTEM-VERSION")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getchildren()[0].text
                        objElem['DATA'] = elem.text
                        system_version.append(objElem)
    for each_path in simple_dico:
        for file in os.listdir(each_path):
            if file.endswith('.dico'):
                fullname = os.path.join(each_path, file)
                tree = etree.parse(fullname)
                if xmlschema_arxml.validate(tree) is not True:
                    logger.warning('The file: ' + fullname + ' is NOT valid with the provided xsd schema')
                else:
                    logger.info('The file: ' + fullname + ' is valid with the provided xsd schema')
                tree = etree.parse(fullname)
                root = tree.getroot()
                pports = root.findall(".//{http://autosar.org/schema/r4.0}P-PORT-PROTOTYPE")
                prports = root.findall(".//{http://autosar.org/schema/r4.0}PR-PORT-PROTOTYPE")
                for elem in pports:
                    provided_ports.append(elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text)
                for elem in prports:
                    provided_ports.append(elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text)
                sender_receiver_interface = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-INTERFACE")
                for elem in sender_receiver_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getprevious().text
                    objElem['DATA'] = elem
                    interfaces.append(objElem)
                client_server_interface = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-INTERFACE")
                for elem in client_server_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getprevious().text
                    objElem['DATA'] = elem
                    interfaces.append(objElem)
                nv_data_interface = root.findall(".//{http://autosar.org/schema/r4.0}NV-DATA-INTERFACE")
                for elem in nv_data_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getprevious().text
                    objElem['DATA'] = elem
                    interfaces.append(objElem)
                parameter_interface = root.findall(".//{http://autosar.org/schema/r4.0}PARAMETER-INTERFACE")
                for elem in parameter_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getprevious().text
                    objElem['DATA'] = elem
                    interfaces.append(objElem)
                mode_switch_interface = root.findall(".//{http://autosar.org/schema/r4.0}MODE-SWITCH-INTERFACE")
                for elem in mode_switch_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getprevious().text
                    objElem['DATA'] = elem
                    interfaces.append(objElem)
                data_types = root.findall(".//{http://autosar.org/schema/r4.0}IMPLEMENTATION-DATA-TYPE")
                for elem in data_types:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getprevious().text
                    objElem['DATA'] = elem
                    types.append(objElem)
                computational_methods = root.findall(".//{http://autosar.org/schema/r4.0}COMPU-METHOD")
                for elem in computational_methods:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getprevious().text
                    objElem['DATA'] = elem
                    compu_methods.append(objElem)
                data_constraints = root.findall(".//{http://autosar.org/schema/r4.0}DATA-CONSTR")
                for elem in data_constraints:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getprevious().text
                    objElem['DATA'] = elem
                    data_constr.append(objElem)
                # data mappings
                temp = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-TO-SIGNAL-GROUP-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    client_server_signal_group_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-TO-SIGNAL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    client_server_signal_group_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-COMPOSITE-ELEMENT-TO-SIGNAL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sender_receiver_composite_element.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-GROUP-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sender_receiver_signal_group_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sender_receiver_signal_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}TRIGGER-TO-SIGNAL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    trigger_signal_mapping.append(objElem)
                # ECU-RESOURCE-MAPPINGS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}ECU-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    trigger_signal_mapping.append(objElem)
                # MAPPING-CONSTRAINT
                temp = root.findall(".//{http://autosar.org/schema/r4.0}COMPONENT-CLUSTERING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    component_clustering.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}COMPONENT-SEPARATION")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    component_separation.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-ECU-MAPPING-CONSTRAINT")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sw_ecu_mapping_constraint.append(objElem)
                # PNC-MAPPINGS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}PNC-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    pnc_mapping.append(objElem)
                # RESOURCE-ESTIMATIONS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}ECU-RESOURCE-ESTIMATION")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    ecu_resource_estimation.append(objElem)
                # SIGNAL-PATH-CONSTRAINTS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}COMMON-SIGNAL-PATH")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    common_signal_path.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}FORBIDDEN-SIGNAL-PATH")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    forbidden_signal_path.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}PERMISSIBLE-SIGNAL-PATH")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    permissible_signal_path.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SEPARATE-SIGNAL-PATH")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    separate_signal_path.append(objElem)
                # SW-IMPL-MAPPINGS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-IMPL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sw_impl_mappings.append(objElem)
                # software mappings
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-ECU-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    swc_ecu_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SW-COMPONENT-PROTOTYPE")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    software_composition.append(objElem)
                # fibex_elements
                temp = root.findall(".//{http://autosar.org/schema/r4.0}FIBEX-ELEMENTS")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    fibex_elements.append(objElem)
                # root software compositions
                temp = root.findall(".//{http://autosar.org/schema/r4.0}ROOT-SW-COMPOSITION-PROTOTYPE")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    root_software_composition.append(objElem)
                # system version
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SYSTEM-VERSION")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getchildren()[0].text
                    objElem['DATA'] = elem.text
                    system_version.append(objElem)
    for each_path in recursive_arxml:
        for directory, directories, files in os.walk(each_path):
            for file in files:
                if file.endswith('.arxml'):
                    fullname = os.path.join(directory, file)
                    try:
                        check_xml_wellformed(fullname)
                        logger.info('The file: ' + fullname + ' is well-formed')
                    except Exception as e:
                        logger.error('The file: ' + fullname + ' is not well-formed: ' + str(e))
                        return
                    tree = etree.parse(fullname)
                    if xmlschema_arxml.validate(tree) is not True:
                        logger.warning('The file: ' + fullname + ' is NOT valid with the provided xsd schema')
                    else:
                        logger.info('The file: ' + fullname + ' is valid with the provided xsd schema')
                    root = tree.getroot()
                    pports = root.findall(".//{http://autosar.org/schema/r4.0}P-PORT-PROTOTYPE")
                    prports = root.findall(".//{http://autosar.org/schema/r4.0}PR-PORT-PROTOTYPE")
                    for elem in pports:
                        provided_ports.append(elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text)
                    for elem in prports:
                        provided_ports.append(elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text)
                    sender_receiver_interface = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-INTERFACE")
                    for elem in sender_receiver_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        arxml_interfaces.append(objElem)
                    client_server_interface = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-INTERFACE")
                    for elem in client_server_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        arxml_interfaces.append(objElem)
                    nv_data_interface = root.findall(".//{http://autosar.org/schema/r4.0}NV-DATA-INTERFACE")
                    for elem in nv_data_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        arxml_interfaces.append(objElem)
                    parameter_interface = root.findall(".//{http://autosar.org/schema/r4.0}PARAMETER-INTERFACE")
                    for elem in parameter_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        arxml_interfaces.append(objElem)
                    mode_switch_interface = root.findall(".//{http://autosar.org/schema/r4.0}MODE-SWITCH-INTERFACE")
                    for elem in mode_switch_interface:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        arxml_interfaces.append(objElem)
                    data_types = root.findall(".//{http://autosar.org/schema/r4.0}IMPLEMENTATION-DATA-TYPE")
                    arxml_types = arxml_types + data_types
                    computational_methods = root.findall(".//{http://autosar.org/schema/r4.0}COMPU-METHOD")
                    arxml_compu_methods = arxml_compu_methods + computational_methods
                    data_constraints = root.findall(".//{http://autosar.org/schema/r4.0}DATA-CONSTR")
                    arxml_data_constr = arxml_data_constr + data_constraints
                    signals = root.findall(".//{http://autosar.org/schema/r4.0}SYSTEM-SIGNAL")
                    for elem in signals:
                        objElem = {}
                        objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        system_signals.append(objElem)
                    # data mappings
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-TO-SIGNAL-GROUP-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[
                            0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        client_server_signal_group_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-TO-SIGNAL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        client_server_signal_group_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-COMPOSITE-ELEMENT-TO-SIGNAL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sender_receiver_composite_element.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-GROUP-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sender_receiver_signal_group_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sender_receiver_signal_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}TRIGGER-TO-SIGNAL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        trigger_signal_mapping.append(objElem)
                    # ECU-RESOURCE-MAPPINGS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}ECU-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        trigger_signal_mapping.append(objElem)
                    # MAPPING-CONSTRAINT
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}COMPONENT-CLUSTERING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        component_clustering.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}COMPONENT-SEPARATION")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        component_separation.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-ECU-MAPPING-CONSTRAINT")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sw_ecu_mapping_constraint.append(objElem)
                    # PNC-MAPPINGS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}PNC-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        pnc_mapping.append(objElem)
                    # RESOURCE-ESTIMATIONS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}ECU-RESOURCE-ESTIMATION")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        ecu_resource_estimation.append(objElem)
                    # SIGNAL-PATH-CONSTRAINTS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}COMMON-SIGNAL-PATH")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        common_signal_path.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}FORBIDDEN-SIGNAL-PATH")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        forbidden_signal_path.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}PERMISSIBLE-SIGNAL-PATH")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        permissible_signal_path.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SEPARATE-SIGNAL-PATH")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        separate_signal_path.append(objElem)
                    # SW-IMPL-MAPPINGS
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-IMPL-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        sw_impl_mappings.append(objElem)
                    # software mappings
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-ECU-MAPPING")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        swc_ecu_mapping.append(objElem)
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SW-COMPONENT-PROTOTYPE")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        software_composition.append(objElem)
                    # fibex_elements
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}FIBEX-ELEMENTS")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        fibex_elements.append(objElem)
                    # root software compositions
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}ROOT-SW-COMPOSITION-PROTOTYPE")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getparent().getchildren()[0].text
                        objElem['DATA'] = elem
                        root_software_composition.append(objElem)
                    # system version
                    temp = root.findall(".//{http://autosar.org/schema/r4.0}SYSTEM-VERSION")
                    for elem in temp:
                        objElem = {}
                        objElem['ROOT'] = elem.getparent().getparent().getparent().getchildren()[0].text
                        objElem['SYSTEM'] = elem.getparent().getchildren()[0].text
                        objElem['DATA'] = elem.text
                        system_version.append(objElem)
    for each_path in simple_arxml:
        for file in os.listdir(each_path):
            if file.endswith('.arxml'):
                fullname = os.path.join(each_path, file)
                try:
                    check_xml_wellformed(fullname)
                    logger.info('The file: ' + fullname + ' is well-formed')
                except Exception as e:
                    logger.error('The file: ' + fullname + ' is not well-formed: ' + str(e))
                    return
                tree = etree.parse(fullname)
                if xmlschema_arxml.validate(tree) is not True:
                    logger.warning('The file: ' + fullname + ' is NOT valid with the provided xsd schema')
                else:
                    logger.info('The file: ' + fullname + ' is valid with the provided xsd schema')
                tree = etree.parse(fullname)
                root = tree.getroot()
                pports = root.findall(".//{http://autosar.org/schema/r4.0}P-PORT-PROTOTYPE")
                prports = root.findall(".//{http://autosar.org/schema/r4.0}PR-PORT-PROTOTYPE")
                for elem in pports:
                    provided_ports.append(elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text)
                for elem in prports:
                    provided_ports.append(elem.find(".//{http://autosar.org/schema/r4.0}SHORT-NAME").text)
                sender_receiver_interface = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-INTERFACE")
                for elem in sender_receiver_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    arxml_interfaces.append(objElem)
                client_server_interface = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-INTERFACE")
                for elem in client_server_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    arxml_interfaces.append(objElem)
                nv_data_interface = root.findall(".//{http://autosar.org/schema/r4.0}NV-DATA-INTERFACE")
                for elem in nv_data_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    arxml_interfaces.append(objElem)
                parameter_interface = root.findall(".//{http://autosar.org/schema/r4.0}PARAMETER-INTERFACE")
                for elem in parameter_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    arxml_interfaces.append(objElem)
                mode_switch_interface = root.findall(".//{http://autosar.org/schema/r4.0}MODE-SWITCH-INTERFACE")
                for elem in mode_switch_interface:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    arxml_interfaces.append(objElem)
                data_types = root.findall(".//{http://autosar.org/schema/r4.0}IMPLEMENTATION-DATA-TYPE")
                arxml_types = arxml_types + data_types
                computational_methods = root.findall(".//{http://autosar.org/schema/r4.0}COMPU-METHOD")
                arxml_compu_methods = arxml_compu_methods + computational_methods
                data_constraints = root.findall(".//{http://autosar.org/schema/r4.0}DATA-CONSTR")
                arxml_data_constr = arxml_data_constr + data_constraints
                signals = root.findall(".//{http://autosar.org/schema/r4.0}SYSTEM-SIGNAL")
                for elem in signals:
                    objElem = {}
                    objElem['PACKAGE'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    system_signals.append(objElem)
                # data mappings
                temp = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-TO-SIGNAL-GROUP-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    client_server_signal_group_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}CLIENT-SERVER-TO-SIGNAL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    client_server_signal_group_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-COMPOSITE-ELEMENT-TO-SIGNAL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sender_receiver_composite_element.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-GROUP-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sender_receiver_signal_group_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SENDER-RECEIVER-TO-SIGNAL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sender_receiver_signal_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}TRIGGER-TO-SIGNAL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    trigger_signal_mapping.append(objElem)
                # ECU-RESOURCE-MAPPINGS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}ECU-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    trigger_signal_mapping.append(objElem)
                # MAPPING-CONSTRAINT
                temp = root.findall(".//{http://autosar.org/schema/r4.0}COMPONENT-CLUSTERING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    component_clustering.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}COMPONENT-SEPARATION")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    component_separation.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-ECU-MAPPING-CONSTRAINT")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sw_ecu_mapping_constraint.append(objElem)
                # PNC-MAPPINGS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}PNC-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    pnc_mapping.append(objElem)
                # RESOURCE-ESTIMATIONS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}ECU-RESOURCE-ESTIMATION")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    ecu_resource_estimation.append(objElem)
                # SIGNAL-PATH-CONSTRAINTS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}COMMON-SIGNAL-PATH")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    common_signal_path.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}FORBIDDEN-SIGNAL-PATH")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    forbidden_signal_path.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}PERMISSIBLE-SIGNAL-PATH")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    permissible_signal_path.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SEPARATE-SIGNAL-PATH")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    separate_signal_path.append(objElem)
                # SW-IMPL-MAPPINGS
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-IMPL-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    sw_impl_mappings.append(objElem)
                # software mappings
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SWC-TO-ECU-MAPPING")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    swc_ecu_mapping.append(objElem)
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SW-COMPONENT-PROTOTYPE")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['NAME'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    software_composition.append(objElem)
                # fibex_elements
                temp = root.findall(".//{http://autosar.org/schema/r4.0}FIBEX-ELEMENTS")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    fibex_elements.append(objElem)
                # root software compositions
                temp = root.findall(".//{http://autosar.org/schema/r4.0}ROOT-SW-COMPOSITION-PROTOTYPE")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getparent().getchildren()[0].text
                    objElem['DATA'] = elem
                    root_software_composition.append(objElem)
                # system version
                temp = root.findall(".//{http://autosar.org/schema/r4.0}SYSTEM-VERSION")
                for elem in temp:
                    objElem = {}
                    objElem['ROOT'] = elem.getparent().getparent().getparent().getchildren()[0].text
                    objElem['SYSTEM'] = elem.getparent().getchildren()[0].text
                    objElem['DATA'] = elem.text
                    system_version.append(objElem)

    # TODO: to check the full path for signal reference
    # TRS.SYSDESC.GEN.004
    logger.info('=================<SENDER-RECEIVER-TO-SIGNAL-MAPPING> without added signal=================')
    for elem in sender_receiver_signal_mapping[:]:
        found = False
        for elem_signal in system_signals:
            if elem_signal['PACKAGE'] in elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SYSTEM-SIGNAL-REF').text:
                if elem_signal['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text in elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SYSTEM-SIGNAL-REF').text:
                    found = True
                    break
        if not found:
            sender_receiver_signal_mapping.remove(elem)
            logger.info('The SENDER-RECEIVER-TO-SIGNAL-MAPPING using the signal' + elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SYSTEM-SIGNAL-REF').text + ' has not beed added because the signal reference is missing')

    # TRS.SYSDESC.GEN.002
    if modularity:
        for index1 in range(len(interfaces)):
            found = False
            for index2 in range(len(interfaces)):
                if index1 != index2:
                    if interfaces[index1]['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text == interfaces[index2]['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text:
                        found = True
                        vers1 = interfaces[index1]['DATA'].find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        vers2 = interfaces[index2]['DATA'].find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        vers1 = vers1.split(".")
                        vers2 = vers2.split(".")
                        if float(vers1[0]) > float(vers2[0]):
                            m_interfaces.append(interfaces[index1])
                        elif float(vers1[0]) < float(vers2[0]):
                            m_interfaces.append(interfaces[index2])
                        else:
                            m_interfaces.append(interfaces[index1])
            if found is False:
                m_interfaces.append(interfaces[index1])
        final_interfaces = list(remove_duplicates(m_interfaces))
        logger.info('=================Interfaces without PPorts/PRPorts=================')
        for interface in final_interfaces:
            found = False
            for port in provided_ports:
                if "PP_"+interface['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text == port or "PRP_"+interface['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text == port:
                    found = True
                    break
            if not found:
                logger.info("The interface " + interface['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text + " doesn't have an PPort or PRPort")
        for interface in arxml_interfaces:
            found = False
            for port in provided_ports:
                if "PP_"+interface['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text == port or "PRP_"+interface['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text == port:
                    found = True
                    break
            if not found:
                logger.info("The interface " + interface['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text + " doesn't have an PPort or PRPort")
        for index1 in range(len(types)):
            found = False
            for index2 in range(len(types)):
                if index1 != index2:
                    if types[index1]['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text == types[index2]['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text:
                        found = True
                        vers1 = types[index1]['DATA'].find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        vers2 = types[index2]['DATA'].find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        vers1 = vers1.split(".")
                        vers2 = vers2.split(".")
                        if float(vers1[0]) > float(vers2[0]):
                            m_types.append(types[index1])
                        elif float(vers1[0]) < float(vers2[0]):
                            m_types.append(types[index2])
                        else:
                            m_types.append(types[index1])
            if found is False:
                m_types.append(types[index1])
        final_types = list(remove_duplicates(m_types))
        for index1 in range(len(data_constr)):
            found = False
            for index2 in range(len(data_constr)):
                if index1 != index2:
                    if data_constr[index1]['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text == data_constr[index2]['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text:
                        found = True
                        vers1 = data_constr[index1]['DATA'].find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        vers2 = data_constr[index2]['DATA'].find(".//{http://autosar.org/schema/r4.0}REVISION-LABEL").text
                        vers1 = vers1.split(".")
                        vers2 = vers2.split(".")
                        if float(vers1[0]) > float(vers2[0]):
                            m_data_constr.append(data_constr[index1])
                        elif float(vers1[0]) < float(vers2[0]):
                            m_data_constr.append(data_constr[index2])
                        else:
                            m_data_constr.append(data_constr[index1])
            if found is False:
                m_data_constr.append(m_data_constr[index1])
        final_data_constr = list(remove_duplicates(m_data_constr))
        compu_methods = list(remove_duplicates(compu_methods))
        for elem_dico in final_interfaces[:]:
            for elem_arxml in arxml_interfaces:
                if elem_dico['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text == elem_arxml['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text:
                    if elem_dico['PACKAGE'] == elem_arxml['PACKAGE']:
                        final_interfaces.remove(elem_dico)
        final_interfaces = sorted(final_interfaces, key=lambda x: x['PACKAGE'])
        for elem_dico in final_types[:]:
            for elem_arxml in arxml_types:
                if elem_dico['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text == elem_arxml.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text:
                    final_types.remove(elem_dico)
        final_types = sorted(final_types, key=lambda x: x['PACKAGE'])
        for elem_dico in compu_methods[:]:
            for elem_arxml in arxml_compu_methods:
                if elem_dico['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text == elem_arxml.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text:
                    compu_methods.remove(elem_dico)
        compu_methods = sorted(compu_methods, key=lambda x: x['PACKAGE'])
        for elem_dico in final_data_constr[:]:
            for elem_arxml in arxml_data_constr:
                if elem_dico['DATA'].find("{http://autosar.org/schema/r4.0}SHORT-NAME").text == elem_arxml.find("{http://autosar.org/schema/r4.0}SHORT-NAME").text:
                    final_data_constr.remove(elem_dico)
        final_data_constr = sorted(final_data_constr, key=lambda x: x['PACKAGE'])

    # TRS.SYSDESC.GEN.003
    software_composition = sorted(software_composition, key=lambda x: x['NAME'])
    final_software_composition = []
    for elem in software_composition[:]:
        temp = []
        for elem2 in software_composition[:]:
            if elem['ROOT'] == elem2['ROOT']:
                if elem['NAME'] == elem2['NAME']:
                    if elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text == elem2['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text:
                        temp.append(elem2)
                        software_composition.remove(elem2)
        if len(temp) == 0:
            continue
        elif len(temp) == 1:
            objElem = {}
            objElem['ROOT'] = elem['ROOT']
            objElem['NAME'] = elem['NAME']
            objElem['DATA'] = elem['DATA']
            final_software_composition.append(objElem)
        else:
            cont = True
            compo_tref = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}TYPE-TREF').text
            for i in range(len(temp)):
                if temp[i]['DATA'].find('.//{http://autosar.org/schema/r4.0}TYPE-TREF').text != compo_tref:
                    cont = False
            if cont:
                objElem = {}
                objElem['ROOT'] = elem['ROOT']
                objElem['NAME'] = elem['NAME']
                element = etree.Element('SW-COMPONENT-PROTOTYPE', nsmap=NSMAP)
                short_name = etree.SubElement(element, 'SHORT-NAME').text = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
                software_composition_tref = etree.SubElement(element, 'TYPE-TREF')
                software_composition_tref.attrib['DEST'] = "APPLICATION-SW-COMPONENT-TYPE"
                software_composition_tref.text = compo_tref
                objElem['DATA'] = element
                final_software_composition.append(objElem)
            else:
                logger.error('SW-COMPONENT-PROTOTYPE with the short-name ' + elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text + ' cannot be merged')
                try:
                    os.remove(output_path + '/SystemGenerated.arxml')
                except OSError:
                    pass
                return
    # <DATA-MAPPINGS>
    client_server_signal_group_mapping = sorted(client_server_signal_group_mapping, key=lambda x: x['NAME'])
    client_server_signal_mapping = sorted(client_server_signal_mapping, key=lambda x: x['NAME'])
    sender_receiver_composite_element = sorted(sender_receiver_composite_element, key=lambda x: x['NAME'])
    sender_receiver_signal_group_mapping = sorted(sender_receiver_signal_group_mapping, key=lambda x: x['NAME'])
    sender_receiver_signal_mapping = sorted(sender_receiver_signal_mapping, key=lambda x: x['NAME'])
    trigger_signal_mapping = sorted(trigger_signal_mapping, key=lambda x: x['NAME'])
    [data_mappings_name.append(elem['NAME']) for elem in client_server_signal_group_mapping if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in client_server_signal_mapping if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in sender_receiver_composite_element if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in sender_receiver_signal_group_mapping if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in sender_receiver_signal_mapping if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in trigger_signal_mapping if elem['NAME'] not in data_mappings_name]
    # <ECU-RESOURCE-MAPPINGS>
    ecu_mapping = sorted(ecu_mapping, key=lambda x: x['NAME'])
    [data_mappings_name.append(elem['NAME']) for elem in ecu_mapping if elem['NAME'] not in data_mappings_name]
    # <MAPPING-CONSTRAINTS>
    component_clustering = sorted(component_clustering, key=lambda x: x['NAME'])
    component_separation = sorted(component_separation, key=lambda x: x['NAME'])
    sw_ecu_mapping_constraint = sorted(sw_ecu_mapping_constraint, key=lambda x: x['NAME'])
    [data_mappings_name.append(elem['NAME']) for elem in component_clustering if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in component_separation if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in sw_ecu_mapping_constraint if elem['NAME'] not in data_mappings_name]
    # <PNC-MAPPINGS>
    pnc_mapping = sorted(pnc_mapping, key=lambda x: x['NAME'])
    [data_mappings_name.append(elem['NAME']) for elem in pnc_mapping if elem['NAME'] not in data_mappings_name]
    # <RESOURCE-ESTIMATIONS>
    ecu_resource_estimation = sorted(ecu_resource_estimation, key=lambda x: x['NAME'])
    [data_mappings_name.append(elem['NAME']) for elem in ecu_resource_estimation if elem['NAME'] not in data_mappings_name]
    # <SIGNAL-PATH-CONSTRAINTS>
    common_signal_path = sorted(common_signal_path, key=lambda x: x['NAME'])
    forbidden_signal_path = sorted(forbidden_signal_path, key=lambda x: x['NAME'])
    permissible_signal_path = sorted(permissible_signal_path, key=lambda x: x['NAME'])
    separate_signal_path = sorted(separate_signal_path, key=lambda x: x['NAME'])
    [data_mappings_name.append(elem['NAME']) for elem in common_signal_path if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in forbidden_signal_path if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in permissible_signal_path if elem['NAME'] not in data_mappings_name]
    [data_mappings_name.append(elem['NAME']) for elem in separate_signal_path if elem['NAME'] not in data_mappings_name]
    # <SW-IMPL-MAPPINGS>
    sw_impl_mappings = sorted(sw_impl_mappings, key=lambda x: x['NAME'])
    final_sw_impl_mapping = []
    for elem in sw_impl_mappings[:]:
        temp = []
        ref = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
        for elem2 in sw_impl_mappings[:]:
            if elem2['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text == ref:
                temp.append(elem2)
                sw_impl_mappings.remove(elem2)
        if len(temp) == 0:
            continue
        elif len(temp) == 1:
            objElem = {}
            objElem['ROOT'] = elem['ROOT']
            objElem['SYSTEM'] = elem['SYSTEM']
            objElem['NAME'] = elem['NAME']
            objElem['DATA'] = elem['DATA']
            final_sw_impl_mapping.append(objElem)
        else:
            cont = True
            ecu_instance = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}COMPONENT-IMPLEMENTATION-REF').text
            for i in range(len(temp)):
                if temp[i]['DATA'].find('.//{http://autosar.org/schema/r4.0}COMPONENT-IMPLEMENTATION-REF').text != ecu_instance:
                    cont = False
            if cont:
                objElem = {}
                objElem['ROOT'] = elem['ROOT']
                objElem['SYSTEM'] = elem['SYSTEM']
                objElem['NAME'] = elem['NAME']
                element = etree.Element('SWC-TO-ECU-MAPPING', nsmap=NSMAP)
                short_name = etree.SubElement(element, 'SHORT-NAME').text = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
                component_irefs = etree.SubElement(element, 'COMPONENT-IREFS')
                for item in range(len(temp)):
                    tag = temp[item]['DATA'].findall('.//{http://autosar.org/schema/r4.0}COMPONENT-IREF')
                    for instance in range(len(tag)):
                        component_irefs.append(tag[instance])
                component_implementation_ref = etree.SubElement(element, 'COMPONENT-IMPLEMENTATION-REF')
                component_implementation_ref.attrib['DEST'] = "SWC-IMPLEMENTATION"
                component_implementation_ref.text = temp[item]['DATA'].find('.//{http://autosar.org/schema/r4.0}COMPONENT-IMPLEMENTATION-REF').text
                objElem['DATA'] = element
                final_sw_impl_mapping.append(objElem)
            else:
                logger.error('SWC-TO-IMPL-MAPPING with the short-name ' + elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text + ' cannot be merged')
                try:
                    os.remove(output_path + '/SystemGenerated.arxml')
                except OSError:
                    pass
                return
    [data_mappings_name.append(elem['NAME']) for elem in final_sw_impl_mapping if elem['NAME'] not in data_mappings_name]
    # <SW-MAPPINGS>
    swc_ecu_mapping = sorted(swc_ecu_mapping, key=lambda x: x['NAME'])
    final_swc_ecu_mappings = []
    for elem in swc_ecu_mapping[:]:
        temp = []
        ref = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
        for elem2 in swc_ecu_mapping[:]:
            if elem2['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text == ref:
                temp.append(elem2)
                swc_ecu_mapping.remove(elem2)
        if len(temp) == 0:
            continue
        elif len(temp) == 1:
            objElem = {}
            objElem['ROOT'] = elem['ROOT']
            objElem['SYSTEM'] = elem['SYSTEM']
            objElem['NAME'] = elem['NAME']
            objElem['DATA'] = elem['DATA']
            final_swc_ecu_mappings.append(objElem)
        else:
            cont = True
            ecu_instance = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}ECU-INSTANCE-REF').text
            for index in range(len(temp)):
                if temp[index]['DATA'].find('.//{http://autosar.org/schema/r4.0}ECU-INSTANCE-REF').text != ecu_instance:
                    cont = False
            if cont:
                objElem = {}
                objElem['ROOT'] = elem['ROOT']
                objElem['SYSTEM'] = elem['SYSTEM']
                objElem['NAME'] = elem['NAME']
                element = etree.Element('SWC-TO-ECU-MAPPING', nsmap=NSMAP)
                short_name = etree.SubElement(element, 'SHORT-NAME').text = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
                component_irefs = etree.SubElement(element, 'COMPONENT-IREFS')
                for i in range(len(temp)):
                    tag = temp[i]['DATA'].findall('.//{http://autosar.org/schema/r4.0}COMPONENT-IREF')
                    for instance in range(len(tag)):
                        component_irefs.append(tag[instance])
                instance_ref = etree.SubElement(element, 'ECU-INSTANCE-REF')
                instance_ref.attrib['DEST'] = "ECU-INSTANCE"
                instance_ref.text = temp[i]['DATA'].find('.//{http://autosar.org/schema/r4.0}ECU-INSTANCE-REF').text
                objElem['DATA'] = element
                final_swc_ecu_mappings.append(objElem)
            else:
                logger.error('SWC-TO-ECU-MAPPING with the short-name ' + elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text + ' cannot be merged')
                try:
                    os.remove(output_path + '/SystemGenerated.arxml')
                except OSError:
                    pass
                return
    [data_mappings_name.append(elem['NAME']) for elem in final_swc_ecu_mappings if elem['NAME'] not in data_mappings_name]
    # <FIBEX-ELEMENTS>
    fibex_elements = sorted(fibex_elements, key=lambda x: x['SYSTEM'])
    # <SYSTEM-VERSION>
    system_version = sorted(system_version, key=lambda x: x['SYSTEM'])
    final_system_version = []
    temp_system_version = []
    for elem in range(len(system_version)):
        version = system_version[elem]['DATA']
        for elem2 in range(len(system_version)):
            if elem != elem2:
                if system_version[elem]['ROOT'] == system_version[elem2]['ROOT']:
                    if system_version[elem]['SYSTEM'] == system_version[elem2]['SYSTEM']:
                        if version != system_version[elem2]['DATA']:
                            logger.error(
                                'Multiple <SYSTEM-VERSION> values: ' + version + ' <-> ' + system_version[elem2]['DATA'] + " for " +
                                system_version[elem]['ROOT'] + '/' + system_version[elem]['SYSTEM'])
                            try:
                                os.remove(output_path + '/SystemGenerated.arxml')
                            except OSError:
                                pass
                            return
                        else:
                            temp_system_version.append(system_version[elem])
    [final_system_version.append(elem) for elem in temp_system_version if elem not in final_system_version]
    # <ROOT-SOFTWARE-COMPOSITIONS>
    root_software_composition = sorted(root_software_composition, key=lambda x: x['SYSTEM'])
    final_root_software_composition = []
    for elem in root_software_composition[:]:
        temp = []
        for elem2 in root_software_composition[:]:
            if elem['ROOT'] == elem2['ROOT']:
                if elem['SYSTEM'] == elem2['SYSTEM']:
                    if elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text == elem2['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text:
                        temp.append(elem2)
                        root_software_composition.remove(elem2)
        if len(temp) == 0:
            continue
        elif len(temp) == 1:
            objElem = {}
            objElem['ROOT'] = elem['ROOT']
            objElem['SYSTEM'] = elem['SYSTEM']
            objElem['DATA'] = elem['DATA']
            final_root_software_composition.append(objElem)
        else:
            cont = True
            compo_tref = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SOFTWARE-COMPOSITION-TREF').text
            for i in range(len(temp)):
                if temp[i]['DATA'].find('.//{http://autosar.org/schema/r4.0}SOFTWARE-COMPOSITION-TREF').text != compo_tref:
                    cont = False
            if cont:
                objElem = {}
                objElem['ROOT'] = elem['ROOT']
                objElem['SYSTEM'] = elem['SYSTEM']
                element = etree.Element('ROOT-SW-COMPOSITION-PROTOTYPE', nsmap=NSMAP)
                short_name = etree.SubElement(element, 'SHORT-NAME').text = elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
                software_composition_tref = etree.SubElement(element, 'SOFTWARE-COMPOSITION-TREF')
                software_composition_tref.attrib['DEST'] = "COMPOSITION-SW-COMPONENT-TYPE"
                software_composition_tref.text = compo_tref
                objElem['DATA'] = element
                final_root_software_composition.append(objElem)
            else:
                logger.error('ROOT-SW-COMPOSITION-PROTOTYPE with the short-name ' + elem['DATA'].find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text + ' cannot be merged')
                try:
                    os.remove(output_path + '/SystemGenerated.arxml')
                except OSError:
                    pass
                return

    # create arxml file
    rootSystem = etree.Element('AUTOSAR', {attr_qname: 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd'}, nsmap=NSMAP)
    packages = etree.SubElement(rootSystem, 'AR-PACKAGES')
    package = ""
    if modularity:
        for elem in final_interfaces:
            if package != elem['PACKAGE']:
                package = elem['PACKAGE']
                compo = etree.SubElement(packages, 'AR-PACKAGE')
                short_name = etree.SubElement(compo, 'SHORT-NAME').text = elem['PACKAGE']
                elements = etree.SubElement(compo, 'ELEMENTS')
                elements.append(elem['DATA'])
            else:
                elements.append(elem['DATA'])
        for elem in final_types:
            if package != elem['PACKAGE']:
                package = elem['PACKAGE']
                compo = etree.SubElement(packages, 'AR-PACKAGE')
                short_name = etree.SubElement(compo, 'SHORT-NAME').text = elem['PACKAGE']
                elements = etree.SubElement(compo, 'ELEMENTS')
                elements.append(elem['DATA'])
            else:
                elements.append(elem['DATA'])
        for elem in compu_methods:
            if package != elem['PACKAGE']:
                package = elem['PACKAGE']
                compo = etree.SubElement(packages, 'AR-PACKAGE')
                short_name = etree.SubElement(compo, 'SHORT-NAME').text = elem['PACKAGE']
                elements = etree.SubElement(compo, 'ELEMENTS')
                elements.append(elem['DATA'])
            else:
                elements.append(elem['DATA'])
        for elem in final_data_constr:
            if package != elem['PACKAGE']:
                package = elem['PACKAGE']
                compo = etree.SubElement(packages, 'AR-PACKAGE')
                short_name = etree.SubElement(compo, 'SHORT-NAME').text = elem['PACKAGE']
                elements = etree.SubElement(compo, 'ELEMENTS')
                elements.append(elem['DATA'])
            else:
                elements.append(elem['DATA'])
    package = ""
    if system_name != "":
        for elem in system_version:
            if package != elem['ROOT']:
                temp_fibex = []
                temp_root = []
                package = elem['ROOT']
                system_list = []
                component = etree.SubElement(packages, 'AR-PACKAGE')
                short_name = etree.SubElement(component, 'SHORT-NAME').text = elem['ROOT']
                elements_tag = etree.SubElement(component, 'ELEMENTS')
                for elem2 in fibex_elements:
                    if elem2['ROOT'] == package:
                        temp_fibex.append(elem2)
                for elem2 in final_root_software_composition:
                    if elem2['ROOT'] == package:
                        temp_root.append(elem2)
                [system_list.append(elem['SYSTEM']) for elem in temp_root if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in temp_fibex if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in client_server_signal_group_mapping if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in client_server_signal_mapping if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in sender_receiver_composite_element if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in sender_receiver_signal_group_mapping if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in sender_receiver_signal_mapping if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in trigger_signal_mapping if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in swc_ecu_mapping if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in component_clustering if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in component_separation if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in sw_ecu_mapping_constraint if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in pnc_mapping if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in ecu_resource_estimation if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in common_signal_path if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in forbidden_signal_path if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in permissible_signal_path if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in separate_signal_path if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in final_swc_ecu_mappings if elem['SYSTEM'] not in system_list]
                [system_list.append(elem['SYSTEM']) for elem in final_sw_impl_mapping if elem['SYSTEM'] not in system_list]
                for sysname in system_list:
                    if sysname == system_name:
                        system_tag = etree.SubElement(elements_tag, 'SYSTEM')
                        short_name_system = etree.SubElement(system_tag, 'SHORT-NAME').text = sysname
                        for elem_fibex in temp_fibex:
                            if sysname == elem_fibex['SYSTEM']:
                                system_tag.append(elem_fibex['DATA'])
                        mappings_tag = etree.SubElement(system_tag, 'MAPPINGS')
                        if mapping_name != "":
                            for elem in data_mappings_name:
                                if elem == mapping_name:
                                    system_mapping_tag = etree.SubElement(mappings_tag, 'SYSTEM-MAPPING')
                                    short_name_mappings = etree.SubElement(system_mapping_tag, 'SHORT-NAME').text = str(elem)
                                    data_mappings_tag = etree.SubElement(system_mapping_tag, 'DATA-MAPPINGS')
                                    for element in client_server_signal_group_mapping:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            data_mappings_tag.append(element['DATA'])
                                    for element in client_server_signal_mapping:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            data_mappings_tag.append(element['DATA'])
                                    for element in sender_receiver_composite_element:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            data_mappings_tag.append(element['DATA'])
                                    for element in sender_receiver_signal_group_mapping:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            data_mappings_tag.append(element['DATA'])
                                    for element in sender_receiver_signal_mapping:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            data_mappings_tag.append(element['DATA'])
                                    for element in trigger_signal_mapping:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            data_mappings_tag.append(element['DATA'])
                                    ecu_mappings_tag = etree.SubElement(system_mapping_tag, 'ECU-RESOURCE-MAPPINGS')
                                    for element in swc_ecu_mapping:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            ecu_mappings_tag.append(element['DATA'])
                                    mapping_constraints_tag = etree.SubElement(system_mapping_tag, 'MAPPING-CONSTRAINTS')
                                    for element in component_clustering:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            mapping_constraints_tag.append(element['DATA'])
                                    for element in component_separation:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            mapping_constraints_tag.append(element['DATA'])
                                    for element in sw_ecu_mapping_constraint:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            mapping_constraints_tag.append(element['DATA'])
                                    pnc_mapping_tag = etree.SubElement(system_mapping_tag, 'PNC-MAPPINGS')
                                    for element in pnc_mapping:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            pnc_mapping_tag.append(element['DATA'])
                                    resource_estimation_tag = etree.SubElement(system_mapping_tag, 'RESOURCE-ESTIMATIONS')
                                    for element in ecu_resource_estimation:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            resource_estimation_tag.append(element['DATA'])
                                    signal_path_constraints_tag = etree.SubElement(system_mapping_tag, 'SIGNAL-PATH-CONSTRAINTS')
                                    for element in common_signal_path:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            signal_path_constraints_tag.append(element['DATA'])
                                    for element in forbidden_signal_path:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            signal_path_constraints_tag.append(element['DATA'])
                                    for element in permissible_signal_path:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            signal_path_constraints_tag.append(element['DATA'])
                                    for element in separate_signal_path:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            signal_path_constraints_tag.append(element['DATA'])
                                    sw_impl_mappings_tag = etree.SubElement(system_mapping_tag, 'SW-IMPL-MAPPINGS')
                                    for element in final_sw_impl_mapping:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            sw_impl_mappings_tag.append(element['DATA'])
                                    sw_mappings_tag = etree.SubElement(system_mapping_tag, 'SW-MAPPINGS')
                                    for element in final_swc_ecu_mappings:
                                        if element['NAME'] == elem and element['ROOT'] == package and element['SYSTEM'] == sysname:
                                            sw_mappings_tag.append(element['DATA'])
                        rsc = etree.SubElement(system_tag, 'ROOT-SOFTWARE-COMPOSITIONS')
                        for elem_root in temp_root:
                            if sysname == elem_root['SYSTEM']:
                                rsc.append(elem_root['DATA'])
                        for elem_version in final_system_version:
                            if elem_version['ROOT'] == package:
                                if elem_version['SYSTEM'] == sysname:
                                    version = etree.Element('SYSTEM-VERSION', nsmap=NSMAP)
                                    version.text = elem_version['DATA']
                                    system_tag.append(version)
    package = ""
    if composition_name != "":
        for elem in final_software_composition:
            if package != elem['ROOT']:
                temp = []
                package = elem['ROOT']
                component = etree.SubElement(packages, 'AR-PACKAGE')
                short_name = etree.SubElement(component, 'SHORT-NAME').text = elem['ROOT']
                elements_tag = etree.SubElement(component, 'ELEMENTS')
                for elem2 in final_software_composition:
                    if elem2['ROOT'] == package:
                        temp.append(elem2)
                temp = sorted(temp, key=lambda x: x['NAME'])
                compo = composition_name
                composition_sw_tag = etree.SubElement(elements_tag, 'COMPOSITION-SW-COMPONENT-TYPE')
                short_name_compo = etree.SubElement(composition_sw_tag, 'SHORT-NAME').text = composition_name
                components_tag = etree.SubElement(composition_sw_tag, 'COMPONENTS')
                for element in temp:
                    if compo == element['NAME']:
                        components_tag.append(element['DATA'])
    pretty_xml = new_prettify(rootSystem)
    output = etree.ElementTree(etree.fromstring(pretty_xml))
    output.write(output_path + '/SystemGenerated.arxml', encoding='UTF-8', xml_declaration=True, method="xml")
    logger.info('=================Output file information=================')
    if xmlschema_arxml.validate(etree.parse(output_path + '/SystemGenerated.arxml')) is not True:
        logger.warning('The file: ' + 'SystemGenerated.arxml' + ' is NOT valid with the provided xsd schema')
    else:
        logger.info('The file: ' + 'SystemGenerated.arxml' + ' is valid with the provided xsd schema')


def main():
    # get the command-line parameter
    parser = argparse.ArgumentParser()
    arg_parse(parser)
    args = parser.parse_args()
    config_file = args.config
    system_name = ""
    composition_name = ""
    mapping_name = ""
    modularity = False
    if args.system:
        system_name = args.system
    if args.mapping:
        mapping_name = args.mapping
    if args.compo:
        composition_name = args.compo
    if args.modularity:
        modularity = True
    config_file = config_file.replace("\\", "/")
    # get all configuration parameters
    recursive_path_arxml = []
    simple_path_arxml = []
    recursive_path_dico = []
    simple_path_dico = []
    tree = etree.parse(config_file)
    root = tree.getroot()
    directories = root.findall(".//DIR")
    sys_path = report_path = ""
    for element in directories:
        if element.getparent().tag == "ARXML":
            if element.attrib['RECURSIVE'] == "true":
                recursive_path_arxml.append(element.text)
            else:
                simple_path_arxml.append(element.text)
        elif element.getparent().tag == "DICO":
            if element.attrib['RECURSIVE'] == "true":
                recursive_path_dico.append(element.text)
            else:
                simple_path_dico.append(element.text)
        elif element.getparent().tag == "SYS_ARXML":
            sys_path = element.text
        elif element.getparent().tag == "REPORT":
            report_path = element.text
    xsd_path = root.find(".//FILE_PATH").text
    # logger creation and setting
    logger = logging.getLogger('result')
    hdlr = logging.FileHandler(report_path + '/result.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    open(report_path + '/result.log', 'w').close()
    # function calls: create systemDescriptor
    generation = True
    if modularity:
        generation = check_compatibility(recursive_path_dico, simple_path_dico, logger)
    if generation:
        generate_system(recursive_path_arxml, recursive_path_dico, simple_path_arxml, simple_path_dico, sys_path, xsd_path, system_name, mapping_name, composition_name, modularity, logger)


def check_xml_wellformed(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)


if __name__ == "__main__":
    main()
