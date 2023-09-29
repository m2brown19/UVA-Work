# This is the skeleton code for Networking Project Implementing a DNS server
# Uploading/distributing the code or solution to this project will be considered an
# Honor Code violation
# You should work on this project individually 
# -Best Daniel Graham PhD


# Task: Implement a DNS server that will act as an intermediary between the user and the Google dns server 8.8.8.8.
# Your server will intercept and relay the traffic to the Google DNS server.
# However,  if there server receives a request that contains a URL in intercept file it should replace the IP address response with IP addres in the file  For web request that the DNS server has already seen it should
# reply directly to responses without query the other server. 


import argparse
import logging
import socket
from  dnsPacket import DNSPacket
from dnsPacketModifier import DNSPacketModifier

DNS_UDP_PORT = 53 #Port 53 is the agreed on standard for DNS
BUFFERSIZE = 1024

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rServer',
                        help='the DNS server to forward recursive queries to')
    #Fun example of an intercept
    parser.add_argument('iFile', 
                        help='the containing list of urls to intercep example www.vt.edu @ 128.143.67.11')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose output')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)


    #Setup UDP socket that will  receice DNS request
    sock_DNS_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_DNS_in.bind(('', DNS_UDP_PORT))

    #New instance of the Modifier
    modifier = DNSPacketModifier(args.iFile, args.rServer, DNS_UDP_PORT, BUFFERSIZE)

    #Currently the server does work you need complete the TODO sections. 
    while True:
        data, addr = sock_DNS_in.recvfrom(BUFFERSIZE) # buffer size is 1024 bytes

        #print(data)
        #print(addr)


        logging.info('DNS Server State: %s', 'started and recieved first packet', extra={'bufferSize': BUFFERSIZE})

        #byte strewam passed to obj
        dnsPacket = DNSPacket(data) #create dns packet. obj created from network data stream from socket.

        print("----------------Packet Recieved------------\n " + str(dnsPacket))
        dnsPacketModified = modifier.modify(dnsPacket)

        print("----------------Packet Sent--------------\n "+ str(dnsPacketModified))

        # print(dnsPacketModified)
        sock_DNS_in.sendto(dnsPacketModified.serializePacket(),addr)

main()
