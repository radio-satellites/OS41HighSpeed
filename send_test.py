import pigpio
from nrf24 import *
import sys

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

f = open("test_full.jpg",'rb')
while True:
    data = f.read(32)
    if not data:
        break
    nrf.send(data)
f.close()
