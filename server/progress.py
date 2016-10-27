import wx
import numpy as np
import random

ROWS = 6
COLS = 25

class ProgressPanel(wx.Panel):
    def __init__(self, parent, full_count, label, color):
        wx.Panel.__init__(self, parent, -1)
        self.SetBackgroundColour(wx.WHITE)
        
        self.label = wx.StaticText(self, -1, label)
        self.progress   = ProgressGrid(self, full_count, color)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
                
        sizer.Add(self.label,    0, flag=wx.ALIGN_CENTER)
        sizer.Add(self.progress, 1, 
                  flag=wx.ALIGN_CENTER_HORIZONTAL|wx.SHAPED|wx.ALL, 
                  border=2)
        self.SetSizer(sizer)
        
    def setCount(self, count):
        self.progress.setCount(count)

        #~ self.Bind(wx.EVT_SIZE,  self.OnSize)

    #~ def OnSize(self, event):
        #~ w, h = self.GetSizeTuple()
        #~ print 'outer', w, h
        #~ self.Layout()
        
class ProgressGrid(wx.Panel):
    def __init__(self, parent, full_count, color):
        wx.Panel.__init__(self, parent, -1, size=(COLS*7, ROWS*7))
        ##self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetBackgroundColour(wx.WHITE)
        
        self.color = color
        r, g, b= color.Get()
        self.full_color = wx.Colour(r*0.75, g*0.75, b*0.75)
        
        self.progress   = np.zeros((ROWS, COLS), dtype=int)
        self.full_count = float(full_count)
        self.timer      = wx.Timer(self)
        self.timer.Start(20)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE,  self.OnSize)
        #~ self.Bind(wx.EVT_TIMER, self.OnTimer)
        
    def Reset(self):
        self.progress[:,:] = 0
        self.Refresh()
        
    def Add(self, row, col, value=1):
        self.progress[row, col] = min(self.full_count, self.progress[row, col] + value)
        
    def OnTimer(self, event):
        for i in range(random.randint(0, 100)):
            r = random.randint(0, ROWS-1)
            c = random.randint(0, COLS-1)
            self.Add(r, c)
        self.Refresh()
        
    def setCount(self, count):
        index, leftover = divmod(count, self.full_count)
        self.progress[:,:] = 0
        raveled = self.progress.ravel()
        if index >= len(raveled):
            raveled[:] = self.full_count
        else:
            raveled[:index] = self.full_count
            raveled[index] = leftover
        self.Refresh()

    def OnSize(self, event):
        self.Refresh()
    
    def OnPaint(self, event):
        w, h = self.GetClientSizeTuple()
        delta = min((w-2) // COLS, (h-2) // ROWS)
        x_offset = (w - (COLS * delta)) // 2
        y_offset = (h - (ROWS * delta)) // 2
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        dc = wx.GCDC(dc)
        full = delta - 4
        progress = (np.sqrt(self.progress/self.full_count) * full).astype(int)
        for r in range(ROWS):
            y = r * delta + y_offset
            for c in range(COLS):
                x = c * delta + x_offset
                d = progress[r, c]
                if (d > 2) and ((delta - d) % 2 == 1):
                    d -= 1
                gap = (delta - d)//2 + 1
                if d == full:
                    dc.SetBrush(wx.Brush(self.full_color))
                else:
                    dc.SetBrush(wx.Brush(self.color))
                    
                dc.SetPen(wx.NullPen)
                if d:
                    dc.DrawRectangle(x+gap, y+gap, d+1, d+1)
                
                dc.SetBrush(wx.NullBrush)
                dc.SetPen(wx.Pen(wx.BLACK, 0.5))
                dc.DrawRectangle(x+2, y+2, delta-1, delta-1)
            

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, "Progress Panel Test", size=(600, 200))
    panel = ProgressPanel(frame, 100, 'Label', wx.RED)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(panel, 1, flag=wx.EXPAND)
    frame.SetSizer(sizer)
    frame.Show(True)
    app.MainLoop()
