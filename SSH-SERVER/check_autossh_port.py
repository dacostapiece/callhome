import subprocess
import paramiko
import logging

from config_ssh_server import PORT_TO_CHECK

# Configure logging
logging.basicConfig(filename='/tmp/check_autossh_port.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_ssh_responding(host, port):
    """ Check if SSH is responding on the specified host and port. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=port, username='dummy', password='dummy', timeout=5)
        client.close()
        print("working open port")
        return True
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("not working")
        return False
    except paramiko.ssh_exception.AuthenticationException:
        print("working failed auth - just testing")
        return True  # Authentication failure means SSH is up
    except Exception as e:
        logging.error(f"Unexpected error while checking SSH: {str(e)}")
        print("not working")
        return False

def kill_ssh_process(port):
    """ Kill SSH processes listening on a specific port. """
    try:
        result = subprocess.check_output(
            f"lsof -i :{port} -t", shell=True).decode().strip()
        if result:
            for pid in result.split("\n"):
                subprocess.run(["kill", "-9", pid], check=True)
                logging.info(f"Killed process with PID: {pid} listening on port: {port}")
        else:
            logging.info(f"No process found listening on port: {port}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to find or kill process on port {port}: {e}")

def main():
    # Define the host to check (localhost in this case)
    host = 'localhost'

    # Check if SSH is responding
    if is_ssh_responding(host, PORT_TO_CHECK)==True:
        logging.info(f"SSH on port {PORT_TO_CHECK} is responding. No action required.")
        print(f"SSH on port {PORT_TO_CHECK} is responding. No action required.")
    else:
        logging.warning(f"SSH on port {PORT_TO_CHECK} is not responding. Killing SSH process.")
        print(f"SSH on port {PORT_TO_CHECK} is not responding. Killing SSH process.")
        kill_ssh_process(PORT_TO_CHECK)

if __name__ == "__main__":
    main()
