import paramiko
import time
import re
print("Adtran EMS Server List")
print("1) East =      10.74.8.166")
print("2) Midwest =   10.74.8.136")
print("3) Central =   10.74.8.167")
print("4) West    =   10.74.8.168")
print("5) Vader   =   10.177.171.73")
print("6) Skywalker = 10.177.171.66")

count = 0
choice = input ("Enter a number between  1 and 6: ")

while (True):
    
    def choose_server():
        global ip
        global login
        global passwd
        global server
    
    if choice == "1":
        ip  = "10.74.8.166" 
        login = "ems"
        passwd = "Admin123!"
        server = "East"
        break
    elif choice == "2":
        ip = "10.74.8.136"
        login = "ems"
        passwd = "Admin123!"
        server = "Midwest'"
        break
    elif choice == "3":
        ip = "10.74.8.167"
        login = "ems"
        passwd = "Admin123!"
        server = "Central"
        break
    elif choice == "4":
        ip = "10.74.8.168"
        login = "ems"
        passwd = "Admin123!"
        server = "West"
        break
    elif choice == "5":
        ip = "10.177.171.73"
        login = "ems"
        passwd = "Admin123!"
        server = "Vader"
        break
    elif choice == "6" :
        ip = "10.177.171.66"
        login = "ems"
        passwd = "Admin123!"
        server = "Skywalker"
        break
    else:
        print('ERROR: please choose a number between 1-6!')
count = count + 1
        



def ssh_conn(ip):
   
   #date_time = datetime.datetime.now().strftime("%Y-%m-%d)
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=22, username=login, password=passwd, look_for_keys=False, timeout=None)
    global connection
    connection = ssh.invoke_shell()
    time.sleep(2)
    

def get_sql_log():
    global name
    partnum = input ("Put a single quote before the part number as in ('1187016F1) ")
    name = input ("Enter Card Name ")
        
    # Emulating command: /opt/dorado/mysql/bin/mysql -D reportsplus -e "SELECT * from EQUIPMENT WHERE partNumber IN ('1187133F1', '1187120L1', '1187130F1')"
    
    connection.send('/opt/dorado/mysql/bin/mysql -D reportsplus -e "SELECT * from EQUIPMENT WHERE partNumber LIKE ' + partnum + '\'"\n')
    #connection.send('''/opt/dorado/mysql/bin/mysql -D reportsplus -e "SELECT * from EQUIPMENT WHERE partNumber LIKE ''' + """ ' """ + partnum + """ ' """ "\n''')
    print('working.......')
    time.sleep(2)
    time.sleep(1)
    print("5....")
    time.sleep(1)
    print("4....")
    time.sleep(1)
    print("3....")
    time.sleep(1)
    print("2....")
    time.sleep(1)
    print("1....")
    output = connection.recv(100000)
    output = output.decode("ascii")
    
    
#def save_to_file():
    output = output.strip()
    #Create File
    File=open("./Inventory "+ server + " _ " + name + "_Access_Modules.csv","w+" )
    File=open("./" + server + " _ " + name + "_Access_Modules.csv","w+" )
    
    #File.write(output)
    for line in File:
        line = line.rstrip
        if line.startswith("|"):
            print(line)
            
    File.write(output)
    File.close
   
    
def finish_program():
    #Exit SQL process in server
    connection.send('\x03')
    response1 = connection.recv(100)
    print(response1)
    #Exit Server
    connection.send ("exit")
    response2 = connection.recv(100)
    print(response2)
    print("See Inventory File on Computer")
    time.sleep(5)
   
  
choose_server()
ssh_conn(ip)
get_sql_log()
#save_to_file()
finish_program()



