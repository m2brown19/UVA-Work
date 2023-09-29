#!/usr/bin/env python3

import socket

#Make TCP Connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.connect(("127.0.0.1", 25))
	#sock.connect(("1.1.1.2", 25))
	
	#Read server greeting
	data = sock.recv(4096)
	response = data.decode('utf-8')
	
	if not response.startswith('220'):
		raise Exception('220 reply not received from server.')
		
	#Send HELO command and get response
	cmd_HELO = 'HELO alice\r\n'
	print(cmd_HELO)
	sock.send(cmd_HELO.encode())
	
	response = sock.recv(4096).decode('utf-8')
	print(response)
	
	if not response.startswith('250'):
		raise Exception('250 reply not received from server.')
		
	#Send MAIL FROM command
	cmd_MAIL_FROM = 'MAIL FROM: <mjb4us@virginia.edu>\r\n'
	print(cmd_MAIL_FROM)
	sock.send(cmd_MAIL_FROM.encode())
	
	response = sock.recv(4096).decode('utf-8')
	print(response)
	if not response.startswith('250'):
		raise Exception('250 reply not received from server')
	

	
	#Send RCPT TO command. send to <sys> 
	cmd_RCPT_TO = 'RCPT TO: <sys>\r\n'
	print(cmd_RCPT_TO)
	sock.send(cmd_RCPT_TO.encode())
	response = sock.recv(4096).decode('utf-8')
	print(response)
	if not response.startswith('250'):
		raise Exception('250 reply not received from server')
	

	#send DATA cmd
	cmd_DATA = "DATA\r\n"
	cmd_SUBJECT = "SUBJECT: GREETINGS\r\nHi there, how's the weather? From Mike\r\n"
	cmd_PERIOD = ".\r\n"
	print(cmd_DATA)
	sock.send(cmd_DATA.encode())
	response = sock.recv(4096).decode('utf-8')
	print(response)
	if not response.startswith('354'):
		raise Exception('354 reply not received from server')
	
	
	sock.send(cmd_SUBJECT.encode())
	sock.send(cmd_PERIOD.encode())
	
	
	response = sock.recv(4096).decode('utf-8')
	print(response)
	if not response.startswith('250'):
		raise Exception('250 reply not received from server')
	
	
	#Send msg data
	
	#End with line with single period
	
	#send QUIT cmd
	cmd_QUIT = "QUIT\r\n"
	sock.send(cmd_QUIT.encode())
	response = sock.recv(4096).decode('utf-8')
	print(response)
	if not response.startswith('221'):
		raise Exception('221 reply not received from server')

		
	#Accept response??????
	
	#Close socket when done
	sock.close() #may not be needed with with statement...
	
