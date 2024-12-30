
import paramiko
import time


# Note need to build logic to change between VDSL and  ADSL Profiles
# Note need to change the password for the particular servers

print("Adtran EMS Server List")
print("1) East =      10.74.8.166")
print("2) Midwest =   10.74.8.136")
print("3) Central =   10.74.8.167")
print("4) West    =   10.74.8.168")
print("5) Vader   =   10.177.171.73")
print("6) Skywalker = 10.177.171.66")

choice = input("Single Pair ADSL PROFILE PUSH - Choose Adtran EMS Server ")

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
    global port
    DSLAM = input( "Enter DSLAM CLLI: ")
    PORT0 = input ( "Enter DSLAM port eg:for Shelf 1, Rack1, Slot1, Port 1  in format 1111 : ")
    PROF = input ( "Enter SINGLE PAIR ADSL Profile Name: ")
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

    
    dash = ("-")      
    sp= PORT0[0] + dash + PORT0[1] + dash + PORT0[2] + dash + PORT0[3]
        
    
    connection.send ("ED-ADSL:"+ DSLAM + ":ADSL-"+str(sp)+ ":3152:::ADSLPROFNM="+ PROF + ",PORTID=14:IS;\n")
        
            
    time.sleep(4)
    output = connection.recv(100000)
    print(output.decode())
    
    connection.send("STP-CMDSSN:" + DSLAM  +":COM:" + str(session)+";\n")
    time.sleep(1)
    output = connection.recv(100000)
    print(output.decode())


    connection.send("RTRV-ADSL:"+ DSLAM + ":ADSL-"+str(sp)+":3151;\n")
    print("")
    print("")
    
    time.sleep(.5)
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

    







