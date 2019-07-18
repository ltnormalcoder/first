#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import deal_email_data
import os
import sys#sys.argv
import dnspod
import opendkim
import statistics
import iptable
import verifyemail
import verifyweb
import apiemail

reload(sys)
sys.setdefaultencoding('utf8')

print('————发邮件准备步骤,从上到下依次完成!,打错字按crtl+删除键回删！————\n生成密匙 \n删除全部域名解析\n添加全部域名解析\n检查邮件\n检查域名\nip轮询')
print('————发邮件开始步骤————\n记录和查看进度\n群发邮件\n发件统计')
print('————windows多服务器开启api步骤(从上到下依次输入即可)————\n检查api客户邮件\n导入客户邮箱到api\n开启客户邮箱api接口')
input_words= raw_input("""\n\033[1;32;40m请输入执行动作名字:""")

if input_words=='记录和查看进度':	
		deal_email_data.mail_record()
elif input_words=='群发邮件':
		deal_email_data.sendemail()
elif input_words=='检查邮件':
		verifyemail.verifyemail()
elif input_words=='检查域名':
		verifyweb.verifyweb()
elif input_words=='删除全部域名解析' or input_words=='添加全部域名解析':
	 dnspod.dnspod(input_words)
elif input_words=='生成密匙':
     opendkim.opendkim()
elif input_words=='发件统计':
     statistics.statistics()
elif input_words=='ip轮询':
     iptable.iptable()
elif input_words=='检查api邮件':
     verifyemail.verifyapiemail()
elif input_words=='导入客户邮箱到api':
     apiemail.msq_insert('all')
elif input_words=='开启客户邮箱api接口':
     apiemail.start_useremail_api()