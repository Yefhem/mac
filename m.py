#!/usr/bin/env python3

import subprocess, optparse, re, time

def input():
	usage = "usage: %prog [options] -i <interface> -m <mac_address>"
	parseObject = optparse.OptionParser(usage)
	parseObject.add_option("-i","--interface",dest="interface",help="Please enter the interface you want to change!")
	parseObject.add_option("-m","--mac",dest="macAdd",help="Please enter a MAC address!")

	return parseObject.parse_args()  # Bir tuple döndürüyor

def change(userInterface,userMacAdd):
	subprocess.call(["ifconfig",userInterface,"down"])
	subprocess.call(["ifconfig",userInterface,"hw","ether",userMacAdd])
	subprocess.call(["ifconfig",userInterface,"up"])

def oldMac(interface):
	ifconfig = subprocess.check_output(["ifconfig",interface])
	oldMac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
	
	return oldMac.group(0)

def newMac(interface):
	ifconfig = subprocess.check_output(["ifconfig",interface])
	newMac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
	
	if newMac: 
		return newMac.group(0)
	else:
		return None

(userInput, arguments)= input()
oldmac = oldMac(userInput.interface)
change(userInput.interface, userInput.macAdd)
newmac = newMac(userInput.interface)


if newmac == userInput.macAdd:
	time.sleep(2)
	print("[+] Change successful! \n\n[+]Old Mac: {} \n[+]New Mac: {}".format(oldmac,newmac))
else:
	print("[-] MAC not chnaged!")
	
