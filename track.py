'''
Created on Jan 16, 2010

@author: maxjohnson
'''
class Track(dict):
    def __init__(self, track = None):
        if (track == None):
            self.track = None
            self["name"] = ""
            self["artist"] = ""
            self["album"] = ""
            self["composer"] = ""
            self["genre"] = ""
            self["discCount"] = 0
            self["discNum"] = 0
            self["trackNum"] = 0
            self["trackCount"] = 0
            self["year"] = 0
            self["duration"] = 0
    
    def merge(self, track):
        #don't really know what we should do here...
        pass
    
    def replace(self, track):
        for k in track:
            self[k] = track[k]
    
    def copy(self):
        r = Track()
        r.replace(self)
        return r
    
    @property
    def lookupInfo(self):
        return (self["name"], self["artist"])

    @property
    def uid(self):
        raise NotImplementedError("Track does not have a unique identifier")
