# ARP SCANNER / SEMI - IPS SYSTEM         # DEVELOPED BY NSM BARII


# IMPORTS FOR OTHER PROGRAM MODULES
from monitor import monitor_mode
from user_settings import settings_menu


# NETWORK IMPORTS
from scapy.all import Ether, IP, ARP, srp, json
import ipaddress, socket

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()
console_width = console.size.width
import pyfiglet

# ETC IMPORTS
import threading, requests, random, os, time
from plyer import notification 




class arp_scanner():
    """Responsible for performing arp scan across network"""
    lock = threading.Lock()

    def __init__(self):
        self.lock = threading.Lock()
        self.active_devices = 0
        self.ative_device_list = []
        self.data = file_handling()

    def ip_subnet(self):
        """Verifies that user inputs a valid IP Range"""
        
        # LOGIC FOR DEFAULT SUBNET
        from user_settings import user_settings
        data = user_settings().load_file()
        default_subnet = data["subnet_address"]
        
        if default_subnet:
            option = f"( or Press Enter for {default_subnet} )"
        else:

            option = ""

        while True:
            try:
                console.print(f"\n[bold green]Default Subnet currently set to:[/bold green] [bold red]{default_subnet}[/bold red]\n\n")
                subnet = console.input(f"[bold blue]Enter Network Range [/bold blue][bold green]{option}[/bold green]: ")
                if subnet == "":
                    subnet = default_subnet 
                valid_subnet = ipaddress.ip_network(subnet, strict=False)
                return valid_subnet
            

            except ipaddress.AddressValueError as e:
                console.print(e)
            
            except ipaddress.NetmaskValueError as e:
                console.print(e)

            except Exception as e:
                console.print(e)
        
    
    def threader(self,target):
        """Creates a thread for each ip in the network range"""

        table = Table(title="ARP Scan", style="purple", header_style="bold red", title_style="bold red")
        table.add_column("#")
        table.add_column("Vendor", style="red")
        table.add_column("Host Name", style="bold green")
        table.add_column("IP Address", style="bold blue")
        table.add_column("MAC Address", style="yellow")

    

        subnet = self.ip_subnet()
        threads = []
         
        # SOME SPACE BETWEEN PRINTS
        print("\n")
    
        
    
        for ip in subnet:
            t = threading.Thread(target=target, args=(ip, table))
            threads.append(t)
     


        with Live(table, console=console, refresh_per_second=4):

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
   
    
    def arp_scan(self, ip, table):
        """Performs the actual layer 2 subnet scan"""

        # FOLDER IMPORT
        from extra_features import utilities
        
        
        valid_ip = str(ip)
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=valid_ip)
        
        result = srp(packet, timeout= 2, verbose=False)[0]

        
    
        for sent, recieved in result:

            ip_found = recieved.psrc
            mac_found = recieved.hwsrc
            vendor = utilities.get_vendor(mac=mac_found)

            try:

                host = socket.gethostbyaddr(ip_found)
                host = host[0]                           # PULL ONLY THE HOST NAME AND DITCH THE IP          
                host_unsplit = host.split('.')                    # CUTS OUT THE .IAN  //  EXAMPLE   LAPTOP.IAN   INSTEAD, LAPTOP
                host = host_unsplit[0]                            # STORES BACKINTO THE HOST VARIABLE
            
            except socket.gaierror as e:
                host = "unknown"

            except Exception as e:
                host = "unknown"


            with self.lock:
                self.active_devices += 1

                # GET VENDOR
                
            
                # CREATE A KEY COMBO THAT WE CAN THEN USE LATER
                key_combo = f"{self.active_devices} / {vendor} / {host} / {ip_found} / {mac_found}" 

                table.add_row(f"{self.active_devices}", f"{vendor}", f"{host}", f"{ip_found}", f"{mac_found}")
                self.ative_device_list.append(key_combo)
                
                
    
    def main(self):
        """Responsible for main run"""

        self.active_devices = 0
        self.threader(target=self.arp_scan)
        print("")
        #console.print(f"[bold blue]Total Active Devices:[/bold blue] [bold green]{self.active_devices}[/bold green]")

        # SAVE THE SCAN RESULTS WITH // THE DATA CLASS
        self.data.create_file(letter=self.ative_device_list, type=1)


