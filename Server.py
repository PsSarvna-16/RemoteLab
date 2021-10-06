import socket,time
from pyfirmata import Arduino,util, STRING_DATA

def lcd(arduino,text):
    if text:
        arduino.send_sysex( STRING_DATA, util.str_to_two_byte_iter( text ) )


class Socket():
	self.name = ""
	self.ip = ""
	self.port = ""
	self.soc = ""

	def __init__(self,port):
		self.soc = socket.socket()
		self.name = socket.gethostname()
		self.ip = socket.gethostbyname(name)
		self.soc.bind(('',port))
		self.soc.listen(1)



try:
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
				lcd(arduino,'S')
				time.sleep(1)
				arduino.exit()
				break;
			elif(code  == "TERMINATE"):
				ser.write(0)
				time.sleep(1)
				lcd(arduino,'S')
				time.sleep(1)
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
		ser.soc.close()
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