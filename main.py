# MAIN MODULE FOR RUNNING MAIN CODE // NET ALERT 2.0

# IMPORT
import os


# IMPORT OF ONE MODULE TO ACCESS THE REST
from scanlogic import user_interface
from extra_features import connection_status, utilities

from monitor import monitor_mode
from user_settings import settings_menu

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()
console_width = console.size.width
import pyfiglet, threading, time


# START OF MAIN PROGRAM // ALL MODULES FROM THIS POINT
if __name__ == "__main__":

    # CREATE OBJECTS
    main = user_interface()
    online_status = connection_status()
    utilities = utilities()
    
    

    # LOOP THE MAIN PROGRAM 
    while True:
        main.welcome()
        online_status.connection_check()
        #t = threading.Thread(target=)
       # t.start()
        main.user_choose()
        utilities.clear_screen()
        
        
        