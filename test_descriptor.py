import unittest
import os
import os.path
import ntpath
import HtmlTestRunner
from lxml import etree


class FileCompare():
    def areSame(first_location, second_location):
        file1 = open(first_location)
        file2 = open(second_location)

        line_file1 = file1.readline()
        line_file2 = file2.readline()

        while line_file1 != "" or line_file2 != "":
            line_file1 = line_file1.rstrip()
            line_file1 = line_file1.lstrip()
            line_file2 = line_file2.rstrip()
            line_file2 = line_file2.lstrip()
            if line_file1 != line_file2:
                return False
            line_file1 = file1.readline()
            line_file2 = file2.readline()

        file1.close()
        file2.close()
        return True

    def matchLine(path, line_number, text):
        """
        path = used for defining the file to be checked
        line_number = used to identify the line that will be checked
        text = string containing the text to match
        """
        datafile = open(path)
        line_file = datafile.readline()
        line_file = line_file.rstrip()
        line_no = 1
        while line_file != "":
            if line_no == line_number:
                if line_file == text:
                    return True
                else:
                    return False
            line_no = line_no+1
            line_file = datafile.readline()
            line_file = line_file.rstrip()

    def checkLog(path, level, message):
        """
        path = used for defining the file to be checked
        level = criticity level :INFO, WARNING, ERROR
        message = string to be matched
        """
        datafile = open(path)
        line_file = datafile.readline()
        while line_file != "":
            for text in message:
                if level in line_file:
                    if text in line_file:
                        # print(line_file)
                        return True
            line_file = datafile.readline()
        return False

    def checkParsing(path1, path2, message, extension):
        """
        path1 = used for taking the .arxml files name
        path2 = used for defining the file to be checked
        message = string to be matched
        extension = the file extension
        """
        all_files = []
        found_files = []
        for file in os.listdir(path1):
            if file.endswith(extension):
                all_files.append(file)
        for file in all_files:
            found_files.append(False)
        datafile = open(path2)
        line_file = datafile.readline()
        i = 0
        while line_file != "":
            for files in all_files:
                if files + " " + message in line_file:
                    found_files[i] = True
                    i = i + 1
            line_file = datafile.readline()
        for item in found_files:
            if item == False:
                return False
        return True

    def findParam(path, tag, name):
        """
        path = used for defining the file to be checked
        tag = used for defining the tag name (SYSTEM, MAPPINGS, COMPOSITION-SW-COMPONENT-TYPE)
        name = used for deifning the tag short-name
        """
        tree = etree.parse(path)
        root = tree.getroot()
        param = root.find('.//{http://autosar.org/schema/r4.0}' + tag)
        if param is not None:
            for elem in param:
                if elem.tag == '{http://autosar.org/schema/r4.0}SHORT-NAME':
                    if name in elem.text:
                        return True
                else:
                    return False
        else:
            return False

    def checkInterfaces(path):
        """
        path = used for defining the file to be checked
        """
        list = []
        tree = etree.parse(path)
        root = tree.getroot()
        interfaces = ['NV-DATA-INTERFACE', 'SENDER-RECEIVER-INTERFACE', 'CLIENT-SERVER-INTERFACE', 'MODE-SWITCH-INTERFACE']
        for elem in interfaces:
            param = root.find('.//{http://autosar.org/schema/r4.0}' + elem)
            if param is not None:
                list.append(True)
            else:
                list.append(False)
        if True in (elem for elem in list):
            return True
        else:
            return False

    def isOutput(path):
        """
        path = used for defining the file folder to be checked
        """
        if os.path.isfile(path):
            return True
        else:
            return False


