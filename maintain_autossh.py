#!/usr/bin/env python3
import subprocess
import logging

# Configure logging
logging.basicConfig(filename='/tmp/maintain_autossh_script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def restart_autossh():
    """ Restart autossh process. """
    try:
        subprocess.run(["killall", "autossh"], check=True)
        logging.info("Stopped existing autossh process.")
        print("Stopped existing autossh process.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to stop autossh: {e}")
        print(f"Failed to stop autossh: {e}")

restart_autossh()
