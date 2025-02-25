#THREADED COMMON PORT SCAN // NET ALERT 2.0

# This module is purely theoretical, still in production and working out the logic especially with threading in the mix
# will be working on this until its perfected to then combine into my next project which will involve mass network attacks


# OTHER MODULE IMPORTS
from extra_features import utilities



# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()



# IMPORTS 
import ipaddress, socket, threading, time, os, requests
from scapy.all import Ether, ARP, srp
import manuf
from pathlib import Path

# NETWORK IMPORTS
from scapy.all import DNS, UDP, IP, DNSRR, send, sniff, send, socket, Ether, ARP, ICMP, sendp, sendpfast, send, sr1


# MAIN DIRECTORY
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "LAN Scanner"
base_dir.mkdir(parents=True, exist_ok=True)

# SETTINGS PATH
file_path = base_dir / "settings.json"



class common_port_scanner():
    """Responsible for performing a multi - threaded port scan of 1024 ports in a couple seconds"""


    def __init__(self):
        self.open_ports = 0
        self.filtered_ports = 0
        self.filtered_ports_to_show = 0
        self.closed_ports = 0
        self.lock = threading.Lock
        pass

    def port_scan(self, ip: str, port: int, table, filter):
        """Pass a valid ip which will be scanned with ports 1 - 1024, with a thread created for each port """

        known_ports = {
            465: "smtp",
            587: "smtp",
            2053: "cloudflare",
            2082: "cPanel",
            2083: "cPanel",
            2086: "whm",
            2087: "whm",
            2052: "clearVisn Services",
            2095: "cPanel Webmail",
            2096: "cPanel Webmail",
            2087: "cPanel whm",
            8080: "Http Alternative",
            8443: "Https Alternative",
            8880: "Http Alternative"
        }
       
        
        try:
           with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip, port))

                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    
                    except OSError:
                        service = known_ports.get(port, "unkown")

                    table.add_row(f"{port}", f"{service}" , f"OPEN")
                    
                    self.open_ports += 1
                
             #   elif result ==

                elif result in [111, 113]:
                    self.closed_ports += 1
                    return
                   
                    
                else:
                    self.filtered_ports += 1
                    
                    
                    try:
                        service = socket.getservbyport(port)
                    
                    except OSError:
                        service = known_ports.get(port, "unkown")
                        return
                    
                    self.filtered_ports_to_show += 1

                    if filter:
                        table.add_row(f"{port}", f"{service}" , f"[yellow]FILTERED[/yellow]")
                    
                    return
            
        except socket.timeout:
            self.filtered_ports += 1 

        except socket.gaierror:
            self.closed_ports += 1  
            
        except Exception as e:
            console.print(e)
            self.closed_ports += 1
        
       # finally:
            # NOW TO SCAN UDP PORT
        #    self.port_scan_udp(ip,port,table)
        
    
    def port_scan_udp(self, ip: str, port: int, table):
        """Responsible for udp port scan"""

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip,port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "unkown"

                    table.add_row(f"{port} / udp", f"{service}" , f"OPEN")
                    self.open_ports += 1
                
                else:
                    self.closed_ports += 1
        
        except Exception as e:
            self.closed_ports += 1
    
    def threader(self, ip: str, host, mac, vendor, filter):
        """Responsible for calling upon the port scan function for each and every port in range. (1024)"""

        # RESET VALUES 
       # self.open_ports = 0 
       # self.closed_ports = 0
        start = True
        table_name = vendor

        # USE THIS VARIABLE TO KEEP UNUSED CODE TO COME BACK TO LATER ON
        use = False
        
        if use:
            # SET TABLE NAME
            if vendor == "unkown":
                table_name = host 
            
            if host == "unkown":
                table_name = ip
        
        else:
            table_name = ip


        # CREATE OUTPUT TABLE
        if start:
            table = Table(title=f"[bold green]{table_name}[/bold green]", style="bold purple", header_style="bold red")
            #table = Table(title=f"[bold green]{vendor}[/bold green] - [bold green]{host}[/bold green]\n[blue]{ip}[/blue] - [blue]{mac}[/blue]", style="bold purple", header_style="bold red")
            table.add_column("Port", style="yellow")
            table.add_column("Service", style="bold blue")
            table.add_column("Status", style="bold green")
       
        #table.add_row(f"{host} - {ip} - {mac}")
        
        # STORE THREADS WITHIN THIS LIST
        threads = []
        
        for port in range(1024):
            t = threading.Thread(target=self.port_scan, args=(ip, port, table, filter))
            threads.append(t)

        with Live(table, console=console, refresh_per_second=10):
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

        
        
        console.print(f"\n[bold green]Open Ports: {self.open_ports}[/bold green]")
        console.print(f"[yellow]Filtered Ports w/Services: {self.filtered_ports_to_show}[/yellow]")
        console.print(f"[yellow]Total Filtered Ports: {self.filtered_ports}[/yellow]")
        console.print(f"[bold red]Closed Ports: {self.closed_ports}[/bold red]")
        color = "bold green"
        console.print(f"\n[bold blue]Vendor:[/bold blue][bold green] {vendor}[/bold green] - [bold blue]Host name:[/bold blue] [{color}]{host}[/{color}] - [bold blue]IP Address:[/bold blue] [{color}]{ip}[/{color}] - [bold blue]MAC Address:[/bold blue] [{color}]{mac}[/{color}]")
        
        # PUT SOME SPAE IN BETWEEN TABLES
        print("\n")
        

       # console.input("ENTER TO CONTINUE: ")

