** Settings ***
Library    XML
Library    OperatingSystem
Library    Collections
Library    BuiltIn
Library    RequestsLibrary
Library    String
Library    ${EXECDIR}/ONT_linkSpeed.py

*** Variables ***
${base_url_modify}            http://10.250.37.132:8080
${endpoint_modify}            /soap/services/ApcRemotePort/9.6

${base_url_query}            https://10.250.37.132:8443
${endpoint_query}            /idm/services/InventoryRetrievalMgrExtns

${base_url_autoNegot}            https://10.250.37.132:8443
${endpoint_autoNegot}            /ams/services/ActionExecutorMgr

${soapUI_user}         tnn283
${passWord}            %{ECO_PASSWORD}

${queryFilePath}                 ${EXECDIR}/queryEthPort.xml
${queryResponseFilePath}         ${EXECDIR}/queryEthPortResponse.xml
${query_ONT_meNm}                LWVLLABN7360P05
${query_ONT_propNm}              /type=Ethernet Port/R1.S1.LT1.PON1.ONT11.C10.P1 

${resetPORT_filePath}           ${EXECDIR}/resetPORT.xml
${resetPORT_meNm}                LWVLLABN7360P05
${resetPORT_ptpNm}               /rack=1/shelf=1/slot=LT1/port=1/remote_unit=11/slot=10/port=1
${resetPORT_lock_action}         PORT_LOCK
${resetPORT_unlock_action}       PORT_UNLOCK

