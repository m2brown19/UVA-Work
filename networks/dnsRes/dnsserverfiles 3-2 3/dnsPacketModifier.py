from socket import *
from dnsPacket import DNSPacket
from Utilities import Util
class DNSPacketModifier:

  

    def __init__(self, _file, _serverName, _DNS_UDP_PORT, _BUFFERSIZE):
        self.DNS_UDP_PORT = _DNS_UDP_PORT
        self.BUFFERSIZE = _BUFFERSIZE
        self.serverName = _serverName
        self.urlIPMap = self.parseFile(_file)
        self.socket_DNS_out = socket(AF_INET, SOCK_DGRAM) #socket out to root dns server
        self.dnsCache = {}

        
         
    def parseFile(self, _file):
        """
            This function parsers the file. 
            This file currently only supports IPV4 address.
        """
        urlIPMap = {}
        lines = open(_file,'r').readlines()
        for line in  lines: 
            splitLine = line.split(' ')
            urlIPMap[splitLine[0]] = splitLine[1]
        return urlIPMap

    def modify(self, dnsPacket): 
        """
            This function is responsible for representing the modify module in the write
            It should take in a DNSPacket. Do a recursive query and get the result.
            If intercept.txt file contains the QNAME found it query it should replace the answer
            section with IPV4 address from the intercept file. 
            Finally it should cache the result and then check the cache before doing future recursive queries. 
        """
        #TODO: Student impment the modifier method

        while True:
            #CHECK THE CACHE!!!
            for question in dnsPacket.ArrayOfQuestions:
                q_name = question.get_QNAME()

                if q_name in self.dnsCache:
                    #print("It's cached already")
                    #print(self.dnsCache.get(q_name))
                    #print("-------")
                    #Give dns packet back

                    cached_dns_resp = self.dnsCache.get(q_name)
                    cached_dns_resp.set_ID(dnsPacket.get_ID())
                    return cached_dns_resp

                else:
                    #print("NOT CACHED YET")
                    #Not cached, send to recursvie dns server

                    #send dns packet to recursive dns root server. tuple is ip and port.
                    self.socket_DNS_out.sendto(dnsPacket.serializePacket(), (self.serverName, 53)) #not a tuple servername

                    data, addr = self.socket_DNS_out.recvfrom(self.BUFFERSIZE)

                    dnsPacket = DNSPacket(data) #create dns packet
                    # print("DNS PACKET HERE")
                    # print(dnsPacket)

                    #Get QNAME and determine if it needs to be modified
                    #each element in array is binary byte string

                    #make a list of the intercept.txt names
                    int_names = []
                    with open('intercept.txt') as intercept_file:
                        for line in intercept_file:

                            int_names.append(line.strip().replace("\n","").split())


                    #array of questions has QuestionSection objects!!! I can get the name from them

                    # for question in dnsPacket.ArrayOfQuestions:
                    #     q_name = question.get_QNAME()

                    # print("qname length == ", len(q_name))

                    for domain in int_names:

                        # print(len(q_name))
                        # if (q_name == domain[0]):
                        #     print("MODIFY IT")

                        #domain is list --- domain, ip address from intercept.txt

                        if domain[0] == q_name:
                            #MODIFY PACKET!!!
                            #print("MODIFY PACKET!!")
                            ip_mod_to = domain[1]

                            answer_sect = dnsPacket.ArrayOfAnswers

                            #print(answer_sect[0])

                            for i in range(0, len(answer_sect)):

                                answer_obj = dnsPacket.getAnswerSectionAtIndex(i)

                                #Create a new answer object to replace old one.
                                # print("GOT IN HERE ---------")
                                # print(answer_obj)

                                new_answer_obj = answer_obj.set_RDATA(ip_mod_to)

                                dnsPacket.replaceAnswerSection(new_answer_obj, i)

                            #dnsPacket.ArrayOfAnswers = answer_sect #save to dns packet. the modified answers
                        else:
                            #
                            pass



                    #cache result
                    self.dnsCache[q_name] = dnsPacket


                    return dnsPacket

