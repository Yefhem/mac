#!/usr/bin/env python

import subprocess, optparse, re, sys, os, time

class MacChanger():
	def __init__(self):
		os.system('clear')
		print("  ** MacChanger **  \nsss")
		
	def input(self):
		usage = "usage: %prog [options] -i eth0 -m 00:EE:SS:28:10:98"
		parseObject = optparse.OptionParser(usage)
		parseObject.add_option("-i","--interface",dest="interface",help="Please enter the interface you want to change!")
		parseObject.add_option("-m","--mac",dest="macAdd",help="Please enter a MAC address!")
		(userInput, arguments) = parseObject.parse_args()  
			
		if not userInput.interface or not userInput.macAdd:
			sys.stderr.write("> Error! Missing parameter!!\n")
			sys.exit()
		return userInput
			
	def change(self,interface,macAdd):
		subprocess.call(["ifconfig",interface,"down"])
		subprocess.call(["ifconfig",interface,"hw","ether",macAdd])
		subprocess.call(["ifconfig",interface,"up"])
		
	def get(self,interface):
		ifconfig = subprocess.check_output(["ifconfig",interface])
		mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
	
		return mac.group(0)
		
macChanger = MacChanger()
options = macChanger.input()
oldMac = macChanger.get(options.interface)
macChanger.change(options.interface, options.macAdd)
newMac = macChanger.get(options.interface)

if newMac == options.macAdd:
	time.sleep(0.5)
	print("> Change successful! \n\n> Old Mac: {} \n> New Mac: {}".format(oldMac,newMac))
else:
	print("> MAC not changed!")