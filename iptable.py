#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys#sys.argv
import os
import random 
import subprocess
import re
import tldextract
import requests
import datetime
import pytz
import time
import io
import json
from email.mime.text import MIMEText

reload(sys)
sys.setdefaultencoding('utf8')

def iptable():
  os.system('iptables -t nat -F POSTROUTING')
  netcard=clear(str(shell_cmd('ip addr')).split('\n2: ')[1][0:20].split(':')[0])
  ip_list=ip_listx()
  ip_list_num=len(ip_list)
  for ip in ip_list:
    num=ip_list.index(ip)
    os.system('iptables  -t nat -I POSTROUTING -m state --state NEW -p tcp --dport 25 -o '+netcard+' -m statistic --mode nth --every '+str(ip_list_num)+' --packet '+str(num)+'  -j SNAT --to-source   ' + ip)
def iplist():
	output=shell_cmd('ip addr')
	ipall=re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/',str(output.split('\n2:')[1]),)
	ipall=''.join(ipall).split('/')
	while '' in ipall:
		ipall.remove('')
	return ipall
def shell_cmd(cmd):
	run_watch=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output,err_msg=run_watch.communicate()
	run_watch.returncode
	return output
def extract_domain(domain):
    suffix = {'.com','.la','.io', '.co', '.cn','.info', '.net', '.org','.me', '.mobi', '.us', '.biz', '.xxx', '.ca', '.co.jp', '.com.cn', '.net.cn', '.org.cn', '.mx','.tv', '.ws', '.ag', '.com.ag', '.net.ag', '.org.ag','.am','.asia', '.at', '.be', '.com.br', '.net.br', '.name', '.live', '.news', '.bz', '.tech', '.pub', '.wang', '.space', '.top', '.xin', '.social', '.date', '.site', '.red', '.studio', '.link', '.online', '.help', '.kr', '.club', '.com.bz', '.net.bz', '.cc', '.band', '.market', '.com.co', '.net.co', '.nom.co', '.lawyer', '.de', '.es', '.com.es', '.nom.es', '.org.es', '.eu', '.wiki', '.design', '.software', '.fm', '.fr', '.gs', '.in', '.co.in', '.firm.in', '.gen.in', '.ind.in', '.net.in', '.org.in', '.it', '.jobs', '.jp', '.ms', '.com.mx', '.nl','.nu','.co.nz','.net.nz', '.org.nz', '.se', '.tc', '.tk', '.tw', '.com.tw', '.idv.tw', '.org.tw', '.hk', '.co.uk', '.me.uk', '.org.uk', '.vg'}

    domain = domain.lower()
    names = domain.split(".")
    if len(names) >= 3:
        if ("."+".".join(names[-2:])) in suffix:
            return ".".join(names[-3:]), ".".join(names[:-3])
        elif ("."+names[-1]) in suffix:
            return ".".join(names[-2:]), ".".join(names[:-2])

    pos = domain.rfind("/")
    if pos >= 0: # maybe subdomain contains /, for dns tunnel tool
        ext = tldextract.extract(domain[pos+1:])
        subdomain = domain[:pos+1] + ext.subdomain
    else:
        ext = tldextract.extract(domain)
        subdomain = ext.subdomain
    if ext.suffix:
        mdomain = ext.domain + "." + ext.suffix
    else:
        mdomain = ext.domain
    return mdomain, subdomain

def hostwebsverify():
  okhostwebs=hostweb()
  with open('res/static/hostweb.txt','w') as f:
  	f.write("".join(okhostwebs))
def hostweb():
	okhostwebs=[]
	hostwebs = open("res/static/hostweb.txt","r").read().split('\n')
	for hostweb in hostwebs:
		hostweb=extract_domain(clear(hostweb))[0]+'\n'
		if len(hostweb)<=20:
			okhostwebs.append(hostweb)
	return list(set(okhostwebs))
def hostwebone():
	hostwebs=hostweb()
	return clear(hostwebs[random.randint(0, len(hostwebs))])

