"""
@author: Michael Brown

@sources: https://www.tutorialsteacher.com/python/python-read-write-file#:~:text=The%20open()%20function%20opens,in%20binary%20format%20for%20writing.
https://appdividend.com/2021/04/09/how-to-convert-python-bytes-to-int/
https://www.tutorialspoint.com/How-to-convert-hex-string-into-int-in-Python#:~:text=You%20can%20convert%20the%20hexstring,hex%20string%20into%20an%20integer.
https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
"""
import sys
import hashlib
import json


#read file from CLI
#file_name = sys.argv[1]


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


def hex_string_switch_endian(hex_string):
    byte_array = bytearray.fromhex(hex_string)
    return little_to_big_endian(byte_array)


#index is the index on the line.
def readPreamble(index, line_list):
    #print("Line num start fn=", line_num)
    # at index of line, find the magic num and block size

    line_length = len(line_list)

    if index <= (line_length - 8): #TODO -- verify correctness
        #preamble is on one line.
        magic_num = line_list[index:index+4]
        block_size = line_list[index+4:index+8]
        #CONVERT TO BIG ENDIAN
        index += 8
        part_magic = put_bytes_in_list(magic_num)
        magic_num = bytes(part_magic).hex() #little_to_big_endian(part_magic) #just check magic num in little endian
        part_size = put_bytes_in_list(block_size)
        block_size = little_to_big_endian(part_size)

        return magic_num, block_size, index
    # else:
    #     #TODO
    #     #print("Diff lines")
    #     #grab as many bytes as can on this line, then get rest on next line
    #     end_line_bytes = line_list[line_num][index:]
    #     length_end_line = len(end_line_bytes)
    #
    #     index = 0
    #     line_num += 1
    #
    #     rest_of_bytes_nbr = 8 - length_end_line
    #     #switched to an ew line with new index. Get rest of bytes for preamble to equal 8 bytes total
    #     rest_of_bytes = line_list[line_num][index:rest_of_bytes_nbr]
    #     #gets everything up to but not including that num. update index to that spot and parse preamble
    #     index = rest_of_bytes_nbr
    #
    #     all_preamble_bytes = combine_bytes_in_list(end_line_bytes, rest_of_bytes)
    #     #separate this list now, then convert both to big endian
    #     part_magic = all_preamble_bytes[0:4]
    #     part_size = all_preamble_bytes[4:8]
    #     magic_num = little_to_big_endian(part_magic)
    #     block_size = little_to_big_endian(part_size)
    #
    #     return magic_num, block_size, index, line_num


def readHeader(index, line_list):

    line_length = len(line_list)


    header = line_list[index:index+80]
    header = put_bytes_in_list(header)
    block_version = header[0:4]
    prev_header_hash = header[4:36]
    merkle_root_hash = header[36:68]
    time_header = header[68:72]
    nbits = header[72:76]
    nonce = header[76:80]

    #CONVERT TO BIG ENDIAN
    block_version = little_to_big_endian(block_version)
    prev_header_hash = bytes(prev_header_hash).hex() #little_to_big_endian(prev_header_hash) RETURN AS little endian hex string
    merkle_root_hash = little_to_big_endian(merkle_root_hash)
    time_header = little_to_big_endian(time_header)
    nbits = little_to_big_endian(nbits)
    nonce = little_to_big_endian(nonce)
    index += 80
    return index, block_version, prev_header_hash, merkle_root_hash, time_header, nbits, nonce


#pass in 9 bytes. determine how many bytes the csunit is then return it and the index + size of it
def readCompactUInt(index, line_list):
    line_length = len(line_list)

    csuint = line_list[index:index + 9]
    csuint = put_bytes_in_list(csuint)
    b = csuint[0]
    if b < 253:
        index += 1

        return index, str(hex(b))[2:]
    elif (b == 253):
        #reutrn next two bytes
        num = csuint[1:3]
        num = little_to_big_endian(num)
        index+=3
        return index, num
    elif (b == 254):
        index+=5
        num = csuint[1:5]
        num = little_to_big_endian(num)
        return index, num
    elif (b == 255):
        index += 9
        num = csuint[1:9]
        num = little_to_big_endian(num)
        return index, num

