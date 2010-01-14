#!/usr/bin/env python
# encoding: utf-8
"""
Main.py

Created by Max Johnson on 2009-08-21.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from wxMain import MyApp


#needs to be replaced by some UI
def main():
	app = MyApp(False)
	app.MainLoop()




if __name__ == '__main__':
	main()