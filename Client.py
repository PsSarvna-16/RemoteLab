import socket
from tkinter import *
import time
import threading

class Socket:
	ip = ""
	port = 0
	con = ""

soc = Socket()
soc.ip = '192.168.43.179'
soc.port = 8888
con = ""

toggle = False

def Status(msg):
	status_e.delete(0,END)
	status_e.insert(0,msg)

def sendData(msg,soc):
	soc.send(bytes(msg,'utf-8'))
	if(msg == "EXIT" or msg == "TERMINATE"):
		exit()
	Status(soc.recv(1024).decode())
	return

def connectServer(ip,port):
	print("********CLIENT SIDE**********")
	soc.con = socket.socket()
	soc.con.connect((soc.ip,soc.port))
	print("Connected to the Server\n");
	print("Servo Motor Control\n");
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


def sendReal():
	prev = -1
	while real.get():
		if prev != slider.get():
			prev = int(slider.get())
			sendData(str(prev),soc.con)
			time.sleep(0.15)
		if not toggle:
			break

def sendLoop():
	update_L.config(state = DISABLED)
	val = sliderL.get()
	while True and val:
		for ang in range(0,181, val):
			sendData(str(ang),soc.con)
			time.sleep(0.1)
		time.sleep(0.5)
		for ang in range(180,-1,-1*val):
			sendData(str(ang),soc.con)
			time.sleep(0.1)
		sendData("0",soc.con)
		if not loop.get():
			break
	update_L.config(state = NORMAL)

def realThreading():
	thread1 = threading.Thread(target = sendReal)
	thread1.start()

def loopThreading():
	thread2 = threading.Thread(target = sendLoop)
	thread2.start()

def key_pressed(event):
 global toggle
 toggle = not toggle
 print(toggle)


window = Tk()
window.title("Remote Lab")
window.geometry("250x350")

real = BooleanVar()
loop = BooleanVar()

connect_b = Button(window,width=20, text ="Connect to Server", command = lambda:connectServer(soc.ip,soc.port))
connect_b.place(x=50,y=10)

lineh = Canvas(window,width = 230, height = 1 , bg = "black")
lineh.place(x=10,y=45)

real_cb = Checkbutton(window, text ="Angle",variable = real,offvalue = False,onvalue = True)
real_cb.place(x=100,y=60)

slider = Scale(window,from_ = 0, to = 180,state = DISABLED, orient = HORIZONTAL)
slider.place(x=20,y=95)

update_b = Button(window, text ="Update",state = DISABLED,command = lambda:realThreading() )
update_b.place(x=150,y=115)

lineh = Canvas(window,width = 230, height = 1 , bg = "black")
lineh.place(x=10,y=150)


loop_ch = Checkbutton(window, text ="Loop",variable = loop ,offvalue = False,onvalue = True)
loop_ch.place(x=100,y=165)

sliderL = Scale(window,from_ = 0, to = 45, orient = HORIZONTAL)
sliderL.place(x=20,y=200)

update_L = Button(window, text ="Update",state = NORMAL, command = lambda:loopThreading())
update_L.place(x=150,y=220)

lineh = Canvas(window,width = 230, height = 1 , bg = "black")
lineh.place(x=10,y=255)

status_e = Entry(window,width = 30,justify = "center",background= "#EBEBEB")
status_e.place(x=35,y=275)
Status("Not Connected")

exit_b = Button(window, text ="Exit", command = lambda:sendData("EXIT",soc.con),state = DISABLED)
exit_b.place(x=30,y=315)

term_b = Button(window, text ="Terminate", command = lambda:sendData("TERMINATE",soc.con),state = DISABLED)
term_b.place(x=160,y=315)

window.bind("<F12>",key_pressed)


window.mainloop()