def readTxn(index, line_list):
    version_num = put_bytes_in_list(line_list[index:index+4])
    index+=4
    index, tx_in_count = readCompactUInt(index, line_list)

    #READ TX_IN --- varies in size
    in_count_decimal = int(tx_in_count, 16)
    index, list_of_tx_ins = read_Tx_in(index, in_count_decimal, line_list)


    index, tx_out_count = readCompactUInt(index, line_list)
    out_count_decimal = int(tx_out_count, 16)

    #TODO
    #READ TX_OUT
    index, list_of_tx_out = read_tx_out(index, out_count_decimal, line_list)


    lock_time = put_bytes_in_list(line_list[index:index+4])
    index+=4

    #switch to bit endian hex
    version_num = little_to_big_endian(version_num)
    lock_time = little_to_big_endian(lock_time)

    #return values and index
    return index, version_num, tx_in_count, list_of_tx_ins, tx_out_count, list_of_tx_out, lock_time


#Build a list of transaction inputs in big endian hex
def read_Tx_in(index, count, line_list):
    tx_inputs = []
    for i in range(0, count):
        #print("test --- do not go over count") #TODO CHECK

        #read a tx input
        tx_hash = put_bytes_in_list(line_list[index:index + 32])
        index += 32
        output_index = put_bytes_in_list(line_list[index:index + 4])
        index+=4
        index , in_script_bytes = readCompactUInt(index, line_list)
        size_of_script_decimal = int(in_script_bytes, 16) #int.from_bytes(in_script_bytes, "big", signed=False)

        sig_script = put_bytes_in_list(line_list[index:index + size_of_script_decimal])
        index += size_of_script_decimal

        sequence_num = put_bytes_in_list(line_list[index:index + 4])
        index += 4

        tx_hash = little_to_big_endian(tx_hash)
        output_index = little_to_big_endian(output_index)
        sig_script = little_to_big_endian(sig_script)
        sequence_num = little_to_big_endian(sequence_num)

        a_transaction = [tx_hash, output_index, in_script_bytes, sig_script, sequence_num]
        tx_inputs.append(a_transaction)

    return index, tx_inputs

def read_tx_out(index, count, line_list):
    tx_outputs = []
    for i in range(0, count):
        #print("test --- do not go over count in output fn") #TODO CHECK

        value = put_bytes_in_list(line_list[index:index+8])
        index+=8
        index, out_script_bytes = readCompactUInt(index, line_list)
        size_of_script_decimal = int(out_script_bytes, 16) #int.from_bytes(out_script_bytes, "big", signed=False)

        sig_script = put_bytes_in_list(line_list[index:index + size_of_script_decimal])
        index += size_of_script_decimal

        value = little_to_big_endian(value)
        sig_script = little_to_big_endian(sig_script)

        a_transaction = [value, out_script_bytes, sig_script]
        tx_outputs.append(a_transaction)

    return index, tx_outputs


#pass in a list of all the lists of the txns in the blockchain
#the txns in the list are gonna be a hex string
def merk_root_hash(all_txn_lists):
    # get all initial hashes, store in list
    hash_list = []
    for i in range(0, len(all_txn_lists)):
        txn_data = bytes.fromhex(all_txn_lists[i])
        hash1 = hashlib.sha256(txn_data).digest()
        hash2 = hashlib.sha256(hash1).digest()
        hash_list.append(hash2)
        #print("len count OG param")
    not_one_left = True

    #then do loop to keep halfing it
    if (len(hash_list) == 1):
        #do hashlist sub 0 . hex to print it
        hash2ba = bytearray(hash_list[0])
        hash2ba.reverse()
        hash = ''.join(format(x, '02x') for x in hash2ba)
        return hash

    while (not_one_left == True):
        #keep figuring out the hashes
        #cycle thru the list two at a time
        upperlvl = [] #store concatenatd hashes from current lvl here each time
        #print("outer while loop merkle")

        #even case
        if (len(hash_list) % 2 == 0):
            #print("even case merkle")
            for i in range(0, len(hash_list), 2):
                #concat two, double hash, then inc i by an extra
                concatHash = hash_list[i] + hash_list[i + 1]
                hash1 = hashlib.sha256(concatHash).digest()
                hash2 = hashlib.sha256(hash1).digest()
                upperlvl.append(hash2)
                #store this hash in the new list


        else:
            #print("Odd case merkle")
            #odd case
            i = 0
            while (i < len(hash_list) - 1):
                #print("Odd case merkle in while loop")
                #concat two, double hash, then inc i by an extra
                concatHash = hash_list[i] + hash_list[i + 1]
                hash1 = hashlib.sha256(concatHash).digest()
                hash2 = hashlib.sha256(hash1).digest()
                upperlvl.append(hash2)
                #store this hash in the new list
                i += 2

            #store last one
            concatHash = hash_list[i] + hash_list[i]
            hash1 = hashlib.sha256(concatHash).digest()
            hash2 = hashlib.sha256(hash1).digest()
            upperlvl.append(hash2)

        hash_list = upperlvl #store upper level in hash list for next iteration

        if len(hash_list) == 1:
            not_one_left = False

            # return bytes.hex(hash_list[0])
            hash2ba = bytearray(hash_list[0])
            hash2ba.reverse()
            hash = ''.join(format(x, '02x') for x in hash2ba)
            return hash





