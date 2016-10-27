
# third-party modules
import wx
import sys
from wx.lib.pubsub import pub

# custom modules
from match import MatchPanel
import server


# grab the preferred ethernet ip address
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
local_ip_address = s.getsockname()[0]


class MainFrame(wx.Frame):
    def __init__(self, **kwargs):
        wx.Frame.__init__(self, None, -1, "SDR with GNU Radio", **kwargs)
        panel = MatchPanel(self)
        
        self.setupToolBar()
        
        self.server = server.Server()
        self.server.start()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.timer = wx.Timer()
        self.timer.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(200)
        
        self.waterfall_timer = wx.Timer()
        self.waterfall_timer.Bind(wx.EVT_TIMER, self.onWaterfallTimer)
        self.waterfall_timer.Start(1, oneShot=True)
        
    def onTimer(self, event):
        MAX = float(server.NUM_BLOCKS)
        gs = server.game_state
        time_val = gs[server.TIME]
        pub.sendMessage('SetTime', time_val = time_val/10.0)
        pub.sendMessage('TeamStatus', 
                        team      = 'Red', 
                        pulled    = gs[server.RED_PULLED], 
                        verified  = int(min(gs[server.RED_VERIFIED], MAX)), 
                        complete  = min(gs[server.RED_VERIFIED], MAX) / MAX, 
                        time_last = gs[server.RED_LAST])

        pub.sendMessage('TeamStatus', 
                        team      = 'Blue', 
                        pulled    = gs[server.BLUE_PULLED], 
                        verified  = int(min(gs[server.BLUE_VERIFIED], MAX)), 
                        complete  = min(gs[server.BLUE_VERIFIED], MAX) / MAX, 
                        time_last = gs[server.BLUE_LAST])
            
    def onWaterfallTimer(self, event):
        pub.sendMessage('StartWaterfall')
        
    def onClose(self, event):
        if self.server.is_alive():
            self.server.terminate()
            self.server.join()
        sys.exit()
        
        
    def setupToolBar(self):
        tsize = (32, 32)
        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL |
                                     #~ wx.NO_BORDER     |
                                     wx.TB_FLAT      
                                     #~ wx.TB_TEXT
                                     #~ wx.TB_HORZ_LAYOUT
                                     )
                                     
        start_bmp = wx.Bitmap('art/play.png')
        self.start_btn = toolbar.AddSimpleTool(-1, start_bmp, "Start")
        self.Bind(wx.EVT_TOOL, self.OnStart, id = self.start_btn.GetId())

        stop_bmp = wx.Bitmap('art/stop.png')
        self.stop_btn = toolbar.AddSimpleTool(-1, stop_bmp, "Stop")
        self.Bind(wx.EVT_TOOL, self.OnStop, id = self.stop_btn.GetId())
        toolbar.EnableTool(self.stop_btn.GetId(), False)
        
        reset_bmp = wx.Bitmap('art/reset.png')
        self.reset_btn = toolbar.AddSimpleTool(-1, reset_bmp, "Reset")
        self.Bind(wx.EVT_TOOL, self.OnReset, id = self.reset_btn.GetId())
        toolbar.EnableTool(self.reset_btn.GetId(), False)
        
        toolbar.AddSeparator()
        self.center_freq = wx.TextCtrl(toolbar, -1)
        toolbar.AddControl(wx.StaticText(toolbar, -1, 'Center Frequency (MHz):'))
        toolbar.AddControl(self.center_freq)
        self.center_freq.Bind(wx.EVT_TEXT, self.OnFreqChange)

        toolbar.AddSeparator()
        self.red_team = wx.TextCtrl(toolbar, -1, size=(150, -1))
        toolbar.AddControl(wx.StaticText(toolbar, -1, 'Red Team:'))
        toolbar.AddControl(self.red_team)

        toolbar.AddSeparator()
        self.blue_team = wx.TextCtrl(toolbar, -1, size=(150, -1))
        toolbar.AddControl(wx.StaticText(toolbar, -1, 'Blue Team:', style=wx.ALIGN_RIGHT))
        toolbar.AddControl(self.blue_team)
        
        self.enable_blue = wx.CheckBox(toolbar, -1, '')
        self.enable_blue.SetValue(False)
        self.OnBlueEnable(None)
        toolbar.AddControl(self.enable_blue)
        self.center_freq.Bind(wx.EVT_TEXT, self.OnFreqChange)
        self.enable_blue.Bind(wx.EVT_CHECKBOX, self.OnBlueEnable)
        
        toolbar.AddSeparator()
        toolbar.AddControl(wx.StaticText(toolbar, -1, 'Server IP Address: '+local_ip_address))
        
        toolbar.Realize()
        self.blue_team.Bind(wx.EVT_TEXT, self.OnNameChange)
        self.red_team.Bind(wx.EVT_TEXT, self.OnNameChange)

    def OnBlueEnable(self, event):
        if self.enable_blue.GetValue():
            name = self.blue_team.GetValue()
            server.game_state[server.SINGLE_TEAM] = False
        else:
            name = '---'
            server.game_state[server.SINGLE_TEAM] = True

        pub.sendMessage('SetTeamName',team='Blue', name=name)
             

    def OnFreqChange(self, event):
        freq = self.center_freq.GetValue()
        try:
            freq = int(freq)
        except ValueError:
            return
        if 300 <= freq <= 3800:
            pub.sendMessage('SetFrequency', freq = freq*1e6)
        
    def OnNameChange(self, event):
        ctrl = event.GetEventObject()
        text = ctrl.GetValue()
        team = 'Red' if ctrl is self.red_team else 'Blue'
        pub.sendMessage('SetTeamName', team=team, name=text)
            
    def OnStart(self, event):
        toolbar = self.GetToolBar()
        toolbar.EnableTool(self.stop_btn.GetId(), True)
        toolbar.EnableTool(self.start_btn.GetId(), False)
        toolbar.EnableTool(self.reset_btn.GetId(), False)
        toolbar.EnableTool(self.enable_blue.GetId(), False)
        pub.sendMessage('Start')
        server.game_state[server.RUNNING] = True

    def OnStop(self, event):
        toolbar = self.GetToolBar()
        toolbar.EnableTool(self.stop_btn.GetId(), False)
        toolbar.EnableTool(self.reset_btn.GetId(), True)
        pub.sendMessage('Stop')
        server.game_state[server.RUNNING] = False
        
    def OnReset(self, event):
        toolbar = self.GetToolBar()
        toolbar.EnableTool(self.start_btn.GetId(), True)
        toolbar.EnableTool(self.reset_btn.GetId(), False)
        toolbar.EnableTool(self.enable_blue.GetId(), True)
        pub.sendMessage('Reset')
        server.reset()

        
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
    frame = MainFrame(size=(1200, 950))
    frame.Show(True)
    
    app.MainLoop()
