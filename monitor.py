# MONITOR MODE MODULE // NETALERT 2.0

# IMPORTS FOR NETWORKING
from scapy.all import ARP, Ether, srp, IP


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()
console_width = console.size.width
import pyfiglet

# ETC IMPORTS
import socket
import time
from datetime import datetime
import requests, json, sys, subprocess, random, threading




class monitor_mode():
    """Solely Responsible for scanning LAN & displaying to the user feedback on scan results"""


    # CLASS METHOD
    watchlist = []
    

    def __init__(self):
        import packet_inspection, extra_features
        self.lock = threading.Lock()
        self.white_list = []
        self.total_devices_in_whitelist = 0
        self.noty_counter = extra_features.utilities()
        self.rate_limiter = packet_inspection.packet_rate_limiting()

    def get_white_list(self):
        """Responsible for getting white list"""

        
        # SEPERATE MODULE IMPORT
        from scanlogic import file_handling 
        data = file_handling()
        device_info = data.load_file(type=2)

        if  device_info ==  None:
           console.print("[bold red]No white list found,[/bold red] [yellow]Returning you to the main menu where u can create one!!![/yellow]")
           subprocess.run([sys.executable, "main.py"])  # Restart the script



        # TABLE FOR WHITE LIST PRINT
        table = Table(title="Current White List", style="bold blue", header_style="bold purple", title_style="purple")
        table.add_column("#")
        table.add_column("Vendor", style="red")
        table.add_column("Host Name", style="bold blue")
        table.add_column("IP Address", style="bold green")
        table.add_column("MAC Address", style="yellow")


        
        # GET DICTIONARY INFO
        for key, value in device_info.items():
            
            key_value = f"{key}. {value}"
            # print(key_value)
            
            # SPLIT INFO INTO SEPARATE VARIABLES & STRIP EXTRA SPACES
            info = [part.strip() for part in value.split('/')]

            vendor = info[0]
            host = info[1]
            ip = info[2]
            mac = info[3]

            # FORMAT DEVICE INFO CONSISTENTLY
            device = f"{ip} / {mac}"

            # NOW TO ADD INFO TO TABLE // TO THEN PRINT IT
            table.add_row(f"{key}", f"{vendor}", f"{host}", f"{ip}", f"{mac}")

            
            # APPEND TO WHITE LIST WITH CLEANED FORMAT
            self.white_list.append(device)
        
        self.total_devices_in_whitelist = key
        console.print(table)
        print("\n")


    def monitor(self):
        """Responsible for performing arp scan and comparing it against white list"""

        # CALL UPON THE WHITE LIST METHOD TO INITIATE/DEFINE THE WHITE LIST.
        self.get_white_list()
        
        # WERE RESULTS WILL BE STORED TO THEN BE COMPARED AGAINST WHITELIST
        device_list = []

        
        # IMPORT SUBNET
        from user_settings import user_settings
        ns = user_settings().load_file()
         
        subnet = ns['subnet_address']
        
        if not subnet:
            console.print("No valid subnet found!")
            import ipaddress
                     
            while True:
                try:
                    subnet = console.input("[bold blue]Enter Network Range:[/bold blue] ")
                    valid_subnet = ipaddress.ip_network(subnet, strict=False)
                    valid_subnet = str(valid_subnet)

                    # NOW TO SAVE SUBNET
                    data = user_settings()
                    load = data.load_file()
                    load["subnet_address"] = valid_subnet
                    data.save_data(changed_data=load)

                    console.print(f"[bold green]Default IP Subnet: {valid_subnet}  Successfully Updated![/bold green]\n\n")
                    time.sleep(1.8)
                    break

                except ipaddress.AddressValueError as e:
                    console.print(e)
                
                except ipaddress.NetmaskValueError as e:
                    console.print(e)

                except Exception as e:
                    console.print(e)


        # FOR TABLE NUMBERS
 
        online_devices = 0
        offline_devices = 0

        # ARP SCAN
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(subnet))
        result = srp(packet, timeout=2, verbose=False)[0]
        
        from extra_features import utilities

        for sent,recieved in result:

            # INFO DIRECTELY FROM ARP
            ip = recieved.psrc
            mac = recieved.hwsrc


            device_info = f"{ip} / {mac}"
            
            device_list.append(device_info)

         
        
        unauthorized_devices = []
        processed_devices = set()  # Track already processed devices

       

        # TABLE FOR AUTHORIZED DEVICES
        table_good = Table(title="Found Authorized Devices", style="bold green", border_style="green", header_style="bold green")
        table_good.add_column("#")
        table_good.add_column("Vendor")
        table_good.add_column("Host Name")
        table_good.add_column("IP Address")
        table_good.add_column("MAC Address")

        # TABLE FOR UNAUTHORIZED DEVICES
        table_bad = Table(title="Found Unauthorized Devices", style="bold red", border_style="bold red", header_style="bold red")
        table_bad.add_column("#")
        table_bad.add_column("Vendor")
        table_bad.add_column("Host Name")
        table_bad.add_column("IP Address")
        table_bad.add_column("MAC Address")

        # NOW TO USE THE TABLES's // TESTING
        
        try:
            with Live(table_good, console=console, refresh_per_second=10):
                for device in device_list[:]:  # Iterate over a copy to allow safe removal
                    device = device.strip()  # Clean up any whitespace
                    if device in processed_devices:
                        continue

                    processed_devices.add(device)  # Add to processed to avoid redundant checks

                    split = device.split('/')
                    
                    # GET IP & MAC
                    ip = split[0]
                    mac = split[1]

                    
                    # GET VENDOR
                    mac = mac.strip()
                    vendor = utilities.get_vendor(mac)
                    
                    # GET HOST NAME
                    ip = ip.strip()
                   # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s
                    try:
                    
                        host = socket.gethostbyaddr(ip)[0].split('.')[0]
     
                    except (socket.herror, socket.gaierror):
                        host = "N/A"

                    except Exception as e:
                        host = "N/A"
                    

                    # WILL GO MORE INTO DEPTH WITH THIS SOON 

                    # FOR ROUTER
                    if ip == "192.168.1.1":
                        router_info = (ip, mac)
                        host = "Gateway"
                    
                    # FOR PLAYSTATIONS
                    if "sony" in vendor or "Sony" in vendor and host == "N/A":
                        host = "Playstation"
            

                    # REDIFNE THE VARIABLE // GET RID OF WHITE SPACES
                    device = f"{ip} / {mac}"

                    is_allowed = any(device.strip() == allowed.strip() for allowed in self.white_list)

                    time.sleep(0.2)


                    if is_allowed:
                        
                  
                        table_good.add_row(f"{online_devices + 1}", f"{vendor}" ,f"{host}", f"{ip}", f"{mac}")
                        online_devices += 1

                    else:

                        device_list.remove(device)  # Safe removal
                        table_bad.add_row(f"{offline_devices +1}",f"{vendor}", f"{host}", f"{ip}", f"{mac}")
                        offline_devices += 1
                        
                        
                        # ADD UNATHORIZED DEVICE TO LIST
                        device = f"Vendor: {vendor} | host: {host} | IP: {ip} | MAC: {mac}"
                        unauthorized_devices.append(device)


        except KeyboardInterrupt as e:
            console.print("\nNow Exiting to main menu", style="bold red")
            time.sleep(1)
            

        print("\n")
        console.print(table_bad)

        num = 0
        if unauthorized_devices:

            # ALERT
            console.print(f"\n\nCAUTION: UNAUTHORIZED DEVICES WERE FOUND ON YOUR NETWORK!\n", style="bold red")

            # GET DISCORD WEBHOOK
            from user_settings import user_settings
            from extra_features import Logging
            
            
            ns = user_settings().load_file()
            webhook = ns["discord_webhook"]
            subnet = ns["subnet_address"]
            intrusion_update = ns["intrusion_updates"]

            kick = utilities()

            
            try:
                for device in unauthorized_devices:

                    # PARSE FOR DEVICE INFO
                    vendor = device.split('|')[0].split(':')[1].strip()
                    host = device.split('|')[1].split(':')[1].strip()
                    ip = device.split('|')[2].split(':')[1].strip()
                    mac = device.split('|')[3].partition(':')[2].strip()
                    
                   
                    #console.print(f"Currently On device: {ip} | {mac}")

                    # LOG INTRUSION  
                    color_out = "bold cyan"  # Adjusted for better contrast  
                    log_format = (  
                        "[bold red][INTRUSION DETECTED][/bold red] - "  
                        f"[bold white]IP:[/bold white] [bold cyan]{ip}[/bold cyan] | "  
                        f"[bold white]MAC:[/bold white] [bold yellow]{mac}[/bold yellow] | "  
                        f"[bold white]Vendor:[/bold white] [bold magenta]{vendor}[/bold magenta] | "  
                        f"[bold white]Host:[/bold white] [bold green]{host}[/bold green]"  
                    )  
                    Logging().log_results_write(log=log_format)

                    

                    # SIMPLE CONSTANT THAT WILL BE USED TO DETERMINE WEATHER PROGRAM WILL GO BEYOND CAPTURING PACKETS
                    type = 2
                    USE = True if type == 1 else False

                    
                    # NOW TO RATE LIMIT THE DEVICE // MONITOR AND RECORD PACKETS
                    threading.Thread(target=self.rate_limiter.packet_limiting, args=(ip, console, vendor, host, mac, self.lock, USE), daemon=True).start()

                    
                    # FOR DIRECTLY INTERACTING WITH LOCAL ROUTER // STILL IN TESTING PHASE MAIN LOGIC IN ROUTER_CONTROLLER MODUEL
                    if type == 1:
                        kick.kick_blacklist(vendor, host, ip, mac)
                    
                    # FOR ARP POISONING ATTACK
                    elif type == 2:
                        threading.Thread(target=kick.kick_arp, args=(ip, mac, router_info, console), daemon=True).start()
                        time.sleep(.5)

                    num += 1

                    # FOR SPACE  // PROOF THAT I DONT EVEN NEED THE NUM VARIABLE LOL 
                    if num != len(unauthorized_devices):
                        print("")
                    
                    else:
                        console.print(f"\nCurrent devices under Network Supervision: {self.rate_limiter.watch_list}")

                    
            
            except Exception as e:
                console.print(f"{e}: {ip}")

                #console.print(f"[bold red]Unauthorized Device Detected![/bold red] → [yellow]{device}[/yellow]")

          
            
           # timestamp = datetime().strftime("%d/%m/%Y - %H:%M:%S")
            content = '\n\n'.join(unauthorized_devices)
            payload = {"content":  f"\nWarning {num} Unauthorized Devices Found on your Network!!!\n\n{content}\n\nDo you want to DOS unathorized users?"}
            

            # CHECKS TO SEE IF INTRUSION UPDATES ARE ON OR OFF // TRUE = SEND
            if intrusion_update:                                
                send = requests.post(webhook, data=json.dumps(payload), headers={"content-type": "application/json"})

                # CHECK STATUS CODE TO MAKE SURE IT WAS SENT SUCCESSFULLY
                if send.status_code == 204:
                    console.print("\nUser Successfully Notified", style="bold green")
                else:
                    console.print("\nFailed to notify user about unathorized devices found on network", style="bold red")
        

        # PRINT FINAL MESSAGE WITH SCAN RESULTS
        total_found = online_devices + offline_devices
        self.total_devices_in_whitelist = int(self.total_devices_in_whitelist)
        whitelist_offline = self.total_devices_in_whitelist - online_devices

        table_results = Table(title="Monitor Mode Results", style='bold green', border_style='bold green')
        table_results.add_column("Variable")
        table_results.add_column("Value")
        
        table_results.add_row("Total Unauthorized Devices", f"{offline_devices}")
        table_results.add_row("Whitelisted Devices Online", f"{online_devices}")
        table_results.add_row("Whitelisted Devices Offline", f"{whitelist_offline}")
        table_results.add_row("Total Whitelisted Devices", f"{self.total_devices_in_whitelist}")
        table_results.add_section()
        table_results.add_row("Total Device Detected", f"{total_found}")
        
        print("\n")
        console.print(table_results)
        
        
        # IMPORT OTHER MODULES FOR MORE FEATURES
        from extra_features import utilities
        

           
        # NOTIFY VOICE ASSISTANT
        
        # PLURAL
        if num > 1: 
            warn = f"{num} unauthorized devices found on your netowrk"
        
        # SINGULAR
        elif num == 1:
            warn = f"{num} unauthorized device found on your netowrk"
        
        
        else:
            warn = f"0 unauthorized devices found, Network safely Secured"   

    

        with self.lock:
            utilities().tts("ATTENTION!")
            time.sleep(0.2)
   
            threading.Thread(target=utilities().tts, args=(warn,)).start()
                    

        # NOTIFY USER OF SCAN
        if num > 0:
            msg = (
                f"🚨 Network Scan Complete 🚨\n"
                f"{num} Unauthorized Device(s) found on your LAN!\n"
                f"Open NetAlert for more details."
            )

        else:
            
            msg = (
                f"✅ Network Scan Complete ✅\n"
                f"{num} Unauthorized Devices found on your LAN!\n"
                f"Congratulations, your network is secure!"
            )

        # IN CHARGE OF KEEPING TRACK OF THE AMOUNT OF NOTIFICATIONS THAT WERE SENT // MEANT TO LIMIT OVERLOADING CONSOLE WITH NOTIFICATIONS
        send = self.noty_counter.noty_count()
        

        # SEND NOTIFICATION
        if send:     
            noty_user = utilities()
            noty_user.noty(msg)  

        # KEEP TRACK OF THE AMOUNT OF MONITOR MODE SCANS COMPLETED // PLACE THIS AT THE END IN CASE OF FAILURE FROM TOP TO BOTTOM
        data = user_settings().load_file()
        data["monitor_mode_scans"] += 1
        user_settings().save_data(changed_data=data)
        
        #time.sleep(3.5)
        #utilities().tts(letter="NOW LAUNCHING DENIAL OF SERVICE ATTACK ACROSS NETWORK WIDE DEVICES", voice_rate=25)
        


    def main(self):
        """In charge of looping through monitor mode"""
    

        # SEPERATE MODULE IMPORT
        from user_settings import user_settings
        main = user_settings()
        content = main.load_file()

        # GET SCAN INTERVAL VARIABLE
        interval = content["scan_interval"]
        interval = int(interval)

        # GET SUBNET
        subnet = content["subnet_address"]

        # GET TOTAL MM SCANS COMPLETED
        times = content["monitor_mode_scans"]

        print("\n\n")
        scan_interval = interval * 60


        while True:
            try:

                # CREATE TIMESTAMPS
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # UPDATE TIMES VALUE EACH ITERATION
                content = main.load_file()
                times = content["monitor_mode_scans"]

                # VALUES
                console.print(f"\n\n[bold blue]Scans Completed:[/bold blue] [bold green]{times}[/bold green]")
                console.print(f"[bold blue]TimeStamp:[/bold blue] {timestamp}")
                console.print(f"[bold blue]Subnet: [/bold blue] [bold green]{subnet}[/bold green]")
                console.print(f"[bold blue]Scan Interval:[/bold blue] [bold green]{interval} Minutes[/bold green]\n\n")
                
                self.monitor()
                print("\n\n")
       
               
               # WANT TO MAKE TIMER COUNTDOWN IN SEPERATE THREAD SO U CAN SCOLL THROUGH CMD FREELY !!!
               # def live_timer():

                     
                timer = interval * 60
                panel_t = Panel(f"[bold red]Beginning next subnet scan in:[/bold red][bold green] {timer}[/bold green]        ",
                                border_style="bold red",
                                expand=False
                                #width=min(130, console_width - 2)
                                ) 

                with Live(panel_t, console=console, refresh_per_second=10):
                    while timer > 0:
                    
                        timer -= 1
                        time.sleep(1)
                        panel_t.renderable = f"[bold red]Beginning next subnet scan in:[/bold red][bold green] {timer}[/bold green]"
                
                            

            except KeyboardInterrupt as e:
                print("")
                console.print("Now exiting program", style="bold red")
                time.sleep(.6)
                break
            
            except Exception as e:
                console.print(f"Exception Error: {e}")
                time.sleep(.6)
            




if __name__ == "__main__":
    """This is strictily for testing this module"""

    type = 3

    if type == 1:
        nsm = monitor_mode()
        nsm.get_white_list()
        nsm.monitor()
        input("press enter to leave the program monitor mode: ")

    elif type == 2:
        nsm = monitor_mode()
        nsm.monitor()

    elif type == 3:
        nsm = monitor_mode()
        nsm.main()


