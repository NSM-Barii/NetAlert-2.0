# PACKET INSPECTION // RATE LIMITING // NETALERT 2.0

# THIS MODULE IS A CHILD OF THE EXTRA_FEATURES MODULE BUT IN ITS OWN DOMAIN FOR BETTER MODULARITY


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console_l = Console()
console_width = console_l.size.width
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
from user_settings import user_settings
from extra_features import Logging, utilities

# BASE DIRECTORY
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetAlert2" / "ip_logging"  
base_dir.mkdir(parents=True, exist_ok=True)

# FILE PATH WAY FOR EACH IP ADDRESS FOUND
path_ip = ""


class packet_rate_limiting():
    """This class will be responsible for keep tracking off the amount of packets being sent by each device within the subnet"""

    def __init__(self):
        self.lock = threading.Lock()
        self.watch_list = []
        pass
    

    def packet_limiting(self, ip: str, console, vendor, host, mac, locker):
        """Keep track of packets for ip param"""

        def limiter(pkt):
            """This will be triggered upon rate limit hit"""

            pkt = str(pkt.summary())
            self.ip_logging(ip=ip, info=pkt)

        
        
        # CHECK TO MAKE SURE DEVICE ISNT ALREADY ON THE WATCHLIST
        listed = any(ip in device for device in self.watch_list)

        if listed == False:
            
            # GET RATE LIMIT AND BACKGROUND THREAD
            load = user_settings().load_file()
            rate_limit = load.get("rate_limit", 500)
            
            # NOW TO MAKE BACKGROUND THREAD TRUE
            load["background_thread"] = True
            user_settings().save_data(changed_data=load)
            background_thread = True

            # NOW TO APPEND IP TO WATCHLIST
            self.watch_list.append(ip)
            console.print(f"Now starting Rate limiting on: {ip} with a limit of: {rate_limit} packets")


            while background_thread:

                # FOR DEBUGGING
                #console.print(background_thread, rate_limit)
                
                try:

                    # THIS IS USED TO CONTINUE THE THREAD OR KILL IT WITHOUT THE USE OF DAEMON SINCE THE PROGRAM MIGHT STILL BE ACTIVE
                    load = user_settings().load_file()
                    rate_limit = load.get("rate_limit", 500)
                    background_thread = load["background_thread"]  

                    use = True
                     
                    count_down = time.time()
                    sniff(filter=f"host {ip}",prn=limiter, store=0, count=rate_limit, timeout=60)

                    count_down_done = time.time() - count_down

                    # RECHECK THE BACKGROUND THREAD AGAIN TO MAKE SURE VALUE IS TRUE
                    if user_settings().load_file()['background_thread']:

                        if count_down_done < 60:
                            console.print(f"[bold red]Rate Limiting Triggered:[/bold red] {ip} [yellow]has sent over {rate_limit} packets in the last minute[/yellow]")
                        
                            if use:
                                with locker:

                                    # LOG THE INCIDENT
                                    log_format = (  
                                        "[yellow][RATE LIMITING TRIGGERED][/yellow] - "  
                                        f"[bold white]IP:[/bold white] [bold cyan]{ip}[/bold cyan] | "  
                                        f"[bold white]MAC:[/bold white] [bold yellow]{mac}[/bold yellow] | "  
                                        f"[bold white]Vendor:[/bold white] [bold magenta]{vendor}[/bold magenta] | "  
                                        f"[bold white]Host:[/bold white] [bold green]{host}[/bold green]"  
                                    )  
                                    Logging().log_results_write(log=log_format, console=console)


                                    # WARN THE USER
                                    utilities().tts(letter=f"RATE LIMITING TRIGGERED ON: {ip}", voice_rate=15)
                                    
                        


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

        pkt = '_'.join(ip.split('.'))
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
                console_l.print(f"Successfully created a designated file path for: {ip}")



# ONLY FOR MODULE TESTING
if __name__ == "__main__":


    ip = "192.168.1.1"
    rate_limit = 50

   # packet_rate_limiting().packet_limiting(ip,rate_limit)


    import os


class testing():

    def count_lines_of_code(directory, extensions=[".py"]):
        total_lines = 0

        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        total_lines += len(lines)

        return total_lines
    
    # Set your project's directory path
    project_directory = "C:/Users/jabar\Documents/NSM Tools/Network Tools/ARP Scanner/united_scripts"  # Change this to your actual path
    lines_of_code = count_lines_of_code(project_directory)

    print(f"Total lines of code: {lines_of_code}")



    def for_php():

        from datetime import datetime

        time_stamp = datetime.now().strftime("%d/%m/%Y")
        console_l.print(time_stamp)
        
        
        if time_stamp == "27/02/2025":
            console_l.print("Your demo is still valid")
        
        else:
            console_l.print("ur trial session is over u can no longer use the demo")
        
    for_php()
