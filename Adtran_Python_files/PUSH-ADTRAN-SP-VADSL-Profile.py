
import paramiko
import time


# Note need to build logic to change between VDSL and  ADSL Profiles
# Note need to change the password for the particular servers

print("Single Pair ADSL ON VDSL CARD PROFILE PUSH - Choose Adtran EMS Server")
print("1) East =      10.74.8.166")
print("2) Midwest =   10.74.8.136")
print("3) Central =   10.74.8.167")
print("4) West    =   10.74.8.168")
print("5) Vader   =   10.177.171.73")
print("6) Skywalker = 10.177.171.66")

choice = input("Enter the desired server number: ")

def Select_AOE_Server():
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
        print('error please Select a number between 1-6')


def Select_SP_or_BP():
    global param
    print("Select Adtran Pair Type")
    print("1) Single Pair")
    print("2) Bonded Pair")
    if choice == "1":
        param  = "SP" 
       
    if choice=="2":
        param = "DP"
        

def Select_ADSL_or_VDSL():
    global prof
    print("Select Adtran Profile Type")
    print("1) ADSL")
    print("2) VDSL")
    if choice == "1":
        prof  = "ADSL" 
       
    if choice=="2":
        prof = "VDSL"



 
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
    DSLAM = input( "Enter DSLAM CLLI: ")
    PORT = input ( "Enter DSLAM port eg:for Shelf 1, Rack1, Slot1, Port 1  in format 1111 : ")
    PROF = input ( "Enter Profile Name: ")
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

  

   #Build  port as follows:
    #In preparation to iterate PORT 0 convert it to integer as can't add integer to string
    dash = ("-")
    #SP Stands for single pair.
    SP = PORT[0] + dash + PORT[1] + dash + PORT[2] + dash + PORT[3]
     
    
     
    connection.send ("ED-VDSL2:"+ DSLAM + ":VDSL2-"+str(SP)+ ":3152:::ADSLPROFNM="+ PROF + ",PORTID=14:IS;\n")
     
    time.sleep(4)
    output = connection.recv(100000)
    print(output.decode())


    connection.send("STP-CMDSSN:" + DSLAM  +":COM:" + str(session)+";\n")
    time.sleep(1)
    output = connection.recv(100000)
    print(output.decode())


    connection.send("RTRV-ADSL:"+ DSLAM + ":ADSL-"+str(SP)+":3151;\n")
   
    
    
    time.sleep(.5)
    output = connection.recv(100000)
    print(output.decode())

    
    

    connection.send("exit\n")
    time.sleep(10)

    connection.send("exit\n")
    time.sleep(1)
     
    ssh.close()







Select_AOE_Server()
Access_DSLAM(ip)

Start_tl1()


    







