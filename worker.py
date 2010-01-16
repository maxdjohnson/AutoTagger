'''
Created on Jan 16, 2010

@author: maxjohnson
'''
import wx
import threading
from platform import ThreadRun

class ThreadEvent(wx.PyCommandEvent):
    """Simple event to notify the controller thread of changes"""
    
    ID = wx.NewId()
    COMPLETE, UPDATE_TRACK, UPDATE_STATUS = range(3)
    
    def __init__(self, thread, type, message = None):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(ThreadEvent.ID)
        self.thread = thread
        self.type = type
        self.message = message

class Worker(threading.Thread):
    """Specialized thread that performs actions on a list of tracks until it's empty"""
    
    def __init__(self, number, controller, command):
        threading.Thread.__init__(self)
        self.number = number
        self.controller = controller
        self.command = command
        self.__alive = True
    
    @ThreadRun
    def run(self):
        while self.__alive and self.controller.tracklist:
            track = self.controller.tracklist.pop()
            wx.PostEvent(self.controller, ThreadEvent(self, ThreadEvent.UPDATE_TRACK, "%(artist)s - %(name)s" % track))
            self.command(track, self._callback)
        wx.PostEvent(self.controller, ThreadEvent(self, ThreadEvent.COMPLETE))
    
    def _callback(self, message):
        wx.PostEvent(self.controller, ThreadEvent(self, ThreadEvent.UPDATE_STATUS, message))
    
    def die(self):
        """Tell thread to stop"""
        self.__alive = False
