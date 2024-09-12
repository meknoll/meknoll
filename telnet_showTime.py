import telnetlib

# Define device details
HOST = "<your_device_ip>"
PORT = 23
USER = "<your_username>"
PASSWORD = "<your_password>"
PROMPT = b"$"  # Adjust this based on your device's prompt

def telnet_login(host, user, password, prompt, port=23):
    try:
        # Establish connection
        tn = telnetlib.Telnet(host, port)

        # Read until login prompt
        tn.read_until(b"login: ")
        tn.write(user.encode('ascii') + b"\n")

        # Read until password prompt
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        # Wait until the prompt after login
        tn.read_until(prompt)
        return tn

    except Exception as e:
        print(f"Error during connection: {e}")
        return None

def execute_command(tn, command, prompt):
    try:
        # Send command
        tn.write(command.encode('ascii') + b"\n")

        # Read until the prompt returns
        output = tn.read_until(prompt).decode('ascii')
        return output
    except Exception as e:
        print(f"Error executing command: {e}")
        return None

def main():
    # Establish connection and login
    tn = telnet_login(HOST, USER, PASSWORD, PROMPT)
    if tn:
        print("Connected to device.")

        # Execute 'show time' command
        output = execute_command(tn, "show time", PROMPT)
        if output:
            print("Command output:")
            print(output)

        # Close connection
        tn.write(b"exit\n")
        tn.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
