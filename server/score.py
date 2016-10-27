import wx


FIELDS = (('# Packets Pulled:', 'packets_pulled'),
          ('# Packets Verified:', 'packets_verified'),
          ('% Complete:', 'percent_complete'),
          ('Time of Last Packet:', 'time_last_packet'))
         
class ScorePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.SetBackgroundColour(wx.WHITE)
        font = self.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.NORMAL)
        self.SetFont(font)
        sizer = wx.FlexGridSizer(4, 2, 0, 5)
        for text, attr in FIELDS:
            label = wx.StaticText(self, -1, text)
            font = label.GetFont()
            font.SetWeight(wx.BOLD)
            label.SetFont(font)
            
            value = wx.StaticText(self, -1, '', size=(100, -1))
            setattr(self, attr, value)
            
            sizer.Add(label, 0, flag=wx.ALIGN_RIGHT)
            sizer.Add(value, 0)
        
        self.SetSizer(sizer)
        
    def update(self, pulled, verified, complete, time_last):
        self.packets_pulled.SetLabel(str(pulled))
        self.packets_verified.SetLabel(str(verified))
        self.percent_complete.SetLabel('%0.1f' % (complete*100))
        self.time_last_packet.SetLabel('%02d:%02d' % (divmod(time_last, 60)))


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, "Test")
    panel = ScorePanel(frame)
    frame.Show(True)
    app.MainLoop()