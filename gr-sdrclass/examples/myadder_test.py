#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Myadder Test
# Generated: Wed Oct 26 14:18:31 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class myadder_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Myadder Test")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.vec_source_1 = blocks.vector_source_f((2,2,2,2,2), False, 1, [])
        self.vec_source_0 = blocks.vector_source_f((1,2,3,4,5), False, 1, [])
        self.my_sink = blocks.vector_sink_f(1)
        self.myadd = blocks.add_vff(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.myadd, 0), (self.my_sink, 0))    
        self.connect((self.vec_source_0, 0), (self.myadd, 0))    
        self.connect((self.vec_source_1, 0), (self.myadd, 1))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=myadder_test, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()
    print "Output of myadder_test: {}".format(tb.my_sink.data())


if __name__ == '__main__':
    main()
