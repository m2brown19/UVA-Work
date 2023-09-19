from scapy.all import *

#sniffs 1000 packets
packets = sniff(count=1000, iface="lo0") # iface="lo0" this causes it to hang forever...
xmas_packets = []

for packet in packets:
    if packet.haslayer(TCP):
        # print(packet.payload.flags)
        if ("F" in packet[TCP].flags) & ("P" in packet[TCP].flags) & ("U" in packet[TCP].flags):
            #print(packet[TCP].flags)
            xmas_packets.append(packet)

if len(xmas_packets) > 0:
    port = xmas_packets[0][TCP].dport
    print("Xmas Scan Detected on Port", port)
