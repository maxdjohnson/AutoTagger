'''
Created on Jan 6, 2010

@author: maxjohnson

Handles all persistent storage needs
Tracks are saved and retrieved with store(track) and fetch(track)
Configuration options are stored and retrieved with setconfig(k, v) and config(k)
'''

import sys, shelve, threading

_defaults = {'max_threads': 4,
             'max_song_delta': 3}

#set up and initialize database
_db = shelve.open("AutoTag.dat")
_dblock = threading.Condition(threading.Lock())
for k, v in _defaults.items():
    if not k in _db:
        _db[k] = v

def store(track):
    _dblock.acquire()
    try:
        _db[str(track.track.databaseID())] = track.copy()
    finally:
        _dblock.release()

def fetch(track):
    _dblock.acquire()
    try:
        return _db[str(track.uid)]
    finally:
        _dblock.release()

def config(k):
    _dblock.acquire()
    try:
        return _db[k]
    finally:
        _dblock.release()

def setConfig(k, v):
    _dblock.acquire()
    try:
        _db[k] = v
    finally:
        _dblock.release()
