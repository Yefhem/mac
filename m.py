#!/usr/bin/env python

import subprocess, optparse, re, sys, os, time

class MacChanger():
	def __init__(self):
		os.system('clear')
		print("**Welcome**")
		
	def input(self):
		usage = "usage: %prog [options] -i eth0 -m 00:EE:SS:28:10:98"
		parseObject = optparse.OptionParser(usage)
		parseObject.add_option("-i","--interface",dest="interface",help="Please enter the interface you want to change!")
		parseObject.add_option("-m","--mac",dest="macAdd",help="Please enter a MAC address!")
		(userInput, arguments) = parseObject.parse_args()  
			
		if not userInput.interface or not userInput.macAdd:
			sys.stderr.write("[-]Error!Eksik parametre!!\n")
			sys.exit()
		else:
			return userInput
			
	def change(self,interface,macAdd):
		subprocess.call(["ifconfig",interface,"down"])
		subprocess.call(["ifconfig",interface,"hw","ether",macAdd])
		subprocess.call(["ifconfig",interface,"up"])
		
	def mac_getir(self,interface):
		ifconfig = subprocess.check_output(["ifconfig",interface])
		gelen_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
	
		return gelen_mac.group(0)
		

mac_changer = MacChanger()
options = mac_changer.input()

eski_mac_adres = mac_changer.mac_getir(options.interface)

mac_changer.change(options.interface, options.macAdd)

yeni_mac_adres = mac_changer.mac_getir(options.interface)


if yeni_mac_adres == options.macAdd:
	time.sleep(0.5)
	print("> Change successful! \n\n> Old Mac: {} \n> New Mac: {}".format(eski_mac_adres,yeni_mac_adres))
else:
	print("[-]MAC not changed!")