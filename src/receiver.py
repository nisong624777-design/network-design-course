import socket
import argparse
from packet import Packet

def main():
    parser = argparse.ArgumentParser(description="UDP Receiver (Phase 1a & 1b)")
    parser.add_argument('--port', type=int, required=True, help='UDP port to bind')
    parser.add_argument('--out', type=str, required=True, help='Path to write received bytes')
    args = parser.parse_args()

    # set UDP 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', args.port))
    
    print(f"Server is listening on port {args.port}...")

    with open(args.out, 'wb') as f:
        while True:
            raw_data, addr = sock.recvfrom(2048)
            packet = Packet.decode(raw_data)

            # Phase 1(a): 
            if packet.data == b"HELLO":
                print(f"Phase 1(a) - Received: {packet.data.decode()} from {addr}")
                sock.sendto(packet.encode(), addr) # Echo back [cite: 76]
                print("Phase 1(a) - Echoed back to client.")
                continue

            # Phase 1(b): RDT 1.0 
            if packet.pkt_type == 1: # 
                print("Phase 1(b) - EOF received. File transfer complete.")
                break
            
            f.write(packet.data)
            print(f"Phase 1(b) - Received packet {packet.seq_num}")

    sock.close()

if __name__ == "__main__":
    main()