*** Settings ***
Library     Telnet
Library     OperatingSystem
Library     JSONLibrary
Library     BuiltIn

*** Variables ***
${VAR_FILE}    var.json

*** Test Cases ***
Configure Service via Telnet
    # Step 1: Load JSON Configuration
    ${config} =    Load JSON From File    ${VAR_FILE}
    
    # Step 2: Extract variables from JSON
    ${HOST} =    Set Variable    ${config['HOST']}
    ${user} =    Set Variable    ${config['user']}
    ${password} =    Set Variable    ${config['password']}
    ${ONT_Port} =    Set Variable    ${config['ONT_Port']}
    ${eth_svc} =    Set Variable    ${config['eth_svc']}
    ${bw_profile} =    Set Variable    ${config['bw_profile']}
    ${st_act} =    Set Variable    ${config['ST_Act']}
    ${outer_vlan} =    Set Variable    ${config['outer_vlan']}
    ${inner_vlan} =    Set Variable    ${config['inner_vlan']}
    
    # Step 3: Check for optional parameters with defaults
    ${mcast_profile} =    Get Value From Dictionary    ${config}    mcast_profile    default_mcast_profile
    ${description} =    Get Value From Dictionary    ${config}    description    default_description
    ${pon_cos} =    Get Value From Dictionary    ${config}    pon_cos    default_pon_cos
    
    # Step 4: Telnet connection setup
    Open Connection    ${HOST}
    
    # Step 5: Login using username and password
    Write Until    Username:    ${user}
    Write Until    Password:    ${password}
    
    # Step 6: Disable session pager
    Write    set session pager disabled
    Sleep    5s
    
    # Step 7: Construct and send the main command
    ${command} =    Set Variable    add eth-svc ${eth_svc} to-ont-port ${ONT_Port} bw-profile ${bw_profile} svc-tag-action ${st_act} outer-vlan ${outer_vlan} inner-vlan ${inner_vlan} mcast-profile ${mcast_profile} description ${description} pon-cos ${pon_cos} admin-state enabled
    Write    ${command}
    Sleep    5s
    
    # Step 8: Set ONT port admin state to disabled
    Write    set ont-port 1/g1 admin-state disabled
    Sleep    5s
    
    # Step 9: Set ONT port admin state to enabled
    Write    set ont-port 1/g1 admin-state enabled
    Sleep    90s
    
    # Step 10: Show DHCP leases for the ONT port
    Write    show dhcp leases ont-port 1/g1
    
    # Step 11: Exit the Telnet session
    Write    exit
    
    # Step 12: Read and log all session output
    ${output} =    Read Until    ${EMPTY}
    Log    ${output}
    
    # Step 13: Close the Telnet connection
    Close All Connections