# parse list of lines to read blockchain
#debugger tool
# myhash = "0100000000000000000000000000000000 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  00 00 00 00 3b a3 ed fd  7a 7b 12 b2 7a c7 2c 3e  67 76 8f 61 7f c8 1b c3  88 8a 51 32 3a 9f b8 aa  4b 1e 5e 4a 29 ab 5f 49   ff ff 00 1d 1d ac 2b 7c"
# myhash = myhash.split(" ")
# mynewhash = ""
# for each in myhash:
#     mynewhash += each
# print(mynewhash)
#file_name = "blk00000-b29664.blk"       #TODO CHANGE
file_name = sys.argv[1]
f = open(file_name, "rb")
all_lines = []
for line in f:
    for byte in line:
        all_lines.append(byte)
f.close()

mydict = {} #final dict.
all_blocks_list = []

index = 0 #start of first block is in list[0]. This var will hold start of next block
length_file = len(all_lines)
block_num = 0
prev_timestamp = 0
prev_header_hash = "" #use to keep track of prev header hash to compare to when reading header
errors = False #change to true if find an error
list_all_blocks_txn_bytes_str = []

list_of_each_block_merkle = []
error_type = ""
while (index < length_file):         #TODO CHECK --- <= or <

    #Read preamble
    if index <= (length_file - 8):
        magic_num, block_size, index = readPreamble(index, all_lines)
        if magic_num != "f9beb4d9":

            print("error 1 block", block_num)
            #error_type = "error 1 block " + str(block_num)
            errors = True
            break

        #check, then read header
        if (index <= length_file - 80):
            #TODO --- there may not be a prev header hash nor a time header for block 0
            header_bytes_little_end = all_lines[index:index+80] #get header bytes --- little endian
            fresh_bytes = bytes(header_bytes_little_end)
            header_bytes_little_end = put_bytes_in_list(header_bytes_little_end)
            header_bytes_little_end = bytes(header_bytes_little_end).hex() #GET IT AS LITTLE ENDIAN hex string. take hash of this twice. use to compare next block's headeer hash to
            str_header_bytes = header_bytes_little_end
            header_bytes_little_end = int(header_bytes_little_end, 16) #convert to int, then convert to hex num
            header_bytes_little_end = hex(header_bytes_little_end)
            index, block_version, real_prev_header_hash_check, merkle_root_hash, time_header, nbits, nonce = readHeader(index, all_lines)

            # print("SHOW MERKLE HASH")
            # print(merkle_root_hash)
            list_of_each_block_merkle.append(merkle_root_hash)

            current_time = int(time_header, 16) #put here so json can access


            if (block_version != "00000001"):
                print("error 2 block", block_num)
                # error_type = "error 2 block " + str(block_num)
                errors = True
                break

            #TODO -- validate prev header hash
            if (block_num != 0):

                #TODO validate prev header hash
                if (prev_header_hash != real_prev_header_hash_check):
                    #ERROR ON PREV HEADER HASH CHECK
                    #print(real_prev_header_hash_check)
                    print("error 3 block", block_num)
                    # error_type = "error 3 block " + str(block_num)
                    errors = True
                    break
                #grab 80 bytes of current, hash it twice LE, compare when next block has the hash of prev header alreaady
                prev_header_hash = hashlib.sha256(fresh_bytes).digest() #UPDATE PREV HEADER HASH
                prev_header_hash = hashlib.sha256(prev_header_hash).hexdigest()

                current_time = int(time_header, 16)
                #compare times
                if (prev_timestamp - current_time > 7200):
                    #current is more than 2 hours before previous block time. Invalid!
                    print("error 4 block", block_num)
                    # error_type = "error 4 block " + str(block_num)
                    errors = True
                    break
                prev_timestamp = int(time_header, 16)
            else:
                #block num is equal to 0... get prev header hash
                prev_header_hash = hashlib.sha256(fresh_bytes).digest()

                prev_header_hash = hashlib.sha256(prev_header_hash).hexdigest()

                prev_timestamp = int(time_header, 16) #store time of block into prev block timer to compare to current next


            #check, then read txn count
            #TODO CHECK -- its gonna be variable... bc this will inc by csu int
            index, tx_nbr = readCompactUInt(index, all_lines) #TODO CHECK its correct number times
            tx_nbr = int(tx_nbr, 16)

            #GRAB the entire txns in a block
            #i have the starting index point.
            # block size at start tells me the end
            #slice all lines for it
            # old way to help validate merkle root hash
            #int_block_size = int(block_size, 16)
            #end_block = int_block_size + 8


            #all_txns_in_a_block = all_lines[index:end_block] #TODO CHECK -- ensure it is all txn, nothing else
            #all_txns_in_a_block = put_bytes_in_list(all_txns_in_a_block)

            #all_txns_in_a_block = bytes(all_txns_in_a_block).hex()
            # print("Check ascii")
            # print(all_txns_in_a_block)
            #add to the official list of each blocks entire txn list
            #list_all_blocks_txn_bytes_str.append(all_txns_in_a_block)
            #END OLD WAY VALIDATE MERKLE

            # if this block is valid, add to my dictionary.
            # make a temp dict

            big_endian_prev_hash = hex_string_switch_endian(real_prev_header_hash_check) #switch to big endian to store


            cur_block = {}
            cur_block["height"] = block_num
            cur_block["version"] = int(block_version, 16)
            cur_block["previous_hash"] = big_endian_prev_hash #real_prev_header_hash_check
            cur_block["merkle_hash"] = merkle_root_hash #TODO CHECK
            cur_block["timestamp"] = current_time
            cur_block["nbits"] = nbits
            cur_block["nonce"] = int(nonce, 16)
            cur_block["txn_count"] = tx_nbr
            txn_list = []

            #go thru txns and add
            all_txns_in_a_block = [] #add each txn to this
            for i in range(0, tx_nbr):
                start_txn_index = index
                index, version_num, tx_in_count, list_of_tx_ins, tx_out_count, list_of_tx_out, lock_time = readTxn(index, all_lines)
                end_txn_index = index

                #grab a full txn, then convert to string. keep little endian
                a_full_txn = all_lines[start_txn_index:end_txn_index] #TODO CHECK -- ensure it is all txn, nothing else
                a_full_txn = put_bytes_in_list(a_full_txn)

                a_full_txn = bytes(a_full_txn).hex() #hex str little endian. Add this to list of txns in a block
                all_txns_in_a_block.append(a_full_txn)

                if (version_num != "00000001"):

                    print("error 5 block", block_num)
                    # error_type = "error 5 block " + str(block_num)
                    errors = True
                    break

                txn_object = {}
                txn_object["version"] = int(version_num, 16)
                txn_object["txn_in_count"] = int(tx_in_count)
                one_txn_inputs_list = []


                #go thru list of tx inputs
                for i in range(0, len(list_of_tx_ins)):
                    #add each txn input to txn list to add for a single transaction
                    tx_hash = list_of_tx_ins[i][0]
                    output_index = list_of_tx_ins[i][1]
                    in_script_bytes = list_of_tx_ins[i][2]
                    sig_script = list_of_tx_ins[i][3]
                    sequence_num = list_of_tx_ins[i][4]
                    sig_script = hex_string_switch_endian(sig_script)
                    #TODO -- check the uxto hash is correct, also sig scripts.. got var names labelled unforunately
                    a_txn_input = {"utxo_hash": tx_hash, "index":int(output_index, 16), "input_script_size":int(in_script_bytes, 16), "input_script_bytes": sig_script, "sequence": int(sequence_num, 16)}
                    one_txn_inputs_list.append(a_txn_input)

                    #parse format
                    #a_transaction = [tx_hash, output_index, in_script_bytes, sig_script, sequence_num]
                     #tx_inputs.append(a_transaction)
                txn_object["txn_inputs"] = one_txn_inputs_list

                #now give txn object output info
                txn_object["txn_out_count"] = int(tx_out_count)

                one_txn_output_list = []
                for i in range(0, len(list_of_tx_out)):
                    #add each txn output to list of output list for a single txn
                    value, out_script_bytes, sig_script = list_of_tx_out[i][0], list_of_tx_out[i][1], list_of_tx_out[i][2]
                    sig_script = hex_string_switch_endian(sig_script)
                    a_txn_output = {"satoshis": int(value, 16), "output_script_size": int(out_script_bytes, 16), "output_script_bytes": sig_script}
                    one_txn_output_list.append(a_txn_output)
                    #parse format
                    #a_transaction = [value, out_script_bytes, sig_script]
                    #tx_outputs.append(a_transaction)

                txn_object["txn_outputs"] = one_txn_output_list
                txn_object["lock_time"] = int(lock_time, 16)

                #add object to txn list
                txn_list.append(txn_object)

            cur_block["transactions"] = txn_list

            all_blocks_list.append(cur_block)

            if (errors == True):
                break

            # TODO -- verify merkle tree root hash
            #all txns in a block added to list
            block_merk_root_hash = merk_root_hash(all_txns_in_a_block)

            #print("block", block_num, "merkle hash:", block_merk_root_hash)
            if (block_merk_root_hash != merkle_root_hash):
                print("error 6 block", block_num)
                errors = True
                break


        else:
            print("error 2 block", block_num)
            # error_type = "error 2 block " + str(block_num)
            errors = True
            break


    #Repeat if not done.
    else:
        print("error 1 block", block_num)
        # error_type = "error 1 block " + str(block_num)
        errors = True
        break
    block_num +=1

