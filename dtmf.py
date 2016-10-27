#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dtmf
# Generated: Mon Oct 24 16:14:29 2016
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class dtmf(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dtmf")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.bstar = bstar = 0
        self.bhash = bhash = 0
        self.b9 = b9 = 0
        self.b8 = b8 = 0
        self.b7 = b7 = 0
        self.b6 = b6 = 0
        self.b5 = b5 = 0
        self.b4 = b4 = 0
        self.b3 = b3 = 0
        self.b2 = b2 = 0
        self.b1 = b1 = 0
        self.b0 = b0 = 0

        ##################################################
        # Blocks
        ##################################################
        self.blocks_multiply_const_vxx_0_9 = blocks.multiply_const_vff((b9, ))
        self.blocks_multiply_const_vxx_0_8 = blocks.multiply_const_vff((b6, ))
        self.blocks_multiply_const_vxx_0_7 = blocks.multiply_const_vff((b3, ))
        self.blocks_multiply_const_vxx_0_6 = blocks.multiply_const_vff((0, ))
        self.blocks_multiply_const_vxx_0_5 = blocks.multiply_const_vff((b8, ))
        self.blocks_multiply_const_vxx_0_4 = blocks.multiply_const_vff((b5, ))
        self.blocks_multiply_const_vxx_0_3 = blocks.multiply_const_vff((b2, ))
        self.blocks_multiply_const_vxx_0_2 = blocks.multiply_const_vff((bstar, ))
        self.blocks_multiply_const_vxx_0_10 = blocks.multiply_const_vff((0, ))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vff((b7, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((b4, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((b1, ))
        self.blocks_add_xx_0_9 = blocks.add_vff(1)
        self.blocks_add_xx_0_8 = blocks.add_vff(1)
        self.blocks_add_xx_0_7 = blocks.add_vff(1)
        self.blocks_add_xx_0_6 = blocks.add_vff(1)
        self.blocks_add_xx_0_5 = blocks.add_vff(1)
        self.blocks_add_xx_0_4 = blocks.add_vff(1)
        self.blocks_add_xx_0_3 = blocks.add_vff(1)
        self.blocks_add_xx_0_2 = blocks.add_vff(1)
        self.blocks_add_xx_0_11_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_11_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_11_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_11 = blocks.add_vff(1)
        self.blocks_add_xx_0_10 = blocks.add_vff(1)
        self.blocks_add_xx_0_1 = blocks.add_vff(1)
        self.blocks_add_xx_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_sig_source_x_0_5 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 941, .5, 0)
        self.analog_sig_source_x_0_4 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 852, .5, 0)
        self.analog_sig_source_x_0_3 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 770, .5, 0)
        self.analog_sig_source_x_0_2 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1477, .5, 0)
        self.analog_sig_source_x_0_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1336, .5, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 697, 0.5, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1209, .5, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0_2, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0_5, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0_8, 0))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0_1, 1))    
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_add_xx_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_add_xx_0_3, 0))    
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_add_xx_0_6, 0))    
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_add_xx_0_9, 0))    
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0_1, 0))    
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0_10, 0))    
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0_4, 0))    
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0_7, 0))    
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_2, 1))    
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_3, 1))    
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_4, 1))    
        self.connect((self.analog_sig_source_x_0_4, 0), (self.blocks_add_xx_0_5, 1))    
        self.connect((self.analog_sig_source_x_0_4, 0), (self.blocks_add_xx_0_6, 1))    
        self.connect((self.analog_sig_source_x_0_4, 0), (self.blocks_add_xx_0_7, 1))    
        self.connect((self.analog_sig_source_x_0_5, 0), (self.blocks_add_xx_0_10, 1))    
        self.connect((self.analog_sig_source_x_0_5, 0), (self.blocks_add_xx_0_8, 1))    
        self.connect((self.analog_sig_source_x_0_5, 0), (self.blocks_add_xx_0_9, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_multiply_const_vxx_0_3, 0))    
        self.connect((self.blocks_add_xx_0_1, 0), (self.blocks_multiply_const_vxx_0_7, 0))    
        self.connect((self.blocks_add_xx_0_10, 0), (self.blocks_multiply_const_vxx_0_10, 0))    
        self.connect((self.blocks_add_xx_0_11, 0), (self.blocks_add_xx_0_11_0_0_0, 2))    
        self.connect((self.blocks_add_xx_0_11_0, 0), (self.blocks_add_xx_0_11_0_0_0, 1))    
        self.connect((self.blocks_add_xx_0_11_0_0, 0), (self.blocks_add_xx_0_11_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_11_0_0_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_add_xx_0_2, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.blocks_add_xx_0_3, 0), (self.blocks_multiply_const_vxx_0_4, 0))    
        self.connect((self.blocks_add_xx_0_4, 0), (self.blocks_multiply_const_vxx_0_8, 0))    
        self.connect((self.blocks_add_xx_0_5, 0), (self.blocks_multiply_const_vxx_0_1, 0))    
        self.connect((self.blocks_add_xx_0_6, 0), (self.blocks_multiply_const_vxx_0_5, 0))    
        self.connect((self.blocks_add_xx_0_7, 0), (self.blocks_multiply_const_vxx_0_9, 0))    
        self.connect((self.blocks_add_xx_0_8, 0), (self.blocks_multiply_const_vxx_0_2, 0))    
        self.connect((self.blocks_add_xx_0_9, 0), (self.blocks_multiply_const_vxx_0_6, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0_11, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0_11, 1))    
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_add_xx_0_11, 2))    
        self.connect((self.blocks_multiply_const_vxx_0_10, 0), (self.blocks_add_xx_0_11_0_0, 3))    
        self.connect((self.blocks_multiply_const_vxx_0_2, 0), (self.blocks_add_xx_0_11, 3))    
        self.connect((self.blocks_multiply_const_vxx_0_3, 0), (self.blocks_add_xx_0_11_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_4, 0), (self.blocks_add_xx_0_11_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_0_5, 0), (self.blocks_add_xx_0_11_0, 2))    
        self.connect((self.blocks_multiply_const_vxx_0_6, 0), (self.blocks_add_xx_0_11_0, 3))    
        self.connect((self.blocks_multiply_const_vxx_0_7, 0), (self.blocks_add_xx_0_11_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_8, 0), (self.blocks_add_xx_0_11_0_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_0_9, 0), (self.blocks_add_xx_0_11_0_0, 2))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_5.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_4.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_3.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_bstar(self):
        return self.bstar

    def set_bstar(self, bstar):
        self.bstar = bstar
        self.blocks_multiply_const_vxx_0_2.set_k((self.bstar, ))

    def get_bhash(self):
        return self.bhash

    def set_bhash(self, bhash):
        self.bhash = bhash

    def get_b9(self):
        return self.b9

    def set_b9(self, b9):
        self.b9 = b9
        self.blocks_multiply_const_vxx_0_9.set_k((self.b9, ))

    def get_b8(self):
        return self.b8

    def set_b8(self, b8):
        self.b8 = b8
        self.blocks_multiply_const_vxx_0_5.set_k((self.b8, ))

    def get_b7(self):
        return self.b7

    def set_b7(self, b7):
        self.b7 = b7
        self.blocks_multiply_const_vxx_0_1.set_k((self.b7, ))

    def get_b6(self):
        return self.b6

    def set_b6(self, b6):
        self.b6 = b6
        self.blocks_multiply_const_vxx_0_8.set_k((self.b6, ))

    def get_b5(self):
        return self.b5

    def set_b5(self, b5):
        self.b5 = b5
        self.blocks_multiply_const_vxx_0_4.set_k((self.b5, ))

    def get_b4(self):
        return self.b4

    def set_b4(self, b4):
        self.b4 = b4
        self.blocks_multiply_const_vxx_0_0.set_k((self.b4, ))

    def get_b3(self):
        return self.b3

    def set_b3(self, b3):
        self.b3 = b3
        self.blocks_multiply_const_vxx_0_7.set_k((self.b3, ))

    def get_b2(self):
        return self.b2

    def set_b2(self, b2):
        self.b2 = b2
        self.blocks_multiply_const_vxx_0_3.set_k((self.b2, ))

    def get_b1(self):
        return self.b1

    def set_b1(self, b1):
        self.b1 = b1
        self.blocks_multiply_const_vxx_0.set_k((self.b1, ))

    def get_b0(self):
        return self.b0

    def set_b0(self, b0):
        self.b0 = b0


def main(top_block_cls=dtmf, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
