*** Settings ***
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

${resetONT_filePath}        ${EXECDIR}/resetONT.xml
${resetONT_meNm}            LWVLLABN7360P05
${resetONT_ehNm}            /rack=1/shelf=1/slot=LT1/port=1/remote_unit=11
${resetONT_action}          RESET

*** Test Cases ***
Auto Negotiate Reset ONT    
 
    ${timestamp}      Get Time        result_format=%Y-%m-%d hh:mm:ss
    ${timestamp}      Replace String    ${timestamp}    :  .  ## change colon to period for Windows file name
    ${ONT_resetDataFile}=      Set Variable    resultData_${timestamp}.txt
    Create File       ${ONT_resetDataFile}     # create a .txt file to store ONT Data result

    ######## ******* CALL PYTHON to SET queryEthPort.XML file with ONT ID/property name  ******* #############
    ${result_query}=    query_xml_value    ${queryFilePath}  ${query_ONT_meNm}  ${query_ONT_propNm}   # Call python function modidy_xml_value
    # Log To Console    ${result_query}
    Run Keyword If    not ${result_query}    Fail    Modification failed: Value not found or did not match expected text

    ######## ******* CALL PYTHON to SET resetONT.XML file value ******* #############
    ${result_action}=    change_resetONT_value    ${resetONT_filePath}  ${resetONT_meNm}  ${resetONT_ehNm}  ${resetONT_action}  # Call python function ??????
    # Log To Console    ${result_action}
    Run Keyword If    not ${result_action}    Fail   failed: Not able to change action value

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

    Log   \n*Before ${resetONT_action} action operation Configure is: ${opstatConfigIndicator} : ${_opstatLinkSpeed_pre}     console=True \n
    Log   \n*Before ${resetONT_action} action operation status is: ${ifOperStatus} : ${operStatus_pre}                       console=True \n
    
    Append To File    ${ONT_resetDataFile}    ******* Result test data for scenario ${resetONT_action} : \n
    IF    '${_opstatLinkSpeed_pre}' == 'Not Detected' or '${operStatus_pre}' == 'Down'
        Append To File    ${ONT_resetDataFile}    Test stopped due to either current Operation State is Down or Configuaration Status is Not Detected \n      
    END
    Should Be Equal As Strings  ${operStatus_pre}  Up    Msg: Before Operation status shows as DOWN  #Check current oper status befor test
    Should Not Be Equal As Strings  ${opstatLinkSpeed_pre}  Not Detected    Msg: Before Operation Link Speed  shows as NOT DETECTED

    ############################ Append Text to file_name ###
    Append To File    ${ONT_resetDataFile}    Before ${resetONT_action} action Operation Configuration Indicator : ${opstatLinkSpeed_pre}\n
    Append To File    ${ONT_resetDataFile}    Before ${resetONT_action} action Operation Status : ${operStatus_pre} \n 
    ##################   

    ##********************************* AUTO NEGOTIATE SCENARIO ACTIONS ************************ 
    ####*********** resetONT.xml SOAP POST REQUEST HEADERS, AUTHENTICATION, BODY to RESET ONT****#######
    @{auth}=    Create List    ${soapUI_user}    ${passWord}
    &{headers_resetONT}    Create Dictionary   Content-Type=text/xml;charset=UTF-8  SOAPAction=""  Host=10.250.37.132:8080  # Only needs SOAPAction
    ${resetONTBody}=    Get Binary File    ${CURDIR}${/}resetONT.xml      
    ######## SOAP request set ONT action to RESET
    Create Session    mySession     ${base_url_autoNegot}     auth=${auth}    disable_warnings=1
    ${response_resetONTBody}=    POST On Session    mySession  ${endpoint_autoNegot}   headers=${headers_resetONT}     data=${resetONTBody}  
   
    
    ####### ********** Verify ONT status is down during RESET scenario ***********##################
    ##########################**********  queryEthPort.xml SOAP REQUEST  HEADERS, AUTHENTICATION, BODY ******#################################
    sleep  15s
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

    Log   \n*During RESET ${resetONT_action} action operation status is: ${ifOperStatus_reset} : ${operStatus_reset}     console=True
    Append To File    ${ONT_resetDataFile}    During Reset for ${resetONT_action} action Operation Status : ${operStatus_reset} \n
    Run Keyword and continue on Failure  Should Be Equal    ${operStatus_reset}    Down    Msg. Status should show Down during reset

    Sleep   60s   # estimated time for ONT reset and come back 40s    # estimated time for ONT reset and come back up

    ######### Check ONT status for another 120 seconds for 'Up' status (refresh every 5s) ######
    FOR    ${counter}    IN RANGE    24
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
    
    Log   \n*After ${resetONT_action} action operation Configure is: ${opstatConfigIndicator_post} : ${opstatLinkSpeed_post}     console=True
    Log   \n*After ${resetONT_action} action operation status is: ${ifOperStatus_post} : ${operStatus_post}                      console=True
    IF    '${opstatLinkSpeed_pre}' == '${opstatLinkSpeed_post}' and '${operStatus_pre}' == '${operStatus_post}' and '${opstatLinkSpeed_post}' != 'Not detected' and '${operStatus_post}'!= 'Down'
        ${test_result}=    Set Variable    PASS
    ELSE
        ${test_result}=    Set Variable    FAIL
    END
    ############################ Append Text to file_name ###
    Append To File    ${ONT_resetDataFile}    After ${resetONT_action} action Operation Configuration Indicator : ${opstatLinkSpeed_post}\n
    Append To File    ${ONT_resetDataFile}    After ${resetONT_action} action Operation Status : ${operStatus_post} \n 
    Append To File    ${ONT_resetDataFile}    Test result for ${resetONT_action} action : ${test_result}
    ################## 
    Run Keyword and continue on Failure  Should Be Equal    ${opstatLinkSpeed_pre}    ${opstatLinkSpeed_post}   Msg. link speed config should be the same after reset
    Run Keyword and continue on Failure  Should Be Equal    ${operStatus_pre}    ${operStatus_post}   Msg. status should be Up after reset is completed
 