# PACKET INSPECTION // RATE LIMITING // NETALERT 2.0

# THIS MODULE IS A CHILD OF THE EXTRA_FEATURES MODULE BUT IN ITS OWN DOMAIN FOR BETTER MODULARITY


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

# FILE PATH WAY FOR EACH IP ADDRESS FOUND
path_ip = ""


class packet_rate_limiting():
    """This class will be responsible for keep tracking off the amount of packets being sent by each device within the subnet"""

    def __init__(self):
        self.watch_list = []
        pass
    

    def packet_limiting(self, ip: str, rate_limit):
        """Keep track of packets for ip param"""

        def limiter(pkt):
            """This will be triggered upon rate limit hit"""

            pkt = str(pkt.summary())
            self.ip_logging(ip=ip, info=pkt)

        
        
        # CHECK TO MAKE SURE DEVICE ISNT ALREADY ON THE WATCHLIST
        listed = any(ip in device for device in self.watch_list)

        if listed == False:

            # NOW TO APPEND IP TO WATCHLIST
            self.watch_list.append(ip)
            console.print(f"Now starting Rate limiting on: {ip} with a limit of: {rate_limit} packets")
        

            while True:
                try:
                     
                    count_down = time.time()
                    sniff(filter=f"host {ip}",prn=limiter, store=0, count=rate_limit)

                    count_down_done = time.time() - count_down

                    if count_down_done < 60:
                        console.print(f"[bold red]Rate Limiting Triggered:[/bold red] {ip} [yellow]has sent over {rate_limit} packets in the last minute[/yellow]")
                    
                        # TESTING PURPOSES WILL CLEAN THIS SCRIPT UP SOON
                        

                        end = ip.split('.')[3]

                        #name = random.randint(1, end)
                        user_id = f"engine_{end}"
                        console.print(user_id)
                        user_id = pyttsx3.init()
                        
                        rate = user_id.getProperty('rate')

                        user_id.setProperty('rate', 160)

                        voices = user_id.getProperty('voices')
                        user_id.setProperty('voice', voices[1].id)
                        user_id.say("RATE LIMITING TRIGGERED")
                        user_id.runAndWait()
                    


                    else:
                        console.print(f"[bold green]Device:[/bold green] {ip}[yellow] has passed the check[/yellow]")
            
                except Exception as e:
                    console.print(e)
 


        # FOR TESTING PURPOSES TO MAKE SURE THIS IS WORKING
        else:
            console.print(f"Device: {ip} is already inside of the watchlist")


    
    def ip_logging(self,ip: str, info: any):
        """This method will be responsible for logging any and all traffic flowing through said ip address"""
        

        # THIS WILL SPLIT THE . OUT OF THE IP AND REPLACE IT WITH _
        ips = ip.split('.')   
        pkt = []
        for i in ips:
            pkt.append(i)
      
        pkt = '_'.join(pkt)  
        path = base_dir / pkt
        date = datetime.now()

        # LOOP IN CASE OF EXCEPTION
        while True:
            timestamp = date.strftime("%Y-%m-%d %H:%M:%S")
            path = f"{path}.txt"
            try:
                with open(path, "a") as file:
                    msg = f"Timestamp: {timestamp}  -  {info}\n"
                    file.write(msg)

                    break
            
            except FileNotFoundError as e:
                console.print(f"Successfully created a designated file path for: {ip}")



# ONLY FOR MODULE TESTING
if __name__ == "__main__":

    ip = "192.168.1.1"
    rate_limit = 50

    packet_rate_limiting().packet_limiting(ip,rate_limit)
