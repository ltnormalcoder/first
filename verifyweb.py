#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys#sys.argv
import subprocess
import re
import iptable

def verifyweb():
	iplist = iptable.iplist()
	webs = iptable.somelist("res/web.txt")
	webok=[]
	for web in webs:
		l=re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',getIP(web))
		if l:
			if l[0] in iplist:
				webok.append(web)
				print 'join  '+web
	with open('res/web.txt','w') as f:
         f.write('\n'.join(webok))

def getIP(domain):
	run_watch=subprocess.Popen('ping -c 1 -w 1 %s'%domain,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output,err_msg=run_watch.communicate()
	run_watch.returncode
	return output
def delweb(web):
	iplist = iptable.iplist()
	webs = open("res/web.txt","r").read().replace(web, "")
	with open('res/web.txt','w') as f:
         f.write(webs)

def verifyhostweb():
	webs = iptable.hostweblist()
	webok=[]
	for web in webs:
		l=re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',getIP(web))
		if l:
			webok.append(web)
			print 'join  '+web
	with open('res/static/hostweb.txt','w') as f:
         f.write('\n'.join(webok))