class get_ip_subnet():
    """Once user enters a valid ipaddress or subnet address, that entire network will be scanned with a thread for each and every ip """
    
    def __init__(self, scan_ports = False, filtered_scan = False):
        self.active_ip_count = 0
        self.lock = threading.Lock()
        self.scan_ports = scan_ports
        self.filtered_scan = filtered_scan 
        

    def ip_subnet(self):
        """Responsible for validating user inputted subnet"""
        
        keep = True

        # LOOKS THROUGH UNTIL USER ENTERS VALID SUBNET
        while True:
            try:
                subnet = console.input("[bold blue]Enter subnet range: [/bold blue]")
                valid_subnet = ipaddress.ip_network(subnet)
                
                while keep:
                    scan = console.input("Do you want to scan filtered ports [bold green](y/[/bold green][bold red]n): [/bold red]")
                    
                    if scan == "y":
                        self.filtered_scan = True
                        keep = False

                    
                    elif scan == "n":
                        self.filtered_scan = False
                        keep = False
                    
                    else:
                        console.print("[bold red]Try again with a valid input please[/bold red]")
                    
                
                return valid_subnet
        

            except (ipaddress.AddressValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
                console.print(e)
            
            except Exception as e:
                console.print(e)
    

    def scan_subnet(self, ip):
        """Responsible for performs subnet scan"""

        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

        result = srp(packet, timeout=2, verbose=False)[0]

        for sent, recieved in result:

            ip = recieved.psrc
            mac = recieved.hwsrc
            
            
            # TRY AND GET THE HOST NAME IF AVAIABLE
            try:
                host = socket.gethostbyaddr(ip)[0]
            
            except socket.gaierror:
                host = "N/A"

            except Exception:
                host = "N/A"
            
            # TRY AND GET VENDOR
            finally:
                vendor = self.get_vendor(mac=mac)
            
            time.sleep(.0002)
            # INCREMENT ACTIVE IP COUNT AND SEND ACTIVE RESULTS FORWARD
            with self.lock:   
                self.active_ip_count += 1

                if self.filtered_scan:
                    filter = True
                
                else:
                    filter = False
                
                if self.scan_ports:
                    
                    common_port_scanner().threader(ip, host, mac, vendor, filter)

                   # console.print(f"{self.active_ip_count, host, ip, mac}")
               # return host, ip, mac

    def get_vendor(self, mac):
        """Responsible for getting vendor info // Testing and playing around with vendor info"""
        
        url = f"https://api.macvendors.com/{mac}"

        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                return response.text.strip()

            else:
                vendor = utilities.get_vendor(mac)
                vendor = vendor if vendor else "N/A"
                return vendor
                
               
                
        
        except requests.RequestException as e:
            vendor = utilities.get_vendor(mac)
            vendor = vendor if vendor else "N/A"
            return vendor
    
        



    
    def threader(self):
        """Creates a thread for each and every ip address found within the subnet"""
        
        # GET SUBNET
        subnet = self.ip_subnet()

   
        # STORE THREADS IN LIST
        threads = []
        t_a = 1
        start_time = time.time()
        complete = 0

        for p in subnet:
            
            console.print(f"{complete}")
            complete +=1
        
        total = complete

        console.print(f"\nPotential Targets:[bold red] {total}[/bold red]\n")

        for ip in subnet:
            ip = str(ip)
            t = threading.Thread(target=self.scan_subnet, args=(ip,))
            threads.append(t)
            #print(f"Launching scan on: {ip}")

        for thread in threads:
            #print(f"Starting Thread #{t_a} on: {ip}", end='\r', flush=True)
            t_a += 1
            
            thread.start()

        for thread in threads:
            thread.join()
        
       
        elapsed_time = time.time() - start_time
        
        # NOTIFICATION
        from extra_features import utilities
        msg = f"Subnet Scan Complete\n{self.active_ip_count} Devices found on your LAN!"
        ns = utilities()
        ns.noty(msg=msg)
        
        # VOICE
        def results():
            msgg = f"Subnet scan successfully completed, a total of {self.active_ip_count} devices were found on your network!"
            utilities().tts(msgg)

        threading.Thread(target=results).start()
        
        # PRINT TO OUTPUT
        console.print(f"[bold green]Total Devices found:[/bold green] [bold red]{self.active_ip_count}[/bold red]")
        console.print(f"[bold green]Subnet Scan Completed in:[/bold green] [bold red]{elapsed_time:.2f}[/bold red]")
        
    
    
    def main(self):
        """Responsible for main program output"""
        start = common_port_scanner()
        self.threader()






start = 6

if __name__ == "__main__":
    
    if start == 1:
        nsm = get_ip_subnet(scan_ports=True)
        nsm.threader()


        input("\n\nEnter to exit")
    

    elif start == 2:

        time.sleep(20)

        msgg = "NOW PERFORMING GEO LOOKUP ON CODY AND JAWUAN"

        utilities().tts(msgg)

        time.sleep(2)

        msgg = "Targets live in the united states are, State lookup failed, City lookup failed."
        utilities().tts(msgg)

        time.sleep(2)

        msgg = "SAVING TARGET INFO FOR LATER USAGE, OPEN PROGRAM FOR MORE INFO"
        utilities().tts(msgg)

    

        from datetime import datetime

        now = datetime.now()

        time_stamp = now.strftime("%Y-%m-%d  %H:%M:%S")

        console.print(time_stamp)



        table = Table(title="Testing", border_style="green", header_style="bold red")
        table.add_column("Key", style="green")
        table.add_column("Value", style="red")

        import random

        txt = random.randbytes(10)




        with Live(table, console=console, refresh_per_second=4):
            for i in range(1000):
                tr = ["INTRUSION DETECTED", "DEVICE BLACKLISTED", "NEW WHITELIST CREATED", f"SCAN INTERVAL UPDATED TO {i}"]
                num = random.randint(0,3)
                txt = random.randbytes(8)
                ip = random.randint(0,255)
                table.add_row(f"{tr[num]}", f"IP: {ip} | MAC: {txt}")


import pyttsx3

class packet_rate_limiting():
    """This class will be responsible for keep tracking off the amount of packets being sent by each device within the subnet"""

    def __init__(self):
        self.watch_list = []
        pass
    

    def packet_limiting(self, ip: str, rate_limit):
        """Keep track of packets for ip param"""

        def limiter(pkt):
            """This will be triggered upon rate limit hit"""

        # console.print(f"[bold red]Rate Limiting Triggered:[/bold red] {ip} [yellow]has sent over 1,000 packets in the last minute[/yellow]")
            console.print(pkt)

        # CHECK TO MAKE SURE DEVICE ISNT ALREADY ON THE WATCHLIST
        
        console.print(self.watch_list)
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

#packet_rate_limiting().packet_limiting(ip="192.168.1.133", rate_limit=50)



def light():
    ip = "192.168.1.92"
    rate = 180
 


    import asyncio
    from kasa import SmartBulb

    async def control_bulb():
        bulb = SmartBulb("192.168.1.70")
        await bulb.update()  # This needs to be inside an async function
        print(bulb.alias)  # Check if it responds
        # Example action
        
        await bulb.wifi_scan()

        

        await bulb.turn_off()
        time.sleep(1)
        await bulb.turn_on()


    # Run the async function properly
    #asyncio.run(control_bulb())
    console.print("howdy")



    cmd = {"smartlife.iot.smartbulb.lightingservice":{"transition_light_state":{"on_off":0,"ignore_default":1}}}









