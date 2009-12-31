#!/usr/bin/env python
# encoding: utf-8
"""
iTMS.py

Created by Max Johnson on 2009-08-16.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import socket
from random import randrange
from base64 import b64decode
import re
from hashlib import md5
import urllib
import zlib
from iTunesMac import *

def search(info):
	host = "ax.search.itunes.apple.com"
	#ERROR this breaks when the thing gets weird unicode letters
	path = "/WebObjects/MZSearch.woa/wa/advancedSearch?media=all&searchButton=submit&allArtistNames=" + urllib.quote(info[1]) + "&allTitle=" + urllib.quote(info[0]) + "&flavor=0&mediaType=1&ringtone=0"
	url = "http://"+host+path
	ua = "iTunes/7.0 (Macintosh; U; PPC Mac OS X 10.4.7)"
	
	while True:
		c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		c.connect((host, 80))
		fileobj = c.makefile('r', 0)
	
		msg = "GET "+path+" HTTP/1.1\r\n"
		msg += "X-Apple-Tz: -21600\r\n"
		msg += "X-Apple-Store-Front: 143441\r\n"
		msg += "User-Agent: "+ua+"\r\n"
		msg += "Accept-Language: en-us, en;q=0.50\r\n"
		msg += "X-Apple-Validation: "+validation(url, ua)
		msg += "Accept-Encoding: gzip, x-aes-cbc\r\n"
		msg += "Connection: close\r\n"
		msg += "Host: " + host + "\r\n\r\n"
		
		fileobj.write(msg)
		result = fileobj.read()
		
		index = result.rfind("<key>listType</key><string>search</string>")
		if result[:15] == "HTTP/1.1 200 OK" and index != -1 : break
	
	#TODO: unescape html entities
	#You know what, this entire thing should really just use an html parser. I dunno why i did this by hand
	result = result[index:]
	
	reg = re.compile("<key>([^<]*)<\\/key><(?:integer|string)>([^<]*)<\\/(?:integer|string)>")
	startIndex = 0
	endIndex = 0
	while True:
		try:
			startIndex = result.index("<dict>", endIndex)
			endIndex = result.index("</dict>", startIndex)
		except: break;
		
		entry = result[startIndex:endIndex]
		track = Track()
		kind = "song"
		for match in reg.finditer(entry):
			k = match.group(1)
			v = match.group(2)
			
			if k == "artistName": track["artist"] = v
			if k == "composerName": track["composer"] = v
			if k == "duration": track["duration"] = float(v)/1000
			if k == "genre": track["genre"] = v
			if k == "itemName": track["name"] = v
			if k == "kind": kind = v
			if k == "playlistName": 
				v.replace(" - Single", "")
				v.replace(" (Original Motion Picture Soundtrack)", "")
				track["album"] = v
			if k == "popularity": pass
			if k == "trackCount": track["trackCount"] = int(v)
			if k == "trackNumber": track["trackNum"] = int(v)
			if k == "year": track["year"] = int(v)
		
		if kind != "song": continue
		yield track

def validation(url, ua):
	"""generates x-apple-validation"""
	random = "%04X%04X" % (randrange(0x10000), randrange(0x10000))
	static = b64decode("ROkjAaKid4EUF5kGtTNn3Q==")
	url_end = re.match(".*/.*/.*(/.+)$", url).group(1)
	digest = md5(url_end + ua + static + random).digest()
	return random + '-' + digest.upper()

class iTMSTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	#unittest.main()
	pass