class SystemDescriptor(unittest.TestCase):

    def test_TRS_SYSDESC_FUNC_002_01(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_01\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_01\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_01\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_01\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_FUNC_002_02(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_02\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_02\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.FUNC.002_02\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.FUNC.002_02\\output\\result_SysDesc.log', "ERROR", ["SR_ApportCarbDetecteTest has different versions"]))

    def test_TRS_SYSDESC_FUNC_002_03(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_03\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_03\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_03\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_03\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_FUNC_002_04(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_04\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_04\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.FUNC.002_04\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.FUNC.002_04\\output\\result_SysDesc.log', "ERROR", ["The type: tBinaire"]))

    def test_TRS_SYSDESC_FUNC_002_05(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_05\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_05\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_05\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_05\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_FUNC_002_06(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_06\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_06\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_06\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_06\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_FUNC_002_07(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_07\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_07\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_07\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_07\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_FUNC_002_08(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_08\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_08\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_08\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_08\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_002_01(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.GEN.002_01\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.GEN.002_01\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.GEN.002_01\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.GEN.002_01\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_002_02(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.GEN.002_02\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.GEN.002_02\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.GEN.002_02\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.GEN.002_02\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_001(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.GEN.001\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.GEN.001\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.matchLine(head+'\\tests\TRS.SYSDESC.GEN.001\output\SystemGenerated.arxml', 1, "<?xml version='1.0' encoding='UTF-8'?>"))
        self.assertTrue(FileCompare.matchLine(head+'\\tests\TRS.SYSDESC.GEN.001\output\SystemGenerated.arxml', 2, '<AUTOSAR xmlns="http://autosar.org/schema/r4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd">'))

    def test_TRS_SYSDESC_FUNC_006_01(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.FUNC.006_01\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_FUNC_006_02(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_02\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_02\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.findParam(head+'\\Tests\\TRS.SYSDESC.GEN.003_2\\Output\\SystemGenerated.arxml', 'SYSTEM', 'VSM_System'))

    def test_TRS_SYSDESC_FUNC_006_03(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_03\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_03\\Output -compo /RootP_Composition/Compo_VSM -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.findParam(head + '\\Tests\\TRS.SYSDESC.FUNC.006_03\\Output\\SystemGenerated.arxml', 'SYSTEM', 'VSM_System'))

    def test_TRS_SYSDESC_FUNC_006_04(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_04\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_04\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.findParam(head + '\\Tests\\TRS.SYSDESC.FUNC.006_04\\Output\\SystemGenerated.arxml', 'SYSTEM-MAPPING', 'SystemMapping'))

    def test_TRS_SYSDESC_FUNC_006_05(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_05\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_05\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -modularity')
        self.assertFalse(FileCompare.findParam(head + '\\Tests\\TRS.SYSDESC.FUNC.006_05\\Output\\SystemGenerated.arxml', 'SYSTEM-MAPPING', 'SystemMapping'))

    def test_TRS_SYSDESC_FUNC_006_06(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_06\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_06\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.findParam(head + '\\Tests\\TRS.SYSDESC.FUNC.006_06\\Output\\SystemGenerated.arxml', 'COMPOSITION-SW-COMPONENT-TYPE', 'Compo_VSM'))

    def test_TRS_SYSDESC_FUNC_006_07(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_07\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_07\\Output -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.findParam(head + '\\Tests\\TRS.SYSDESC.FUNC.006_07\\Output\\SystemGenerated.arxml', 'COMPOSITION-SW-COMPONENT-TYPE', 'Compo_VSM'))

    def test_TRS_SYSDESC_FUNC_006_08(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_08\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_08\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.checkInterfaces(head + '\\Tests\\TRS.SYSDESC.FUNC.006_08\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_FUNC_006_09(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_09\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.FUNC.006_09\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping')
        self.assertFalse(FileCompare.checkInterfaces(head + '\\Tests\\TRS.SYSDESC.FUNC.006_09\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_INOUT_001(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.INOUT.001\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.INOUT.001\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.checkParsing(head + '\\Tests\\TRS.SYSDESC.INOUT.001\input', head + '\\Tests\\TRS.SYSDESC.INOUT.001\output\\result_SysDesc.log', "is well", ".arxml"))

    def test_TRS_SYSDESC_INOUT_002(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.INOUT.002\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.INOUT.002\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.checkParsing(head + '\\Tests\\TRS.SYSDESC.INOUT.002\Input', head + '\\Tests\\TRS.SYSDESC.INOUT.002\output\\result_SysDesc.log', "is well", ".dico"))

    def test_TRS_SYSDESC_INOUT_100(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.SYSDESC.INOUT.100\\Input -out ' + head + '\\Tests\\TRS.SYSDESC.INOUT.100\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.INOUT.100\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_02(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_2\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_2\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_2\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_2\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_04(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_4\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_4\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_4\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_4\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_05(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_5\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_5\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_5\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_5\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_06(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_6\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_6\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.GEN.003_6\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.GEN.003_6\\output\\result_SysDesc.log', "ERROR", ["SWC-TO-ECU-MAPPING"]))

    def test_TRS_SYSDESC_GEN_003_07(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_7\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_7\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_7\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_7\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_08(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_8\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_8\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_8\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_8\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_09(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_9\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_9\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_9\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_9\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_10(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_10\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_10\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.GEN.003_10\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.GEN.003_10\\output\\result_SysDesc.log', "ERROR", ["SW-COMPONENT-PROTOTYPE"]))

    def test_TRS_SYSDESC_GEN_003_11(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_11\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_11\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_11\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_11\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_12(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_12\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_12\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_12\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_12\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_13(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_13\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_13\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_13\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.003_13\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_003_14(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.003_14\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.003_14\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.GEN.003_14\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.GEN.003_14\\output\\result_SysDesc.log', "ERROR", ["ROOT-SW-COMPOSITION-PROTOTYPE"]))

    def test_TRS_SYSDESC_GEN_004_1(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.004_1\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.004_1\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping_ASWC_A26 -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.004_1\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.004_1\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_GEN_004_2(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.GEN.004_2\\Input -out ' + head + '\\Tests\TRS.SYSDESC.GEN.004_2\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping_ASWC_A26 -modularity')
        self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.004_2\\SystemGenerated.arxml', head + '\\Tests\\TRS.SYSDESC.GEN.004_2\\Output\\SystemGenerated.arxml'))

    def test_TRS_SYSDESC_FUNC_200_1(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.FUNC.200_1\\Input -out ' + head + '\\Tests\TRS.SYSDESC.FUNC.200_1\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.FUNC.200_1\\output\\result_SysDesc.log', "INFO", ["SR_ApportCarbDetecteTest"]))

    def test_TRS_SYSDESC_FUNC_200_2(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.FUNC.200_2\\Input -out ' + head + '\\Tests\TRS.SYSDESC.FUNC.200_2\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.FUNC.200_2\\output\\result_SysDesc.log', "INFO", ["SENDER-RECEIVER-TO-SIGNAL-MAPPING using the signal/RootP_NetworkDesc/AUTONOMIE_HS1_52E"]))

    def test_TRS_SYSDESC_1(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.1\\Input -out ' + head + '\\Tests\TRS.SYSDESC.1\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.1\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.1\\output\\result_SysDesc.log', "ERROR", ["ASWC_A26.aswc.arxml"]))

    def test_TRS_SYSDESC_2(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\TRS.SYSDESC.2\\Input -out ' + head + '\\Tests\TRS.SYSDESC.2\\Output -compo /RootP_Composition/Compo_VSM -system VSM_System -mapping /RootP_NetworkDesc/VSM_System/SystemMapping -modularity')
        self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.2\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.2\\output\\result_SysDesc.log', "ERROR", ["ASWC_A26.mappings1.dico"]))

    def test_TRS_DIAGNOSTIC_MERGE_01(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.1\Input -out ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.1\Output -service_table')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.DIAGNOSTIC.MERGE.1\\SystemGenerated.arxml', head+'\\Tests\\TRS.DIAGNOSTIC.MERGE.1\\Output\\SystemGenerated.arxml'))

    def test_TRS_DIAGNOSTIC_MERGE_02(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.2\Input -out ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.2\Output -service_table')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.DIAGNOSTIC.MERGE.2\\SystemGenerated.arxml', head+'\\Tests\\TRS.DIAGNOSTIC.MERGE.2\\Output\\SystemGenerated.arxml'))

    def test_TRS_DIAGNOSTIC_MERGE_03(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.3\Input -out ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.3\Output -service_table')
        self.assertFalse(FileCompare.isOutput(head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.3\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.3\\output\\result_SysDesc.log', "ERROR", ["VSM_ServicesTable"]))

    def test_TRS_DIAGNOSTIC_MERGE_04(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.4\Input -out ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.4\Output -service_table')
        self.assertFalse(FileCompare.isOutput(head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.4\\Output\\SystemGenerated.arxml'))
        self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.4\\output\\result_SysDesc.log', "ERROR", ["VSM_ServicesTable"]))

    def test_TRS_DIAGNOSTIC_MERGE_05(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.5\Input -out ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.5\Output -service_table')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.DIAGNOSTIC.MERGE.5\\SystemGenerated.arxml', head+'\\Tests\\TRS.DIAGNOSTIC.MERGE.5\\Output\\SystemGenerated.arxml'))

    def test_TRS_DIAGNOSTIC_MERGE_06(self):
        current_path = os.path.realpath(__file__)
        head, tail = ntpath.split(current_path)
        os.system('SystemDescriptor.py -in ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.6\\Input -out ' + head + '\\Tests\\TRS.DIAGNOSTIC.MERGE.6\\Output -service_table')
        self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.DIAGNOSTIC.MERGE.6\\SystemGenerated.arxml', head+'\\Tests\\TRS.DIAGNOSTIC.MERGE.6\\Output\\SystemGenerated.arxml'))


suite = unittest.TestLoader().loadTestsFromTestCase(SystemDescriptor)
unittest.TextTestRunner(verbosity=2).run(suite)

# current_path = os.path.realpath(__file__)
# head, tail = ntpath.split(current_path)
# if __name__ == "__main__":
#     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=head + "\\tests"))
