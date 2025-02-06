NetAlert 2.0 is a Python-based network monitoring and intrusion detection tool. It scans your local network using ARP, compares discovered devices against a whitelist of authorized devices, and alerts you if any unauthorized devices are detected. It also features a deauthentication module (for Linux/Kali environments) to disconnect unwanted devices and integrates with Discord and text-to-speech for notifications—all wrapped in a rich terminal interface.

Features:
  ARP Scanning: Actively scans your network to detect connected devices.
  Whitelist Management: Compares detected devices against an authorized list.
  Dynamic Terminal UI: Uses the rich library to display beautiful, real-time output.
  Customizable Settings: Configure scan intervals, whitelist files, notification methods, and more.


Coming Soon:
  Unauthorized Device Detection: Automatically alerts you via Discord and/or TTS when an unknown device is found.
  Deauthentication Module: (Linux/Kali Only) Optionally disconnect unauthorized devices using crafted 802.11 deauth frames.

Requirements:
  Python 3.7+
  Scapy – for packet crafting and ARP scanning.
  Rich – for creating dynamic terminal output.
  Pyfiglet – for ASCII art banners.
  Requests – for API calls (e.g., fetching vendor info).
