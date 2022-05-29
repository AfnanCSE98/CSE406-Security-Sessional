import socket
import aes_1705098
import rsa_1705098
import pickle 
import os
import time 

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def pad(str):
    
    n = len(str)
    if n == 16:
        return str 
    elif n < 16:
        for _ in range(n , 16):
            str += '0'
        return str 
    else:
        nearest_multiple = 16*(1 + int(n/16))
        for _ in range(n , nearest_multiple):
            str += '0'
        return str 

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

text =input("Enter msg to cipher : ")
text_to_cipher = pad(text)
pad_amount = len(text_to_cipher) - len(text)

k=""
for c in text_to_cipher:
    k += format(ord(c), "x")

encrypted_msg =""

for i in range(0 , len(k) , 32):
    encrypted_msg += aes_obj.cipher(k[i:i+32])


k=32
rsa_obj = rsa_1705098.RSA(k)
rsa_obj.generate_pq(int(k/2))
rsa_obj.set_n()
rsa_obj.set_phi_n()
rsa_obj.set_e()
rsa_obj.set_d()

encrypted_key = rsa_obj.encrypt(key)

public_key = rsa_obj.public

data = [encrypted_msg , encrypted_key , public_key , pad_amount]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data=pickle.dumps(data)
    
    #keep private key in a folder
    directory = "Don't Open this"
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(directory + "/private_key.txt","w+")
    f.write(rsa_obj.d.__str__())
    f.close()

    s.send(data)

    #while(pickle.loads(s.recv(1024)) != "ack"):
    #    continue
    time.sleep(2)

    f = open(directory + "/private_key.txt","r")
    contents =f.read()
    f.close()

    if( contents == text):
        print("Successful")
    else:
        print("didn't match!")