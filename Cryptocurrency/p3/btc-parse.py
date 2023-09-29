"""
@author: Michael Brown

@sources: https://www.tutorialsteacher.com/python/python-read-write-file#:~:text=The%20open()%20function%20opens,in%20binary%20format%20for%20writing.


"""
import sys



#read file from CLI
file_name = sys.argv[1]
f = open(file_name, "rb")
all_lines = []
for line in f:
    all_lines.append(line)



f.close()
#print(all_lines)
# print(len(all_lines[0]))
# print()
var1 = all_lines[0][0:4]
print(var1)
var2 = all_lines[0][4:8]
print(var2)
combine = []
for i in range(0, len(var1)):
    combine.append(var1[i])
for i in range(0, len(var2)):
    combine.append(var2[i])
print(combine)
print(combine.reverse())
print(bytes(combine).hex())
print(combine)

#process --- do the list slice, use combine function if needed to split across two vars, then convert to big endian

#use thiss to combine 2 byte array (that i got from sub-listing byte array)
def combine_bytes_in_list(var1, var2):
    combine = []
    for i in range(0, len(var1)):
        combine.append(var1[i])
    for i in range(0, len(var2)):
        combine.append(var2[i])
    return combine          #return an array of bytes. in decimal format.

def put_bytes_in_list(var):
    my_list = []
    for i in range(0, len(var)):
        my_list.append(var[i])
    return my_list          #return an array of bytes. in decimal format.

#return a list of big endian bytes in hex as a string.
#argument is of the type file[line][index:index2]
#BEFORE USING, call combine bytes in list or put bytes in list
#ARG IS A LIST OF BYTES
def little_to_big_endian(byte_array):
    byte_array.reverse() #in big endian, but they are in decimal int form...
    return bytes(byte_array).hex()      #returns as big endian hex string.


#index is the index on the line.
def readPreamble(line_num, index, line_list):
    # at index of line, find the magic num and block size
    one_line = line_list[line_num]
    # Cases: it will be on one line or split.
    line_length = len(one_line)


    if index <= (line_length - 8): #TODO -- verify correctness
        #preamble is on one line.
        magic_num = line_list[line_num][index:index+4]
        block_size = line_list[line_num][index+4:index+8]
        #CONVERT TO BIG ENDIAN
        index += 8
        part_magic = put_bytes_in_list(magic_num)
        magic_num = little_to_big_endian(part_magic)
        part_size = put_bytes_in_list(block_size)
        block_size = little_to_big_endian(part_size)
        return magic_num, block_size, index, line_num
    else:
        #TODO
        #grab as many bytes as can on this line, then get rest on next line
        end_line_bytes = line_list[line_num][index:]
        length_end_line = len(end_line_bytes)

        index = 0
        line_num += 1

        rest_of_bytes_nbr = 8 - length_end_line
        #switched to an ew line with new index. Get rest of bytes for preamble to equal 8 bytes total
        rest_of_bytes = line_list[line_num][index:rest_of_bytes_nbr]
        #gets everything up to but not including that num. update index to that spot and parse preamble
        index = rest_of_bytes_nbr

        all_preamble_bytes = combine_bytes_in_list(end_line_bytes, rest_of_bytes)
        #separate this list now, then convert both to big endian
        part_magic = all_preamble_bytes[0:4]
        part_size = all_preamble_bytes[4:8]
        magic_num = little_to_big_endian(part_magic)
        block_size = little_to_big_endian(part_size)

        return magic_num, block_size, index, line_num

print(readPreamble(0, 0, all_lines))





#parse list of lines to read blockchain
start = 0 #start of first block is in list[0]. This var will hold start of next block
for line in all_lines:
    #determine start of next block
    pass


