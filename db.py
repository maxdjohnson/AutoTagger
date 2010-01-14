'''
Created on Jan 6, 2010

@author: maxjohnson
'''

import sys, shelve, threading
if sys.platform == 'darwin':
    import iTunesMac as Library
elif sys.platform == 'win32':
    #import iTunesWin as Library
    raise NotImplementedError('AutoTagger is not yet supported on windows')
else:
    raise NotImplementedError('AutoTagger is not supported on this OS')

_defaults = {'max_threads': 4,
             'max_song_delta': 3}

#set up and initialize database
#_db = shelve.open("AutoTag.dat")
_dblock = threading.Condition(threading.Lock())
#for k, v in _defaults.items():
#    if not k in _db:
#        _db[k] = v

def store(track):
    return
    s = Library.Track()
    s.replace(track)
    _dblock.acquire()
    _db[str(track.track.databaseID())] = s
    _dblock.release()

def fetch(track):
    return None
    _dblock.acquire()
    ret = _db[str(track.track.databaseID())]
    _dblock.release()
    return ret

def config(k):
    return _defaults[k]
    _dblock.acquire()
    ret = _db[k]
    _dblock.release()
    return ret

def setConfig(k, v):
    return
    _dblock.acquire()
    _db[k] = v
    _dblock.release()

def restoreConfig(key=None):
    return
    if key == None:
        for k, v in _defaults:
            _dblock.acquire()
            _db[k] = v
            _dblock.release()
    else:
        _dblock.acquire()
        _db[key] = _defaults[key]
        _dblock.release()
