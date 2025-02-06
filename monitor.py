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
import requests, json




class monitor_mode():
    """Solely Responsible for scanning LAN & displaying to the user feedback on scan results"""
    

    def __init__(self):
        self.white_list = []
        self.total_devices_in_whitelist = 0

    def get_white_list(self):
        """Responsible for getting white list"""

        
        # SEPERATE MODULE IMPORT
        from scanlogic import file_handling 
        data = file_handling()
        device_info = data.load_file(type=2)


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
                    try:
                        host = socket.gethostbyaddr(ip)[0].split('.')[0]
                        
                    
     
                    except (socket.herror, socket.gaierror):
                        host = "unknown"

                    except Exception as e:
                        host = "unknown"
                    

                    # FOR ROUTER
                    if ip == "192.168.1.1":
                        host = "Router"

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
                        device = f"Vendor: {vendor} - host: -{host} - IP: {ip} - MAC: {mac}"
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
            
            
            ns = user_settings().load_file()
            webhook = ns["discord_webhook"]
            subnet = ns["subnet_address"]
            intrusion_update = ns["intrusion_updates"]
            


            for device in unauthorized_devices:
                #data[num] = f"Unathorized Device: {device}"
                num += 1

                #console.print(f"[bold red]Unauthorized Device Detected![/bold red] → [yellow]{device}[/yellow]")


            
           # timestamp = datetime().strftime("%d/%m/%Y - %H:%M:%S")
            content = '\n'.join(unauthorized_devices)
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


        utilities().tts("ATTENTION!")
        time.sleep(0.4)
        utilities().tts(warn)
                    

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


        # SEND NOTIFICATION
        noty_user = utilities()
        noty_user.noty(msg)  


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

        print("\n\n")
        scan_interval = interval * 60


        while True:
            try:

                # CREATE TIMESTAMPS
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                console.print(f"\n\n[bold blue]TimeStamp:[/bold blue] {timestamp}")
                console.print(f"[bold blue]Subnet: [/bold blue] [bold green]{subnet}[/bold green]")
                console.print(f"[bold blue]Scan Interval:[/bold blue] [bold green]{interval} Minutes[/bold green]\n\n")
                self.monitor()
                print("\n\n")

                for i in range(interval * 60,0,-1):
                    print(f"Beginning next Subnet Scan in: {i} Seconds", end='\r', flush=True)     
                    time.sleep(1)


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


