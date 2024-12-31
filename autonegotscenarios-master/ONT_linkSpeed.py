import xml.etree.ElementTree as ET
import time
# from time import sleep
# from robot.libraries import BuiltIn

def query_xml_value(queryFilePath, ONT_meNm, ONT_propNm):  # change modifyEthPort.xml value
    namespaces = {
    'xmlns' : 'alu.v1',
    'alu' : 'alu.v1',
    'soapenv' : 'http://schemas.xmlsoap.org/soap/envelope/',
    'tmf854': 'tmf854.v1',
    'xsd' : 'http://www.w3.org/2001/XMLSchema',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'    
    }
    
    tree = ET.parse(queryFilePath)
    root = tree.getroot()

    # Locate the value element using namespace-aware XPath
    ONT_meNm_elenment = root.find(".//soapenv:Body/alu:query/alu:baseObjectList/alu:baseObject/tmf854:meNm", namespaces)     ## meNm
    print(ONT_meNm_elenment.text)

    ONT_prop_elenment = root.find(".//soapenv:Body/alu:query/alu:baseObjectList/alu:baseObject/tmf854:propNm", namespaces)     ## propNm
    print(ONT_prop_elenment.text)

    ## Update the text value ONT_meNm_elenment.text  with ONT_meNm
    ONT_meNm_elenment.text = ONT_meNm
    ONT_prop_elenment.text = ONT_propNm

    # Save changes back to the file
    tree.write(queryFilePath, encoding="utf-8", xml_declaration=True)
    return True  # Modification successful
    return False  # Modification not done


def modify_xml_value(file_path, objectName_elem, name_elem, value_elem):  # change modifyEthPort.xml value
    namespaces = {
        'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
        'ns': 'uri://alcatel.com/apc/9.6'
    }
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Locate the value element using namespace-aware XPath
    objectName_element = root.find(".//soapenv:Body/ns:modify/objectName", namespaces)
    name_element = root.find(".//soapenv:Body/ns:modify/argument/name", namespaces)
    value_element = root.find(".//soapenv:Body/ns:modify/argument/value", namespaces)     
    
    ## Update the text value
    objectName_element.text = objectName_elem
    name_element.text = name_elem
    value_element.text = value_elem
    
    ## Save changes back to the file
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
    return True  # Modification successful
    return False  # Modification not done

##### Query result function
def query_response_eth_port (file_path,):
    # file_path =  'queryEthPortResponse.xml'
    namespaces = {
        'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
        'tmf854': 'tmf854.v1',
        'alu': 'alu.v1'
    }

    tree = ET.parse(file_path)
    root = tree.getroot()

    # Locate the <name> element using the namespace-aware XPath
    autoDetectConfigName_elem = root.find(".//soapenv:Body/alu:queryResponse/alu:queryObjectData/alu:queryObject/alu:vendorExtensions/alu:package/alu:NameAndStringValue[4]/tmf854:name", namespaces)
    autoDetectConfig = autoDetectConfigName_elem.text
    autoDectLinkSpeed_elem = root.find(".//soapenv:Body/alu:queryResponse/alu:queryObjectData/alu:queryObject/alu:vendorExtensions/alu:package/alu:NameAndStringValue[4]/tmf854:value", namespaces)
    autoDectLinkSpeed= autoDectLinkSpeed_elem.text
    print(autoDetectConfig, ':', autoDectLinkSpeed)
  
    opstatConfigIndicatorName_elem = root.find(".//soapenv:Body/alu:queryResponse/alu:queryObjectData/alu:queryObject/alu:vendorExtensions/alu:package/alu:NameAndStringValue[23]/tmf854:name", namespaces)
    opstatConfigIndicator = opstatConfigIndicatorName_elem.text
    opstatLinkSpeed_elem = root.find(".//soapenv:Body/alu:queryResponse/alu:queryObjectData/alu:queryObject/alu:vendorExtensions/alu:package/alu:NameAndStringValue[23]/tmf854:value", namespaces)
    opstatLinkSpeed= opstatLinkSpeed_elem.text
    print(opstatConfigIndicator, ':', opstatLinkSpeed)

    ifOperStatusName_elem = root.find(".//soapenv:Body/alu:queryResponse/alu:queryObjectData/alu:queryObject/alu:vendorExtensions/alu:package/alu:NameAndStringValue[51]/tmf854:name", namespaces)
    ifOperStatus = ifOperStatusName_elem.text
    operStatus_elem = root.find(".//soapenv:Body/alu:queryResponse/alu:queryObjectData/alu:queryObject/alu:vendorExtensions/alu:package/alu:NameAndStringValue[51]/tmf854:value", namespaces)
    operStatus= operStatus_elem.text
    print(ifOperStatus, ':', operStatus)
    
    return autoDetectConfig , autoDectLinkSpeed, opstatConfigIndicator, opstatLinkSpeed, ifOperStatus, operStatus


