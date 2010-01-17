'''
Created on Aug 15, 2010

@author: maxjohnson
'''

import re
import itms
import db
from tracktrie import TrackTrie

def fix(track, callback):
    """Looks up the track and fixes it if possible, calling the callback with status updates"""
    callback("Fixing %(artist)s - $(name)s (%(duration)d):" % track)
    candidates = TrackTrie()
    for permutation in _PermutationGenerator(track.lookupInfo):
        for candidate in itms.search(permutation):
            if abs(candidate["duration"] - track["duration"]) <= db.config('max_song_delta'):
                callback("found candidate: %(artist)s - $(name)s (%(duration)d)" % track)
                candidates.add(candidate)
            else:
                callback("found candidate: %(artist)s - $(name)s (%(duration)d), rejected due to time mismatch" % track)
                pass
        if len(candidates) != 0: break
    if len(candidates) == 0: 
        callback("No suitable candidates found")
        return
    best = candidates.pick(track)
    callback("Picked best: %(artist)s - $(name)s (%(duration)d)" % best)
    db.store(track)
    track.replace(best)
    track.save()

def undo(track, callback):
    """Replaces the track with the stored version in the database"""
    callback("Looking up in database")
    try:
        orig = db.fetch(track)
    except KeyError:
        callback("Not Found") 
        return
    callback("Found, saving")
    track.replace(orig)
    track.save()

def _PermutationGenerator(searchInfo):
    """
    takes a searchInfo (3-tuple of track, artist, duration) and generates permutations
    should be iterated over, i.e. for permutation in _PermutationGenerator(searchInfo):
    """
    #first, yield the parameter. With any luck, it will be found and we don't have to do any more generation
    generated = [(searchInfo[0].strip(), searchInfo[1].strip())]
    yield generated[0]
    
    #try spell checking things
    """permutation = Google.spellCheck(searchInfo)
    if permutation != None:
        yield return permutation
        generated.append(permutation)"""
    
    #split by hyphens in name
    #the counting is to ensure we only permutate the trackinfos generated earlier
    counter = 0
    maxCount = len(generated)
    for info in generated:
        if counter == maxCount: break
        splitted = info[0].split('-')
        for name in splitted:
            for artist in splitted:
                if name == artist: continue;
                permutation = (name.strip(), artist.strip())
                if permutation[0] != "" and permutation[1] != "":
                    yield permutation
                    generated.append(permutation)
        counter += 1
    
    #remove "featuring" and variants first from name, throw them into artists
    reg = re.compile("\\s*[\\(\\[]?(feat|ft|featuring)(\\.|:|\\s)", re.I);
    counter = 0
    maxCount = len(generated)
    for info in generated:
        if counter == maxCount: break
        m = reg.search(info[0])
        if m != None:
            permutation = (info[0][:m.start()], (info[1]+info[0][m.start():]).strip())
            if permutation[0] != "" and permutation[1] != "":
                yield permutation
                generated.append(permutation)
        counter += 1
    
    #check for multiple artists
    reg = re.compile("(?:\\s*[\\]\\(]?(?:and|w[\\\\/]|with|feat|ft|featuring)(?:\\.|:|\\s))|[&,]", re.I)
    counter = 0
    maxCount = len(generated)
    for info in generated:
        if counter == maxCount: break
        splits = reg.split(info[1])
        if len(splits) < 2: continue;
        for artist in splits:
            permutation = (info[0], artist.strip())
            if permutation[0] != "" and permutation[1] != "":
                yield permutation
                generated.append(permutation)
        counter += 1
    
    #check for () or [] in name, remove. for now just cuts after '(', it seems to work fine
    counter = 0
    maxCount = len(generated)
    for info in generated:
        if counter == maxCount: break
        try:
            permutation = (info[0][:info[0].index('(')].strip(), info[1])
            if permutation[0] != "" and permutation[1] != "":
                yield permutation
                generated.append(permutation)
        except ValueError: pass
        try:
            permutation = (info[0][:info[0].index('[')].strip(), info[1])
            if permutation[0] != "" and permutation[1] != "":
                yield permutation
                generated.append(permutation)
        except ValueError: pass
        counter += 1
