import re
import mechanize
import urllib2
import httplib
import HTMLParser
import socket
import re
from bs4 import BeautifulSoup
from sys import argv

start = argv

#compiles ips
def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []
   
   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))    
      
   return ip_range

#adds IPs together
def addIp(addresses, x, y):
	ip_range = ipRange(x,y)
	for ip in ip_range:
		addresses.append(ip)
	return addresses



#makes IP list
def compileIp(collection):
	collection = addIp(collection,"79.125.0.0", "79.125.127.255")
	collection = addIp(collection,"46.51.128.0", "46.51.191.255")
	collection = addIp(collection,"46.51.192.0", "46.51.207.255")
	collection = addIp(collection,"46.137.0.0", "46.137.127.255")
	collection = addIp(collection,"46.137.128.0", "46.137.191.255")
	collection = addIp(collection,"176.34.128.0", "176.34.255.255")
	collection = addIp(collection,"176.34.64.0", "176.34.127.255")	
	return collection

ireland = compileIp([])


# goes through each website and grabs title, IP address, & a mailto tag
#this is used in conjunction with itself - I usually run about 100 of these scripts with a nohup command to 
#be most effiecient. The 1515 is just how many IPs this script is running. You pass in where you want to start at the beginning
def ipFiller(start, ogIp):
	ips = []
	i = int(start[1])
	while (i < int(start[1]) + 1515):
		ips.append(ogIp[i])
		i += 1
	for ip in ips:
		br = mechanize.Browser()
		try:
			br.open("http://" + ip, timeout = 2) 
			soup = BeautifulSoup(br.open("http://" + ip).read())
			mailto = soup.find_all(href=re.compile("mailto"))
			print br.title() + "," + ip + "," + str(mailto)
		except mechanize._mechanize.BrowserStateError:
			br.close()
			pass
		except urllib2.URLError:
			br.close()
			pass
		except httplib.BadStatusLine:
			br.close()
			pass
		except httplib.IncompleteRead:
			br.close()
			pass
		except RuntimeError:
			br.close()
			pass
		except TypeError:
			br.close()
			pass
		except UnicodeEncodeError:
			br.close()
			pass
		except HTMLParser.HTMLParseError:
			br.close()
			pass
		except socket.timeout:
			br.close()
			pass
		br.close()


#run me, baby
ipFiller(start, ireland)



