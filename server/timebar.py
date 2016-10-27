import wx
import time
from wx.lib.pubsub import pub


class TimeBarPanel(wx.Panel):
    def __init__(self, parent, max_time=180.0):
        wx.Panel.__init__(self, parent, -1, style=wx.FULL_REPAINT_ON_RESIZE)
        self.SetDoubleBuffered(True)
        self.SetBackgroundColour(wx.WHITE)
        font = self.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.BOLD)
        self.SetFont(font)
        
        self.ribbon = TimeRibbon(self, max_time)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, -1, 'Match Time', style=wx.ALIGN_CENTER), 0, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        sizer.Add(self.ribbon, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        
        #~ self.Bind(wx.EVT_TIMER, self.OnTimer)
        
        self.start_time = time.time()-120
        self.timer = wx.Timer(self)
        #~ pub.subscribe(self.onStart, 'Start')
        #~ pub.subscribe(self.onStop, 'Stop')
        pub.subscribe(self.onSetTime, 'SetTime')

    def onSetTime(self, time_val):
        self.ribbon.SetTime(time_val)
        
    def onStart(self, msg):
        self.start_time = time.time()
        self.timer.Start(200)
        
    def onStop(self, msg):
        self.timer.Stop()
        
    def OnTimer(self, event):
        elapsed = time.time() - self.start_time
        self.ribbon.SetTime(elapsed)
        
        
NORMAL = (64, 255, 64)
DONE   = (64, 192, 64)
class TimeRibbon(wx.Panel):
    def __init__(self, parent, max_time):
        wx.Panel.__init__(self, parent, -1)
        ##self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetBackgroundColour(wx.WHITE)
        font = self.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.NORMAL)
        self.SetFont(font)
        self.max_time = max_time
        self.time = 0.0
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def SetTime(self, time_value):
        self.time = min(self.max_time, time_value)
        self.Refresh()
        
    def OnSize(self, event):
        self.Refresh()
        
    def OnPaint(self, event):
        w, h = self.GetClientSizeTuple()
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        dc = wx.GCDC(dc)
        tw, th = dc.GetTextExtent(str(self.max_time))
        tw += 4
        box_w = w - tw*2  # center the ribbon, and allow room for labels
        box_h = h - th
        margin_x = 4
        margin_y = th // 2
        
        dc.SetPen(wx.Pen((128, 128, 128)))
        dc.SetBrush(wx.Brush((240, 240, 240)))
        dc.DrawRectangle(tw, margin_y, box_w+1, box_h+1)
        if self.time == self.max_time:
            dc.SetBrush(wx.Brush(DONE))
        else:
            dc.SetBrush(wx.Brush(NORMAL))
        h1 = box_h * (self.time/self.max_time)
        dc.DrawRectangle(margin_x+tw, box_h-h1+margin_y, box_w-margin_x*2, h1+1)
        
        # draw y axis labels
        x = box_w + tw
        dy = box_h / self.max_time
        spacing = 5
        if dy < 0.0:
            return
        while dy * spacing < th:
            spacing += 5
        t = 0
        y = base_y = box_h + margin_y
        while t <= self.max_time:
            dc.DrawLine(x, y, x+margin_x, y)
            dc.DrawText(str(t), x+margin_x+5, y-th/2)
            t += spacing
            y = base_y - (t * dy)
            


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, "Test", size=(30, 600))
    panel = TimeBarPanel(frame)
    panel.ribbon.SetTime(0)
    frame.Show(True)
    app.MainLoop()