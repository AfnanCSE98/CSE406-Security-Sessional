import aes_1705098
import tqdm
import os
from BitVector import * 
import time



decipher_output = BitVector(size=0)
AES_output = BitVector(size=0)
AES_input = BitVector(size=0)

pad_count_input = 0

def input_file():
    global AES_input, pad_count_input, input_filename

    input_filename = input("Enter filename : ")

    file = open("{}".format(input_filename), "rb")
    file_content = bytes.hex(file.read())
    file.close()

    # padding
    if (len(file_content) % 32) != 0:
        pad_count_input = 32 - len(file_content) % 32
        file_content = file_content + "0" * pad_count_input
    elif len(file_content) == 0:
        return False

    AES_input += BitVector(hexstring=file_content)

def output_file():
    global decipher_output

    file = open("orig_{}".format(input_filename), "wb+")
    file.write(bytes.fromhex(decipher_output.get_bitvector_in_hex()[: len(decipher_output.get_bitvector_in_hex()) - pad_count_input]))
    file.close()

    print("File decrypted successfully")


def pad_key(str):
    n = len(str)
    if n == 16:
        return str 
    elif n < 16:
        for _ in range(n , 16):
            str += '0'
        return str 
    else:
        return str[:16]
    

key = input("Enter AES key : ")
key = pad_key(key)

k=""
for c in key:
    k += format(ord(c), "x")

aes_obj = aes_1705098.AES(k)

input_file()

#print(len(AES_input.get_bitvector_in_hex())/32)
#print(AES_input.get_bitvector_in_hex()[: 32])
out=""
for i in range(0 , len(AES_input.get_bitvector_in_hex()) , 32):
        out += aes_obj.cipher(AES_input.get_bitvector_in_hex()[i : i + 32])

AES_output = BitVector(hexstring=out)

print("File Cipher (hex) : " + AES_output.get_bitvector_in_hex())

print("\nDeciphering....")

global decryption_time



out=""
for i in range(len(AES_output.get_bitvector_in_hex()) // 32):
    out += aes_obj.decipher(AES_output.get_bitvector_in_hex()[i * 32: i * 32 + 32])

decipher_output = BitVector(hexstring = out)


output_file()

