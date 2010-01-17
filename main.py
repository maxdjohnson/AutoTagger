'''
Created on Aug 21, 2010

@author: maxjohnson
'''

from controller import Controller

def main():
	app = Controller(False)
	app.MainLoop()

if __name__ == '__main__':
	main()