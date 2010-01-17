'''
Created on Jan 16, 2010

@author: maxjohnson
'''
class Track(dict):
    """Platform-neutral track representation. Should be subclassed to implement saving to the library"""
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
        """Merge with another track. Ignores it for now"""
        #don't really know what we should do here...
        pass
    
    def replace(self, track):
        """Replace all self's values with track's values"""
        for k in track:
            self[k] = track[k]
    
    def copy(self):
        """Makes a copy of itself"""
        r = Track()
        r.replace(self)
        return r
    
    def save(self):
        """Should be defined in subclasses to implement saving to the library"""
        raise NotImplementedError("save() not implemented")
    
    @property
    def lookupInfo(self):
        """Returns a tuple of name and artist for the purpose of looking the track up"""
        return (self["name"], self["artist"])

    @property
    def uid(self):
        """Should be defined in subclasses to return a unique, persistent identifier"""
        raise NotImplementedError("Track does not have a unique identifier")
