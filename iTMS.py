#!/usr/bin/env python
# encoding: utf-8
"""
iTMS.py

Created by Max Johnson on 2009-12-21.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import socket
from random import randrange
from base64 import b64decode
import re
from hashlib import md5
import urllib
import iTunesMac as Library
import plistlib

def search(info):
	host = "ax.search.itunes.apple.com"
	#ERROR this breaks when the thing gets weird unicode letters
	path = "/WebObjects/MZSearch.woa/wa/advancedSearch?media=all&searchButton=submit&allArtistNames=" + urllib.quote(info[1].encode("utf-8")) + "&allTitle=" + urllib.quote(info[0].encode("utf-8")) + "&flavor=0&mediaType=1&ringtone=0"
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
		
		try:
			header, body = result.split("\r\n\r\n", 2)
			string = body[body.rindex("<plist"):body.rindex("</plist>")+8]
		except ValueError:
			continue
		
		if header.startswith("HTTP/1.1 200 OK"):
			break
	
	tracklist = plistlib.readPlistFromString(string)
	for item in filter(lambda i: i["kind"] == "song", tracklist["items"]):
		track = Library.Track()
		if "artistName" in item: 
			track["artist"] = item["artistName"]
		if "composerName" in item: 
			track["composer"] = item["composerName"]
		if "duration" in item: 
			track["duration"] = float(item["duration"])/1000
		if "genre" in item: 
			track["genre"] = item["genre"]
		if "itemName" in item: 
			track["name"] = item["itemName"]
		if "playlistName" in item: 
			track["album"] = item["playlistName"].replace(" - Single", "").replace(" (Original Motion Picture Soundtrack)", "")
		if "trackCount" in item: 
			track["trackCount"] = item["trackCount"]
		if "trackNumber" in item: 
			track["trackNum"] = item["trackNumber"]
		if "year" in item: 
			track["year"] = item["year"]
		yield track

def validation(url, ua):
	"""generates x-apple-validation"""
	random = "%04X%04X" % (randrange(0x10000), randrange(0x10000))
	static = b64decode("ROkjAaKid4EUF5kGtTNn3Q==")
	url_end = re.match(".*/.*/.*(/.+)$", url).group(1)
	digest = md5(url_end + ua + static + random).digest()
	return random + '-' + digest.upper()
