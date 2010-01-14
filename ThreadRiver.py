'''
Created on Jan 6, 2010

@author: maxjohnson
'''

import sys
from threading import Condition, Lock
from time import sleep

if sys.platform != 'darwin':
    from threading import Thread
    
else:
    #If we're using OSX, threads need to be wrapped in an autoreleasepool
    import threading
    from Foundation import NSAutoreleasePool
    
    class Thread(threading.Thread):
        def start(self):
            autoreleasepool = NSAutoreleasePool.alloc().init()
            try:
                threading.Thread.start(self)
            finally:
                autoreleasepool.release()

class ThreadRiver:

    """Works like a thread pool, but instead of popping tasks off of a list 
    of tasks, it gets them from a generator. This way the tasks can be 
    generated on demand.
    Based on the thread pool at http://code.activestate.com/recipes/203871/"""
    
    def __init__(self, numThreads, generator):

        """Initialize the thread pool with numThreads workers."""
        
        self.__threads = []
        self.__resizeLock = Condition(Lock())
        self.__generatorLock = Condition(Lock())
        self.__generator = generator
        self.__isDone = False
        self.__isJoining = False
        self.setThreadCount(numThreads)

    def setThreadCount(self, newNumThreads):

        """ External method to set the current pool size.  Acquires
        the resizing lock, then calls the internal version to do real
        work."""
        
        # Can't change the thread count if we're shutting down the pool!
        if self.__isJoining:
            return False
        
        self.__resizeLock.acquire()
        try:
            self.__setThreadCountNolock(newNumThreads)
        finally:
            self.__resizeLock.release()
        return True

    def __setThreadCountNolock(self, newNumThreads):
        
        """Set the current pool size, spawning or terminating threads
        if necessary.  Internal use only; assumes the resizing lock is
        held."""
        
        # If we need to grow the pool, do so
        while newNumThreads > len(self.__threads):
            newThread = ThreadRiverThread(len(self.__threads), self)
            self.__threads.append(newThread)
            newThread.start()
        # If we need to shrink the pool, do so
        while newNumThreads < len(self.__threads):
            self.__threads[0].goAway()
            del self.__threads[0]

    def getThreadCount(self):

        """Return the number of threads in the pool."""
        
        self.__resizeLock.acquire()
        try:
            return len(self.__threads)
        finally:
            self.__resizeLock.release()

    def getNextTask(self):

        """ Retrieve the next task from the generator.  For use
        only by ThreadRiverThread objects contained in the pool."""
        
        self.__generatorLock.acquire()
        try:
            return self.__generator.next()
        except StopIteration:
            self.__isDone = True
            return (None, None, None)
        finally:
            self.__generatorLock.release()
    
    def joinAll(self, waitForTasks = True, waitForThreads = True):

        """ Clear the task queue and terminate all pooled threads,
        optionally allowing the tasks and threads to finish."""
        
        # Mark the pool as joining to prevent any more task queueing
        self.__isJoining = True

        # Wait for tasks to finish
        if waitForTasks:
            while not self.__isDone:
                sleep(.1)

        # Tell all the threads to quit
        self.__resizeLock.acquire()
        try:
            self.__setThreadCountNolock(0)
            self.__isJoining = True

            # Wait until all threads have exited
            if waitForThreads:
                for t in self.__threads:
                    t.join()
                    del t

            # Reset the pool for potential reuse
            self.__isJoining = False
        finally:
            self.__resizeLock.release()


        
class ThreadRiverThread(Thread):

    """ Pooled thread class. """
    
    threadSleepTime = 0.1

    def __init__(self, number, river):

        """ Initialize the thread and remember the river. """
        
        Thread.__init__(self)
        self.__number = number
        self.__river = river
        self.__isDying = False
        
    def run(self):

        """ Until told to quit, retrieve the next task and execute
        it, calling the callback if any.  """
        
        while self.__isDying == False:
            cmd, args, callback = self.__river.getNextTask()
            # If there's nothing to do, just sleep a bit
            if cmd is None:
                sleep(ThreadRiverThread.threadSleepTime)
            elif callback is None:
                cmd(self.__number, args)
            else:
                callback(cmd(self.__number, args))
    
    def goAway(self):

        """ Exit the run loop next time through."""
        
        self.__isDying = True


