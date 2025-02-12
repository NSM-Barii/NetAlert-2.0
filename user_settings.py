# MODULE ONLY FOR USERT SETTING // SETTING JSON FILE       # DEVELOPED BY NSM BARII

# WILL BE UPDATING THIS MODULE SOON

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()
console_width = console.size.width
import pyfiglet

# CONSOLE OBJECTS
console = Console()
console_width = console.size.width

# ETC IMPORTS
import json, os, time, requests


# FILE PATH
from pathlib import Path

base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetAlert2"
base_dir.mkdir(parents=True, exist_ok=True)


# SETTINGS PATH
settings_path = base_dir / "settings.json"



class user_settings():
    """Primary and only responsibility of this class is to keep track of user data/settings!"""

    def __init__(self):
        self.file_user_settings = settings_path
    

    def save_data(self, changed_data):
        """Responsible for saving user changed data // settings"""


        # NOT NEEDED // BUT I WANTED A MORE COMPACT VARIABLE NAME
        path = self.file_user_settings 
        indent = 10

        try:
            with open(path, "w")  as file:
                json.dump(changed_data, file, indent=indent)
                console.print("File successfully updated", style="bold green")
            
        except FileNotFoundError as e:
            self.create_file()
        
        except Exception as e:
            self.create_file()    # PLACE THE ERROR IN CREATE FILE METHOD // TO MAKE TROUBLE SHOOTING EASIER!


    def load_file(self):

        # NOT NEEDED // BUT I WANTED A MORE COMPACT VARIABLE NAME
        path = self.file_user_settings 
        
        # AFTER DEFAULT PATH IS CREATED LOOP BACK THROUGH THE TRY BLOCK
        while True:

            try:
                with open(path, "r") as file:
                    content = json.load(file)
                    return content
                
            except FileNotFoundError as e:
                console.print("User filepath not found", style="bold red")
                self.create_file()
            
            except Exception as e:
                self.create_file()    # PLACE THE ERROR IN CREATE FILE TO MAKE TROUBLE SHOOTING EASIER
        
        
    def create_file(self):
        """Responsible for creating user default file settings if they cant be found by the program"""
        
        # NOT NEEDED // BUT I WANTED A MORE COMPACT VARIABLE NAME
        path = self.file_user_settings 
        indent = 10
       

       # THIS LOOP ENSURES THAT AFTER A EXCEPTION THE MAIN TRY CONDITION IS REATTEMPTED!
        while True:
            try:

                # DEFAULT DATA
                data = {
                    "display_name": "user",
                    "monitor_mode": False,
                    "continous_monitoring": False,
                    "discord_webhook": False,
                    "intrusion_updates": False,
                    "live_updates": False,
                    "subnet_address": "",
                    "scan_interval": 15,
                    "monitor_mode_scans": 0
                }


                with open(path, "w") as file:
                    json.dump(data, file, indent = indent)
                    console.print("[bold green]Default File Path Successfully Created![/bold green]")
                    time.sleep(2)
                    break
            
            # IN CASE USER FILE // JSON FILE IS CORRUPTED WE RESET IT BACK TO NORMAL
            except json.JSONDecodeError as e:
                data = {}
                with open(path, "w") as file:
                    json.dump(data, file, indent=indent)
                    console.print("Corrupt File safetly fixed!", style="bold green")
                    time.sleep(1)

            except Exception as e:
                console.print(e)
                Console.input("Please restart the program to attempt to fix the issue: ")

                # THIS WILL NOT WORK IN EXE // NOT RECOMMENDED BUT WILL USE FOR NOW
                exit() 
                

