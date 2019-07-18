
# coding:utf-8
 
import json
from urlparse import parse_qs
from wsgiref.simple_server import make_server
import MySQLdb
import sys 
import time
import iptable

def db_config():
	db_config={}
	db_config['host']="127.0.0.1"
	db_config['username']="ewomail"
	db_config['passwords']="GGHheZdnkcdTFvVu"
	db_config['db_name']="apiemail"
	return db_config

def msq_select(condition,table=''):
    db = MySQLdb.connect(db_config()['host'], db_config()['username'], db_config()['passwords'], db_config()['db_name'], charset='utf8')
    cursor = db.cursor()
    #user=msq_select('order by id asc limit 1')[0]
    table=check_table(table)
    sql='select * from '+table+' '+condition
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute(sql)
    datalist=[]
    for x in cursor:
        datalist.append({'id':x[0],'useremail':x[1],'status':x[2]})
    return datalist
def msq_update(condition,table=''):
    #msq_update('status =1 where id='+str(user['id']))
    db = MySQLdb.connect(db_config()['host'], db_config()['username'], db_config()['passwords'], db_config()['db_name'], charset='utf8' )
    cursor = db.cursor()
    table=check_table(table)
    sql='update '+table+' set '+condition
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()
   
def msq_insert(email='',table=''):
    db = MySQLdb.connect(db_config()['host'], db_config()['username'], db_config()['passwords'], db_config()['db_name'], charset='utf8' )
    cursor = db.cursor()
    table=check_table(table)
    if email=='all':
        useremail=''
        for x in iptable.somelist("res/apiuseremail.txt"):
            useremail=useremail+'("'+x+'")'+','
    else:
        useremail='("'+email+'")'
    sql = 'insert into '+table+'(useremail) values'+useremail[:-1] 
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()
def check_table(table):
    if table=='':
        table='useremails'
    return  table

# 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
def application(environ, start_response):
    # 打开数据库连接
    # 定义文件请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'text/html')])
    # 获取当前get请求的所有数据，返回是string类型
    params = parse_qs(environ['QUERY_STRING'])
    # 获取get中key为name的值
    useremail =  params.get('useremail', [''])[0]
    status= params.get('status', [''])[0]
    #请求的两个参数邮箱和状态
    if useremail=='':
        try:
            user=msq_select('where status=0 order by id asc limit 1')[0]
            msq_update('status =1 where useremail="'+user['useremail']+'"')
        except Exception as e:
             dic = {'useremail': '','status':''}
        else:
            dic = {'useremail': user['useremail'],'status': user['status']}
    else :
        msq_update('status ='+status+' where useremail="'+useremail+'"')
        db = MySQLdb.connect(db_config()['host'], db_config()['username'], db_config()['passwords'], db_config()['db_name'], charset='utf8' )
        cursor = db.cursor()
        cursor.execute('select count(*) from useremails where status=0')
        left_num=cursor.fetchall()[0][0]
        dic = {'useremail': useremail,'status': status,'left':left_num}
    return [json.dumps(dic)]
def start_useremail_api():
    port = 5088
    httpd = make_server("0.0.0.0", port, application)
    print "serving http on port {0}...".format(str(port))
    httpd.serve_forever() 




 




    
