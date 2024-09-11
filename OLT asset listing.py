import telnetlib
import paramiko
import time
import getpass
#from netmiko import ConnectHandler
#from xtelnet import Telnet

# Dictionary of lab OLT's configuration
olt = {
    'AXS2200GPON': ['10.177.174.44', 'GPON', 'Fort Wayne', 'Motorola AXS2200', 'Telnet'],
    'MRCCGPONOL1': ['10.177.174.43', 'GPON', 'Fort Wayne', 'Motorola AXS2200', 'Telnet'],
    'FWINALUOLT5': ['10.177.174.55', 'GPON', 'Fort Wayne', 'Nokia 7342', 'Telnet'],
    'FWINALUOLT6': ['10.177.174.56', 'GPON', 'Fort Wayne', 'Nokia 7342', 'Telnet'],
    'FWINALUOLT7': ['10.177.174.57', 'GPON', 'Fort Wayne', 'Nokia 7342', 'Telnet'],
    'LWVLLABN7342P01': ['10.224.131.126', 'GPON', 'Lewisville', 'Nokia 7342', 'Telnet'],
    'CalixOLT9': ['10.177.171.178', 'GPON', 'Fort Wayne', 'Calix E7-20', 'Telnet'],
    'IPDE7HV2L03': ['10.240.6.159', 'GPON', 'Fort Wayne', 'Calix E7-2', 'Telnet'],
    'IPDE7HV2L07': ['10.224.130.36', 'GPON', 'Fort Wayne', 'Calix E7-2', 'Telnet'],
    'LWVLLABCE72P01': ['10.224.131.198', 'GPON', 'Lewisville', 'Calix E7-2', 'Telnet'],
    'FTWYLAB7360DP10': ['10.240.6.177', 'XGS-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'FTWYLAB7360DP11': ['10.224.134.10', 'XGS-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'FTWYLABN7360DP12': ['10.240.6.229', 'XGS-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'FTWYLABN7360DP13': ['10.240.6.230', 'XGS-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'FTWYLABN7360DP15': ['10.224.141.2', 'XGS-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'FTWYLAB7360DP16': ['10.224.141.18', 'XGS-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'FWINALUOLT8': ['10.177.174.79', 'X&G-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'FWINALUOLT09': ['10.240.6.227', 'XGS-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'IPD7360DEV01': ['107.191.129.103', 'GPON', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'IPD7360PTE01': ['107.191.129.26', 'GPON', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'IPD7360VNG00': ['10.240.6.130', 'GPON', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'FTWYIN736025G': ['10.240.6.228', '25G-Pon', 'Fort Wayne', 'Nokia 7360', 'SSH'],
    'LWVLLABN7360P02': ['10.224.131.37', 'XGS-Pon', 'Lewisville', 'Nokia 7360', 'SSH'],
    'LWVLLABN7360P04': ['10.224.131.214', 'XGS-Pon', 'Lewisville', 'Nokia 7360', 'SSH'],
    'LWVLLABN7360P05': ['10.224.131.101', 'XGS-Pon', 'Lewisville', 'Nokia 7360', 'SSH'],
    'LWVLLABN7360P06': ['10.224.131.69', 'XGS-Pon', 'Lewisville', 'Nokia 7360', 'SSH'],
    'LWVLLABN7360P07': ['10.224.131.40', 'XGS-Pon', 'Lewisville', 'Nokia 7360', 'SSH'],
    'LWVMLABN7360P01': ['10.224.131.35', 'XGS-Pon', 'Lewisville', 'Nokia 7360', 'SSH'],
    'LWVMLABN7360P02': ['10.224.131.36', 'X&G-Pon', 'Lewisville', 'Nokia 7360', 'SSH'],
}

# Print OLT selection list
for index, (olt_name, details) in enumerate(olt.items(), start=1):
    print(f'{index}: OLT: {olt_name}, IP address: {details[0]}')

# Select OLT to pull inventory from
while True:
    try:
        sel = int(input('Input OLT selection number: '))
        selected_olt = list(olt.keys())[sel - 1]
        host = olt[selected_olt][0]
        cli_access = olt[selected_olt][4]
        break
    except (IndexError, ValueError):
        print('Invalid selection. Please input the number corresponding to the OLT.')

# Function to establish Telnet connection
def telnet_connect(host):
    retrycount = 0
    while retrycount < 4:
        try:
            tn = telnetlib.Telnet(host)
            return tn
        except Exception as e:
            print(f'Telnet error: {e}. Retrying in 5 seconds...')
            time.sleep(5)
            retrycount += 1
    print('Failed to connect via Telnet after multiple attempts.')
    return None


# Function to connect to SSH
def ssh_connect(host, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password, timeout=10)
        print(f"Connected to {host} via SSH")
        return client
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection: {e}")
    except Exception as e:
        print(f"Error connecting to {host} via SSH: {e}")
    return None

#define Calix command set, commands to be issued to retrieve ONT list

#define Nokia command set, commands to be issued to retrieve ONT list


# Check CLI access method and connect accordingly
if cli_access == 'Telnet':
    # Establish Telnet connection
    tn = telnet_connect(host)
    
    if tn:
        # Prompt for user credentials
        user = input('Please enter username: ')
        password = getpass.getpass('Please enter password: ')
        
        # Send username and password
        tn.read_until(b'Username: ')
        tn.write(user.encode('utf-8') + b'\n')
        tn.read_until(b'Password: ')
        tn.write(password.encode('utf-8') + b'\n')
        #define commands based on OLT make/model
        #define commands for Motorola
        if olt[selected_olt][3] == 'Motorola AXS2200':
            for pon in range(3, 19):
                for port in range(1, 5):
                    # Construct and send command
                    command = 'show pon au-' + str(pon) + '-' + str(port)
                    tn.write(command.encode('utf-8') + b'\n')
                    
                    # Read and print response
                    rcvd_msg = tn.read_until(b'>')
                    print("Sent Command:", command)
                    print(rcvd_msg.decode('utf-8'))
                    
                    time.sleep(2)
        #define commands for Calix
        elif olt[selected_olt][3] == 'Calix E7-20' or olt[selected_olt][3] == 'Calix E7-2':
            for pon in range(1, 21):
                for port in range(1, 9):
                    # Construct and send command
                    command = 'show ont on-gpon-port ' + str(pon) + '/' + str(port)
                    tn.write(command.encode('utf-8') + b'\n')
                    
                    # Read and print response
                    rcvd_msg = tn.read_until(b'>')
                    print("Sent Command:", command)
                    print(rcvd_msg.decode('utf-8'))

                    time.sleep(2)

        # Close the Telnet connection
        tn.close()
        print('Telnet connection closed')


elif cli_access == 'SSH':
    # Prompt for user credentials
    user = input('Please enter username: ')
    password = getpass.getpass('Please enter password: ')

    # Establish SSH connection
    sc = ssh_connect(host, user, password)

    if sc:
        try:
            # Example: Execute a command
            stdin, stdout, stderr = sc.exec_command('echo "SSH connection successful"')

            # Read command output and errors
            output = stdout.read().decode()
            errors = stderr.read().decode()

            if output:
                print("Output:", output)
            if errors:
                print("Errors:", errors)
            
        except paramiko.SSHException as e:
            print(f"SSHException encountered: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            # Ensure the SSH connection is closed
            sc.close()
            print('SSH connection closed')

#write output to text file
tn.write(b"exit\n")
file=tn.read_all()
datacap=open(".ONTAudit.txt" , "w+")
file=file.decode('UTF-8')
datacap.write(file)
datacap.close()
tn.close()
print('Session Closed')
fhandle=open("ONTAudit.txt")
for line in fhandle:
		line = line.rstrip()
        #strip off the newline character
wds = line.split()
        #splits the line into words separated by spaces
print(wds)
channel = wds[1]
serial = wds[2]
location = wds[0]
Equipment_ID = wds[5]
		#pull out the desired words
print(location, channel, serial, Equipment_ID)
print('oltid + location + channel + serial + Equipment_ID')
tn.read_until(b'oltid')
tn.close()