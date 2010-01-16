'''
Created on Jan 16, 2010

@author: maxjohnson
'''

import wx
import db

class Main(wx.Frame):
    """ The main frame for the window, displaying short instructions and buttons for fix and undo """
    def __init__(self):
        wx.Frame.__init__(self, None , -1, "AutoTagger", size=(390, 90))
        
        MenuBar = wx.MenuBar()
        
        FileMenu = wx.Menu()
        self.menu_exit = FileMenu.Append(wx.ID_EXIT, text = "&Exit")
#        self.menu_prefs = FileMenu.Append(wx.ID_PREFERENCES, text = "&Preferences")
#        self.menu_log = FileMenu.Append(-1, text = "&View Log")
        MenuBar.Append(FileMenu, "&File")
        
        HelpMenu = wx.Menu()
        self.menu_help = HelpMenu.Append(wx.ID_HELP, "AutoTagger &Help", "Help for AutoTagger")
        self.menu_about = HelpMenu.Append(wx.ID_ABOUT, "&About", "More information about AutoTagger")
        MenuBar.Append(HelpMenu, "&Help")

        self.SetMenuBar(MenuBar)
        
        panel = wx.Panel(self, -1)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, -1, 'Select songs in iTunes, then click a button')
        st1.SetFont(font)
        hbox1.Add(st1, 0, wx.RIGHT, 8)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        vbox.Add((-1, 10))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_fix = wx.Button(panel, -1, 'Run', size=(70, 30))
        hbox5.Add(self.button_fix, 0)
        self.button_undo = wx.Button(panel, -1, 'Undo', size=(70, 30))
        hbox5.Add(self.button_undo, 0, wx.LEFT | wx.BOTTOM , 5)
        vbox.Add(hbox5, 0, wx.ALIGN_CENTER | wx.RIGHT, 10)

        panel.SetSizer(vbox)

        
class Running(wx.Frame):
    """Window that displays feedback from currently running threads"""
    
    def __init__(self):
        wx.Frame.__init__(self, None , -1, "Running...", size=(390, 300))
        
        MenuBar = wx.MenuBar()
        
        FileMenu = wx.Menu()
        self.menu_cancel = FileMenu.Append(wx.ID_EXIT, text = "&Cancel")
        MenuBar.Append(FileMenu, "&File")

        self.SetMenuBar(MenuBar)
        
        panel = wx.Panel(self, -1)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add((-1, 10))
        
        self.threadlabels = []
        for i in range(db.config('max_threads')):
            label1 = wx.StaticText(panel, -1, 'Thread %d' % i)
            label2 = wx.StaticText(panel, -1, 'Starting Thread...')
            self.threadlabels.append((label1, label2))
            vbox.Add(label1, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
            vbox.Add(label2, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_cancel = wx.Button(panel, -1, 'Cancel', size=(70, 30))
        hbox5.Add(self.button_cancel, 0, wx.LEFT | wx.BOTTOM , 5)
        vbox.Add(hbox5, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

        panel.SetSizer(vbox)
    
    def update_track(self, index, message):
        """Updates the track label for the thread"""
        self.threadlabels[index][0].SetLabel(message)
        
    def update_status(self, index, message):
        """Updates the status label for the thread"""
        self.threadlabels[index][1].SetLabel(message)

        