from scapy.all import *
import time

def send_covert_icmp(target_ip, message, delay=1):
    # Break the message into chunks for multiple packets if necessary
    data_chunks = [message[i:i+16] for i in range(0, len(message), 16)]  # Max 16 bytes per packet

    for chunk in data_chunks:
        packet = IP(dst=target_ip)/ICMP(type="echo-request")/chunk
        send(packet, verbose=0)
        print(f"Sent covert ICMP packet with data: {chunk}")
        
        # Optional delay between packets
        time.sleep(delay)

# Target IP and message
target_ip = "192.168.56.103"  # Replace with victim IP address
message = "Covert Channel Using ICMP"

# Send the covert message
send_covert_icmp(target_ip, message)
