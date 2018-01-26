
from bluetooth import *
import time
import Adafruit_ADXL345

accel = Adafruit_ADXL345.ADXL345()

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [SERIAL_PORT_PROFILE], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        x, y, z = accel.read()
        data = "X=" + str(x) + " Y=" + str(y) + " Z=" + str(z)
        client_sock.send(data)
        time.sleep(0.1)
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
