import socket
import pickle
import aes_1705098
import rsa_1705098

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

k=32
rsa_obj = rsa_1705098.RSA(k)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = pickle.loads(data)
            """
            data = [encrypted_msg , encrypted_key , public_key]
            """
            encrypted_msg = data[0]
            encrypted_key = data[1]
            public_key = data[2]
            pad_amount = data[3]

            rsa_obj.e = public_key[0]
            rsa_obj.n = public_key[1]
            
            # set d
            directory = "Don't Open this"
            f = open(directory + "/private_key.txt","r")
            contents =f.read()
            f.close()
            #print(contents)
            rsa_obj.d = int(contents)
            
            # get AES key
            key = rsa_obj.decrypt(encrypted_key)
            print("decrypted key = " + key)
            k=""
            for c in key:
                k += format(ord(c), "x")
            
            aes_obj = aes_1705098.AES(k)
            
            # decrypt msg
            decrypted_msg = ""
            for i in range(0 , len(encrypted_msg) , 32):

                msg = aes_obj.decipher(encrypted_msg[i:i+32])
                decrypted_msg += bytearray.fromhex(msg).decode()

            n = len(decrypted_msg)
            decrypted_msg = decrypted_msg[:n-pad_amount]

            f = open(directory + "/private_key.txt","w")
            f.write(decrypted_msg)
            f.close()

            #s.send(pickle.dumps("ack"))

            print("decrypted msg = " + decrypted_msg)