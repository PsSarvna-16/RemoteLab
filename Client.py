import socket
from tkinter import *

class Socket:
	ip = ""
	port = 0
	con = ""

soc = Socket()
soc.ip = '192.168.43.179'
soc.port = 8888
con = ""

def Status(msg):
	status_e.config(state = NORMAL)
	status_e.delete(0,END)
	status_e.insert(0,"Status : "+msg)
	status_e.config(state =DISABLED)

def sendData(msg,soc):
	soc.send(bytes(msg,'utf-8'))
	Status(soc.recv(1024).decode())
	if(msg == "EXIT" or msg == "TERMINATE"):
		exit()
	return

def connectServer(ip,port):
	print("********CLIENT SIDE**********")
	soc.con = socket.socket()
	soc.con.connect((soc.ip,soc.port))
	print("Connected to the Server\n");
	print("Led Blinking Code\n");
	msg = soc.con.recv(1024).decode()
	Status(msg)
	if(msg == "Arduino Not Conneced"):
		exit()
	slider.config(state = NORMAL)
	update_b.config(state = NORMAL)
	exit_b.config(state = NORMAL)
	term_b.config(state = NORMAL)
	connect_b.configure(text = "Connected")
	return

window = Tk()
window.title("Remote Lab")
window.geometry("250x250")

connect_b = Button(window, text ="Connect to Server", command = lambda:connectServer(soc.ip,soc.port))
connect_b.pack(pady =10)

slider = Scale(window,from_ = 0, to = 100,state = DISABLED, orient = HORIZONTAL)
slider.pack(pady =10 )

update_b = Button(window, text ="Update Changes",state = DISABLED, command = lambda:sendData(str(float(slider.get())),soc.con))
update_b.pack(pady =10 )

status_e = Entry(window,width = 30,justify = "center",background= "#EBEBEB")
status_e.pack(pady =10)
Status("Not Connected")

exit_b = Button(window, text ="Exit", command = lambda:sendData("EXIT",soc.con),state = DISABLED)
exit_b.pack(padx =10 , side = LEFT)

term_b = Button(window, text ="Terminate", command = lambda:sendData("TERMINATE",soc.con),state = DISABLED)
term_b.pack(padx =10 ,side = RIGHT)

window.mainloop()