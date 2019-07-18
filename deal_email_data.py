#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib,email,dkim 
from email.mime.text import MIMEText
from email.header import Header
import dns.resolver 
import iptable
import random
import time
import re  
import os
import sys#sys.argv

 
reload(sys)
sys.setdefaultencoding('utf8')

def senderemail():
	web =  random.choice(iptable.somelist("res/web.txt"))
	name = iptable.clear(random.choice(iptable.somelist("res/static/name.txt")))
	sender=name+'@'+web
	return sender

def sendemail():
  os.system('rm -rf /var/log/maillog')
  os.system('chmod 777 -R /var/log')
  os.system('service rsyslog restart')
  user_emails=iptable.somelist("res/useremail.txt")
  all_num=len(user_emails)
  time_now=time.time()
  ip_list_num=len(iptable.iplist())
  donum=0
  for useremail in user_emails:
    iptable_reset = int(open("res/static/iptable_reset.txt","r").read())
    if iptable_reset % ip_list_num==0:
      iptable.iptable()
      iptable_reset=0
    donum=mail(useremail,donum,user_emails.index(useremail),all_num,time_now)
    iptable_reset=iptable_reset+1
    with open('res/static/iptable_reset.txt','w') as f:
          f.write(str(iptable_reset))
    time.sleep(random.randint(12,21))

def mail(useremail,donum,dealnum,all_num,time_now):
  try:
    os.system('hostname '+iptable.hostwebone())
    sender=senderemail()
    web=sender.split('@')[1]
    message_str=iptable.mail_detail(sender,useremail)
    sig = dkim.sign(message_str, 'default',web, open(os.path.join("/etc/opendkim/keys/"+web+'/', 'default.private')).read())
    message_str='DKIM-Signature: '+sig[len("DKIM-Signature: "):]+message_str
  except :
    with open('res/useremail.txt','a+') as f:
          f.write('\n'+useremail)
  else:
    try:
      sendmaildeal(sender,useremail,message_str)
      message_detail = sender+' sendto '+useremail
      timeuse=time.time()-time_now
    except smtplib.SMTPException as e:
      print e
      if e[0]==550:
        with open('res/useremail.txt','a+') as f:
          f.write('\n'+useremail)
      else:
        with open('res/useremail.txt','a+') as f:
          f.write('\n'+useremail)
    except :
      with open('res/useremail.txt','a+') as f:
        f.write('\n'+useremail)
    else:
		donum=donum+1
		left=all_num-donum
		timeper=timeuse/(dealnum+1)
		oneday_num=str(int((3600*24)/int(timeper)))
		record_process = str(int(timeper))+'秒/每封 '+'  处理 '+str(dealnum+1)+'  成功  '+str(donum)+' 剩余 '+str(left)+'  耗时 '+str(int(timeuse/60))+'分钟 '+oneday_num+'封/天 '+message_detail+'\n'
		with open('res/static/progress.txt','a+') as f:
			f.write(record_process)
		print record_process.replace("\n", "")
  return donum
def sendmaildeal(mailfrom, mailto, msg):  
  domain = email.Utils.unquote(mailto).split("@")[1]
  host = dns.resolver.query(domain, "MX")[0].exchange
  smtp = smtplib.SMTP(str(host))
  smtp.sendmail(mailfrom, [mailto], msg)
  smtp.quit()

def mail_record():
  with open('res/static/progress.txt','r') as fr:
    record_one= fr.readlines()[-1]
    record_mail = iptable.clear(record_one.split('sendto ')[1])
  try:
    undomail=open("res/useremail.txt","r").read().split(record_mail)[1]
    with open('res/useremail.txt','w') as f:
      f.write("\n"+undomail)
    print '记录进度成功！'+record_one
  except :
    print "记录失败请稍后再试！"
