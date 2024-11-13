import socket

import struct



def extract_covert_icmp(packet):

    # Estrae i dati dal pacchetto ICMP (tipo 8 è Echo Request)

    icmp_type = packet[20]

    if icmp_type == 8:  # Echo Request

        # Estrae i dati nel payload

        data = packet[28:].decode('utf-8', errors='ignore')  # Escludi gli header (20 bytes IP + 8 bytes ICMP)

        print(f"Received covert data: {data}")



def sniff_covert_icmp(interface="enp0s3"):

    # Creiamo un socket raw per catturare pacchetti ICMP

    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))  # AF_PACKET = Link-layer

    s.bind((interface, 0))  # Bind su interfaccia di rete



    print("Listening for covert ICMP messages...")

    while True:

        packet, addr = s.recvfrom(65565)  # Riceve pacchetti

        extract_covert_icmp(packet)



# Avvia lo sniffing sull'interfaccia di rete specificata

sniff_covert_icmp("enp0s3")
