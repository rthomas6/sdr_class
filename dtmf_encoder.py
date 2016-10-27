#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dtmf Encoder
# Generated: Mon Oct 24 16:12:24 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys


class dtmf_encoder(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Dtmf Encoder")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Dtmf Encoder")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "dtmf_encoder")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
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
        _bstar_push_button = Qt.QPushButton('*')
        self._bstar_choices = {'Pressed': 1, 'Released': 0}
        _bstar_push_button.pressed.connect(lambda: self.set_bstar(self._bstar_choices['Pressed']))
        _bstar_push_button.released.connect(lambda: self.set_bstar(self._bstar_choices['Released']))
        self.top_grid_layout.addWidget(_bstar_push_button, 3,0,1,1)
        _bhash_push_button = Qt.QPushButton('#')
        self._bhash_choices = {'Pressed': 1, 'Released': 0}
        _bhash_push_button.pressed.connect(lambda: self.set_bhash(self._bhash_choices['Pressed']))
        _bhash_push_button.released.connect(lambda: self.set_bhash(self._bhash_choices['Released']))
        self.top_grid_layout.addWidget(_bhash_push_button, 3,2,1,1)
        _b9_push_button = Qt.QPushButton('9')
        self._b9_choices = {'Pressed': 1, 'Released': 0}
        _b9_push_button.pressed.connect(lambda: self.set_b9(self._b9_choices['Pressed']))
        _b9_push_button.released.connect(lambda: self.set_b9(self._b9_choices['Released']))
        self.top_grid_layout.addWidget(_b9_push_button, 2,2,1,1)
        _b8_push_button = Qt.QPushButton('8')
        self._b8_choices = {'Pressed': 1, 'Released': 0}
        _b8_push_button.pressed.connect(lambda: self.set_b8(self._b8_choices['Pressed']))
        _b8_push_button.released.connect(lambda: self.set_b8(self._b8_choices['Released']))
        self.top_grid_layout.addWidget(_b8_push_button, 2,1,1,1)
        _b7_push_button = Qt.QPushButton('7')
        self._b7_choices = {'Pressed': 1, 'Released': 0}
        _b7_push_button.pressed.connect(lambda: self.set_b7(self._b7_choices['Pressed']))
        _b7_push_button.released.connect(lambda: self.set_b7(self._b7_choices['Released']))
        self.top_grid_layout.addWidget(_b7_push_button, 2,0,1,1)
        _b6_push_button = Qt.QPushButton('6')
        self._b6_choices = {'Pressed': 1, 'Released': 0}
        _b6_push_button.pressed.connect(lambda: self.set_b6(self._b6_choices['Pressed']))
        _b6_push_button.released.connect(lambda: self.set_b6(self._b6_choices['Released']))
        self.top_grid_layout.addWidget(_b6_push_button, 1,2,1,1)
        _b5_push_button = Qt.QPushButton('5')
        self._b5_choices = {'Pressed': 1, 'Released': 0}
        _b5_push_button.pressed.connect(lambda: self.set_b5(self._b5_choices['Pressed']))
        _b5_push_button.released.connect(lambda: self.set_b5(self._b5_choices['Released']))
        self.top_grid_layout.addWidget(_b5_push_button, 1,1,1,1)
        _b4_push_button = Qt.QPushButton('4')
        self._b4_choices = {'Pressed': 1, 'Released': 0}
        _b4_push_button.pressed.connect(lambda: self.set_b4(self._b4_choices['Pressed']))
        _b4_push_button.released.connect(lambda: self.set_b4(self._b4_choices['Released']))
        self.top_grid_layout.addWidget(_b4_push_button, 1,0,1,1)
        _b3_push_button = Qt.QPushButton('3')
        self._b3_choices = {'Pressed': 1, 'Released': 0}
        _b3_push_button.pressed.connect(lambda: self.set_b3(self._b3_choices['Pressed']))
        _b3_push_button.released.connect(lambda: self.set_b3(self._b3_choices['Released']))
        self.top_grid_layout.addWidget(_b3_push_button, 0,2,1,1)
        _b2_push_button = Qt.QPushButton('2')
        self._b2_choices = {'Pressed': 1, 'Released': 0}
        _b2_push_button.pressed.connect(lambda: self.set_b2(self._b2_choices['Pressed']))
        _b2_push_button.released.connect(lambda: self.set_b2(self._b2_choices['Released']))
        self.top_grid_layout.addWidget(_b2_push_button, 0,1,1,1)
        _b1_push_button = Qt.QPushButton('1')
        self._b1_choices = {'Pressed': 1, 'Released': 0}
        _b1_push_button.pressed.connect(lambda: self.set_b1(self._b1_choices['Pressed']))
        _b1_push_button.released.connect(lambda: self.set_b1(self._b1_choices['Released']))
        self.top_grid_layout.addWidget(_b1_push_button, 0,0,1,1)
        _b0_push_button = Qt.QPushButton('0')
        self._b0_choices = {'Pressed': 1, 'Released': 0}
        _b0_push_button.pressed.connect(lambda: self.set_b0(self._b0_choices['Pressed']))
        _b0_push_button.released.connect(lambda: self.set_b0(self._b0_choices['Released']))
        self.top_grid_layout.addWidget(_b0_push_button, 3,1,1,1)
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0_0_0 = blocks.multiply_const_vff((bhash, ))
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0_0 = blocks.multiply_const_vff((b9, ))
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0 = blocks.multiply_const_vff((b6, ))
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0 = blocks.multiply_const_vff((b3, ))
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0 = blocks.multiply_const_vff((b0, ))
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0 = blocks.multiply_const_vff((b8, ))
        self.blocks_multiply_const_vxx_0_0_0_0_0_0 = blocks.multiply_const_vff((b5, ))
        self.blocks_multiply_const_vxx_0_0_0_0_0 = blocks.multiply_const_vff((b2, ))
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_vff((bstar, ))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vff((b7, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((b4, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((b1, ))
        self.blocks_add_xx_2 = blocks.add_vff(1)
        self.blocks_add_xx_1 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_sig_source_x_0_2_0_4 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 697, 0.5, 0)
        self.analog_sig_source_x_0_2_0_3 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1209, 0.5, 0)
        self.analog_sig_source_x_0_2_0_2 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1336, 0.5, 0)
        self.analog_sig_source_x_0_2_0_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1477, 0.5, 0)
        self.analog_sig_source_x_0_2_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 770, 0.5, 0)
        self.analog_sig_source_x_0_2_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 852, 0.5, 0)
        self.analog_sig_source_x_0_2 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 941, 0.5, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2_0, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2_0, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2_0, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2_0_0, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2_0_0, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2_0_0, 0), (self.blocks_add_xx_2, 1))    
        self.connect((self.analog_sig_source_x_0_2_0_1, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_1, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_1, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_1, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_2, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_2, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_2, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_2, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_3, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_3, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_3, 0), (self.blocks_add_xx_1, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_3, 0), (self.blocks_add_xx_2, 0))    
        self.connect((self.analog_sig_source_x_0_2_0_4, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2_0_4, 0), (self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_2_0_4, 0), (self.blocks_add_xx_1, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_0_0_1_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0_0_0, 0))    
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_add_xx_2, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 3))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0, 6))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.blocks_add_xx_0, 9))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 4))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 7))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 10))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 2))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 5))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 8))    
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 11))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "dtmf_encoder")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_2_0_4.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2_0_3.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2_0_2.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2.set_sampling_freq(self.samp_rate)

    def get_bstar(self):
        return self.bstar

    def set_bstar(self, bstar):
        self.bstar = bstar
        self.blocks_multiply_const_vxx_0_0_0_0.set_k((self.bstar, ))

    def get_bhash(self):
        return self.bhash

    def set_bhash(self, bhash):
        self.bhash = bhash
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0_0_0.set_k((self.bhash, ))

    def get_b9(self):
        return self.b9

    def set_b9(self, b9):
        self.b9 = b9
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0_0.set_k((self.b9, ))

    def get_b8(self):
        return self.b8

    def set_b8(self, b8):
        self.b8 = b8
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0.set_k((self.b8, ))

    def get_b7(self):
        return self.b7

    def set_b7(self, b7):
        self.b7 = b7
        self.blocks_multiply_const_vxx_0_0_0.set_k((self.b7, ))

    def get_b6(self):
        return self.b6

    def set_b6(self, b6):
        self.b6 = b6
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0_0.set_k((self.b6, ))

    def get_b5(self):
        return self.b5

    def set_b5(self, b5):
        self.b5 = b5
        self.blocks_multiply_const_vxx_0_0_0_0_0_0.set_k((self.b5, ))

    def get_b4(self):
        return self.b4

    def set_b4(self, b4):
        self.b4 = b4
        self.blocks_multiply_const_vxx_0_0.set_k((self.b4, ))

    def get_b3(self):
        return self.b3

    def set_b3(self, b3):
        self.b3 = b3
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0_0.set_k((self.b3, ))

    def get_b2(self):
        return self.b2

    def set_b2(self, b2):
        self.b2 = b2
        self.blocks_multiply_const_vxx_0_0_0_0_0.set_k((self.b2, ))

    def get_b1(self):
        return self.b1

    def set_b1(self, b1):
        self.b1 = b1
        self.blocks_multiply_const_vxx_0.set_k((self.b1, ))

    def get_b0(self):
        return self.b0

    def set_b0(self, b0):
        self.b0 = b0
        self.blocks_multiply_const_vxx_0_0_0_0_0_0_0_0.set_k((self.b0, ))


def main(top_block_cls=dtmf_encoder, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
