*** Settings ***
Library     Telnet    prompt=$


*** Test Cases ***
Try Telnet
      Open Connection     10.224.131.198     port=23
   Set Prompt        (> |# )    
   Set Newline       \\n
      Set Newline       CRLF
	
	Login     e7      admin
	Write     commands
	${out} =  Read Until Prompt
