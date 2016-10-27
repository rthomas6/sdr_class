import wx
from wx.lib.pubsub import pub

from progress import ProgressPanel
from score    import ScorePanel


# URL: https://www.youtube.com/watch?v=JzBHFQKwI3o
FULL = 100

COLOR = {'Red': wx.Colour(255, 0, 0), 'Blue': wx.Colour(0, 0, 255)}


class Header(wx.Panel):
    def __init__(self, parent, team, label):
        wx.Panel.__init__(self, parent, -1, style=wx.FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundColour(COLOR[team])
        self.label = wx.StaticText(self, -1, label)
        self.label.SetForegroundColour(wx.WHITE)
        font = self.label.GetFont()
        font.SetPointSize(14)
        self.label.SetFont(font)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, 1, border=4, flag=wx.ALL|wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        
    
class TeamPanel(wx.Panel):
    def __init__(self, parent, color='Red'):
        wx.Panel.__init__(self, parent, -1, style=wx.FULL_REPAINT_ON_RESIZE)
        self.color = color
        self.team_name = '%s Team' % color
        
        self.SetDoubleBuffered(True)
        self.SetBackgroundColour(wx.WHITE)
        font = self.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.BOLD)

        #font.MakeBold()
        self.SetFont(font)
        
        self.name = Header(self, color, self.team_name)
        
        self.pulled    = ProgressPanel(self, FULL, 'Source Pull Packet Map', COLOR[color])
        self.delivered = ProgressPanel(self, FULL, 'Delivered Packet Map', COLOR[color])
        self.score     = ScorePanel(self)
        
        outer = wx.BoxSizer(wx.VERTICAL)
        inner = wx.BoxSizer(wx.HORIZONTAL)
        left  = wx.BoxSizer(wx.VERTICAL)
        
        left.Add(self.pulled,    1, flag=wx.EXPAND)
        left.Add(self.delivered, 1, flag=wx.EXPAND)
        
        inner.Add(left, 1, flag=wx.EXPAND)
        inner.Add(self.score, 0, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        
        outer.Add(self.name, 0, flag=wx.EXPAND)
        outer.Add(inner, 1, flag=wx.EXPAND)
        self.SetSizer(outer)
        pub.subscribe(self.onTeamStatus, 'TeamStatus')
        pub.subscribe(self.onSetTeamName, 'SetTeamName')

    def onTeamStatus(self, team, pulled, verified, complete, time_last):
        if self.color == team:
            self.score.update(pulled, verified, complete, time_last)
            self.pulled.setCount(pulled)
            self.delivered.setCount(verified)
            
    def onSetTeamName(self, team, name):
        if not name:
            name = '%s Team' % team
        if self.color == team:
            self.name.label.SetLabel(name)

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, "Test", size=(800, 400))
    panel = TeamPanel(frame, 'Red')
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(panel, 1, flag=wx.EXPAND)
    frame.SetSizer(sizer)
    frame.Show(True)
    app.MainLoop()
