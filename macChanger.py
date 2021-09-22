#!/usr/bin/env python

import subprocess, argparse, re, sys, os, time
from generate_mac import generate_mac

class Mac_changer():
	def __init__(self):
		pass
		
	def clear(self):
		os.system('clear')
		print(">>>> MacChanger <<<<\n")
		
	def input(self):
		usage = "macChanger.py [options] \n[-i eth0 -m 00:EE:SS:28:10:98] \n[--interface eth0 --mac 00:EE:SS:28:10:98] \n[-i eth0 -r 15] \n[--interface eth0 --random 15]"
		parseObject = argparse.ArgumentParser(usage)
		parseObject.add_argument("-i","--interface",dest="interface",help="Please enter the interface you want to change!")
		parseObject.add_argument("-m","--mac",dest="mac_add",help="Please enter a MAC address!")
		parseObject.add_argument("-r","--random",dest="random_mac",type=int,help="Please specify the duration(second)!")
		args = parseObject.parse_args()
			
		if not len(sys.argv) == 5:
			self.error()
		return args
			
	def change(self,interface,mac_add):
		subprocess.call(["ifconfig",interface,"down"])
		subprocess.call(["ifconfig",interface,"hw","ether",mac_add])
		subprocess.call(["ifconfig",interface,"up"])
		
	def get(self,interface):
		ifconfig = subprocess.check_output(["ifconfig",interface])
		mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
	
		return mac.group(0)
	
	def show(self,old,new):
		print("> Change successful! \n\n> Old Mac: {} \n> New Mac: {}".format(old,new))
		
	def error(self):
		sys.stderr.write("> Error! Missing or incorrect parameter!!\n")
		sys.exit()
	
mac_changer = Mac_changer()
options = mac_changer.input()

if options.random_mac and options.interface:
	while True:
		mac_changer.clear()
		old_mac = mac_changer.get(options.interface)
		new_random_mac = generate_mac.total_random()
		mac_changer.change(options.interface,new_random_mac)
		mac_changer.show(old_mac,new_random_mac)
		time.sleep(options.random_mac)	
					
if options.interface and options.mac_add:
	if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", options.mac_add.lower()):
		mac_changer.clear()
		old_mac = mac_changer.get(options.interface)
		mac_changer.change(options.interface,options.mac_add)
		new_mac = mac_changer.get(options.interface)
		if options.mac_add == new_mac:
			mac_changer.show(old_mac,new_mac)
		else:
			print("> MAC not changed!")
	else:
		mac_changer.error()