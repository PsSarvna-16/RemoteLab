import socket
from pyfirmata import Arduino

try:
	soc = socket.socket()
	print('Socket created')

	port = 8888
	name = socket.gethostname()
	ip = socket.gethostbyname(name)
	print(f"{name} :  {ip} : {port}")

	soc.bind(('',port))
	soc.listen(1)

	while True:
		print('\nwaiting For Clients..')
		try:
			client.close()
		except:
			pass

		client,addr = soc.accept()
		print(f"Connected with {addr}")

		try:
			arduino = Arduino('COM3')
			msg = "Connected Successfully"
		except:
			msg = "Arduino Not Connected"
			print("\n" + msg)
			client.send(bytes(msg,'utf-8'))
			exit()
		led = arduino.get_pin('d:9:p')

		print("\n" + msg + "\n")
		client.send(bytes(msg,'utf-8'))

		while True:
			code = client.recv(1024).decode()
			print("User Input : " + code)

			if(code  == "100.0"):
				led.write(1)
				msg = "Led is On"
			elif(code  == "0.0"):
				led.write(0)
				msg = "Led is OFF"
			elif(code  == "EXIT"):
				led.write(0)
				arduino.exit()
				msg = "CONNECTION ABORTED BY USER!!"
				print(msg)
				client.send(bytes(msg,'utf-8'))
				break;
			elif(code  == "TERMINATE"):
				led.write(0)
				arduino.exit()
				msg = "SERVER TERMINATED !!"
				print(msg)
				client.send(bytes(msg,'utf-8'))
				exit()
			elif(float(code) > 0.0 and float(code) < 100.0 ):
				led.write(float(code)/100)
				msg = "Led duty Cycle : " + code 
			else:
				msg = "Invalid Input"
			print(msg)
			client.send(bytes(msg,'utf-8'))
finally:
	try:
		soc.close()
	except:
		pass	
	try:
		arduino.exit()
	except:
		pass
	try:
		client.close()
	except:
		pass