class white_list():
    """Responsible for allowing the user to choose to choose what devices they want to white list"""

    def __init__(self):

        # FILE VARIABLES
        self.data = file_handling()
        self.utilities = extra_shii()

        # FOR STORING WHITE LIST VARIABLE


    def device_list(self):
    
        # LOAD DEVICES
        devices = self.data.load_file(type=1)

        # CREATE A EMPTY LIST FOR STORING IPS, DEFINE WHITE LIST FOR USER INPUT AND CHOICES SO USER CANT REPEAT THE SAME INPUT
        keys = []
        white_list = []
        choices = []
        print(keys)
        

        show = False
        picked = False
        error = False

        
        while True:

            # NOW TO PRINT SAID DEVICES
            for key, value in devices.items():

                if show:
                   print(f"{key}: {value}")
                
                keys.append(key)



            # NOW ALLOW THE USER TO CHOOSE WHICH DEVICES TO WHITE LIST
            try:
                if error:
                    if e_type == 1:
                        console.print("\n\nunable to append all devices since the current white list isnt empty\n", style="bold red")
                    
                    elif e_type == 2:
                        console.print("\n\nCannot duplicate inputs: Please try again\n", style="bold red")
                    
                    elif e_type == 3:
                        console.print("\n\nCannot add a invalid key: Please try again\n", style="bold red")
                    

                    error = False
                    e_type = 0




                console.print("\n[bold blue]All[/bold blue] == [bold green]whitelist all devices[/bold green] - [bold blue]Exit[/bold blue] == [bold red]to leave[/bold red]")
                choice = console.input("\n[bold blue]Choose the device you want to[/bold blue] [bold green]whitelist:[/bold green] ")

                try:

                    choice = choice.strip().lower()
                  #  console.print("yu were stripped")
                
                except Exception:
                    pass


                # TO EXIT 
                if choice == "exit":
                    
                    # PRINT USER MADE WHITE LIST
                    self.utilities.clear_screen()
                    console.print("Here is your current white list:\n", style="bold green")
                    console.print(white_list)

                    # NOW TO SAVE WHITE LIST TO FILE 
                    self.data.create_file(letter=white_list, type=2)
                    
                   # console.print("White List Successfully Created! ", style="bold green")
                    console.print(f"Now exiting", style="bold red")
                    time.sleep(2)
                    break
                
                # TO APPEND ALL DEVICES TO THE WHITELIST
                elif choice == "all":

                    if picked:
                        self.utilities.clear_screen()
                       # console.print("\nunable to append all devices since the current white list isnt empty", style="bold red")
                        console.print("Current White List:", style="bold blue\n")
                        console.print(white_list)  
                        print("")
                        error = True
                        e_type = 1
                    
                    else:
                        for key, value in devices.items():

                            white_list.append(value)
                            
                        console.print(white_list)
                        console.print("\n\nAll devices successfully appended to White List.", style="bold blue")
                        console.input("\n[yellow]Press enter to return to main menu: [/yellow]")


                        # NOW TO SAVE WHITE LIST TO FILE 
                        self.data.create_file(letter=white_list, type=2)
                        
                        # console.print("White List Successfully Created! ", style="bold green")
                        console.print(f"Now exiting", style="bold red")
                        time.sleep(2)
                        break



                elif choice in choices:
                  #  console.print("Cannot duplicate inputs: Please try again")
                   # time.sleep(2)
                    self.utilities.clear_screen()
                    console.print("Current White List:", style="bold blue\n")
                    console.print(white_list)  
                    print("")
                    error = True
                    e_type = 2



                    picked = True
                
                # VERIFIES USER CHOICE IS IN THE RANGE OF DEVICES FOUND
                elif choice in keys:
                    
                    # NOW TO CALL UPON DEVICES
                    allowed_device = devices[choice]
    
                    white_list.append(allowed_device)   # KEEPS TRACK OF USER CHOOSEN WHITE LIST
                    choices.append(choice)              # KEEPS TRACK OF USER CHOICES TO PREVENT DUPLICATION
                   
                    self.utilities.clear_screen()
                    console.print("Current White List:", style="bold blue\n")
                    console.print(white_list)  
                    print("")

                    show = True
                    
   
                


                    self.utilities.clear_screen()
                    console.print("Current White List:", style="bold blue\n")
                    console.print(white_list)  
                    print("")

                    error = True
                    e_type = 3
                
            except KeyError as e:
                console.print(f"[bold red]Error:[/bold red] [yellow]Please enter a valid key #[/yellow]")
            

            except Exception as e:
                console.print(f"[bold red]{e}[/bold red]")