def ip_listx():
  try:
   ipall=open('res/static/ip_list.txt',"r").read().split('\n')
  except :
    output=shell_cmd('ip addr')
    ipall=re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/',str(output.split('\n2:')[1]),)
    ipall=''.join(ipall).split('/')
    while '' in ipall:
      ipall.remove('')
    ip_list=ipall
    random.shuffle(ip_list)
    ip_list_num=len(ip_list)
    with open('res/static/ip_list.txt','w') as f:
      for ip in ip_list:
        f.write('\n'+ip)
  ipall=open('res/static/ip_list.txt',"r").read().split('\n')
  iplist=[]
  for ip in ipall:
    ip=clear(ip)
    if ip != '':
      iplist.append(ip)
  return iplist
def clear(word):
	return  word.replace('"', '').replace("\n", "").replace(' ', '').strip().replace('	', '')
def somelist(list_path):
  some_list=[]
  some_all=open(list_path,"r").read().split('\n')
  some_list= list(set(some_list))
  for someone in some_all:
    someone=clear(someone)
    if someone != '':
      some_list.append(someone)
  return some_list
def mail_detail(sender,useremail):
    text= MIMEText(rand_words('txt'), 'plain', 'utf-8').as_string().split('Content-Transfer-Encoding: base64')[1] 
    msg={}
    msg['X-Virus-Scanned']='amavisd-new at '+sender.split('@')[1]
    msg['Mime-Version']='1.0'
    msg['Date'] = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%a, %d %b %Y %H:%M:%S')+' +0800'
    msg['Content-Type'] ='text/plain; charset="utf-8"'
    msg['Message-ID'] = "<" + str(time.time()) +sender+ ">"
    msg['X-Mailer']='RainLoop/1.10.0.103'
    msg['From'] =sender
    msg['Subject'] =rand_words('subject')
    msg['To'] =useremail
    msg['Content-Transfer-Encoding']='base64'
    msg_order=['X-Virus-Scanned','Mime-Version','Date','Content-Type','Content-Transfer-Encoding','Message-ID','X-Mailer','From','Subject','To']
    i=0
    message_str=''
    for key in msg:
      message_str=message_str+msg_order[i]+': '+msg[msg_order[i]]+'\n'
      i=i+1
    message_str=message_str+text
    return message_str
def content_data(typename):
  content_type={}
  novel=io.open("res/static/novel.txt","r",encoding="utf8").read()
  randomlem =random.randint(0,len(novel))
  content_type['subject'] = subString(novel,randomlem,12+randomlem)
  content_type['txt']= subString(novel,randomlem,500+randomlem)
  return content_type.get(typename)
def subString(string,start,length):
  if length >= len(string):
        return string
  result = ''
  i = 0
  p = 0
  while True:
        ch = ord(string[i])
        #1111110x
        if ch >= 252:
            p = p + 6
        #111110xx
        elif ch >= 248:
            p = p + 5
        #11110xxx
        elif ch >= 240:
            p = p + 4
        #1110xxxx
        elif ch >= 224:
            p = p + 3
        #110xxxxx
        elif ch >= 192:
            p = p + 2
        else:
            p = p + 1
        if p >= length:
            break;
        else:
            i = p
  return string[start:i]


