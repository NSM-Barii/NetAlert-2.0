# ARP TESTING SITE

# IMPORTS
import requests, random, time

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
console = Console()


ips = ["nsm", "computer", "pc", "tablet", "ps4", "ps5", "3ds"]
active_devices = {}
amount = len(ips)


def iti():
    for device in ips:
        for num in range(amount):
            if num != 0:
                print(active_devices)
                active_devices[num] = f"{device}"


def logic():
    num = 1
    for device in ips:

        active_devices[num] = f"{device}"
        num += 1






    print(active_devices)

    white_list = []
    choices = []

    while True:
        try:
            choice = console.input("Choose the ip you want to whitelist: ")
            
            if choice == "exit":
                console.print(f"Now exiting")
                time.sleep(2)
                break

            elif choice in choices:
                console.print("Can no duplicate inputs: Please try again")
            
            else:
                dict_key = int(choice)
                device = (active_devices[dict_key])
                choices.append(choice)
                white_list.append(f"{dict_key}. {device}")
                print(white_list)
                #print(active_devices[dict_key])


        except KeyError as e:
            console.print(f"Error: Please enter a valid key")

            




    console.input("Press enter to leave")

    data = {
        "1": "nsm",
        "2": "pc",
        "3": "computer",
        "4": "laptop",
        "5": "tablet",
        "6": "phone",
        "7": "ps4",
        "8": "ps5"
    }

    import pyfiglet

import pyfiglet
import time

class user_interface():
    def __init__(self):
        pass

    def welcome(self):
        welcome = pyfiglet.figlet_format("Welcome to\nNet Alert 2.0",font="slant")
        console.print(f"[bold red]{welcome}[/bold red]")

nsm = user_interface()
nsm.welcome()


def art():
    import pyfiglet
    import time

    text = "Welcome to NetAlert!"
    ascii_art = pyfiglet.figlet_format(text, font="slant")

    for char in ascii_art:
        print(char, end='', flush=True)
        time.sleep(0.02)
input()