class file_handling():

    def __init__(self):
        self.file_devices = "active_device_list.json"
        self.file_white_list = "white_list.json"
        self.file_user_setting = "user_setting.json"
        pass

    def create_file(self, letter, type):
        """Responsible for creating file information, type 1 is for creating active ip list, type 2 is for creating white list"""
       

        try:
            num = 1
            data = {}

            # CREATE ACTIVE IP LIST
            if type == 1:
                
                # SET FILE PATH
                file_path = self.file_devices
                msg = "Active IP List"     

                # SPLIT THE INFO INTO VARIABLES SO WE CAN THEN ADD IT TO A DICTIONARY AS A KEY PAIR
                for key_combo in letter:
                    info = key_combo.split('/')
                    num = info[0]
                    vendor = info[1]
                    host = info[2]
                    ip = info[3]
                    mac = info[4]
                    
                    # CREATE A KEY VALUE 
                    ip_info = f"{vendor} / {host} / {ip} / {mac}"
                    #ip_info = f"Host Name: {host},  IP Address: {ip},  MAC Address: {mac}"
                    
                    # TURN STR TO INT SO WE CAN USE THE NUM VARIABLE AS A KEY TO STORE INTO A DICTIONARY
                    num = int(num)
                    data[num] = ip_info   
                    #console.print(ip_info)
                    
                    # INCREMENT THE KEY NUMBER
                    num += 1


            # CREATE WHITE LIST  
            elif type == 2:
                
                num = 0
                # SET FILE PATH
                file_path = self.file_white_list 
                msg = "White List"  
                
                # SPLIT THE INFO INTO VARIABLES SO WE CAN THEN ADD IT TO A DICTIONARY AS A KEY PAIR
                for key_combo in letter:
                    info = key_combo.split('/')
                    
                    vendor = info[0]
                    host = info[1]
                    ip = info[2]
                    mac = info[3]
                    num += 1

                    # CREATE A KEY VALUE 
                    ip_info = f"{vendor} / {host} / {ip} / {mac}"

                    # TURN STR INTO INT FOR DICTIONARY
                    num = int(num)
                    data[num] = ip_info

            
            with open(file_path, "w") as file:
                json.dump(data, file, indent=num)
                console.print(f"[bold green]{msg} successfully Created[/bold green]")
         


        except Exception as e:
            console.print(e)
    
    def load_file(self, type):
        """Responsible for loading file information, type 1 is for loading active ip list, type 2 is for loading user made white list"""
        
        while True:
            # FOR SELECETING BETWEEN LOADING USER SETTINGS OR SAVED DATA
            if type == 1:
                file_path = self.file_devices        # LOAD ACTIVE IP LIST
            
            elif type == 2:
                file_path = self.file_white_list    # LOAD  WHITE LIST


            while True:
            
                try:
                    with open(file_path, "r") as file:
                        content = json.load(file)
                       # console.print("File found")
                        return content
                    
                except FileNotFoundError:
                    console.print("[bold red]Error:[/bold red] [yellow]File not found please perform a Network Scan to[/yellow] [bold green]start defending your network[/bold green]")
                    #self.create_file(letter="", type=2)
                    time.sleep(2)

                
