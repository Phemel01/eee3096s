
import busio
import digitalio
import board 
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
import time
import datetime
import threading
stime=1             #sample time on screen
clo= time.time()
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

chan = AnalogIn(mcp, MCP.P1)

chan2 = AnalogIn(mcp, MCP.P2)
def sen_val():
       nt=time.time()
       global stime
       global clo                 #Time since last cycle
       tn=round(nt-clo)           #Run time calculated
       thread =threading.Timer(stime, sen_val)
       thread.daemon =True
       thread.start()
       temp=chan.voltage
       print(f"{str(tn):<15}{str(chan.value):^6}{str(round((chan.voltage-0.5)/0.0105,2))+' C':^30}{str(chan2.value):^1}")

       clo=nt         # set previous runtime to the current time for next iteration

# create the spi bus
def setup():
       #setup button pin 36 board
       
       GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
       GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback, bouncetime=200)
def my_callback(channel1):
       global stime
       tm= time.time()
       while GPIO.input(channel1)==0:
             break
       dtime=time.time()-tm
       #print("testing")
       if  stime==1:
                 stime=5
       elif stime==5:
                 stime=10
       else:
                 stime=1
       #print(dtime)
       if  dtime>=0.1:
           pass


# create the cs (chip select)

# create the mcp object

# create an analog input channel on pin 0





if __name__=="__main__":
   try:
      setup()
      print(f"{'Runtime':<15}{'Temp Reading':^10}{'Temp':^15}{'Light Reading':>22}")
      sen_val()
      while True:
           pass
   except Exception as e:
      print(e)
   finally:
      GPIO.cleanup()