###### Change value for resetONT.xml ######
def change_resetONT_value (resetONT_filePath, resetONT_meNm, resetONT_ehNm, resetONT_action):  # change resetONT.xml value
    
    namespaces = {
        'soapenv' : 'http://schemas.xmlsoap.org/soap/envelope/',
        'tmf' : 'tmf854.v1',
        'alu' : 'alu.v1'   
    }

    tree = ET.parse(resetONT_filePath)
    root = tree.getroot()
    print(root)


    # Locate the value element using namespace-aware XPath
    ONT_meNm_element = root.find(".//soapenv:Body/alu:executeAction/alu:name/tmf:meNm", namespaces)     ## meNm
    print(ONT_meNm_element.text)

    ONT_ehNm_element = root.find(".//soapenv:Body/alu:executeAction/alu:name/tmf:ehNm", namespaces)     ## meNm
    print(ONT_ehNm_element.text)

    ONT_action_element = root.find(".//soapenv:Body/alu:executeAction/alu:action", namespaces)     ## propNm
    print(ONT_action_element.text)

    ## Update the text value ONT_meNm_elenment.text  with ONT_meNm
    ONT_meNm_element.text = resetONT_meNm
    ONT_ehNm_element.text = resetONT_ehNm
    ONT_action_element.text = resetONT_action


    ### Save changes back to the file
    tree.write(resetONT_filePath , encoding="utf-8", xml_declaration=True)
    
    return True  # Modification successful
    return False  # Modification not done
        # #********** END Stand alone f or modifyXM.py ***************#



    ###### Change value for reset OLT.xml ######
def change_resetLT_value (resetLT_filePath, resetLT_meNm, resetLT_ehNm, resetLT_value):  # change resetLT_SelfTest.xml value
    
    namespaces = {
        'soapenv' : 'http://schemas.xmlsoap.org/soap/envelope/',
        'tmf' : 'tmf854.v1',
        'alu' : 'alu.v1'   
    }

    tree = ET.parse(resetLT_filePath)
    root = tree.getroot()
    print(root)
    
    OLT_meNm_element = root.find(".//soapenv:Body/alu:executeAction/alu:name/tmf:meNm", namespaces)     ## meNm
    print(OLT_meNm_element.text)

    OLT_ehNm_element = root.find(".//soapenv:Body/alu:executeAction/alu:name/tmf:ehNm", namespaces)     ## meNm
    print(OLT_ehNm_element.text)

    OLT_tmf_value_element = root.find(".//soapenv:Body/alu:executeAction/alu:arguments/alu:package/alu:NameAndStringValue/tmf:value", namespaces)     ## propNm
    print(OLT_tmf_value_element.text)
        

    ## Update the text value OLT_meNm_elenment.text  with OLT_meNm
    OLT_meNm_element.text = resetLT_meNm
    OLT_ehNm_element.text = resetLT_ehNm
    OLT_tmf_value_element.text = resetLT_value
    # time.sleep(2)

    ### Save changes back to the file
    tree.write(resetLT_filePath , encoding="utf-8", xml_declaration=True)
    
    return True  # Modification successful
    return False  # Modification not done
        # #********** END Stand alone f or modifyXM.py ***************#
          
        
##### Change value for reset PORT.xml ######
def change_resetPORT_value (resetPORT_filePath, resetPORT_meNm, resetPORT_ptpNm, resetPORT_action):  # change resetLT_SelfTest.xml value
    print(resetPORT_action)
    
    namespaces = {
        'soapenv' : 'http://schemas.xmlsoap.org/soap/envelope/',
        'tmf' : 'tmf854.v1',
        'alu' : 'alu.v1'   
    }

    tree = ET.parse(resetPORT_filePath)
    root = tree.getroot()
    print(root)

    # Locate the value element using namespace-aware XPath
    ONT_meNm_element = root.find(".//soapenv:Body/alu:executeAction/alu:name/tmf:meNm", namespaces)     ## meNm
    ONT_meNm_element.text = resetPORT_meNm  ## update meNm with new value
    print(ONT_meNm_element.text)

    ONT_ptpNm_element = root.find(".//soapenv:Body/alu:executeAction/alu:name/tmf:ptpNm", namespaces)     ## ptpNm
    ONT_ptpNm_element.text = resetPORT_ptpNm  ## update ptpNm with new value
    print(ONT_ptpNm_element.text)

    ONT_action_element = root.find(".//soapenv:Body/alu:executeAction/alu:action", namespaces)     ## lock or unlock
    ONT_action_element.text = resetPORT_action ## update action with new value
    print(ONT_action_element.text)


    ### Save changes back to the file
    tree.write(resetPORT_filePath , encoding="utf-8", xml_declaration=True)
    return True  # Modification successful
    return False  # Modification not done
        # #********** END Stand alone f or modifyXM.py ***************#