class extra_shii():
    def __init__(self):
        pass

    def clear_screen(self):
        """Responsible for inputting the clear screen command // allowing for smoother and cleaner transitions"""

        if os.name == "nt":      # WINDOWS
            os.system("cls")
        
        else:
            os.system("clear")   # UNIX


class user_interface():
    """Responsible for user frontend"""

    def __init__(self):
        self.data = file_handling()
        self.exe = extra_shii()
        self.arp_scan = arp_scanner()
        self.first = True
       
        pass

    def welcome(self):
        welcome = pyfiglet.figlet_format("Welcome to\nNet Alert 2.0",font="slant")
        welcomejr = Panel(f"{welcome}\n[cyan]NetAlert - 2.3[/cyan]   ", style="bold red", border_style="bold red", width=min(130, console_width - 2))
        console.print(welcomejr)
    
            
            

        
    def user_choose(self):
        # USER SELECTION
    
        panel_choices = Panel(
                              "1. Monitor Mode\n\n"
                              "2. Perform ARP Scan\n\n"
                              "3. View White List\n"
                              "4. Create new White list\n\n"
                              "5. Settings\n\n"
                              "6. Exit", 
                              
                              style="green", border_style="bold green", width=min(130, console_width - 2))
        

        console.print(panel_choices)
        

        # USER CHOICE // SELECTION
        while True:
            
            choice = console.input("\n\n[bold purple]Enter your selection here: [/bold purple]")
            

            # ENTER MONITOR MODE
            if choice == "1":
                self.exe.clear_screen()
                mm = monitor_mode()
                mm.main()
               
                break
            

            # PERFORM A REGULAR ARP SCAN
            elif choice == "2":
                self.exe.clear_screen()
                begin = arp_scanner().main()
                begin
                
                console.input("\n[bold red]Press enter to return to main menu: [/bold red]")
                break
                
            

            # VIEW WHITE LIST
            elif choice == "3":
                self.exe.clear_screen()
                data = self.data.load_file(type=2)
                console.print(data)
                console.input("\n\n[red]Press enter to exit: [/red]")
                break
            

            # CREATE A NEW WHITE LIST
            elif choice == "4":
    
                # VERIFY THE USER IS SURE ABOUT THERE CHOICE 
                while True:
                    confirm_choice = console.input("\n\n[yellow]Are you sure u want to create a new white list, this will erase your current one[/yellow][bold green](y[/bold green]/[bold red]n):[/bold red] ").strip().lower()
                
                    if confirm_choice == "y":
                        self.exe.clear_screen()
                        self.arp_scan.main()
                        list = white_list()
                        list.device_list()
                        break

                    elif confirm_choice == "n":
                        console.print("\nReturning to main menu!", style="bold blue")
                        time.sleep(1.5)
                        self.exe.clear_screen
                        break
                    
                    else:
                        console.print("[red]Please choose a valid option[/red]")
                
                break
            
            
            # SETTINGS MENU
            elif choice == "5":
              # REDIRECT TO SETTINGS MODULE
                settings = settings_menu()
                settings.settings()
                self.exe.clear_screen()
                break

            
            # TO EXIT PROGRAM
            elif choice == "6":
                exit()            # NOT RECOMMENDED WILL BE CHANGING THIS B4 EXE VERSION IS RELEASED


            
            else:
                console.print("\n[yellow]Please choose a valid option[/yellow] [bold green](1-6)[/bold green]")


# STRICTLY FOR MODULE TESTING
if __name__ == "__main__":

    start = 1

    if start == 1:
        list = white_list()
        list.device_list()
        

    elif start == 2:
        nsm = arp_scanner()
        nsm.main()
        nsm = white_list()
        nsm.device_list()

    elif start == 3:
        while True:
            main = user_interface()
            main.welcome()
            main.user_choose()


    console.input("Press enter to leave")