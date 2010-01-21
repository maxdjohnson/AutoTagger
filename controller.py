'''
Created on Jan 14, 2010

@author: maxjohnson
'''

import wx, db, view, model
from platform import getselected
from worker import ThreadEvent, Worker

class Controller(wx.App):
    """The Controller for the application. Runs in main thread and handles all messages"""
    
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        
        # This catches events when the app is asked to activate by some other process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

    def OnInit(self):
        """Called when the application is initialized, sets up the main view and shows it"""
        self.view_main = view.Main()
        self.view_running = None
        self.threads = []
        self.Connect(-1, -1, ThreadEvent.ID, self.OnThread)
        
        self.view_main.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.view_main.Bind(wx.EVT_MENU, self.OnQuit, self.view_main.menu_exit)
        #self.view_main.Bind(wx.EVT_MENU, self.OnPrefs, self.view_main.menu_prefs)
        self.view_main.Bind(wx.EVT_MENU, self.OnHelp, self.view_main.menu_help)
        self.view_main.Bind(wx.EVT_MENU, self.OnAbout, self.view_main.menu_about)
        self.view_main.button_fix.Bind(wx.EVT_BUTTON, self.OnFix)
        self.view_main.button_undo.Bind(wx.EVT_BUTTON, self.OnUndo)
        self.view_main.Show()
        return True
    
    def OnQuit(self,Event):
        """Called when the main view is closed, cancels anything running and destroys the main frame"""
        if self.view_running:
            self.OnCancel(None)
        self.view_main.Destroy()
    
    def OnCancel(self, Event):
        """Called when the Running view is closed, or the cancel button is pressed. Kills all running threads"""
        self.view_running.Show(False)
        for t in self.threads:
            t.die()
    
    def OnCancelled(self):
        """Called after all threads have finished exiting. Destroys the Running view, and enables the main view if it exists"""
        self.view_running.Destroy()
        if self.view_main:
            self.view_main.Enable(True)
    
    def OnFix(self, Event):
        """Called when user clicks run button"""
        self.Run(model.fix)
    
    def OnUndo(self, Event):
        """Called when user clicks undo button"""
        self.Run(model.undo)
    
    def Run(self, cmd):
        """Sets up the Running view and starts threads"""
        self.view_running = view.Running()
        self.view_running.Bind(wx.EVT_CLOSE, self.OnCancel)
        self.view_running.Bind(wx.EVT_MENU, self.OnCancel, self.view_main.menu_exit)
        self.view_running.button_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.view_main.Enable(False)
        self.view_running.Show()
        
        self.tracklist = getselected()
        
        for i in range(db.config('max_threads')):
            thread = Worker(i, self, cmd)
            self.threads.append(thread)
            thread.start()
    
    def OnThread(self, Event):
        """Called when threads send messages to the controller. 
        Responsible for destroying threads and calling OnCancelled(), and for updating the Running view
        """
        if Event.type == ThreadEvent.COMPLETE:
            self.threads.remove(Event.thread)
            if not self.threads:
                self.OnCancelled()
        if Event.type == ThreadEvent.UPDATE_TRACK:
            self.view_running.update_track(Event.thread.number, Event.message)
        if Event.type == ThreadEvent.UPDATE_STATUS:
            self.view_running.update_status(Event.thread.number, Event.message)
        
    def OnAbout(self, event):
        """Called when the user selects About from the menu bar"""
        dlg = wx.MessageDialog(self.view_main, "AutoTagger, an open-source music tag fixer for iTunes\n"
                                     "Author Max Johnson (maxdjohnson@gmail.com)\n",
                                "About AutoTagger", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnHelp(self, event):
        """Called when the user selects Help from the menu bar"""
        dlg = wx.MessageDialog(self.view_main, "AutoTagger is a fairly simple tool. You select the tracks that are mis-tagged in iTunes, and then click the \"Fix\" button in AutoTagger. \n"
                               "If it messes up and mis-tags a song, you can always revert it by selecting the song(s) and pressing undo.",
                               "AutoTagger Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def BringWindowToFront(self):
        """Brings window to the front"""
        try: # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass
        
    def OnActivate(self, event):
        """Called when the app is told to activate by another process. Brings window to front"""
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()
        
    def MacReopenApp(self):
        """Called when the doc icon is clicked"""
        self.BringWindowToFront()
