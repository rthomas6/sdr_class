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

from gnuradio import gr
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import time

# From gr-digital
from gnuradio import digital

# from current dir
from receive_path import receive_path
from osmo_interface import osmo_receiver
from constants import *

import struct, sys, zmq


# ======================================================================== #
#                            Receiver Top Block                            #
# ======================================================================== #

class rx_top_block(gr.top_block):
    def __init__(self, demodulator, rx_callback, options):
        gr.top_block.__init__(self)

        if (options.rx_freq is not None):
            # Work-around to get the modulation's bits_per_symbol
            args = demodulator.extract_kwargs_from_options(options)
            symbol_rate = options.bitrate / demodulator(**args).bits_per_symbol()

            self.source = osmo_receiver(options.args, symbol_rate,
                                        options.samples_per_symbol,
                                        options.rx_freq, options.rx_gain,
                                        options.antenna, options.bandwidth)
            options.samples_per_symbol = self.source._sps

        #elif (options.from_file is not None):
        #    sys.stderr.write(("Reading samples from '%s'.\n\n" % (options.from_file)))
        #    self.source = gr.file_source(gr.sizeof_gr_complex, options.from_file)
        else:
            sys.stderr.write("No source defined, pulling samples from null source.\n\n")
            self.source = gr.null_source(gr.sizeof_gr_complex)

        # Set up receive path
        # do this after for any adjustments to the options that may
        # occur in the sinks (specifically the Osmocom sink)
        self.rxpath = receive_path(demodulator, rx_callback, options) 

        self.connect(self.source, self.rxpath)


# ======================================================================== #
#                                   Main                                   #
# ======================================================================== #

class Receiver():

    def __init__(self, mod, options):
        self.n_rcvd = 0
        self.n_right = 0
        self.start_time = 0
        self.mstr_cnt = 0
        self.stop_rcv = 0
        self.verbose = options.verbose
        
        # Set up the ZeroMQ interfaces
        if options.red:
            self.port_out = PORT_OUT_RED
        elif options.blue:
            self.port_out = PORT_OUT_BLUE
        
        self.context = zmq.Context()
        self.sock_dest = self.context.socket(zmq.PUSH)
        self.zmq_server = options.server

        # Build the graph
        self.tb = rx_top_block(mod, self.rx_callback, options)

        r = gr.enable_realtime_scheduling()
        if r != gr.RT_OK:
            print "Warning: Failed to enable realtime scheduling."

    
    # Callback any time a packet is received from the demodulator
    def rx_callback(self, ok, payload):
        #(pktno, crc, sn) = struct.unpack('!HLL', payload[0:10])
        self.n_rcvd += 1
        if ok:
            if not self.n_right:
                self.start_time = time.time()

            self.n_right += 1

            self.sock_dest.send(payload)
            
        if self.verbose:
            print "ok = %5s  n_rcvd = %4d  n_right = %4d" %(ok, self.n_rcvd, self.n_right)


    def run(self):
        self.sock_dest.connect('tcp://%s:%d' % (self.zmq_server, self.port_out))
        
        self.tb.run()    # start GR graph
        
        
    def print_info(self):
        print
        print "=== Receive parameters ==="
        print "Sample rate:         %s"    % (eng_notation.num_to_str(self.tb.source.get_sample_rate()))
        print "Bitrate:             %sb/s" % (eng_notation.num_to_str(self.tb.rxpath.bitrate()))
        print "Modulation:          %s"    % (self.tb.rxpath.modulation())
        print "Differential:        %s"    % (self.tb.rxpath.differential())
        print "Samples per symbol:  %.4f"  % (self.tb.rxpath.samples_per_symbol())
        print "Bandwidth LPF:       %s"    % (eng_notation.num_to_str(self.tb.source.get_bandwidth()))
        print "Gain:                %i"    % (self.tb.source.get_gain())


# Read the options and instantiate the receiver
def main():
    demods = digital.modulation_utils.type_1_demods()

    # Create Options Parser:
    parser = OptionParser (option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")

    parser.add_option("-m", "--modulation", type="choice", choices=demods.keys(), 
                      default='psk',
                      help="Select modulation from: %s [default=%%default]"
                            % (', '.join(demods.keys()),))
    parser.add_option("-s", "--server", default=None,
                      help="competition server IP address")
    parser.add_option("", "--red",  action="store_true", default=False,
                      help="red team")
    parser.add_option("", "--blue",  action="store_true", default=False,
                      help="blue team")
    #parser.add_option("","--from-file", default=None,
    #                  help="input file of samples to demod")

    receive_path.add_options(parser, expert_grp)
    osmo_receiver.add_options(parser)

    for mod in demods.values():
        mod.add_options(expert_grp)

    (options, args) = parser.parse_args()

    if len(args) != 0:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    # Can specify one and only one team
    if bool(options.red) == bool(options.blue):
        sys.stderr.write("Which team are you on? Use --red or --blue\n")
        sys.exit(1)

    # Must specify an input file or radio frequency
    #if options.from_file is None:
    if options.rx_freq is None:
        sys.stderr.write("You must specify -f FREQ or --freq FREQ\n")
        sys.stderr.write("Use --help to see all options\n")
        sys.exit(1)
        
    # Must specify a server
    if options.server is None:
        sys.stderr.write("You must specify -s ADDRESS or --server ADDRESS\n")
        sys.exit(1)

    # Strip out the differential option if dbpsk or dqpsk are selected explicitly
    if (options.modulation == 'dqpsk' or options.modulation == 'dbpsk'):
        del options.differential
        
    # Fire it up
    receiver = Receiver(demods[options.modulation], options)
    receiver.print_info()
    receiver.run()


# Run main if this script is called directly
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
