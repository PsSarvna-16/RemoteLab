import socket

def sendData(msg,soc):
	soc.send(bytes(msg,'utf-8'))
	print(soc.recv(1024).decode())
	if(msg == "EXIT" or msg == "TERMINATE"):
		exit()

def connectServer(ip,port):
	print("********CLIENT SIDE**********")
	soc = socket.socket()

	soc.connect((ip,port))
	print("Connected to the Server\n");
	print("Led Blinking Code\n");

	msg = soc.recv(1024).decode()
	print(msg)
	
	if(msg == "Arduino Not Conneced"):
		exit()
	return soc


ip = '192.168.43.179'
port = 8888
soc = connectServer(ip,port)

while True:
	msg = input("Enter '0.0 -> 1.0' or 'EXIT' : ")
	sendData(msg,soc)