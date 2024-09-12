*** Settings ***
Library     Telnet    prompt=$


*** Test Cases ***
Try Telnet
      Open Connection     10.177.77.77     port=23
   Set Prompt        (> |# )    
   Set Newline       \\n
      Set Newline       CRLF
	
	Login     username      password
	Write     commands
	${out} =  Read Until Prompt
