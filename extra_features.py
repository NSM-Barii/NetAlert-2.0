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

    def __init__(self):
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
    

    def tts(self, letter):
        """Responsible for text to speech"""

        engine = pyttsx3.init()
        
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')
       # pitch = engine.getProperty('pitch')
        
        try:
            engine.setProperty('rate', rate -20)
           # engine.setProperty('pitch', pitch + 10) 
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
                return vendor
      
        
        except requests.exceptions.ConnectTimeout as e:
            vendor = manuf.MacParser().get_manuf_long(mac)
            return vendor
        
        except Exception as e:
            console.print(e)
            vendor = manuf.MacParser().get_manuf_long(mac)
            return vendor
        


def main():
    import threading
    t = threading.Thread(target=utilities().tts("testing"))
    t.start()
    t.join()
        




if __name__ == "__main__":
   while True:
   # start = utilities().tts(letter="Warning!!! 3 Unauthorized devices found on your network. Sending details to your phone.")
     main()
     console.print("toes are white")