class settings_menu():
    """here is where all the settings functionality code will be placed"""

    def __init__(self):
        self.loops = 0
        pass

    def settings(self):
        """Settings module that encapsulates all other settings options"""
        
        while True:
            # CREATE LOAD & SAVE OBJECTS
            data = user_settings()
            load = data.load_file()

            # CREATE CLEAR SCREEN OBJECT
            cls = extra_shii()
            cls.clear_screen()

            


            welcome = pyfiglet.figlet_format("Settings")
            welcomejr = ""

            console.print(f"[bold red]{welcome}[/bold red]")
            console.print(load["display_name"])
            
            # DISPLAY CURRENT SETTING // MORE FLEXIBLE SETTINGS MODULE
            console.print(f"\n[bold red]-----  Current Settings  -----[/bold red]\n")
            for variable, value in load.items():
                console.print(f"[bold green]{variable}[/bold green] --> [bold blue]{value}[/bold blue]")
            
            console.print("\n[bold red]------------------------------[/bold red]\n")

            options = Panel(
                            "1. Display name\n\n"
                            "2. Discord Webhook\n"
                            "3. Intrusion Updates\n"
                            "4. Subnet Address\n"
                            "5. Scan Interval\n"
                            "\n6. Exit",
                            
                            title="Options",
                            style="red",
                            border_style="bold red",
                            width=min(130, console_width - 2)
                            )
        
            console.print(options)

            choice = console.input("\n\n[bold blue]Enter your choice here: [/bold blue]")
            

            # DISPLAY NAME
            if choice == "1":

                # INITIATE AT THE BEGINNING OF EACH BLOCK TO REFRESH AND GET THE MOST UP TO DATE SETTINGS
                data = user_settings()
                load = data.load_file()
                
                change = console.input("[bold blue]Enter new display name: [bold blue]")

                # CALL UPON LOAD METHOD TO SAVE SETTINGS
                load["display_name"] = change

                data.save_data(changed_data=load)
        
            

            # DISCORD WEBHOOD
            elif choice == "2":

                # INITIATE AT THE BEGINNING OF EACH BLOCK TO REFRESH AND GET THE MOST UP TO DATE SETTINGS
                data = user_settings()
                load = data.load_file()
            

                try:
                    # USER INPUTS THERE DISCORD WEBHOOK
                    webhook_url = console.input("[bold blue]Enter Discord Webhook: [/bold blue]")

                    data = {
                        "content": 
                        "Message: Hey there I am necessary to protect your network.\nAny and all threats will be destroyed!",
                        "username": "Intrusion Protection BOT"
                    } 
                    
                    response = requests.post(webhook_url, data=json.dumps(data),  headers={"content-type": "application/json"})
                    

                    # CHECK IF WEBHOOK IS VALID 
                    if response.status_code == 204:
                    
                        # NOW TO SAVE WEBHOOK
                        data = user_settings()
                        load = data.load_file()
                        load["discord_webhook"] = webhook_url
                        data.save_data(changed_data=load)

                        console.print("[bold green]Discord Webhook Successfully Updated![/bold green]")
                        time.sleep(1.5)

                    
                    else:
                        console.print(f"Invalid Webhook given please try again: {webhook_url}")
                        time.sleep(1.5)
                

                # ERROR HANDLING
                except requests.ConnectionError as e:
                    console.print(f"[bold red]Connection Error:[/bold red][yellow]{e}[/yellow]")
                    time.sleep(1.5)
                
                except requests.JSONDecodeError as e:
                    console.print(f"[bold red]JSON Error:[/bold red][yellow]{e}[/yellow]")
                    time.sleep(1.5)
                
                except Exception as e:
                    console.print(f"[bold red]Unkown Exception Error:[/bold red][yellow]{e}[/yellow]")
                    time.sleep(1.5)


            # INTRUSION UPDATES
            elif choice == "3":
                    
                while True:

                    change = console.input("[yellow]Do you want to turn Intrustion Updates[/yellow] [bold green]On[/bold green] [yellow]or[/yellow] [bold red]Off[/bold red]: ").lower()
                
                    if change == "on":
                        
                        # CHANGE VARIABLE TO TRUE
                        data = user_settings()
                        load = data.load_file()
                        load["intrusion_updates"] = True
                        data.save_data(changed_data=load)
                        break
                    
                    elif change == "off":

                        # CHANGE VARIABLE TO FALSE
                        data = user_settings()
                        load = data.load_file()
                        load["intrusion_updates"] = False
                        data.save_data(changed_data=load)
                        break
                    
                    else:
                        console.print(f"[bold red]{change}[/bold red] [yellow]is a invalid choice, please Try again[/yellow]")
            
                console.print(f"[bold blue]Settings Successfully Updated - Intrusion Updates are now:[/bold blue][bold green] {change}[/bold green]")
                time.sleep(1.5)
            
            
            # IP SUBNET
            elif choice == "4":
                
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

                        console.print(f"[bold green]IP Subnet:{valid_subnet}  Successfully Updated![/bold green]")
                        time.sleep(1.8)
                        break

                    except ipaddress.AddressValueError as e:
                        console.print(e)
                    
                    except ipaddress.NetmaskValueError as e:
                        console.print(e)

                    except Exception as e:
                        console.print(e)
            

            # SCAN INTERVAL
            elif choice == "5":

                interval = console.input("[bold blue]Enter scan interval timer in minutes: [/bold blue]")

                # NOW TO SAVE TIMER INTERVAL
                data = user_settings()
                load = data.load_file()
                load["scan_interval"] = interval
                data.save_data(changed_data=load)

                console.print(f"[bold green]Scan interval Successfully Updated to perform a scan every: {interval} Minutes[/bold green]")
                time.sleep(1.8)
                
        
            
            
            # EXIT BACK TO MAIN MENU
            elif choice == "6":
                break     

            # INCORRECT CHOICE
            else:
                console.print(f"Invalid option, please try again with options(1-5)")

    
    def not_in_use(self):
        """Options for settings menu that are no longer or currently not in use"""

        choice = ""


        # LIVE UPDATES
        if choice == "3":
            
            while True:

                change = console.input("[yellow]Do you want to turn Live Updates[/yellow] [bold green]On[/bold green] [yellow]or[/yellow] [bold red]Off[/bold red]: ")
            
                if change == "on":
                    
                    # CHANGE VARIABLE TO TRUE
                    data = user_settings()
                    load = data.load_file()
                    load["live_updates"] = True
                    data.save_data(changed_data=load)
                    break
                
                elif change == "off":

                    # CHANGE VARIABLE TO FALSE
                    data = user_settings()
                    load = data.load_file()
                    load["live_updates"] = False
                    data.save_data(changed_data=load)
                    break
                
                else:
                    console.print(f"[bold red]{change}[/bold red] [yellow]is a invalid choice, please Try again[/yellow]")
            
            console.print(f"[bold blue]Settings Successfully Updated - Live Updates are now:[/bold blue][bold green] {change}[/bold green]")
            time.sleep(1.5)

                   # CONTINOUS MONITORING
        if choice == "5":

            while True:

                change = console.input("[yellow]Do you want to turn Continous Monitoring[/yellow] [bold green]On[/bold green] [yellow]or[/yellow] [bold red]Off[/bold red]: ")
            
                if change == "on":
                    
                    # CHANGE VARIABLE TO TRUE
                    data = user_settings()
                    load = data.load_file()
                    load["continous_monitoring"] = True
                    data.save_data(changed_data=load)
                    break
                
                elif change == "off":

                    # CHANGE VARIABLE TO FALSE
                    data = user_settings()
                    load = data.load_file()
                    load["continous_monitoring"] = False
                    data.save_data(changed_data=load)
                    break
                
                else:
                    console.print(f"[bold red]{change}[/bold red] [yellow]is a invalid choice, please Try again[/yellow]")

            
            console.print(f"[bold blue]Settings Successfully Updated - Continous Monitoring is now set to:[/bold blue][bold green] {change}[/bold green]")
            time.sleep(1.5)


class extra_shii():
    """Clear screen for settings modules"""

    def __init__(self):
        pass

    def clear_screen(self):
        """Clear screen"""

        if os.name == "nt":
            os.system("cls")
        
        else:
            os.system("clear")


if __name__ == "__main__":

    nsm = settings_menu()

    nsm.settings()
            
# 5. Settings

#  1. Change display name  
#  2. Discord Webhook
#  3. Live updates
#  4. Intrusion Updates
#  5. Continous Monitoring
#