def  w(type_words=''):
  words={}
  words['ce']=random.choice('册,冊,侧,荝,测,恻,粣,笧,側,策,測,惻'.split(','))
  words['zhu']=random.choice('住,助,驻,迬,注,祝,柱,炷,砫,紸,筑,軴,註,跓,鉒,飳'.split(','))
  words['xia']=random.choice('虾,下,吓,疜,圷,梺'.split(','))
  words['zai']=random.choice('哉,烖,载,傤,儎'.split(','))
  words['bu']=random.choice('逋,庯,峬,晡,誧,餔,哺,捕,補,悑,埔'.split(','))
  words['yu']=random.choice('鱼,魚,渔,鰅,鲳,鲸,鲲'.split(','))
  words['bai']=random.choice('百,佰,陌,柏,栢,捭,絔,竡,粨,兡'.split(','))
  words['jia']=random.choice('家,傢,镓,鎵,幏,榢,稼,糘'.split(','))
  words['le']=random.choice('乐,楽,樂,鱳'.split(','))
  words['niu']=random.choice('牛,牜,汼,犇,牪'.split(','))
  words['dou']=random.choice('斗,阧,枓,钭,鈄,鬥,閗,鬦'.split(','))
  words['di']=random.choice('啲,地'.split(','))
  words['zhu']=random.choice('主,拄,迬,炷,砫,紸,軴,跓,鉒'.split(','))
  words['ju']=random.choice('局,侷,焗,锔,跼,駶'.split(','))
  words['chong']=random.choice('冲,充,沖,茺,珫,衝,铳,銃'.split(','))
  words['shui']=random.choice('水,氺'.split(','))
  words['rand_words']=random.choice('丰,中,九,久,乏,乌,丹,玍,乍,丘,乔,乖,了,一,丁,万,上,下,不,丑,专,丕,世,丛,严,丽,乙,乜,乱,乸,乳,之,义,主,举,公,共,兴,典,美,羡,勾,匀,冯,冰,冲,冱,冻,冷,冶,净,冽,凋,凉,凌,凄,准,凛,凝,卞,卢,卤,厄,历,厉,厚,厘,原,厦,厮,刁,刃,分,切,刍,初,龟,劈,刚,列,刘,别,利,到,剀,刻,剌,前,削,剧,剡,副,剩,剽,儿,兀,允,光,先,党,兢,二,元,井,五,云,亚,亟,些,区,匹,匝,匡,匿,匾,匮,阨,邠,那,邪,阳,阴,陈,阽,邻,陆,陇,邳,邱,陁,陀,邹,阻,降,陋,陕,郁,郑,郅,陡,险,都,陶,隗,隆,隐,隘,鄙,隤,兑,养,兼,兽,几,凡,凯,卵,冉,冏,罔,冒,劣,劲,劳,劬,劭,劼,勃,勇,勐,勍,勚,勤,勰,冗,农,罕,冥,冢,凶,凹,凸,函,人,从,介,仄,令,仝,众,余,俞,亿,仁,什,仡,伋,仞,仙,仔,仰,伧,价,伉,任,伟,伪,休,优,伛,仲,佁,伴,佊,低,伶,佞,伾,佗,佚,佣,佐,侧,侈,佌,侗,佴,供,佹,佷,佪,佶,佳,侥,佼,侃,侉,侨,佻,依,侏,便,促,俄,俛,侯,俒,俭,俊,俚,俪,俍,俟,俏,侵,俅,俗,侻,信,修,俨,倡,俶,倅,健,倢,倞,倨,倔,倥,倮,俳,倩,倏,倖,倬,偲,偟,偈,假,傀,偻,偶,偏,停,偷,傲,傍,傎,傥,傫,僇,僄,傻,僭,僚,僮,僖,儋,僵,僻,僿,儇,僽,儜,儒,儡,全,十,千,午,半,卉,华,协,卑,单,卓,博,厶,去,县,叆,亢,充,交,亨,京,亮,亲,亭,亵,亶,亹,讱,讪,讷,设,讼,诐,诎,诈,诚,诞,该,诡,诙,诜,详,诩,误,调,谅,谂,谀,诸,谆,谌,谎,谐,谑,谚,谠,谧,谦,谫,谨,谩,谲,谭,廷,延,建,反,双,叔,叛,艾,节,芒,芃,芊,芝,苍,芳,芾,芬,花,芹,芮,芜,苎,苞,苯,苾,苟,苦,苛,苓,茏,茂,苠,苶,苹,茕,苒,苕,英,茁,草,茈,荡,荒,荟,茧,荩,荆,荦,茫,茗,茜,荏,茸,荣,茹,茵,荧,莽,莘,荼,莺,莹,莠,菶,萃,菲,菨,萋,菀,萧,著,葆,落,葩,葸,蓝,蒙,蓬,蓊,蓁,蒸,蔼,蓼,蔓,蔑,蔫,蔚,蕃,蕡,蕙,蕤,蕊,蕴,蕞,薆,薄,薋,蕻,薾,藁,藉,藐,薿,薰,藻,蘖,屯,彻,很,律,徇,徒,徐,得,循,微,徽,川,辽,达,过,迈,迅,迂,迟,近,连,违,远,运,迍,迩,迥,迫,迢,迮,适,逊,逢,逦,速,逖,通,透,逴,逶,逸,逼,遍,遄,遑,遒,遂,遐,逾,遝,遥,遴,遽,邅,邈,邃,邋,寸,对,寿,封,尊,大,夭,太,天,夯,央,夹,夸,夷,奀,奂,奔,奇,奅,奄,奕,奘,奢,奡,奥,奭,奰,飞,干,平,年,幸,工,巨,巧,左,巩,差,引,弘,弛,弥,弱,弸,强,弁,异,弇,弈,弊,广,庄,废,庞,庭,庳,康,庶,庸,廆,廓,廉,廑,廪,归,当,彗,彝,币,帅,希,帖,常,幅,幢,幠,口,叨,古,叫,可,叩,另,右,只,吊,合,各,后,吉,名,吵,呆,呔,否,告,呐,呛,吞,吴,员,咍,和,呿,周,哀,哏,哈,哗,哙,咪,哝,品,咸,响,哑,咽,咫,哿,哨,唐,哲,啷,啉,啬,唰,啴,喎,嗒,喙,喈,喷,善,喜,喧,喑,喁,嗄,嗔,嗲,嗛,嗣,嘈,嘎,嘏,嘒,嘉,嘌,嘕,嘐,嘿,嘹,嘶,噩,噭,嚣,嚚,嚾,囋,马,驯,驳,骀,驽,驶,驼,骉,骄,骁,骏,骊,骍,骚,骛,骜,骞,骠,骤,闳,闶,闷,闰,闲,闹,闿,阆,阔,阒,阖,阙,阘,阗,宁,安,宏,完,宝,定,官,宓,审,实,宛,宜,客,宪,宣,宥,家,害,宽,容,宵,宴,寄,寂,密,宿,寅,富,寒,寞,寝,察,寡,寥,寯,女,妇,奸,好,妄,妋,妙,妥,妩,妍,妖,妹,姌,委,姁,姹,姤,姽,姞,娇,姣,姱,姥,娄,娈,娆,姝,娃,威,姚,姿,娖,娥,娟,娉,娑,娓,娴,娱,婳,婧,婪,婠,婉,婋,婞,婬,媠,媚,婷,媟,媸,嫔,嫡,嫚,嫩,嫳,嫣,嫕,嫽,嬴,嬮,孅,犷,狂,狗,狙,狞,独,狠,狡,狯,狭,狷,狼,猖,猛,猇,猗,猘,猴,猾,猱,猥,猩,獠,山,岌,岂,屼,屹,岑,岐,岖,岸,岿,峃,岩,峤,峣,峥,峨,峻,峭,崇,崔,崛,崎,崖,崟,崭,崒,崿,嵌,嵚,崴,嵬,嵎,嶅,嵩,嵸,嶟,嶪,嶷,巉,巍,巇,彤,彧,彪,彬,彰,尺,尼,尽,层,局,屃,届,居,屈,屎,屑,展,饬,饱,饴,饶,馁,馊,壬,壮,壹,才,扫,把,抗,抠,扰,抟,拗,拐,拧,拓,拙,拱,挢,挠,挑,挺,挣,指,捍,挽,捂,挹,掺,接,捷,掘,排,揙,搓,揭,搊,摇,撑,撝,撅,氾,汃,汲,污,沧,沉,沌,汾,沣,汩,沆,没,沔,沛,沙,汰,汪,沃,汹,沄,泌,泊,沸,沽,泓,浅,泂,沮,泠,沬,沵,泥,泡,泼,沱,泫,泱,油,沾,治,泚,洞,洏,洸,洪,浑,活,济,浃,浇,洁,津,洌,浏,浓,洽,洳,洒,洼,洿,涎,洋,浊,浡,涔,浮,海,浩,涣,涓,浚,浪,涟,流,涊,润,涩,涨,浞,淳,淡,渎,涵,淏,涸,淮,混,淋,渌,淖,清,渠,深,淑,淘,淹,淫,渊,淄,渤,滑,湫,湝,渴,湎,渺,湿,湜,溲,渟,湍,温,渥,湑,游,湛,滞,滋,滀,滚,滈,滉,溷,滥,漓,溜,满,漭,溟,漠,滂,溥,溶,溽,溏,滔,滃,滟,溢,滢,滓,滮,漼,漧,澉,漶,漏,漫,漂,漙,潇,漾,潆,潮,澄,澒,潦,潾,潜,潸,澾,潭,潼,潫,澹,澴,激,澽,澧,潞,濡,瀁,濯,瀚,瀼,灏,红,纤,纫,纨,约,纯,纷,纮,纭,纵,绌,经,练,细,终,组,给,绛,绞,结,绝,绚,绥,绣,绰,绸,绯,绿,绵,绮,绳,综,缁,缓,缕,缅,缇,缃,缊,缤,缟,缛,缦,缪,缥,巽,土,圣,圬,坌,坟,坏,坚,均,块,垂,坤,坦,垫,垢,垝,垲,垮,垚,埌,埋,埆,堕,基,堇,埤,堂,塞,塌,墋,墨,回,团,因,困,固,圃,圆,圜,圞,尧,外,多,夙,夜,够,夥,小,少,尔,尕,尖,尚,尜,恭,忉,忣,忙,忭,怅,忱,忡,怆,快,忪,怃,忺,忻,忮,怊,怛,怪,怦,怯,怗,怏,怡,怿,怔,恻,恒,恍,恢,恛,恺,恪,恲,恰,恬,恌,恸,恟,恂,恹,恽,悖,悍,悁,悃,离,悢,悯,悭,悄,悌,悒,悦,惭,惨,惝,惆,惙,悰,悴,惇,悱,惯,惛,悸,悾,悽,惓,惘,悻,悲,愊,愎,惼,惰,愤,慌,惶,慨,愣,愀,惺,愔,愉,慊,慎,慷,憀,慢,慓,慵,懊,憯,憧,憔,懆,憺,懒,懈,懁,懤,懦,懵,幺,幻,幼,幽,弋,尤,尨,尪,处,备,复,夏,夐,孑,子,孔,孖,孜,孤,季,孟,孩,孪,孬,孰,孱,孺,孽,负,贞,败,贫,贤,质,贲,费,贵,贱,贸,贴,赅,贼,资,赊,赖,赘,赝,赟,赡,赢,比,毖,烈,热,烝,焦,然,煦,照,熙,熊,熏,熟,熹,燕,长,轫,轩,轮,软,轻,轶,较,辁,辊,辑,输,歹,死,残,殆,殄,殊,殑,殢,斗,斜,卮,危,卷,方,旁,旅,旄,旋,族,飒,飖,飘,飙,成,戎,我,戚,戤,戬,戾,所,扁,扇,扈,火,灰,灿,灵,炀,灼,炕,炜,炎,炳,炽,炯,烂,烁,炫,烦,烜,烨,焕,烺,焯,焜,焮,煳,煌,煖,煊,煜,煴,熇,煽,熛,熯,熠,燋,燊,燠,燥,见,规,现,觍,斥,断,斯,新,考,老,者,耇,耄,耆,毛,毨,氄,木,本,末,机,朴,杀,朽,杂,朱,村,杕,极,条,杌,板,杲,果,杰,林,杪,松,枉,枭,杳,标,枸,枯,柔,枵,柴,格,桓,桀,栗,栖,桥,桡,栩,梵,棻,梗,检,梨,梧,棒,椎,棼,楛,棘,棱,棉,森,椭,棕,楚,楞,槁,槃,榷,樊,横,橤,檀,牛,牢,犁,犀,犟,犨,牡,牣,牷,特,犄,牂,片,攻,攸,故,敝,敢,敏,敞,敦,散,敷,整,氛,欠,次,欣,欻,欿,款,欺,歆,歉,歙,旧,旭,旬,早,旨,旱,旷,时,旸,昂,昌,昒,昏,昆,明,旺,昕,易,昪,昶,昧,昵,是,显,星,昫,昱,昭,晃,晟,晅,晏,晔,晧,晦,晚,晤,晛,晢,晻,晶,景,普,晴,暑,晰,暂,智,晬,暗,暋,暖,暐,暇,暄,暧,暠,暝,暮,暴,暵,曀,曛,曩,氐,民,祁,祈,祇,祎,神,祥,禅,祺,禔,手,拳,挚,殷,殿,毅,水,永,沓,泰,淼,玮,珍,班,玼,琅,理,琐,琦,琼,瑳,瑰,瑞,瑟,瑶,璀,璟,璘,璨,韧,韪,文,斋,斑,斌,斐,忍,忽,忠,怠,怼,急,怒,思,总,恶,恩,恚,恝,恳,恧,悫,悉,悬,悠,惫,惠,惑,惄,愁,慈,愚,慇,愿,憋,憃,憨,慧,慜,慼,慰,憝,憖,懋,懃,懿,戆,牙,爻,爽,曲,曳,曶,曼,曾,最,有,肜,肖,肥,肤,肫,胞,背,朏,胡,胧,胖,胜,脆,胹,胶,朗,脓,朓,脡,脩,脏,脞,脯,脱,腓,腑,腆,腴,腹,腼,腻,腯,腥,膏,膗,朦,臊,臃,臞,攲,正,歧,武,歪,白,百,皂,皇,皋,皑,皎,皓,皙,皡,皤,皦,皭,登,甘,甚,甜,瓤,私,秃,秀,秕,种,科,秋,秘,积,秽,稆,秾,稍,稀,稗,稠,稔,稙,稚,穊,稳,稿,穀,穆,穟,穰,钐,钝,钜,钧,钦,铍,铄,铁,铤,铜,铦,银,铮,铢,锋,锐,错,锢,锦,锖,镐,镜,镞,竖,竑,竞,竟,章,童,端,矜,矞,盈,益,盛,盘,盩,盭,母,每,毒,盲,直,眊,眉,眇,盼,眩,眛,眢,真,着,睆,睐,睢,睩,睦,睒,睟,瞆,瞀,睿,瞌,瞒,瞢,瞑,瞎,瞪,瞧,瞳,瞽,矇,瞿,矍,矗,疚,疯,病,疾,疲,痍,痞,痛,痹,痴,瘁,瘅,痼,痯,瘌,瘦,瘟,瘪,瘠,癃,瘸,癞,癫,鸣,鸿,鸷,鹄,鹑,鹤,皮,生,甡,石,研,砥,硁,破,硌,硗,硕,确,硬,碜,碌,碕,碏,碎,碧,磁,碣,磕,磊,磏,磐,磬,磷,矢,矫,矬,短,矮,祟,票,禁,罢,甲,申,畅,畏,留,略,畴,番,畯,畸,疆,玄,玈,率,究,穷,空,穹,穿,突,窎,窊,窅,窈,窄,窕,窘,窭,窳,窿,窾,疌,疏,袢,袾,裕,裨,裸,褊,褡,褐,褴,襜,襢,甫,玉,臧,虬,虻,蚁,蚩,蛊,蛇,蛮,蛙,蜂,蝉,蜜,蜿,融,蟠,蠢,耎,耽,耿,耸,聃,聊,聪,聩,聱,缺,罄,艮,良,艰,虎,虐,虔,虚,虢,虣,虩,臼,臾,舆,耗,耦,粉,粗,粝,粘,粥,粲,粹,精,糊,糙,糟,糨,糯,紧,素,索,紊,累,絜,絮,紫,繁,繇,齐,肉,腐,艳,舒,絡,絪,絑,縓,縯,繟,纁,要,覃,覈,行,衎,衍,裴,褎,褒,襄,翊,翌,翘,翕,翔,翠,翩,翰,翯,翳,翼,聿,肃,肆,至,致,般,竺,笃,笋,笨,答,等,简,筱,簉,籍,臭,輶,辱,赤,赧,赪,赩,赫,赭,豁,覼,觥,觫,觭,里,重,野,鹾,躬,豪,豫,辛,辟,辣,辩,訏,訑,訚,訢,訸,詹,誓,諓,諴,謏,諠,謇,謟,警,譞,讆,讙,邕,酣,酥,酡,酩,酲,酷,酸,酽,醇,醋,醎,醒,醨,醟,醮,醰,醴,醲,釂,赳,超,趣,趫,足,趸,跂,跄,跌,跏,跬,路,跣,跼,踧,踑,踞,踦,踠,蹁,蹇,蹒,蹩,蹙,蹛,蹶,躄,躁,龅,龊,非,靡,阜,金,鋹,閟,闇,青,靓,靖,静,餲,餮,鲁,鲜,鲠,鲸,鲰,雪,雱,零,雾,霉,霈,霅,霏,霍,霜,霞,霨,霪,隽,难,雀,雄,雅,雁,雏,雍,雌,雕,雝,颿,飂,革,鞅,鞫,髐,鬼,魁,魋,魏,魔,面,首,韡,香,馞,馨,頔,頠,顑,顜,顗,顠,韵,韶,髟,髧,髦,鬅,鬈,鬋,鬑,鬘,鬯,高,鬻,駜,駓,騃,黄,黇,鹿,麟,麻,麽,黁,鼎,黑,黕,默,黔,黛,黝,黠,黟,黢,黪,黩,黯,黮,黭,黵,黎,黏,齁,齉,齘,龢,衢,羸,颀,顸,颓,衡,颙,颛,颢,颖,颇,颦,顽,领,颠,顿,颉,颎,频,顷,预,颋,顺,衰,血,羊,群,袁,袅,羲,衷'.split(','))
  return words[type_words]
