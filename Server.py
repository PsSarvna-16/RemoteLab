import socket,time
from pyfirmata import Arduino,util, STRING_DATA

def lcd(arduino,text):
    if text:
        arduino.send_sysex( STRING_DATA, util.str_to_two_byte_iter( text ) )

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
			lcd(arduino," ")
		except:
			msg = "Arduino Not Connected"
			print("\n" + msg)
			client.send(bytes(msg,'utf-8'))
			exit()
		ser = arduino.get_pin('d:6:s')

		print("\n" + msg + "\n")
		client.send(bytes(msg,'utf-8'))

		while True:
			code = client.recv(1024).decode()
			print("User Input : " + code)

			if(code  == "EXIT"):
				ser.write(0)
				msg = "CONNECTION ABORTED BY USER!!"
				print(msg)
				client.send(bytes(msg,'utf-8'))
				time.sleep(1)
				arduino.exit()
				break;
			elif(code  == "TERMINATE"):
				ser.write(0)
				arduino.exit()
				msg = "SERVER TERMINATED !!"
				print(msg)
				client.send(bytes(msg,'utf-8'))
				exit()
			elif(int(code) >= 0 and int (code) <= 180 ):
				ser.write(int(code))
				msg = "Angle: " + code 
				lcd(arduino,str(code))
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