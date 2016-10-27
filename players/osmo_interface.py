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
import osmosdr

import sys


def add_freq_option(parser):
    """
    Hackery that has the -f / --freq option set both tx_freq and rx_freq
    """
    def freq_callback(option, opt_str, value, parser):
        parser.values.rx_freq = value
        parser.values.tx_freq = value

    if not parser.has_option('--freq'):
        parser.add_option('-f', '--freq', type="eng_float",
                          action="callback", callback=freq_callback,
                          help="set Tx and/or Rx frequency to FREQ [default=%default]",
                          metavar="FREQ")


# ======================================================================== #
#                            Osmosdr Interface                             #
# ======================================================================== #

class osmo_interface:
    def __init__(self, istx, args, sym_rate, sps, freq=None,
                 gain=None, antenna=None, bandwidth=None):
        
        if(istx):
            self.o = osmosdr.sink(args=args)
        else:
            self.o = osmosdr.source(args=args)

        # Set the antenna
        if (antenna is not None):
            self.o.set_antenna(antenna)
            
        if (bandwidth is not None):
            print bandwidth
            self.o.set_bandwidth(bandwidth)
        
        self._args = args
        self._ant  = antenna
        self._gain = self.set_gain(gain)
        self._freq = self.set_freq(freq)

        self._rate, self._sps = self.set_sample_rate(sym_rate, sps)

    def set_sample_rate(self, sym_rate, req_sps):
        start_sps = req_sps
        while(True):
            asked_samp_rate = sym_rate * req_sps
            actual_samp_rate = self.o.set_sample_rate(asked_samp_rate)

            sps = actual_samp_rate/sym_rate
            if(sps < 2):
                req_sps +=1
            else:
                actual_sps = sps
                break
        
        if (sps != req_sps):
            print "\nSymbol Rate:         %f" % (sym_rate)
            print "Requested sps:       %f" % (start_sps)
            print "Given sample rate:   %f" % (actual_samp_rate)
            print "Actual sps for rate: %f" % (actual_sps)

        if (actual_samp_rate != asked_samp_rate):
            print "\nRequested sample rate: %f" % (asked_samp_rate)
            print "Actual sample rate: %f" % (actual_samp_rate)

        return (actual_samp_rate, actual_sps)

    def set_gain(self, gain=None):
        if gain is None:
            # if no gain was specified, use the mid-point in dB
            g = self.o.get_gain_range()
            gain = float(g[0].start() + g[0].stop())/2
            print "\nNo gain specified."
            print "Setting gain to %f (from [%f, %f])" % \
                (gain, g.start(), g.stop())
        
        self.o.set_gain_mode(True)
        self.o.set_gain_mode(False)
        return self.o.set_gain(gain)

    def set_freq(self, freq):
        r = self.o.set_center_freq(freq, 0)
        if r:
            return freq
        else:
            frange = self.o.get_freq_range()
            sys.stderr.write(("\nRequested frequency (%f) out or range [%f, %f]\n") % \
                                 (freq, frange[0].start(), frange[0].stop()))
            sys.exit(1)

    def get_sps(self):
        return self._sps

    def get_sample_rate(self):
        return self.o.get_sample_rate()
    
    def get_bandwidth(self):
        return self.o.get_bandwidth()

    def get_bandwidth_options(self):
        bw_vals = self.o.get_bandwidth_range()
        bw_opts = []
        for i in xrange(0, len(bw_vals)):
            bw_opts.append(bw_vals[i].start())
            
        return bw_opts

    def get_gain(self):
        return self.o.get_gain()
    

# ======================================================================== #
#                               Transmitter                                #
# ======================================================================== #

class osmo_transmitter(osmo_interface, gr.hier_block2):
    def __init__(self, args, sym_rate, sps, freq=None, gain=None,
                 antenna=None, bandwidth=None, verbose=False):
        gr.hier_block2.__init__(self, "osmo_transmitter",
                                gr.io_signature(1,1,gr.sizeof_gr_complex),
                                gr.io_signature(0,0,0))

        # Set up the UHD interface as a transmitter
        osmo_interface.__init__(self, True, args, sym_rate, sps,
                                freq, gain, antenna, bandwidth)

        self.connect(self, self.o)

        if(verbose):
            self._print_verbage()
            
    def add_options(parser):
        add_freq_option(parser)
        parser.add_option("-a", "--args", type="string", default="",
                          help="Osmocom device args [default='']")
        parser.add_option("-A", "--antenna", type="string", default=None,
                          help="select Rx Antenna where appropriate")
        parser.add_option("-g", "--tx-gain", type="eng_float", default=30,
                          help="set transmit gain in dB (default is midpoint)")
        parser.add_option("-b", "--bandwidth", type="eng_float", default=None,
                          help="set outgoing LPF bandwidth in Mhz [default=automatic]")
        parser.add_option("-v", "--verbose", action="store_true", default=False)

    # Make a static method to call before instantiation
    add_options = staticmethod(add_options)

    def _print_verbage(self):
        """
        Prints information about the Osmocom transmitter
        """
        print "\nUHD Transmitter:"
        print "Args:     %s"    % (self._args)
        print "Freq:        %sHz"  % (eng_notation.num_to_str(self._freq))
        print "Gain:        %f dB" % (self._gain)
        print "Sample Rate: %ssps" % (eng_notation.num_to_str(self._rate))
        print "Antenna:     %s"    % (self._ant)


# ======================================================================== #
#                                 Receiver                                 #
# ======================================================================== #

class osmo_receiver(osmo_interface, gr.hier_block2):
    def __init__(self, args, sym_rate, sps, freq=None, gain=None,
                 antenna=None, bandwidth=None, verbose=False):
        gr.hier_block2.__init__(self, "osmo_receiver",
                                gr.io_signature(0,0,0),
                                gr.io_signature(1,1,gr.sizeof_gr_complex))
      
        # Set up the Osmocom interface as a receiver
        osmo_interface.__init__(self, False, args, sym_rate, sps,
                                freq, gain, antenna, bandwidth)

        self.connect(self.o, self)

        if(verbose):
            self._print_verbage()

    def add_options(parser):
        add_freq_option(parser)
        parser.add_option("-a", "--args", type="string", default="",
                          help="Osmocom device address args [default='']")
        parser.add_option("-A", "--antenna", type="string", default=None,
                          help="select Rx Antenna where appropriate")
        parser.add_option("-g", "--rx-gain", type="eng_float", default=30,
                          help="set receive gain in dB (default is midpoint)")
        parser.add_option("-b", "--bandwidth", type="eng_float", default=None,
                          help="set incoming LPF bandwidth in Mhz [default=automatic]")

        if not parser.has_option("--verbose"):
            parser.add_option("-v", "--verbose", action="store_true", default=False)

    # Make a static method to call before instantiation
    add_options = staticmethod(add_options)

    def _print_verbage(self):
        """
        Prints information about the Osmocom transmitter
        """
        print "\nOsmocom Receiver:"
        print "Osmo Args    %s"    % (self._args)
        print "Freq:        %sHz"  % (eng_notation.num_to_str(self._freq))
        print "Gain:        %f dB" % (self._gain)
        print "Sample Rate: %ssps" % (eng_notation.num_to_str(self._rate))
        print "Antenna:     %s"    % (self._ant)

