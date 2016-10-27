import time
from multiprocessing import Process, Value, Array
from binascii import crc32
from constants import *

#third-part libs
import zmq
import numpy as np

# State
# running
# single team mode (Red team)
# game_time *10
# Red pulled, verified, last_time * 10
# Blue pulled, verified, last_time * 10


####### object to be shared between server and display processes #########
game_state = Array('i', [0]*9)


RUNNING, TIME, SINGLE_TEAM, RED_PULLED, RED_VERIFIED, RED_LAST, BLUE_PULLED, BLUE_VERIFIED, BLUE_LAST = range(len(game_state))

def reset():
    single = game_state[SINGLE_TEAM]  # preserve this one value
    for i in range(len(game_state)):
        game_state[i] = 0
    game_state[SINGLE_TEAM] = single

def demo(game_time):
    game_state[RED_PULLED]   += 75
    game_state[RED_VERIFIED] += 61
    game_state[RED_LAST] = int(game_time)

class Server(Process):
    def __init__(self):
        Process.__init__(self)
        self.blocks = {}
            
    def run(self):
        while True:
            while not game_state[RUNNING]:
                time.sleep(0.5)
                
            self.initComms()
            self.count = 0
            self.start = time.time()
            reset()
            game_state[RUNNING] = True
            print 'Starting match'
            self.sendPacket(self.src_red)
            if not game_state[SINGLE_TEAM]:
                self.sendPacket(self.src_blue)

            while game_state[RUNNING]:
                game_time = time.time() - self.start
                game_state[TIME] = int(10*game_time)
                readable, _w, _e = zmq.select(self.sockets, 
                                                            [], 
                                                            [], timeout=TIMEOUT) 
                for conn in readable:
                    if conn in self.src_lookup:
                        req = conn.recv()
                        self.sendPacket(conn)
                        
                    elif self.checkBlock(conn.recv()):
                        verified_index, last_index = self.dest_lookup[conn]
                        game_state[verified_index] += 1
                        game_state[last_index]      = int(game_time)
                                    
                self.checkEndGame(game_time)
        
            self.dropComms()
            
    def sendPacket(self, conn):
        index = self.src_lookup[conn]
        conn.send(self.makeBlock())
        game_state[index] += 1
                            
    def initComms(self):
        ''' initialize all of the socket objects and
            wait for the clients to connect'''
        print 'initComms'
        self.context = context = zmq.Context()
        
        self.src_red   = context.socket(zmq.REP)
        self.src_blue  = context.socket(zmq.REP)

        self.dest_red  = context.socket(zmq.PULL)
        self.dest_blue = context.socket(zmq.PULL)
        
        self.src_red.bind('tcp://0.0.0.0:%d' % PORT_IN_RED)
        self.src_blue.bind('tcp://0.0.0.0:%d' % PORT_IN_BLUE)
            
        self.dest_red.bind('tcp://0.0.0.0:%d' % PORT_OUT_RED)
        self.dest_blue.bind('tcp://0.0.0.0:%d' % PORT_OUT_BLUE)
        
        # build some convenience objects for later reference
        self.sockets = [self.src_red, self.src_blue, self.dest_red, self.dest_blue]
        
        self.dest_lookup = {self.dest_red  : (RED_VERIFIED,  RED_LAST),
                            self.dest_blue : (BLUE_VERIFIED, BLUE_LAST)}
                       
        self.src_lookup = {self.src_red   : RED_PULLED,
                           self.src_blue  : BLUE_PULLED}
        
        # wait for the initial connection from the competitors                           
        req = self.src_red.recv()
        if not game_state[SINGLE_TEAM]:
            req = self.src_blue.recv()
        
    def dropComms(self):
        self.context.destroy(linger=False)

    def makeBlock(self):
        block    = np.fromstring(np.random.bytes(BLOCK_SIZE), dtype=np.int32)
        block[0] = self.count
        block    = block.tostring()
        self.blocks[self.count] = crc32(block)
        self.count += 1
        return block
        
    def checkBlock(self, block):
        index = np.fromstring(block, dtype=np.int32)[0]
        if index in self.blocks:
            if crc32(block) == self.blocks[index]:
                del self.blocks[index]
                return True
        return False

    def checkEndGame(self, game_time):
        game_state[RUNNING] = game_state[RUNNING] and (not ((game_time >= GAME_TIME) or 
                        (game_state[RED_VERIFIED]  >= NUM_BLOCKS) or
                        (game_state[BLUE_VERIFIED] >= NUM_BLOCKS)))      
    

if __name__ == '__main__':
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    local_ip_address = s.getsockname()[0]
    print local_ip_address

    s = Server()
    s.start()
    game_state[RUNNING] = True
    game_state[SINGLE_TEAM] = True
    try:
        while True:
            time.sleep(1)
    except KeyboardError:
        s.terminate()
        s.join()
    print 'done'
