import zmq
import time
import random

BLOCK_SIZE = 100

context = zmq.Context()

TO_RED_PORT    = 5500
TO_BLUE_PORT   = 5600

FROM_RED_PORT  = 5501
FROM_BLUE_PORT = 5601

src_red   = context.socket(zmq.REQ)
src_blue  = context.socket(zmq.REQ)
dest_red  = context.socket(zmq.PUSH)
dest_blue = context.socket(zmq.PUSH)

src_red.connect('tcp://*:%d'  % TO_RED_PORT)
src_blue.connect('tcp://*:%d' % TO_BLUE_PORT)
    
dest_red.connect('tcp://*:%d'  % FROM_RED_PORT)
dest_blue.connect('tcp://*:%d' % FROM_BLUE_PORT)

src_blue.send('give')
src_red.send('give')
_ = src_red.recv()
_ = src_blue.recv()
while True:
    if random.random() < 0.4:
        src_red.send('give')
        packet = src_red.recv()
        time.sleep(0.001)
        if random.random() < 0.5:
            dest_red.send(packet)
    else:
        src_blue.send('give')
        packet = src_blue.recv()
        time.sleep(0.001)
        if random.random() < 0.5:
            dest_blue.send(packet)
        
    