#ADD BLOCK NUM TO DICT AT END
mydict["blocks"] = all_blocks_list
mydict["height"] = block_num
#print(len(list_all_blocks_txn_bytes_str))

#OLD MERKLE VALIDATION
# merk_hash = merk_root_hash(list_all_blocks_txn_bytes_str)
# #print(merk_hash)
# #print("Finished most of program, done merkle hash now that i have read all the blocks...")
# mydict["merkle_hash"] = merk_hash #TODO -- change endianness? little to big if need to
#
# #print("Merk hash", merk_hash)
#
# #CHECK THAT THE MERKLE HASH IS EQUAL TO WHAT BLOCKCHAIN THINKS IT IS
# #print the blockchains merkle each time iterated to check if it is same throughout
#
# for i in range(0, len(list_of_each_block_merkle)):
#     #Verify each blocks merkle is good to go
#     if (list_of_each_block_merkle[i] != merk_hash):
#         #error!!!
#         errors = True
#
#         #print("ERROR SLICE", error_type[14:15])
#         is_other_error = len(error_type)
#         if (is_other_error > 2): #another error exists in this case. compare to see which to print
#             other_error_block = int(error_type[14:15])
#             if (other_error_block <= i):
#                 print(error_type)
#                 break
#             else:
#                 print("error 6 block", i)
#                 break
#         else:
#             print("error 6 block", i)
#             break


if (errors == False):
    print("no errors", block_num, "blocks")

    #Create json file if no errors
    json_content = json.dumps(mydict, indent=4, separators=(", ", ": "))
    json_file = file_name + ".json"
    with open(json_file, "w") as outfile:
        outfile.write(json_content)