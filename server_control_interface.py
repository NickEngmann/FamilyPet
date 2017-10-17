#! /usr/bin/python3

import visa
import time
import re
from time import gmtime, strftime, localtime
import requests
import socket


# Get the IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ipAddress = s.getsockname()[0] #get the Ip address of your server (localhost)
print(ipAddress)
s.close()

while(1):
	#sends the request to the server to be time sync'd and compared
	current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	r = requests.post('http://'+ipAddress+':3000/pi', data= {'timestamp':})
	print (r.status_code, r.reason)
	time.sleep(1.0)
