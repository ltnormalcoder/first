#!/usr/bin/python
# -*- coding: utf-8 -*  
#__author__ = 'Administrat  
#coding=utf-8  
import sys
import os 

def statistics():
	send_num = os.popen('grep -E -o ".{0,0}.status=sent.{0,19}" /var/log/maillog | grep -c "sen" ' ).read()
	wrong550_num = os.popen('grep -E -o ".{0,0}.said: 550.{0,19}" /var/log/maillog | grep -c "550" ' ).read()
	Blocked_num= os.popen('grep -E -o ".{0,0}.Blocked: 550.{0,19}|.{0,0}.IP: .{0,13}" /var/log/maillog | grep -c "IP" ' ).read()
	with open('res/static/progress.txt','r') as f:
		record_mail = f.readlines()[-1].split('deal')[1].split('message')[0]
	print('总投递数：'+record_mail+'\n成功投递数：'+send_num+'550错误数：'+wrong550_num+'封禁ip次数：'+Blocked_num)
