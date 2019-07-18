#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import smtplib
import logging
import time
import re
import iptable
import dns.resolver

#logging.basicConfig(level=logging.DEBUG,
                   # format='%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s')

#logger = logging.getLogger()


def fetch_mx(host):
    '''
    解析服务邮箱
    :param host:
    :return:
    '''
    #logger.info('正在查找邮箱服务器')
    answers = dns.resolver.query(host, 'MX')
    res = [str(rdata.exchange)[:-1] for rdata in answers]
    #logger.info('查找结果为：%s' % res)
    return res


def verify_istrue(email,email_path):
    email_list = []
    email_obj = []
    email_ok = []
    final_res = {}
    #firstverify(email,email_path)
    email_obj=iptable.somelist(email_path)
    all_num=len(email_obj)
    s=connect_email()
    for need_verify in email_obj: 
        totol=email_obj.index(need_verify)
        send_from = login_email(s).docmd('RCPT TO:<%s>' % need_verify)
        if send_from[0] == 250 or send_from[0] == 451:
            final_res[need_verify] = 'True'  # 存在
            record_process = '正在检查 第'+str(totol)+' 个用户邮箱  剩余 '+str(all_num-totol)+'  尝试成功！ sendto '+need_verify+'\n'
            print '正在检查 第'+str(totol)+' 个用户邮箱  剩余 '+str(all_num-totol)+' 个'+need_verify+'结果：'+final_res[need_verify]
            with open('res/static/progress.txt','a+') as f:
                f.write(record_process)
            with open('res/gress.txt','a+') as f:
                f.write(need_verify+'\n')
    s.close()
def firstverify(email,email_path):
    if isinstance(email, str) or isinstance(email, bytes):
        email_list.append(email)
    else:
        email_list = email
    email_obj=[]
    for em in email_list:
        if re.match(r'^[0-9a-zA-Z_]{0,19}@qq\.[com,cn,net]{1,3}$',em):  
            email_obj.append(em)
            print '添加'+em
        else:
            print '忽视'+em
    filter(None, email_obj)
    email_obj = list(set(email_obj))
    with open(email_path,'w') as f:
            f.write('\n'.join( email_obj))
def connect_email():
    try:
        s = smtplib.SMTP('smtp.qq.com', timeout=100)
    except Exception as e:
        time.sleep(1)
        s=connect_email()
    else:
        return s
def login_email(si):
    try:
        s=si
        s.login('692494572@qq.com', 'qgmulruqictnbbcg')
        s.docmd('HELO we'+str(random.randint(100000,100000000))+'.cn')
        s.docmd('MAIL FROM:<'+'692494572@qq.com'+'>')
    except Exception as e:
        print '意外断开！'
        time.sleep(600)
        s=login_email(si)
    else:
        return s
def verifyemail():
    useremails=iptable.somelist('res/useremail.txt')
    final_list = verify_istrue(useremails,'res/useremail.txt')
def verifyapiemail():
    useremails=iptable.somelist('res/apiuseremail.txt')
    final_list = verify_istrue(useremails,'res/apiuseremail.txt')