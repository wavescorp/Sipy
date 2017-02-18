import binascii
import socket
import machine
from network import Bluetooth
from network import Sigfox
from machine import Timer
import time

#initialiser SigFox
sig = Sigfox(mode=Sigfox.SIGFOX,  rcz=Sigfox.RCZ1)
s = socket.socket(socket.AF_SIGFOX,  socket.SOCK_RAW)
s.setblocking(True)
s.setsockopt(socket.SOL_SIGFOX,  socket.SO_RX,  False)

#setup a RTC
rtc = machine.RTC()
#rtc.ntp_sync("0.dk.pool.ntp.org") #kald til RTC-server
#print(rtc.now())

#Bluetooth object
bluetooth = Bluetooth()
#Chrono object fra Timer<-machine  - agerer stopur
timeCounter = Timer.Chrono()

#BT-scan - paramter=sekunder, -1 = scanning uden stop
bluetooth.start_scan(-1)
timeCounter.start()
while bluetooth.isscanning():
    adv = bluetooth.get_adv()
    if adv:
        mac = adv[0]
        mac = binascii.hexlify(mac)
        mac = mac.decode()
        if mac=='665544332211': #dummy mac adresse fra C-koden på sensors MCU
            print(adv)
            data = binascii.hexlify(adv[4])
            data = data.decode()
            
            timeElapsed = timeCounter.read()
            timeElapsed = round(timeElapsed, 3)
            print(data[24], data[25], data[28], data[29], timeElapsed)
            stringToSend =""
            stringToSend +=str(data[24])
            stringToSend +=str(data[25])
            stringToSend +=str(data[28])
            stringToSend +=str(data[29])
            stringToSend +=str(timeElapsed)
            #sender via SigFox objektet
            s.send(stringToSend)
            #sover 1000 sekunder
            time.sleep(1000) 
            

#24-25-28-29
