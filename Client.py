import socket
from tkinter import *
import time

def sendData(msg,soc):
	soc.send(bytes(msg,'utf-8'))
	print(soc.recv(1024).decode())
	if(msg == "EXIT" or msg == "TERMINATE"):
		exit()
	return

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


window = Tk()
window.title("Remote Lab")
window.geometry("250x150")
slider_val = 0
slider = Scale(window, variable = slider_val, from_ = 0, to = 100, orient = HORIZONTAL)
slider.pack(pady =10 )

soc = connectServer(ip,port)

update_b = Button(window, text ="Update Changes", command = lambda:sendData(str(float(slider.get())),soc))
update_b.pack(pady =10 )

exit_b = Button(window, text ="Exit", command = lambda:sendData("EXIT",soc))
exit_b.pack(padx =20 , side = LEFT)

term_b = Button(window, text ="Terminate", command = lambda:sendData("TERMINATE",soc))
term_b.pack(padx =20 ,side = RIGHT)
window.mainloop()
