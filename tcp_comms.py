import socket

FILENAME = 'samples.raw'

PORT         = 1234
IP_ADDR      = "127.0.0.1"

SIZE_COMPLEX = 8
NUM_SAMPLES  = 32
NUM_BYTES    = NUM_SAMPLES * SIZE_COMPLEX


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP_ADDR, PORT))

with open(FILENAME, 'rb') as fh:
    while True:
        samples = fh.read(NUM_BYTES)
        if len(samples) == 0:
            break
        
        sock.send(samples)

sock.close()