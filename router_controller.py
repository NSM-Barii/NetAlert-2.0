# THIS MODULE IS A CHILD OF THE PACKET INSPECTION MODULE // NETALERT 2.0
# THIS MODULE WILL HOUSE AND ANY ALL LOGIC FOR INTERACTING FOR EXTERNAL GATEWAY


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()
console_width = console.size.width
import pyfiglet

# IMPORTS
import requests, time, os, socket
from plyer import notification
import pyttsx3, threading
from pathlib import Path
from datetime import datetime
import openai, random, pyttsx3
from datetime import datetime


# NETWORK IMPORTS
from scapy.all import IP, send, UDP, ICMP, sr1flood, sr1, ARP, Ether, sendp, sendpfast, sniff


# FILE HANDLING
from pathlib import Path

# BASE DIRECTORY
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetAlert2" / "ip_logging"  
base_dir.mkdir(parents=True, exist_ok=True)


# ROUTER IMPORTS
from pyglinet.glinet import GlInet

use = False
if use:

    try:
        # LOGIC FOR API COMMANDS TO FLINT 2 ROUTER
        router = GlInet(url="http://192.168.1.1", username="Admin")

        console.print("howdy",router)

        router.login()

        devices = router.__request_with_sid("GET", "router/clients")

        console.print(devices)

    except Exception as e:
        console.print(e)


class Router_Controller():
    """This class will be used to control the router of a Gli-net ( Flint 2 )"""

    def __init__(self):
        pass
    

    def login(self, router_ip: str = "192.168.1.1"):
        """This will be responsible for logging the user in"""

        
        # SET VARIABLE INFO
        url = f"http://{router_ip}/api/login"

        payload = {
            "username": "",
            "password": ""
        }

        try:

            session = requests.Session()

            login = session.post(url=url, json=payload , verify=False)

            if login.status_code == 200:

                console.print("successfull login", style="bold green")
                return session

            else:

                console.print("failed to Login", style="bold red")
                return False
            

        except Exception as e:
            console.print(e)
            return False
    

    def get_devices(self):
        """This will display all the currently connected devices on the network"""

        session = self.login()
        
        try:
            if session:

                devices = session.get(url="http://192.168.1.1/api/clients", verify=False )

                if devices.status_code == 200:
                    console.print("\nvalid\n", style="bold blue")
                    console.print(devices.text)

        
        except Exception as e:
            
            console.print(e)


# FOR MODULE TESTING
if __name__ == "__main__":


    Router_Controller().get_devices()