def rand_words(type_words):
  words={}
  index_url = 'http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=https://bfyx88.com/?ccid='+str(time.time())
  url_down = 'http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=https://bfqp99.com/?ccid='+str(time.time()+100)
  try:
    index_url = json.loads(requests.get(index_url).text)[0]['url_short'].replace('http://','')
    url_down = json.loads(requests.get(url_down).text)[0]['url_short'].replace('http://','')
  except :
    index_url='bfyx88.com/?ccid='+str(time.time())
    url_down = 'bfqp99.com/?ccid='+str(time.time()+100)
  words['subject']=['《滿'+w('ju')+'獎》', '《返5%'+w('shui')+'》', '《'+w('chong')+'送》']
  random.shuffle(words['subject'])
  words['txt']=['，'+w('zhu')+w('ce')+'；'+index_url  +'，','，'+w('xia')+w('zai')+'；'+url_down +'，','，'+'必'+' '+'，'+' '+'發'+'，','，'+w('bu')+w('yu')+'，','，'+w('bai')+w('jia')+w('le')+'，','，'+w('niu')+w('niu')+'，','，'+w('dou')+w('di')+w('zhu')+'，']
  random.shuffle(words['txt'])
  text=content_data(type_words)
  text_front=['\n','\n','\n','\n','\n','\n','\n']
  if type_words=='subject':
    for i in text:
      words[type_words].append(i)
    random.shuffle(words[type_words])
    words[type_words]=''.join(words[type_words])
  elif type_words=='txt':
    words[type_words].extend(text_front)
    random.shuffle(words[type_words])
    words[type_words]=''.join(words[type_words])+'\n'+text
  return words[type_words]