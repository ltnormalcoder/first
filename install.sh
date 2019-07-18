#!/bin/bash
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo;
yum -y install epel-release -y;
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm;
yum clean all;
yum makecache --skip-broken;
yum install python -y;
yum install screen -y;
yum install python-requests -y;
yum install opendkim  -y;
yum install postfix  -y;
yum install lrzsz -y;
rm -rf /etc/postfix/main.cf;
rm -rf /etc/postfix/header_checks; 
rm -rf /etc/postfix/master.cf;
cp linux/main.cf  /etc/postfix/main.cf; 
cp linux/header_checks	  /etc/postfix/header_checks; 
cp linux/master.cf  	/etc/postfix/master.cf;
cat > /etc/opendkim.conf<<EOF
Canonicalization        relaxed/relaxed
ExternalIgnoreList      refile:/etc/opendkim/TrustedHosts
InternalHosts           refile:/etc/opendkim/TrustedHosts
KeyTable                refile:/etc/opendkim/KeyTable
LogWhy                  Yes
MinimumKeyBits          1024
Mode                    sv
PidFile                 /var/run/opendkim/opendkim.pid
SigningTable            refile:/etc/opendkim/SigningTable
Socket                  inet:8891@127.0.0.1
Syslog                  Yes
SyslogSuccess           Yes
TemporaryDirectory      /var/tmp
UMask                   022
UserID                  opendkim:opendkim
EOF
service dkim restart;
service postfix restart;
yum -y install python-pip;
pip install dkimpy;
pip install sh;
pip install pytz;
pip install tldextract;
python do.py;
echo '安装成功';
