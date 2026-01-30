import socket
import argparse
import time
from packet import Packet

def run_phase_1a(sock, dest_addr):
    
    msg = "HELLO".encode()
    pkt = Packet(pkt_type=0, seq_num=0, data=msg)
    sock.sendto(pkt.encode(), dest_addr)
    print(f"Phase 1(a) - Sent: HELLO")
    
    # Echo
    data, _ = sock.recvfrom(2048)
    echo_pkt = Packet.decode(data)
    print(f"Phase 1(a) - Received Echo: {echo_pkt.data.decode()}")

def run_phase_1b(sock, dest_addr, file_path):
    seq_num = 1
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(1024) # 
            if not chunk:
                break
            
            pkt = Packet(pkt_type=0, seq_num=seq_num, data=chunk)
            sock.sendto(pkt.encode(), dest_addr) #
            print(f"Phase 1(b) - Sent packet {seq_num}")
            seq_num += 1
            time.sleep(0.01) # 

    #
    eof_pkt = Packet(pkt_type=1, seq_num=seq_num)
    sock.sendto(eof_pkt.encode(), dest_addr)
    print("Phase 1(b) - EOF sent.")

def main():
    parser = argparse.ArgumentParser(description="UDP Sender (Phase 1a & 1b)")
    parser.add_argument('--host', type=str, required=True, help='Receiver host')
    parser.add_argument('--port', type=int, required=True, help='Receiver port')
    parser.add_argument('--file', type=str, help='File to send for Phase 1b')
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest_addr = (args.host, args.port)

    # Phase 1(a)
    run_phase_1a(sock, dest_addr)
    
    # Phase 1(b)
    if args.file:
        print("\nStarting Phase 1(b) File Transfer...")
        run_phase_1b(sock, dest_addr, args.file)

    sock.close()

if __name__ == "__main__":
    main()