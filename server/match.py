#!/usr/bin/env python

# third-party modules
import time
import wx
from wx.lib.pubsub import pub

# custom modules
from team import TeamPanel
from timebar import TimeBarPanel
from spectrum_display import SpectrumDisplay
# URL: https://www.youtube.com/watch?v=JzBHFQKwI3o
FULL = 100

class Wrapper(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.wrapped = None
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def SetWrapped(self, wrapped):
        self.wrapped = wrapped
                                                      
    def OnSize(self, event):
        if self.wrapped is not None:
            self.wrapped.SetSize(event.GetSize())


class MatchPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.SetBackgroundColour(wx.WHITE)
        
        self.teams = [TeamPanel(self, 'Red'), TeamPanel(self, 'Blue')]
        self.timebar = TimeBarPanel(self)
        self.w_panel = Wrapper(self)
        self.gr_block = SpectrumDisplay(self.w_panel)
        self.waterfall = self.gr_block.waterfallsink.win
        self.w_panel.SetWrapped(self.waterfall)
        
        inner3 = wx.BoxSizer(wx.VERTICAL)
        inner3.Add(self.w_panel, 1, flag=wx.EXPAND)
        
        inner2 = wx.BoxSizer(wx.HORIZONTAL)
        inner2.Add(self.timebar, 0, flag=wx.EXPAND)
        inner2.Add(inner3, 1, flag=wx.EXPAND)
        
        inner = wx.BoxSizer(wx.HORIZONTAL)
        inner.Add(self.teams[0], 1, flag=wx.ALL|wx.EXPAND, border=2)
        inner.Add(self.teams[1], 1, flag=wx.ALL|wx.EXPAND, border=2)
        
        outer = wx.BoxSizer(wx.VERTICAL)
        outer.Add(inner2, 2, flag=wx.ALL|wx.EXPAND, border=5)
        outer.Add(inner, 1, flag=wx.EXPAND)
        
        self.SetSizer(outer)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        pub.subscribe(self.onSetFrequency, 'SetFrequency')
        pub.subscribe(self.onStartWaterfall, 'StartWaterfall')
        
    def onStartWaterfall(self, msg=None):
        self.gr_block.start()
        
    def OnClose(self, event):
        self.gr_block.stop()
        self.gr_block.wait()
        event.Skip()
        
    def onSetFrequency(self, freq):
        self.gr_block.set_center_freq(freq)
        

        
if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
            
    app = wx.App()
    frame = wx.Frame(None, -1, "Test", size=(1200, 700))
    panel = MatchPanel(frame)
    frame.Show(True)
    panel.onStartWaterfall()

    app.MainLoop()
