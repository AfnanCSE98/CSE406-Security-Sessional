from BitVector import *
import math
import time

class RSA:
    
    k = 0
    n = 0
    phi_n = 0
    p = 0
    q = 0
    e = 0
    d = 0

    def __init__(self, k):
       
        self.k = k

    def generate_pq(self , sz):
        bv = BitVector(intVal = 0)
        p = bv
        
        while(1):
            bv = bv.gen_random_bits(sz)  
            check = bv.test_for_primality()
            if abs(check - 1)<= 0.01:
                p = bv
                break
        q = bv
        check = 0
        while( abs(check - 1)>= 0.01):
            bv = bv.gen_random_bits(sz)  
            if p.hamming_distance(bv) == 0: continue
            check = bv.test_for_primality()

        q = bv

        self.p = p.int_val()
        self.q = q.int_val()


    def set_n(self):
        self.n = self.p * self.q

    def set_phi_n(self):
        self.phi_n = (self.p-1)*(self.q-1)

    def set_e(self):
        self.e = -1
        for i in range(2,self.phi_n):
            if(math.gcd(i , self.phi_n) == 1):
                self.e = i
                break
        self.public = (self.e , self.n)

    def set_d(self):
        i = 1
        while((self.phi_n*i +1) % self.e != 0 ):
            i = i+1

        self.d = (self.phi_n*i +1) // self.e
        self.private = (self.d , self.n)

    def encrypt(self , text_to_cipher):
        cipher_list = []
        for c in text_to_cipher:
            asci = ord(c)
            cipher = pow(asci , self.e , self.n)
            cipher_list.append(cipher)
        return cipher_list
    
    def decrypt(self , cipher_list):

        decrypted = ""
        for el in cipher_list:
            deciphered_ascii = pow(el , self.d , self.n)
            decrypted += chr(deciphered_ascii)
        return decrypted

if __name__ == "__main__":
    
    print("Enter text to cipher:" , end='')
    msg = input()
    
    K = [16 , 32 , 64 , 128]
    for k in K:

        print("-----------k = "+ str(k) + "------------")
        rsa = RSA(k)

        #----key generation------
        start_time = time.time()
        rsa.generate_pq(int(k/2))
        print("Key Generation : %s seconds" % (time.time() - start_time))

        rsa.set_n()
        rsa.set_phi_n()
        rsa.set_e()
        rsa.set_d()

        print("Generated Keys\npublic : " + str(rsa.public) + "private : " + str(rsa.private))

        
        #----encryption------
        start_time = time.time()
        cipher_list = rsa.encrypt(msg)
        print("Encryption : %s seconds" % (time.time() - start_time))

        print("cipher text\n " + str(cipher_list))

        #----decrypt----------
        start_time = time.time()
        decrypted_msg = rsa.decrypt(cipher_list)
        print("Decryption : %s seconds" % (time.time() - start_time))

        print("Decrypted_msg : " + decrypted_msg)
