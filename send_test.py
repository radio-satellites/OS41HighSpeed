import pigpio
from nrf24 import *
import sys
import time

from picamera2 import Picamera2, Preview

print("Initializing Camera...")

picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.start()
time.sleep(2)

image_counter = 0

payload = bytearray(32) #32 bytes of zeros

hostname = 'localhost'
port = 8888

# Connect to pigpiod
print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
pi = pigpio.pi(hostname, port)
if not pi.connected:
    print("Not connected to pigpiod deamon. Exiting.")
    sys.exit()

nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MAX)
#nrf.set_address_bytes(len(address))
#nrf.open_writing_pipe(address)
while True:
    #Capture image
    print("Sending image "+str(image_counter))
    image_counter = image_counter + 1
    picam2.switch_mode_and_capture_file(capture_config, "image.jpg")
    f = open("image.jpg",'rb')
    counter = 0
    while True:
        data = f.read(32)
        if not data:
            break
        nrf.send(data)
        if counter % 100 == 0:
            print(str((counter*32)/1024)+"kB sent")
        counter = counter + 1
        
    f.close()
