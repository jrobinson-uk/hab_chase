#!/usr/bin/python3
from piGPS import GPS
from tkinter import *
from PIL import Image,ImageTk
import glob
import os
from time import sleep
import random


try:
    gps = GPS(log=True)
except :
    print("Serial Exception")

window = Tk()

window.overrideredirect(1)
screen_width = 800
screen_height = 480

try:
    file = max(glob.iglob('/home/pi/lora-gateway/ssdv/*.JPG'), key=os.path.getctime)
    print(file)
    im = Image.open(file)
    im = ImageTk.PhotoImage(im.resize((256,192)))
    
except:
    print("Error Loading Image")

up = Image.open("/home/pi/hab_chase/icons/up.png")
up = ImageTk.PhotoImage(up.resize((28,28)))

cross = Image.open("/home/pi/hab_chase/icons/close.png")
cross = ImageTk.PhotoImage(cross.resize((28,28)))

down = Image.open("/home/pi/hab_chase/icons/down.png")
down = ImageTk.PhotoImage(down.resize((28,28)))

ear = Image.open("/home/pi/hab_chase/icons/ear.png")
ear = ImageTk.PhotoImage(ear.resize((28,28)))

car = Image.open("/home/pi/hab_chase/icons/car.png")
car = ImageTk.PhotoImage(car.resize((28,28)))


def upDigit(label):
    oldval = int(label.cget("text"))
    if oldval == 9:
        newval = str(0)
    else:
        newval = str(oldval + 1)
    label.config(text = newval)

def downDigit(label):
    oldval = int(label.cget("text"))
    if oldval == 0:
        newval = str(9)
    else:
        newval = str(oldval - 1)
    label.config(text = newval)

def launchAirspy():
    print("Launching Airspy")
    freq = ''.join([dg1.cget("text"),dg2.cget("text"),dg3.cget("text"),dg4.cget("text"),dg5.cget("text"),dg6.cget("text"),dg7.cget("text")])
    os.system("killall airspy_rx")
    os.system("killall test_rx")
    cmd = 'xterm -into {0} -e /home/pi/hab_chase/launch_rx {1} -geometry 60x20 -sb &'.format(rx_wid,freq)
    print(cmd)
    os.system(cmd)

def close():
    os.system("killall test_rx")
    os.system("killall airspy_rx")
    window.quit()

def toggleMap():
    pass

rxImg = Label(window,bd = 1,image=im)
rxImg.grid(row=0,column=1,columnspan=7)#,sticky=N+S+E+W)




dg1 = Label(window,text ="4")
dg1.grid(row=3,column=1)
dg2 = Label(window,text ="3")
dg2.grid(row=3,column=2)
dg3 = Label(window,text ="4")
dg3.grid(row=3,column=3)
dg4 = Label(window,text =".")
dg4.grid(row=3,column=4)
dg5 = Label(window,text ="2")
dg5.grid(row=3,column=5)
dg6 = Label(window,text ="5")
dg6.grid(row=3,column=6)
dg7 = Label(window,text ="0")
dg7.grid(row=3,column=7)

up1 = Button(window,text ="^", image = up,command = lambda: upDigit(dg1)).grid(row=2,column=1)
up2 = Button(window,text ="^", image = up,command = lambda: upDigit(dg2)).grid(row=2,column=2)
up3 = Button(window,text ="^", image = up,command = lambda: upDigit(dg3)).grid(row=2,column=3)
up4 = Button(window,text ="^", image = up,command = lambda: upDigit(dg5)).grid(row=2,column=5)
up5 = Button(window,text ="^", image = up,command = lambda: upDigit(dg6)).grid(row=2,column=6)
up6 = Button(window,text ="^", image = up,command = lambda: upDigit(dg7)).grid(row=2,column=7)

latLbl = Label(window,text="Lat :").grid(row=1,column=1)
lonLbl = Label(window,text="Lon :").grid(row=1,column=5)
lat=StringVar()
lon=StringVar()
latVal = Label(window,textvariable=lat)
latVal.grid(row=1,column=2,columnspan=2)
lonVal = Label(window,textvariable=lon)
lonVal.grid(row=1,column=6,columnspan=2)

chase_map = Button(window,text ="Car", image=car,command = toggleMap).grid(row=1,column=8)

closeApp = Button(window,image=cross,command=close).grid(sticky=N,row=0,column=8)

airspy = Button(window,text ="Go", image=ear,command = launchAirspy).grid(row=3,column=8)

dn1 = Button(window,text ="^", image = down,command = lambda: downDigit(dg1)).grid(row=4,column=1)
dn2 = Button(window,text ="^", image = down,command = lambda: downDigit(dg2)).grid(row=4,column=2)
dn3 = Button(window,text ="^", image = down,command = lambda: downDigit(dg3)).grid(row=4,column=3)
dn4 = Button(window,text ="^", image = down,command = lambda: downDigit(dg5)).grid(row=4,column=5)
dn5 = Button(window,text ="^", image = down,command = lambda: downDigit(dg6)).grid(row=4,column=6)
dn6 = Button(window,text ="^", image = down,command = lambda: downDigit(dg7)).grid(row=4,column=7)



gateway = Frame(window, height=350, width=500)
gateway.grid(row=0,rowspan=2,column=0,sticky=N+E+S+W,padx=5,pady=5)
gw_wid = gateway.winfo_id()

rx = Frame(window, height=100, width=500)
rx.grid(row=2,rowspan=3,column=0,sticky=N+E+S+W,padx=5,pady=5)
rx_wid = rx.winfo_id()

os.system('xterm -into %d -e /home/pi/hab_chase/launch_gateway -geometry 60x20 -sb &' % gw_wid)

os.system('xterm -into %d -e /home/pi/hab_chase/test_rx -hold -geometry 60x20 -sb &' % rx_wid)

window.geometry("{0}x{1}+0+0".format(screen_width,screen_height))
window.focus_set()

def main():
    print("Main")
    window.after(2000,main)

    try:
        file = max(glob.iglob('/home/pi/lora-gateway/ssdv/*.JPG'), key=os.path.getctime)
        print(file)
        im = Image.open(file)
        im = ImageTk.PhotoImage(im.resize((256,192)))
        

        rxImg.configure(image = im)
        rxImg.image=im
        
    except:
        print("Error Updating")
        
    

    if gps.fix:
        lat.set(gps.lat)
        lon.set(gps.lon)
    



        

              

window.after(2000,main)
window.mainloop()
print("1")
