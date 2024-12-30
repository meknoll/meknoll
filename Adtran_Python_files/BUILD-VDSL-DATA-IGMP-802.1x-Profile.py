
import paramiko
import time


# Note need to build logic to change between VDSL and  ADSL Profiles
# Note need to change the password for the particular servers

print("Single Pair VDSL PROFILE PUSH - Choose Adtran EMS Server")
print("1) East =      10.74.8.166")
print("2) Midwest =   10.74.8.136")
print("3) Central =   10.74.8.167")
print("4) West    =   10.74.8.168")
print("5) Vader   =   10.177.171.73")
print("6) Skywalker = 10.177.171.66")

choice = input("Enter the desired server number: ")

def Choose_AOE_Server():
    global ip
    global login
    global passwd
    host=0
    host=str(host)
    if choice == "1":
        ip  = "10.74.8.166" 
        login = "ems"
        passwd = "Admin123!"
    elif choice=="2":
        ip = "10.74.8.136"
        login = "ems"
        passwd = "Admin123!"
    elif choice=="3":
        ip = "10.74.8.167"
        login = "ems"
        passwd = "Admin123!"
    elif choice=="4":
        ip = "10.74.8.168"
        login = "ems"
        passwd = "Admin123!"
    elif choice == "5":
        ip = "10.177.171.73"
        login = "ems"
        passwd = "Admin123!"
    elif choice == "6":
        ip = "10.177.171.66"
        login = "ems"
        passwd = "Admin123!"
       
       
    else:
        print('error please choose a number between 1-6')




 
def Access_DSLAM(ip):
   
   #date_time = datetime.datetime.now().strftime("%Y-%m-%d)
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=22, username=login, password=passwd, look_for_keys=False, timeout=None)
    global connection
    connection = ssh.invoke_shell()
    time.sleep(2)

def Start_tl1():
    global DSLAM
    #global PORT
    DSLAM = input( "Enter DSLAM CLLI: ")
    PORT0 = input ( "Enter DSLAM port info with 2 digits for the port, ie: for eg:for Shelf 1, Rack1, Slot1, Port 2  in format 11102 : ")
    PROF = input ( "Enter Profile Name: ")
    dash = ("-")      
    pr1= PORT0[0] + dash + PORT0[1] + dash + PORT0[2] + dash + PORT0[3] + PORT0[4]
    session = 100

    connection.send("telnet 0 14001\n")
    time.sleep(2)
    output = connection.recv(100000)
    print(output.decode())

    connection.send("act-user::tl1user:100::tl1user;\n")
    time.sleep(2)
    output = connection.recv(100000)
    print(output.decode())
    time.sleep(1)

    connection.send("STA-CMDSSN:" + DSLAM  +":COM:" + str(session)+";\n")
    time.sleep(.5)
    output = connection.recv(100000)
    print(output.decode())

    

    

    connection.send("DLT-VCL:"+ DSLAM +":LTVCL-"+ pr1 +"-0-35::100;\n")
    connection.send("ED-ATMPORT:"+ DSLAM +":LTATM-"+ pr1 +":100::::OOS;\n")
    connection.send("ED-VDSL2:"+ DSLAM +":VDSL2-"+ pr1 + ":100:::VDSL2PROFNM="+ PROF +":IS;\n")
    connection.send("ED-AUTH-DOT1X:"+ DSLAM +":ETHIF-" + pr1 +":100:::IPHOSTNM=RADIUS_Client_DSL,SRVGRP=SERVER_GROUP_DSL,CNTL=AUTO;\n")
    connection.send("ENT-VLANPORT-ETH:"+ DSLAM +"1:ETHIF-"+ pr1 +":100:::CRSID="+ "1x_SLOT" + PORT0[2] + "P" + PORT0[3]+PORT0[4] + ",TRAFPROFNM=1x_DSL_AUTH,STAG=4090,STAGPRI=INHERIT,PRESERVECTAG=N:IS;\n")
    connection.send("ENT-VLANPORT-ETH:"+ DSLAM +":ETHIF-"+ pr1 + ":100:::CRSID="+"DATA_SLOT" + PORT0[2] + "P" + PORT0[3]+PORT0[4] +",CEVLANID=PRIO,STAG=1003,CTAG=" + PORT0[3]+PORT0[4] + ",STAGPRI=0,TRAFPROFNM="+"DATA_DSL_MAP"+";\n")
    connection.send("ENT-VLANPORT-ETH:"+ DSLAM +":ETHIF-" + pr1 + ":100:::CRSID="+"IGMP_SLOT" + PORT0[2] + "P" + PORT0[3]+PORT0[4]+",CEVLANID=PRIO,STAG=4000,STAGPRI=5,TRAFPROFNM="+"IGMP_VDSL_4STB"+";\n")

    time.sleep(4)
    output = connection.recv(100000)
    print(output.decode())
    
    connection.send("STP-CMDSSN:" + DSLAM  +":COM:" + str(session)+";\n")
    time.sleep(1)
    output = connection.recv(100000)
    print(output.decode())


    connection.send("RTRV-VDSL2:"+ DSLAM + ":VDSL2-" + pr1 + ";IP 10;\n")
    
    
    
    
    time.sleep(.5)
    connection.send("canc-user:tl1user::100;/n")
    output = connection.recv(100000)
    
    print(output.decode())

    
    

    connection.send("exit\n")
    time.sleep(10)

    connection.send("exit\n")
    time.sleep(1)
     
    ssh.close()







Choose_AOE_Server()
Access_DSLAM(ip)
#Choose_SP_or_BP()
#Choose_ADSL_or_VDSL()
Start_tl1()

    







