'''
Created on Jan 15, 2010

@author: maxjohnson

Provides consistent interface to platform-specific tasks, like getting the selected files from iTunes
'''

import sys

if sys.platform == 'darwin':
    from itunesmac import getselected
    from Foundation import NSAutoreleasePool
    
    def ThreadRun(run):
        """Decorator for the run() method in threading.Thread that wraps it in an NSAutorelaeasePool."""
        
        def new_run(self):
            pool = NSAutoreleasePool.alloc().init()
            try:
                run(self)
            finally:
                pool.release()
        return new_run

elif sys.platform == 'win32':
    from ituneswin import get_selected
    
    def ThreadRun(run):
        """Does nothing. Threads on windows doesn't require any special treatment"""
        return run
