#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys#sys.argv
import json
import re
import iptable
#105749,e2d2941a2acb7c1cd6add114a11804ea'
def dnspod(typename):
	l=raw_input("\n\033[1;32;40m请输入dnspod api账号密码 格式 xxxxxx,xxxxxxxxxxx :")
	if l=='':
		print '请输入 api账号密码！'
		exit()
	ip = iptable.iplist()
	web = iptable.somelist("res/web.txt")
	ip_list=ip+ip+ip+ip
	count=0		
	for w in web :	
			www=w
			#print(w+ip_list[web.index(w)])
			if typename=='添加全部域名解析':
					count+=1
					req_data = {'login_token':l,'format':'json','domain':w}
					requrl = "https://dnsapi.cn/Domain.Create"
					try:
						r = json.loads(requests.post(requrl, data=req_data).text)
						dkim_origin=open('/etc/opendkim/keys/'+www+'/default.txt',"r").read()
						dkim=iptable.clear(re.findall(re.compile(r'[(](.*)[)]', re.S), dkim_origin)[0])
						print (www+'添加域名 ->'+r['status']['message'])
						if 'exists' not in r['status']['message']:
							req_data=	[
										{'login_token':l,'format':'json','domain':w,'sub_domain':'@','record_line':'默认','record_type':'A','value':ip_list[web.index(w)]},
										{'login_token':l,'format':'json','domain':w,'sub_domain':'mail','record_line':'默认','record_type':'A','value':ip_list[web.index(w)]},
										{'login_token':l,'format':'json','domain':w,'sub_domain':'*','record_line':'默认','record_type':'CNAME','value':'mail.'+w},
										{'login_token':l,'format':'json','domain':w,'sub_domain':'@','record_line':'默认','record_type':'MX','value':'mail.'+w},
										{'login_token':l,'format':'json','domain':w,'sub_domain':'default._domainkey','record_line':'默认','record_type':'TXT','value':dkim}
										]
							requrl = "https://dnsapi.cn/Record.Create"
							for req_data_one in req_data:
									r = json.loads(requests.post(requrl, data=req_data_one).text)
									print (www+'添加'+req_data_one['record_type']+'记录 ->'+r['status']['message'])
					except :
	  					  print r['status']['message']
			elif typename=='删除全部域名解析':
					count+=1
					req_data = {'login_token':l,'format':'json','domain':w}
					requrl = "https://dnsapi.cn/Domain.Remove"
					r = json.loads(requests.post(requrl, data=req_data).text)
					print (www+'删除'+' ->'+r['status']['message'])

