import subprocess
import time
from config import vpn_probe_target

def check_tun0_ip():
    try:
        # Check if tun0 interface has an IP address
        ip_check = subprocess.check_output(['ip', 'addr', 'show', 'tun0']).decode('utf-8')
        if 'inet ' in ip_check:
            return True
    except subprocess.CalledProcessError:
        pass
    return False

def ping_ip(ip, timeout=60):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            # Ping the IP address
            ping_check = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if ping_check.returncode == 0:
                return True
        except subprocess.SubprocessError:
            pass
        time.sleep(1)
    return False

def check_vpn_connection():
    if check_tun0_ip():
        if ping_ip(vpn_probe_target):
            print("Remote probe ", vpn_probe_target, " is responding!")
            return True
        else:
            print("Dev tun0 has IP address, but remote target isn't replying")
            return False
    else:
        print("Dev tun0 doesnt exist - OpenVPN is not working at all")
        return False