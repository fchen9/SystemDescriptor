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

    # def checkLog(path, level, message):
    #     """
    #     path = used for defining the file to be checked
    #     level = criticity level :INFO, WARNING, ERROR
    #     message = string to be matched
    #     """
    #     datafile = open(path)
    #     line_file = datafile.readline()
    #     bool_message = []
    #     for elem in message:
    #         bool_message.append(False)
    #     i = 0
    #     while line_file != "":
    #         for text in message:
    #             if level in line_file:
    #                 if text in line_file:
    #                     # print(line_file)
    #                     bool_message[i] = True
    #                     i = i + 1
    #         line_file = datafile.readline()
    #     for elem in bool_message:
    #         if elem == False:
    #             return False
    #     return True

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

    def isConnector(path):
        """
        path = used for defining the file to be checked
        """
        tree = etree.parse(path)
        root = tree.getroot()
        found_name = found_provider = found_requester = found_contextP = found_targetP = found_contextR =found_targetR = False
        connectors = root.findall(".//{http://autosar.org/schema/r4.0}ASSEMBLY-SW-CONNECTOR")
        for elem in connectors:
            for c in elem:
                if c.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME":
                    found_name = True
                if c.tag == "{http://autosar.org/schema/r4.0}PROVIDER-IREF":
                    found_provider = True
                    provider = elem.find(".//{http://autosar.org/schema/r4.0}PROVIDER-IREF")
                    for child in provider:
                        if child.tag == "{http://autosar.org/schema/r4.0}CONTEXT-COMPONENT-REF":
                            found_contextP = True
                        if child.tag == "{http://autosar.org/schema/r4.0}TARGET-P-PORT-REF":
                            found_targetP = True
                if c.tag == "{http://autosar.org/schema/r4.0}REQUESTER-IREF":
                    found_requester = True
                    requester = elem.find(".//{http://autosar.org/schema/r4.0}REQUESTER-IREF")
                    for child in requester:
                        if child.tag == "{http://autosar.org/schema/r4.0}CONTEXT-COMPONENT-REF":
                            found_contextR = True
                        if child.tag == "{http://autosar.org/schema/r4.0}TARGET-R-PORT-REF":
                            found_targetR = True

        if found_name and found_provider and found_requester and found_contextP and found_targetP and found_contextR and found_targetR:
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

    # def test_TRS_SYSDESC_FUNC_002_01(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_01\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_01\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_01\\Output\\SystemGenerated.arxml'))
    # #
    # def test_TRS_SYSDESC_FUNC_002_02(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_02\\ConfigSystemDescriptor.xml')
    #     self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.FUNC.002_02\\Output\\SystemGenerated.arxml'))
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.FUNC.002_02\\output\\result.log', "ERROR", ["SR_ApportCarbDetecteTest has different versions"]))
    #
    # def test_TRS_SYSDESC_FUNC_002_03(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_03\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_03\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_03\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_FUNC_002_04(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_04\\ConfigSystemDescriptor.xml')
    #     self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.FUNC.002_04\\Output\\SystemGenerated.arxml'))
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.FUNC.002_04\\output\\result.log', "ERROR", ["The interface: tBinaire"]))

    # def test_TRS_SYSDESC_FUNC_002_05(self):   ##############
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_05\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_05\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_05\\Output\\SystemGenerated.arxml'))

    # def test_TRS_SYSDESC_FUNC_002_07(self):   ##############
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.FUNC.002_07\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.FUNC.002_07\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.FUNC.002_07\\Output\\SystemGenerated.arxml'))



    # def test_TRS_SYSDESC_GEN_002_01(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.GEN.002_01\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.GEN.002_01\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.GEN.002_01\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_GEN_002_02(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.GEN.002_02\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head+'\\Tests\\TRS.SYSDESC.GEN.002_02\\SystemGenerated.arxml', head+'\\Tests\\TRS.SYSDESC.GEN.002_02\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_GEN_001(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.GEN.001\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.matchLine(head+'\\tests\TRS.SYSDESC.GEN.001\output\SystemGenerated.arxml', 1, "<?xml version='1.0' encoding='UTF-8'?>"))
    #     self.assertTrue(FileCompare.matchLine(head+'\\tests\TRS.SYSDESC.GEN.001\output\SystemGenerated.arxml', 2,
    #                                             '<AUTOSAR xmlns="http://autosar.org/schema/r4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://autosar.org/schema/r4.0 AUTOSAR_4-2-2_STRICT_COMPACT.xsd">'))
    #
    # def test_TRS_SYSDESC_INOUT_001(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.INOUT.001\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.checkParsing(head + '\\Tests\\TRS.SYSDESC.INOUT.001\input', head + '\\Tests\\TRS.SYSDESC.INOUT.001\output\\result.log', "is well", ".arxml"))
    #
    # def test_TRS_SYSDESC_INOUT_002(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.INOUT.002\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.checkParsing(head + '\\Tests\\TRS.SYSDESC.INOUT.002\input', head + '\\Tests\\TRS.SYSDESC.INOUT.002\output\\result.log', "is well", ".dico"))
    #
    # def test_TRS_SYSDESC_INOUT_100(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\\TRS.SYSDESC.INOUT.100\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.INOUT.100\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_GEN_003_02(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_2\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_2\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_2\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_GEN_003_04(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_4\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_4\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_4\\Output\\SystemGenerated.arxml'))
    #
    #
    # def test_TRS_SYSDESC_GEN_003_05(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_5\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_5\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_5\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_GEN_003_06(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_6\\ConfigSystemDescriptor.xml')
    #     self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.GEN.003_6\\Output\\SystemGenerated.arxml'))
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.GEN.003_6\\output\\result.log', "ERROR", ["SWC-TO-ECU-MAPPING"]))
    #
    # def test_TRS_SYSDESC_GEN_003_07(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_7\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_7\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_7\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_GEN_003_08(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_8\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_8\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_8\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_GEN_003_09(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_9\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_9\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_9\\Output\\SystemGenerated.arxml'))

    # def test_TRS_SYSDESC_GEN_003_10(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_10\\ConfigSystemDescriptor.xml')
    #     self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.GEN.003_10\\Output\\SystemGenerated.arxml'))
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.GEN.003_10\\output\\result.log', "ERROR", ["SW-COMPONENT-PROTOTYPE"]))

    # def test_TRS_SYSDESC_GEN_003_11(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_11\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_11\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_11\\Output\\SystemGenerated.arxml'))

    # def test_TRS_SYSDESC_GEN_003_13(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_13\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_13\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_13\\Output\\SystemGenerated.arxml'))

    # def test_TRS_SYSDESC_GEN_003_14(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_14\\ConfigSystemDescriptor.xml')
    #     self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.GEN.003_14\\Output\\SystemGenerated.arxml'))
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.GEN.003_14\\output\\result.log', "ERROR", ["ROOT-SW-COMPOSITION-PROTOTYPE"]))

    # def test_TRS_SYSDESC_GEN_003_15(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_15\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.003_15\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.003_15\\Output\\SystemGenerated.arxml'))

    # def test_TRS_SYSDESC_GEN_003_16(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.003_16\\ConfigSystemDescriptor.xml')
    #     self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.GEN.003_16\\Output\\SystemGenerated.arxml'))
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.GEN.003_16\\output\\result.log', "ERROR", ["Multiple <SYSTEM-VERSION>"]))

    # def test_TRS_SYSDESC_GEN_004_1(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.004_1\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.004_1\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.004_1\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_GEN_004_2(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.GEN.004_2\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.areSame(head + '\\Tests\\TRS.SYSDESC.GEN.004_2\\SystemGenerated.arxml',
    #                                         head + '\\Tests\\TRS.SYSDESC.GEN.004_2\\Output\\SystemGenerated.arxml'))
    #
    # def test_TRS_SYSDESC_FUNC_200_1(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.FUNC.200_1\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.FUNC.200_1\\output\\result.log', "INFO", ["SR_ApportCarbDetecteTest"]))
    #
    # def test_TRS_SYSDESC_FUNC_200_2(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.FUNC.200_2\\ConfigSystemDescriptor.xml')
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.FUNC.200_2\\output\\result.log', "INFO", ["SENDER-RECEIVER-TO-SIGNAL-MAPPING using the signal/RootP_NetworkDesc/AUTONOMIE_HS1_52E"]))

    # def test_TRS_SYSDESC_1(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.1\\ConfigSystemDescriptor.xml')
    #     self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.1\\Output\\SystemGenerated.arxml'))
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.1\\output\\result.log', "ERROR", ["ASWC_A26.aswc.arxml"]))

    # def test_TRS_SYSDESC_2(self):
    #     current_path = os.path.realpath(__file__)
    #     head, tail = ntpath.split(current_path)
    #     os.system('SystemDescriptor.py -config ' + head + '\\Tests\TRS.SYSDESC.2\\ConfigSystemDescriptor.xml')
    #     self.assertFalse(FileCompare.isOutput(head+'\\Tests\\TRS.SYSDESC.2\\Output\\SystemGenerated.arxml'))
    #     self.assertTrue(FileCompare.checkLog(head + '\\Tests\\TRS.SYSDESC.2\\output\\result.log', "ERROR", ["ASWC_A26.mappings1.dico"]))



suite = unittest.TestLoader().loadTestsFromTestCase(SystemDescriptor)
unittest.TextTestRunner(verbosity=2).run(suite)

# current_path = os.path.realpath(__file__)
# head, tail = ntpath.split(current_path)
# if __name__ == "__main__":
#     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=head + "\\tests"))
