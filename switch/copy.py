import logging
from switch.telnetClient import TelnetClient
from switch.sshClient import SSHClient
from utils.confRead import Config
from utils.mkDir import mk_dir
import json
import time
import os
import re

class FileCopy():
    def Copy(self):
        '''交换机备份入口函数，实现配置文件中主机列表的遍历备份操作
        '''
        # 从配置文件获取交换机列表的服务器信息
        HOSTS=Config().get_conf("HOSTS")
        hosts_str = HOSTS["hosts"]
        hosts_list= json.loads(hosts_str)
        # logging.info(hosts_list)
        for host in hosts_list:
            host_ip = host["host"]
            username = host["user"]
            password = host["pwd"]
            brand = host["brand"]
            login_type=host["type"]
            if login_type=="telnet":
                try:
                    self.telnet(host)
                    pass
                except Exception as tel_ex:
                    logging.info("导出失败：%s，消息：%s"% (host_ip,repr(tel_ex)))
                    pass
                
            elif login_type=="ssh":
                try:
                    self.ssh(host)
                    pass
                except Exception as ssh_ex:
                    logging.info("导出失败：%s，消息：%s"% (host_ip,repr(ssh_ex)))
                    pass
                
                
    def ssh(self,host):
        host_ip = host["host"]
        username = host["user"]
        password = host["pwd"]
        brand = host["brand"]
        # SSH
        ssh_client=SSHClient()
        if ssh_client.login_transport(host_ip,username,password):
            # 拉取配置
            config_str=""
            if brand=="H3C":
                command="dis cu"
                # 输入命令拉取
                for_index=0
                while True:
                    for_index+=1
                    config_str_ln= ssh_client.send_some_command(command)
                    config_str_ln=config_str_ln.replace("\x1b[16D                \x1b[16D","").replace("\r\r\n","\n").replace("\r\r               \r","").replace("\r\n","\n")
                    if for_index==1:
                        config_str_ln=config_str_ln.replace(command,"")
                    if "---- More ----" in config_str_ln:
                        command=" "
                        config_str_ln=config_str_ln.replace("  ---- More ----","").replace("---- More ----","")
                        config_str+=config_str_ln
                    else:
                        config_str_ln=config_str_ln.replace("return\n","return")
                        config_str+=config_str_ln
                        break
                # config_str=config_str.replace("<H3C>\n","").replace("<H3C>","")
                config_str=self.reg_replace_h3c(config_str)
                pass
            # 退出
            ssh_client.logout_transport()
            # 写入文件                
            self.write_file(host_ip,config_str)
            pass
        pass


    def telnet(self,host):
        host_ip = host["host"]
        username = host["user"]
        password = host["pwd"]
        brand = host["brand"]
        # telnet
        telnet_client = TelnetClient()
        # 如果登录结果返加True，则执行命令，然后退出
        if telnet_client.login_host(host_ip,username,password):
            # 拉取配置
            config_str=""
            if brand=="H3C":
                command="dis cu"
                # 输入命令拉取
                for_index=0
                while True:
                    for_index+=1
                    config_str_ln= telnet_client.execute_some_command(command)
                    config_str_ln=config_str_ln.replace("\x1b[16D                \x1b[16D","").replace("\r\r\n","\n").replace("\r\r               \r","").replace("\r\n","\n")
                    if for_index==1:
                        config_str_ln=config_str_ln.replace(command,"")
                    if "---- More ----" in config_str_ln:
                        command=" "
                        config_str_ln=config_str_ln.replace("  ---- More ----","").replace("---- More ----","")
                        config_str+=config_str_ln
                    else:
                        config_str_ln=config_str_ln.replace("return\n","return")
                        config_str+=config_str_ln
                        break
                # config_str=config_str.replace("<H3C>\n","").replace("<H3C>","")
                config_str=self.reg_replace_h3c(config_str)
                pass
            elif brand=="ruijie":
                command="show run"
                # 输入命令拉取
                for_index=0
                while True:
                    for_index+=1
                    config_str_ln= telnet_client.execute_some_command(command)
                    config_str_ln=config_str_ln.replace("\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08          ","").replace("\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08","").replace("\r\n","\n")
                    if for_index==1:
                        config_str_ln=config_str_ln.replace(command,"")
                    if " --More-- " in config_str_ln:
                        command=" "
                        config_str_ln=config_str_ln.replace(" --More-- ","")
                        config_str+=config_str_ln
                    else:
                        config_str_ln=config_str_ln.replace("return\n","return")
                        config_str+=config_str_ln
                        break
                config_str=config_str.replace("Ruijie#\n","").replace("Ruijie#","")
                pass

            # 退出
            telnet_client.logout_host()
            # 写入文件                
            self.write_file(host_ip,config_str)
            pass
        pass
    
    
    def get_h3c_name(self,test_str):        
        '''提取H3C中输出的提示设备名.'''
        result=""
        # coding=utf8
        # the above tag defines encoding for this document and is for Python 2.x compatibility
        regex = r"return<(.*)>"

        matches = re.finditer(regex, test_str, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            
            # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
            
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                
                # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
                result=match.group(groupNum)
                break
            pass
        return result


        # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.

    def reg_replace_h3c(self,test_str):
        '''替换H3C中输出的提示设备名.
        '''
        h3c_name=self.get_h3c_name(test_str)
        regex = r"<"+h3c_name+">\n"
        result= re.sub(regex, "", test_str, count=0, flags=0)
        regex = r"<"+h3c_name+">|<H3C>"
        result= re.sub(regex, "", result, count=0, flags=0)
        return result


    def write_file(self,host,content):
        REPDIR=Config().get_conf("DIR")
        backup_path=REPDIR["backuppath"]
        backup_path += time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 创建每月的文件夹
        mk_dir(backup_path)
        
        # 文件名
        file_name=host+".cfg"
        backup_file=backup_path + '/' + file_name

        if os.path.exists(backup_file):
            os.remove(backup_file)
            pass
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
            pass
        logging.info("导出成功：%s"% file_name)
        