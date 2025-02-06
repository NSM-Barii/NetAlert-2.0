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

bs = "67.10.155.191"


# IMPORTS 
import ipaddress, socket, threading, time, os, requests
from scapy.all import Ether, ARP, srp



class common_port_scanner():
    """Responsible for performing a multi - threaded port scan of 1024 ports in a couple seconds"""


    def __init__(self):
        self.open_ports = 0
        self.closed_ports = 0
        self.lock = threading.Lock
        pass

    def port_scan(self, ip: str, port: int, table):
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
                   
                    
                else:
                    self.closed_ports += 1

        except socket.gaierror:
            self.closed_ports += 1  
            
        except Exception as e:
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
    
    def threader(self, ip: str, host, mac, vendor):
        """Responsible for calling upon the port scan function for each and every port in range. (1024)"""

        # RESET VALUES 
       # self.open_ports = 0 
       # self.closed_ports = 0
        start = True
        table_name = vendor

        # SET TABLE NAME
        if vendor == "unkown":
            table_name = host 
        
        if host == "unkown":
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
            t = threading.Thread(target=self.port_scan, args=(ip, port, table))
            threads.append(t)

        with Live(table, console=console, refresh_per_second=10):
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

        
        
        console.print(f"\n[bold green]Open Ports: {self.open_ports}[/bold green]")
        console.print(f"[bold red]Closed/Filtered Ports: {self.closed_ports}[/bold red]")
        color = "bold green"
        console.print(f"[bold blue]Vendor:[/bold blue][bold green] {vendor}[/bold green] - [bold blue]Host name:[/bold blue] [{color}]{host}[/{color}] - [bold blue]IP Address:[/bold blue] [{color}]{ip}[/{color}] - [bold blue]MAC Address:[/bold blue] [{color}]{mac}[/{color}]")
        
        # PUT SOME SPAE IN BETWEEN TABLES
        print("\n")


class get_ip_subnet():
    """Once user enters a valid ipaddress or subnet address, that entire network will be scanned with a thread for each and every ip """
    
    def __init__(self, scan_ports = False):
        self.active_ip_count = 0
        self.lock = threading.Lock()
        self.scan_ports = scan_ports
        

    def ip_subnet(self):
        """Responsible for validating user inputted subnet"""
        

        # LOOKS THROUGH UNTIL USER ENTERS VALID SUBNET
        while True:
            try:
                subnet = console.input("[bold blue]Enter subnet range: [/bold blue]")
                valid_subnet = ipaddress.ip_network(subnet)
                return valid_subnet
        

            except (ipaddress.AddressValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
                console.print(e)
            
            except Exception as e:
                console.print(e)
    

    def scan_subnet(self, ip):
        """Responsible for performs subnet scan"""

        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

        result = srp(packet, timeout=5, verbose=False)[0]

        for sent, recieved in result:

            ip = recieved.psrc
            mac = recieved.hwsrc
            
            
            # TRY AND GET THE HOST NAME IF AVAIABLE
            try:
                host = socket.gethostbyaddr(ip)[0]
            
            except socket.gaierror:
                host = "unkown"

            except Exception:
                host = "unkown"
            
            # TRY AND GET VENDOR
            finally:
                vendor = self.get_vendor(mac=mac)
            
            time.sleep(.2)
            # INCREMENT ACTIVE IP COUNT AND SEND ACTIVE RESULTS FORWARD
            with self.lock:   
                self.active_ip_count += 1
                
                if self.scan_ports:
                    common_port_scanner().threader(ip, host, mac, vendor)

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

                return "unknown"
        
        except requests.RequestException as e:
            console.print(mac)
            return "unknown"
        



    
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
            
            print(complete)
            complete +=1
        total = complete
    
        for ip in subnet:
            ip = str(ip)
            t = threading.Thread(target=self.scan_subnet, args=(ip,))
            threads.append(t)
            #print(f"Launching scan on: {ip}")

        for thread in threads:
            print(f"Starting Thread #{t_a} on: {ip}", end='\r', flush=True)
            t_a += 1
            

            thread.start()

        for thread in threads:
            thread.join()
        
        if complete == total:
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
            console.print(f"[bold green]Total Devices found:[/bold green] [bold red]{self.active_ip_count} seconds[/bold red]")
            console.print(f"[bold green]Subnet Scan Completed in:[/bold green] [bold red]{elapsed_time:.2f}[/bold red]")
        
    
    
    def main(self):
        """Responsible for main program output"""
        start = common_port_scanner()
        self.threader()






start = 1

if __name__ == "__main__":
    
    if start == 1:
        nsm = get_ip_subnet(scan_ports=True)
        nsm.threader()


