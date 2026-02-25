ARP Spoofer & MitM Tool
1. What is it? What does it do?
This tool allows you to intercept the data traffic between two devices on a Local Area Network (LAN)—typically a smartphone and a router—by routing it through your own computer.

Man-in-the-Middle (MitM): Your computer tells the router that it is the victim, and tells the victim that it is the router.

Traffic Monitoring: Since the traffic passes through your machine, you can view (if unencrypted) or manipulate the network packets.

2. Technical Requirements 📋
Before running the code, ensure the following are installed:

Python 3.x: Available at python.org.

Scapy Library: Used for packet creation.
```bash
pip install scapy
```
Npcap (For Windows): Required for capturing and sending network packets. Download it from npcap.com and install it with "Loopback Adapter" support.

3. Step-by-Step Execution Guide
1. Preparation Phase
Update these two lines in the code according to your target network:
```bash
Python
victim_ip = "192.168.1.100"  # Target phone's IP address
router_ip = "192.168.1.1"    # Router's IP address
```
2. Running as Administrator
Since low-level access to the network card is required, open your terminal as Administrator (Windows) or use Sudo (Linux/macOS):

```bash
python your_script_name.py
```
3. The Attack Process
MAC Discovery: When started, the program sends an ARP request to the network to find the physical (MAC) addresses of the devices.

Poisoning: Once you see [+] ARP Spoofing active!, the program begins sending fake packets every 2 seconds to deceive the devices.

Internet Routing: If IP Forwarding is not enabled on your computer, the victim's internet will be cut off.

4. Safe Exit (Network Restoration)
Use the Ctrl+C key combination to shut down the program. When closed, the program:

Sends the legitimate MAC addresses back to the victim and the router.

Restores the ARP tables to their original state.

Ensures the victim's internet connectivity returns to normal.

5. ⚠️ Important Warnings
WARNING: Use this tool only on your own network or on devices for which you have explicit permission. This is for educational purposes only.
