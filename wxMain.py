import sys, wx, db, AutoTag
from ThreadRiver import ThreadRiver
if sys.platform == 'darwin':
    import iTunesMac as Library
elif sys.platform == 'win32':
    #import iTunesWin as Library
    raise NotImplementedError('AutoTagger is not yet supported on windows')
else:
    raise NotImplementedError('AutoTagger is not supported on this OS')

class MainFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, menubar, title = "AutoTagger"):
        wx.Frame.__init__(self, None , -1, title, size=(390, 90))

        self.SetMenuBar(menubar)

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
        btn1 = wx.Button(panel, -1, 'Run', size=(70, 30))
        hbox5.Add(btn1, 0)
        btn2 = wx.Button(panel, -1, 'Undo', size=(70, 30))
        hbox5.Add(btn2, 0, wx.LEFT | wx.BOTTOM , 5)
        vbox.Add(hbox5, 0, wx.ALIGN_CENTER | wx.RIGHT, 10)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show(True)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        
class RunFrame(wx.Frame):
    def __init__(self, menubar, cmd, title = "Running..."):
        wx.Frame.__init__(self, None , -1, title, size=(390, 300))

        self.SetMenuBar(menubar)
        
        panel = wx.Panel(self, -1)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add((-1, 10))
        
        #hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        #tc2 = wx.ListBox(panel, -1)
        #hbox3.Add(tc2, 1, wx.EXPAND)
        #vbox.Add(hbox3, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        
        self.threadlabels = []
        for i in range(db.config('max_threads')):
            label = wx.StaticText(panel, -1, 'Starting Thread...')
            self.threadlabels.append(label)
            vbox.Add(label, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn2 = wx.Button(panel, -1, 'Cancel', size=(70, 30))
        hbox5.Add(btn2, 0, wx.LEFT | wx.BOTTOM , 5)
        vbox.Add(hbox5, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

        panel.SetSizer(vbox)
        
        river = ThreadRiver(db.config('max_threads'), self.ThunkGen(cmd, Library.getSelected()))
        river.joinAll()
        
    def Run(self, index, cmd, track):
        self.threadlabels[index].SetLabel("%(artist)s - %(name)s" % track)
        cmd(track)
    
    def ThunkGen(self, cmd, tracks):
        """Generates thunks that apply cmd to each track in tracks"""
    
        for track in tracks:
            yield (lambda n, t: self.Run(n, cmd, t), track, None)
    
class MyApp(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        
        # This catches events when the app is asked to activate by some other
        # process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

    def OnInit(self):
        self.__menubar = self.__MakeMenuBar()
        
        frame = RunFrame(self.__menubar, lambda x: x)
        frame.Show()

        import sys
        for f in  sys.argv[1:]:
            self.OpenFileMessage(f)

        return True
    
    def OnQuit(self,Event):
        self.Destroy()
        
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to test\n"
                                     "the use of menus on Mac, etc.\n",
                                "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnHelp(self, event):
        dlg = wx.MessageDialog(self, "This would be help\n"
                                     "If there was any\n",
                                "Test Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def BringWindowToFront(self):
        try: # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass
        
    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()

    def MacOpenFile(self, filename):
        """Called for files droped on dock icon, or opened via finders context menu"""
        pass
        
    def MacReopenApp(self):
        """Called when the doc icon is clicked, and ???"""
        self.BringWindowToFront()

    def MacNewFile(self):
        pass
    
    def MacPrintFile(self, file_path):
        pass
    
    def __MakeMenuBar(self):
        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        
        item = FileMenu.Append(wx.ID_EXIT, text = "&Exit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

#        item = FileMenu.Append(wx.ID_PREFERENCES, text = "&Preferences")
#        self.Bind(wx.EVT_MENU, self.OnPrefs, item)

        MenuBar.Append(FileMenu, "&File")
        
        HelpMenu = wx.Menu()

        item = HelpMenu.Append(wx.ID_HELP, "AutoTagger &Help",
                                "Help for AutoTagger")
        self.Bind(wx.EVT_MENU, self.OnHelp, item)

        ## this gets put in the App menu on OS-X
        item = HelpMenu.Append(wx.ID_ABOUT, "&About",
                                "More information about AutoTagger")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        MenuBar.Append(HelpMenu, "&Help")
        return MenuBar
 