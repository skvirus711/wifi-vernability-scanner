import ipaddress
import platform
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor


def ping(ip):
    ip = str(ip)

    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", "-w", "500", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "Unknown"

        print(f"[+] {ip} ({hostname})")


def network_scan():
    network = input("\nEnter Network (Example: 192.168.1.0/24): ")

    try:
        net = ipaddress.ip_network(network, strict=False)

        print(f"\nScanning {net}...\n")

        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(ping, net.hosts())

        print("\nScan Complete!")

    except ValueError:
        print("Invalid Network!")


def my_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    print("\n==========")
    print("Your IP Information")
    print("==========")
    print("Hostname :", hostname)
    print("IP       :", ip)


while True:
    print("""
=============================
   PYTHON NETWORK TOOL
=============================

1. Scan Network
2. Show My IP
3. Exit

=============================
""")

    choice = input("Select Option: ")

    if choice == "1":
        network_scan()

    elif choice == "2":
        my_ip()

    elif choice == "3":
        print("Good Bye!")
        break

    else:
        print("Invalid Option!")