*** Test Cases ***
Auto Negotiate OLT PORT_LOCK/UNLOCK

    ${timestamp}      Get Time        result_format=%Y-%m-%d hh:mm:ss
    ${timestamp}      Replace String    ${timestamp}    :  .  ## change colon to period for Windows file name
    ${ONT_resetDataFile}=      Set Variable    LT_Port_reset_Data_${timestamp}.txt
    Create File       ${ONT_resetDataFile}     # create a .txt file to store ONT Data result

    ######## ******* CALL PYTHON to modify queryEthPort.XML file for current status ******* #############
    ${result_query}=    query_xml_value    ${queryFilePath}  ${query_ONT_meNm}  ${query_ONT_propNm}   # Call python function modidy_xml_value
    # Log To Console    ${result_query}
    Run Keyword If    not ${result_query}    Fail    Modification failed: Value not found or did not match expected text

    # ##########################**********  CHECK STATUS-queryEthPort.xml SOAP REQUEST  HEADERS, AUTHENTICATION, BODY ******#################################
    &{headers_query}    Create Dictionary   Content-Type=text/xml;charset=UTF-8  SOAPAction=""  Host=10.250.37.132:8443
    @{auth}=    Create List    ${soapUI_user}    ${passWord}
    ${queryEthPortBody}=    Get Binary File    ${CURDIR}${/}queryEthPort.xml 
    ####### SOAP request to QUERY Ethernet Port response
    Create Session    mySession     ${base_url_query}     auth=${auth}    disable_warnings=1  
    ${response_queryEthPortBody}=    POST On Session    mySession  ${endpoint_query}   headers=${headers_query}     data=${queryEthPortBody}  
    ${xml_content}=    Convert To String   ${response_queryEthPortBody.content} 
    ######## Update file and save request response content
    Create File    queryEthPortResponse.xml    ${xml_content}  

    #############***CALL PYTHON FUNCTION to parse  queryEthPortResponse.xml and check Current operation status
    ${result}    query_response_eth_port   ${queryResponseFilePath}  # Call python function
    ${resultType}    Evaluate    type($result)

    ${autoDetectConfig}=        Set Variable    ${result}[0]
    ${autoDectLinkSpeed}=       Set Variable    ${result}[1]
    Log To Console    \n*Auto Detected Configuration is: ${autoDectLinkSpeed}

    ${opstatConfigIndicator}=   Set Variable    ${result}[2]
    ${opstatLinkSpeed_pre}=         Set Variable    ${result}[3]
    Log To Console    \n*OpstatLinkSpeed_pre is: ${opstatLinkSpeed_pre}

    ${ifOperStatus}=            Set Variable    ${result}[4]
    ${operStatus_pre}=              Set Variable    ${result}[5]
    Log To Console    \n*Status is: ${operStatus_pre}

    Log   \n*Before OLT PORT_lock/Unlock Operation Configure is: ${opstatConfigIndicator} : ${_opstatLinkSpeed_pre}     console=True \n
    Log   \n*Before OLT PORT_lock/Unlock Operation status is: ${ifOperStatus} : ${operStatus_pre}                       console=True \n
    
    Append To File    ${ONT_resetDataFile}    ******* Result test data for scenario of OLT PORT_lock/Unlock : \n
    IF    '${_opstatLinkSpeed_pre}' == 'Not Detected' or '${operStatus_pre}' == 'Down'
        Append To File    ${ONT_resetDataFile}    Test stopped due to either current Operation State is Down or Configuaration Status is Not Detected \n      
    END
    Should Be Equal As Strings  ${operStatus_pre}  Up    Msg: Before Operation status shows as DOWN  #Check current oper status befor test
    Should Not Be Equal As Strings  ${opstatLinkSpeed_pre}  Not Detected    Msg: Before Operation Link Speed  shows as NOT DETECTED

    ############################ Append Text to file_name ###
    Append To File    ${ONT_resetDataFile}    Before OLT PORT_lock/Unlock Operation Configuration Indicator : ${opstatLinkSpeed_pre}\n
    Append To File    ${ONT_resetDataFile}    Before OLT PORT_lock/Unlock action Operation Status : ${operStatus_pre} \n 
    ##################   

    ##********************************* AUTO NEGOTIATE SCENARIO ACTIONS PORT_LOCK / PORT_UNLOCK************************ 

    ######## ******* CALL PYTHON to modify resetPORT.XML file value to PORT_LOCK ******* #############
    ${result_action}=    change_resetPORT_value    ${resetPORT_filePath}  ${resetPORT_meNm}  ${resetPORT_ptpNm}  ${resetPORT_lock_action}   # Call python function set PORT_LOCK
    # Log To Console    ${result_action}
    Run Keyword If    not ${result_action}    Fail   failed: Not able to change action value

    ####*********** resetPORT.xml SOAP POST REQUEST HEADERS, AUTHENTICATION, BODY to set OLT PORT_lock/Unlock ****#######
    @{auth}=    Create List    ${soapUI_user}    ${passWord}
    &{headers_resetONT}    Create Dictionary   Content-Type=text/xml;charset=UTF-8  SOAPAction=""  Host=10.250.37.132:8080  # Only needs SOAPAction
    ${resetOLTbody}=    Get Binary File    ${CURDIR}${/}resetPORT.xml      
    ######## SOAP request set OLT action to set PORT_LODK
    Create Session    mySession     ${base_url_autoNegot}     auth=${auth}    disable_warnings=1
    ${response_resetOLTbody}=    POST On Session    mySession  ${endpoint_autoNegot}   headers=${headers_resetONT}     data=${resetOLTbody}  

    
    ####### ********** Verify ONT status is down during PORT_LOCK ***********##################
    ##########################**********  queryEthPort.xml SOAP REQUEST  HEADERS, AUTHENTICATION, BODY ******#################################
    Sleep    15s
    &{headers_query}    Create Dictionary   Content-Type=text/xml;charset=UTF-8  SOAPAction=""  Host=10.250.37.132:8443
    @{auth}=    Create List    ${soapUI_user}    ${passWord}
    ${queryEthPortBody}=    Get Binary File    ${CURDIR}${/}queryEthPort.xml 
    ####### SOAP request to QUERY Ethernet Port response
    Create Session    mySession     ${base_url_query}     auth=${auth}    disable_warnings=1  
    ${response_queryEthPortBody}=    POST On Session    mySession  ${endpoint_query}   headers=${headers_query}     data=${queryEthPortBody}  
    ${xml_content}=    Convert To String   ${response_queryEthPortBody.content} 
    ######## Update file and save request response content
    Create File    queryEthPortResponse.xml    ${xml_content}  

    #############***CALL PYTHON FUNCTION to parse xml and check Current operation status
    ${result}    query_response_eth_port   ${queryResponseFilePath}  # Call python function
    ${resultType}    Evaluate    type($result)

    ${ifOperStatus_reset}=            Set Variable    ${result}[4]
    ${operStatus_reset}=              Set Variable    ${result}[5]

    Log   \n*During OLT PORT_LOCK ${result_action} action operation status is: ${ifOperStatus_reset} : ${operStatus_reset}     console=True
    Append To File    ${ONT_resetDataFile}    During OLT PORT_LOCK Operation Status : ${operStatus_reset} \n
    Run Keyword and continue on Failure  Should Be Equal    ${operStatus_reset}    Down    Msg. Status should show Down during PORT_LOCK


    ######## ******* CALL PYTHON to modify resetPORT.XML file value to PORT_UNLOCK ******* #############
    ${result_action}=    change_resetPORT_value    ${resetPORT_filePath}  ${resetPORT_meNm}  ${resetPORT_ptpNm}  ${resetPORT_unlock_action}   # Call python function set PORT_UNLOCK
    # Log To Console    ${result_action}
    Run Keyword If    not ${result_action}    Fail   failed: Not able to change action value

    ####*********** resetPORT.xml SOAP POST REQUEST HEADERS, AUTHENTICATION, BODY to OLT PORT_UNLOCK****#######
    @{auth}=    Create List    ${soapUI_user}    ${passWord}
    &{headers_resetONT}    Create Dictionary   Content-Type=text/xml;charset=UTF-8  SOAPAction=""  Host=10.250.37.132:8080  # Only needs SOAPAction
    ${resetOLTbody}=    Get Binary File    ${CURDIR}${/}resetPORT.xml      
    ######## SOAP request set OLT action to set PORT_UNLODK
    Create Session    mySession     ${base_url_autoNegot}     auth=${auth}    disable_warnings=1
    ${response_resetOLTbody}=    POST On Session    mySession  ${endpoint_autoNegot}   headers=${headers_resetONT}     data=${resetOLTbody}  

    Sleep   15s   # estimated time for OLT back online after PORT_UNLOCK

    ######### Check ONT status for another 60 seconds for 'Up' status (refresh every 5s) ######
    FOR    ${counter}    IN RANGE    10
        # ##########################**********  queryEthPort.xml SOAP REQUEST  HEADERS, AUTHENTICATION, BODY ******#################################
        &{headers_query}    Create Dictionary   Content-Type=text/xml;charset=UTF-8  SOAPAction=""  Host=10.250.37.132:8443
        @{auth}=    Create List    ${soapUI_user}    ${passWord}
        ${queryEthPortBody}=    Get Binary File    ${CURDIR}${/}queryEthPort.xml 
        ####### SOAP request to QUERY Ethernet Port response
        Create Session    mySession     ${base_url_query}     auth=${auth}    disable_warnings=1  
        ${response_queryEthPortBody}=    POST On Session    mySession  ${endpoint_query}   headers=${headers_query}     data=${queryEthPortBody}  
        ${xml_content}=    Convert To String   ${response_queryEthPortBody.content} 
        ######## Update file and save request response content
        Create File    queryEthPortResponse.xml    ${xml_content}  

        #############***CALL PYTHON FUNCTION to parse xml and check Current operation status
        ${result}    query_response_eth_port   ${queryResponseFilePath}  # Call python function
        ${resultType}    Evaluate    type($result)

        ${opstatConfigIndicator_post}=   Set Variable    ${result}[2]
        ${opstatLinkSpeed_post}=         Set Variable    ${result}[3]

        ${ifOperStatus_post}=            Set Variable    ${result}[4]
        ${operStatus_post}=              Set Variable    ${result}[5]
        Log To Console   \n*Refresh status - ${operStatus_post}
        Run Keyword If   '${operStatus_post}' == 'Up'    Exit For Loop
    Sleep    5s    
    END
    
    Log   \n*After OLT set PORT_UNLOCK Operation Configure is: ${opstatConfigIndicator_post} : ${opstatLinkSpeed_post}     console=True
    Log   \n*After OLT set PORT_UNLOCK operation Status is: ${ifOperStatus_post} : ${operStatus_post}                      console=True \n
    IF    '${opstatLinkSpeed_pre}' == '${opstatLinkSpeed_post}' and '${operStatus_pre}' == '${operStatus_post}' and '${opstatLinkSpeed_post}' != 'Not detected' and '${operStatus_post}'!= 'Down'
        ${test_result}=    Set Variable    PASS
    ELSE
        ${test_result}=    Set Variable    FAIL
    END     #After OLT set PORT_UNLOCK Operation Configure is:
    ############################ Append Text to file_name ###
    Append To File    ${ONT_resetDataFile}    After OLT set PORT_UNLOCK Operation Configuration Indicator : ${opstatLinkSpeed_post}\n
    Append To File    ${ONT_resetDataFile}    After OLT set PORT_UNLOCK Operation Status : ${operStatus_post} \n 
    Append To File    ${ONT_resetDataFile}    Test result for OLT set PORT_LOCK/UNLOCK: ${test_result}\n\n
    ################## 
    Run Keyword and continue on Failure  Should Be Equal    ${opstatLinkSpeed_pre}    ${opstatLinkSpeed_post}   Fail_Msg. link speed config should be the same after set PORT LOCK/UNLOCK
    Run Keyword and continue on Failure  Should Be Equal    ${operStatus_pre}    ${operStatus_post}   Fail_Msg. status should be Up after set PORT LOCK/UNLOCKt is completed
    
  