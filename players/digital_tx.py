#!/usr/bin/env python
#
# Copyright 2010,2011 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, blocks
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import numpy as np
import time

# From gr-digital
from gnuradio import digital

# from current dir
from transmit_path import transmit_path
from osmo_interface import osmo_transmitter
from constants import *

import time, struct, sys, zmq


# ======================================================================== #
#                          Transmitter Top Block                           #
# ======================================================================== #

class tx_top_block(gr.top_block):
    def __init__(self, modulator, options):
        gr.top_block.__init__(self)

        if (options.tx_freq is not None):
            # Work-around to get the modulation's bits_per_symbol
            kwargs = modulator.extract_kwargs_from_options(options)
            symbol_rate = options.bitrate / modulator(**kwargs).bits_per_symbol()

            self.sink = osmo_transmitter(options.args, symbol_rate,
                                         options.samples_per_symbol,
                                         options.tx_freq, options.tx_gain,
                                         options.antenna, options.bandwidth)
            options.samples_per_symbol = self.sink._sps
            
        #elif (options.to_file is not None):
        #    sys.stderr.write(("Saving samples to '%s'.\n\n" % (options.to_file)))
        #    self.sink = gr.file_sink(gr.sizeof_gr_complex, options.to_file)
        else:
            sys.stderr.write("No sink defined, dumping samples to null sink.\n\n")
            self.sink = blocks.null_sink(gr.sizeof_gr_complex)

        # do this after for any adjustments to the options that may
        # occur in the sinks (specifically the Osmosdr sink)
        self.txpath = transmit_path(modulator, options)

        self.connect(self.txpath, self.sink)


# ======================================================================== #
#                                   Main                                   #
# ======================================================================== #

class Transmitter():

    def __init__(self, mod, options):
        # Set up the ZeroMQ interfaces
        if options.red:
            self.port_in = PORT_IN_RED
        elif options.blue:
            self.port_in = PORT_IN_BLUE
        
        self.context = zmq.Context()
        self.sock_src = self.context.socket(zmq.REQ)
        self.zmq_server = options.server
        
        #self.fake_packet = np.random.bytes(BLOCK_SIZE)

        # build the graph
        self.tb = tx_top_block(mod, options)

        r = gr.enable_realtime_scheduling()
        if r != gr.RT_OK:
            print "Warning: failed to enable realtime scheduling"
            

    def send_packet(self, payload='', eof=False):
        return self.tb.txpath.send_pkt(payload, eof)


    def run(self):
        self.sock_src.connect('tcp://%s:%d' % (self.zmq_server, self.port_in))
        
        self.tb.start()                       # start flow graph
            
        #poller = zmq.Poller()
        #poller.register(sock_srv, zmq.POLLIN)

        n = 0
        pktno = 0
        clear_to_send = True
        got_packet = False
        
        while True:        
            #if options.from_file is None:
            #MESSAGE = struct.pack('!l',pkt_size-2)
            #s.send(MESSAGE)
            #data=s.recv(pkt_size-2)
            
            if clear_to_send:
                self.sock_src.send('yo')
                clear_to_send = False
                
            try:
                if got_packet:
                    payload = self.sock_src.recv()
                else:
                    payload = self.sock_src.recv(zmq.NOBLOCK)
                    print "Got first packet from server."
                got_packet = True
                clear_to_send = True
            except zmq.ZMQError as e:
                if e.errno != zmq.EAGAIN:
                    raise
                payload = np.random.bytes(BLOCK_SIZE)

            #if options.verbose:
            #    # First 4 bytes are checksum followed by the 4 byte sequence number
            #    crc,sn = struct.unpack('!LL',data[:8])
            #    print "Seq #:", sn, " with CRC [", hex(crc), "]"
                    
            #else:
            #    data = source_file.read(pkt_size - 2)
            #    if data == '':
            #        break

            #payload = struct.pack('!H', pktno & 0xffff) + data
            self.send_packet(payload)
            n += len(payload)
            #sys.stdout.write('.')
            
            #if options.discontinuous and pktno % 5 == 4:
            #    time.sleep(1)
                
            pktno += 1
            
        #if options.from_file is None:
        #    s.close()
            
        time.sleep(5)
        send_pkt(eof=True)

        self.tb.wait()                       # wait for it to finish


    def print_info(self):
        print
        print "=== Transmit parameters ==="
        print "Sample rate:         %s"    % (eng_notation.num_to_str(self.tb.sink.get_sample_rate()))
        print "Bitrate:             %sb/s" % (eng_notation.num_to_str(self.tb.txpath.bitrate()))
        print "Modulation:          %s"    % (self.tb.txpath.modulation())
        print "Differential:        %s"    % (self.tb.txpath.differential())
        print "Samples per symbol:  %.4f"  % (self.tb.txpath.samples_per_symbol())
        print "Bandwidth LPF:       %s"    % (eng_notation.num_to_str(self.tb.sink.get_bandwidth()))
        print "Amplitude            %s"    % (self.tb.txpath.tx_amplitude())
        print "Gain:                %i"    % (self.tb.sink.get_gain())


# Read the options and instantiate the transmitter
def main():
    mods = digital.modulation_utils.type_1_mods()

    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")

    parser.add_option("-m", "--modulation", type="choice", choices=mods.keys(),
                      default='psk',
                      help="Select modulation from: %s [default=%%default]"
                            % (', '.join(mods.keys()),))
    #parser.add_option("","--discontinuous", action="store_true", default=False,
    #                  help="enable discontinous transmission (bursts of 5 packets)")
    parser.add_option("-s", "--server", default=None,
                      help="competition server IP address")
    parser.add_option("", "--red", action="store_true", default=False,
                      help="red team")
    parser.add_option("", "--blue", action="store_true", default=False,
                      help="blue team")
    #parser.add_option("","--from-file", default=None,
    #                  help="use input file for packet contents")
    #parser.add_option("","--to-file", default=None,
    #                  help="Output file for modulated samples")

    transmit_path.add_options(parser, expert_grp)
    osmo_transmitter.add_options(parser)

    for mod in mods.values():
        mod.add_options(expert_grp)

    (options, args) = parser.parse_args()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)
           
    # Can specify one and only one team
    if bool(options.red) == bool(options.blue):
        sys.stderr.write("Which team are you on? Use --red or --blue\n")
        sys.exit(1)

    # Must specify an input file or radio frequency
    #if options.from_file is not None:
    #    source_file = open(options.from_file, 'r')

    # Strip out the differential option if dbpsk or dqpsk are selected explicitly
    if (options.modulation == 'dqpsk' or options.modulation == 'dbpsk'):
        del options.differential
        
    transmitter = Transmitter(mods[options.modulation], options)
    transmitter.print_info()
    transmitter.run()


# Run main if this script is called directly
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
