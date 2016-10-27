if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import eng_notation
try:
    from gnuradio import fosphor
except ImportError:
    pass
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx
import constants


class SpectrumDisplay(gr.top_block):
    def __init__(self, parent):
        gr.top_block.__init__(self)
        self.parent = parent

        ##################################################
        # Variables
        ##################################################
        self.samp_rate   = samp_rate   = constants.DEFAULT_SAMP_RATE
        self.center_freq = center_freq = constants.DEFAULT_CF

        ##################################################
        # Blocks
        ##################################################
        try:
            self.waterfallsink = fosphor.wx_sink_c(self.GetWin())
        except NameError:
            self.waterfallsink = waterfallsink2.waterfall_sink_c(
                self.GetWin(),
                baseband_freq=center_freq,
                dynamic_range=100,
                ref_level=0,
                ref_scale=2.0,
                sample_rate=samp_rate,
                fft_size=512,
                fft_rate=15,
                average=False,
                avg_alpha=None,
                title="Waterfall Plot",
            )
            self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        else:
            self.waterfallsink.set_fft_window(window.WIN_BLACKMAN_hARRIS)
            self.waterfallsink.set_frequency_range(center_freq, samp_rate)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(10, 0)
        self.osmosdr_source_0.set_bb_gain(10, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(samp_rate, 0)
          

        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.waterfallsink, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        
        try:
            self.waterfallsink.set_frequency_range(self.center_freq, self.samp_rate)
        except AttributeError:
            self.waterfallsink.set_sample_rate(self.samp_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        try:
            self.waterfallsink.set_frequency_range(self.center_freq, self.samp_rate)
        except AttributeError:
            self.waterfallsink.set_baseband_freq(self.center_freq)

    def Add(self, window):
        pass
    
    def GetWin(self):
        return self.parent


