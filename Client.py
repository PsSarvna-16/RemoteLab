import socket

ip = '192.168.43.179'
port = 8888
print("********CLIENT SIDE**********")
soc = socket.socket()

soc.connect((ip,port))
print("Connected to the Server\n");
print("Led Blinking Code\n");

msg = soc.recv(1024).decode()
print(msg)

if(msg == "Arduino Not Conneced"):
	exit()
while True:
	msg = input("Enter '0.0 -> 1.0' or 'EXIT' : ")
	soc.send(bytes(msg,'utf-8'))
	print(soc.recv(1024).decode())
	if(msg == "EXIT" or msg == "TERMINATE"):
		exit()