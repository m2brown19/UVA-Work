from Utilities import Util
import logging

"""
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

    """

class AnswerSection:
    def __init__(self, _binaryString):
        self.binaryString = _binaryString


    def get_binaryString(self):
        """ 
            Returns a binary string representation of the QuestionSection 
        """
        return self.binaryString

    def get_NAME(self):
        """
        NAME            a domain name to which this resource record pertains.
        Most moderm DNS servers will use a compressed representation for the 
        NAME object this compress representation    
        0xc Name is a pointer
        0x00c Pointer is to the name at offset 0x00c (0x03777777...)
        You will only have to deal with the compressed respresentation value 0xc00c
        """
        if(self.binaryString[0:16] != "1100000000001100"):
            logging.info('DNS recieved unsported NAME Format %s', 'not of the form c0c0x', extra={'NAME': self.binaryString[0:16]})

            return "None Pointer Style Not supported"

            #raise Exception('parse NAME block in answer section and result was not of from 0xc0 0x0c')
        return b'\xc0\x0c'

    def get_TYPE(self) -> int:
        """
        TYPE            two octets containing one of the RR type codes.  This
                        field specifies the meaning of the data in the RDATA
                        field.
                        
        """
        #TODO: Student impment this method -- DONE
        type_part = self.binaryString[16:32] #2 octets = 16 bits
        #
        if (type_part == "0000000000000001"):
            return 1
            #return b'\x00\x01'
        elif (type_part == "0000000000000101"):
            return 5
        elif (type_part == "0000000000000010"):
            return 2
        elif (type_part == "0000000000001111"):
            return 15
        else:
            logging.info('DNS recieved unsported TYPE Format %s', 'not in correct form', extra={'TYPE': type_part})

            return 0



    def get_CLASS(self) -> int:
        """
        CLASS           two octets which specify the class of the data in the
                        RDATA field.
        """
        #TODO: Student impment this method -- DONE
        class_part = self.binaryString[32:48]
        if (class_part == "0000000000000001"):
            return 1
        else:
            logging.info('DNS recieved unsported CLASS Format %s', 'not correct class type', extra={'CLASS': class_part})
            return 0

    def get_TTL(self):
        """
            TTL             a 32 bit unsigned integer that specifies the time
                            interval (in seconds) that the resource record may be
                            cached before it should be discarded.  Zero values are
                            interpreted to mean that the RR can only be used for the
                            transaction in progress, and should not be cached.
        """
        #TODO: Student impment this method -- done
        ttl_part = self.binaryString[48:80]

        return Util.binaryToInt(ttl_part) #defined in utilities...


    def get_RDLENGTH(self):
        """RDLENGTH        an unsigned 16 bit integer that specifies the length in
                        octets of the RDATA field.
                        """
        #TODO: Student impment this method
        rdlen_part = self.binaryString[80:96]
        return Util.binaryToInt(rdlen_part)



    def set_RDLENGTH(self, _RDLENGTH):
        """
            Function takes an int and sets the lenght value for RD_DATA
        """
        #TODO: Student impment this method -- HELP

        return _RDLENGTH


    def get_RDATA(self)-> str:
        """
        RDATA           a variable length string of octets that describes the
                        resource.  The format of this information varies
                        according to the TYPE and CLASS of the resource record.
                        For example, the if the TYPE is A and the CLASS is IN,
                        the RDATA field is a 4 octet ARPA Internet address.
        For this assignment only have to support (Type AAAA with CLASS: IN)  and Type: A with ClASS: IN
        """
        #TODO: Student impment this method

        print("IN GET RDATAMETHOD--------")
        type_field = self.get_TYPE()
        if type_field == 1 & self.get_CLASS() == 1:
            #4 octet IP ADDR. return ip address

            return Util.binaryToIpAddress(self.binaryString[96:128], 4)

        if type_field == 5 & self.get_CLASS() == 1:

            print("HEY, LOOK AT NEW EDIT!!")
            print(Util.binaryToAsciiCNAME(self.binaryString[96:96+(self.get_RDLENGTH()*8)]))

            return Util.binaryToAsciiCNAME(self.binaryString[96:96+(self.get_RDLENGTH()*8)])
        else:
            print("nothing else here........")
    
        return "None"

    def set_RDATA(self, _ip_address):
        #TODO: Student impment this method

        #self.binaryString[96:128] = Util.IpAddressToBinary(_ip_address, 4)
        #try returning new answer object!
        return AnswerSection(self.binaryString[:96] + Util.IpAddressToBinary(_ip_address, 4))

    def __str__(self):
        """ A to String implementation that used to generate the string for log
            Do not modifiy this is used by the grader        
        """
        return ("Answer Section Information \n"
            +"Name: "+str(self.get_NAME()) +"\n"
            +"Type: "+ str(self.get_TYPE()) +"\n"
            +"Class: "+ str(self.get_CLASS()) +"\n"
            +"TTL: "+ str(self.get_TTL()) +"\n"
            +"RDLENGTH: "+ str(self.get_RDLENGTH()) +"\n"
            +"RDDATA: "+ self.get_RDATA() +"\n")
    
    def serializeAnswerSection(self):
        """
         This function returns a byte array repsenting the answer section it should correctly
         Be carefully when serializing the RDATA field
         
         """ 
        return Util.binaryStringToHex(self.binaryString)

class AnswerParsingManager:
   
    @staticmethod
    def extractAnswerObjects(_binaryString, _answer_count):
         """
        Simular to question Parsing Manager the answer parsing manager class is responsible for parsing section all answer sections
        Creating a AnswerSection Array and the index of the bit representing where the next section begins. 

        Returns
            A tuple of the form 
                (Array_of_Answers, base ) 
        """
        #TODO: Student impment this method
         #AnswerSection.__init__(AnswerSection, _binaryString)
         #answer_sect = [AnswerSection.get_NAME(), self.get_TYPE(), self.get_CLASS(), self.get_TTL(), ]
         answerArray = []
         len_binary_string = len(_binaryString)
         base = 0  # represents the end position of the last answer
         # Each of index of the null character considering current index
         end_of_section = 0
         for currentAnswer in range(0, _answer_count):
             for i in range(base, len_binary_string, 8):
                 if _binaryString[i: i + 8] == "00000000":  # The CNAME Section terminates with an octect of zero \0x00
                     newbase = i + 112  #answer section length after name
                     answerArray.append(AnswerSection(_binaryString[base:newbase]))
                     base = newbase
                     end_of_section = base
                     break
         return (answerArray, end_of_section)