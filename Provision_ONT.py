import getpass
import telnetlib
import time
import json

# Load the configuration from the JSON file
with open('var.json', 'r') as file:
    config = json.load(file)

# Assign variables from JSON configuration
HOST = config['HOST']
user = config['user']
password = config['password']
ONT_Port = config['ONT_Port']
eth_svc = config['eth_svc']
bw_profile = config['bw_profile']
st_act = config['ST_Act']
outer_vlan = config['outer_vlan']
inner_vlan = config['inner_vlan']

# Check if the following keys are present in the config and set default values if needed
mcast_profile = config.get('mcast_profile', 'default_mcast_profile')  # Define or provide default
description = config.get('description', 'default_description')        # Define or provide default
pon_cos = config.get('pon_cos', 'default_pon_cos')                    # Define or provide default

# Telnet connection setup
tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")

if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

# Disable session pager
tn.write(b"set session pager disabled\n")
time.sleep(5)

# Send command with formatted variables
command = (
    f"add eth-svc {eth_svc} to-ont-port {ONT_Port} bw-profile {bw_profile} "
    f"svc-tag-action {st_act} outer-vlan {outer_vlan} inner-vlan {inner_vlan} "
    f"mcast-profile {mcast_profile} description {description} pon-cos {pon_cos} "
    f"admin-state enabled\n"
)
tn.write(command.encode('ascii'))  # Ensure command is encoded to ASCII
time.sleep(5)  # Allow some time for the command to execute

tn.write(b"set ont-port 1/g1 admin-state disabled\n")
time.sleep(5)
tn.write(b"set ont-port 1/g1 admin-state enabled\n")
time.sleep(90)
tn.write(b"show dhcp leases ont-port 1/g1\n")

# Exit the Telnet session
tn.write(b"exit\n")

# Print the output from the Telnet session
print(tn.read_all().decode('ascii'))
