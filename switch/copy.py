import logging
from switch.telnetClient import TelnetClient
from switch.sshClient import SSHClient
from utils.confRead import Config
from utils.mkDir import mk_dir
import json
import time
import os

class FileCopy():

    def Copy(self):
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
                self.telnet(host)
            elif login_type="ssh":
                self.ssh(host)
                
    def ssh(self,host):
        host_ip = host["host"]
        username = host["user"]
        password = host["pwd"]
        brand = host["brand"]
        # TODO:待完善SSH
        ssh_client=SSHClient()
        if ssh_client.login_host(host_ip,username,password):
            # 拉取配置
            config_str=""
            if brand=="H3C":
                command="dis cu"
                # 输入命令拉取
                for_index=0
                while True:
                    for_index+=1
                    config_str_ln= ssh_client.execute_some_command(command)
                    if for_index==1:
                        config_str_ln=config_str_ln.replace("dis cu","")
                    if "---- More ----" in config_str_ln:
                        command=" "
                        config_str_ln=config_str_ln.replace("---- More ----","")
                        config_str+=config_str_ln
                    else:
                        config_str_ln=config_str_ln.replace("return\n","return")
                        config_str+=config_str_ln
                        break
                config_str=config_str.replace("<H3C>\n","").replace("<H3C>","")
                pass
            # 退出
            ssh_client.logout_host()
            # 写入文件                
            self.write_file(host_ip,config_str)
            pass
        pass


    def telnet(self,host):
        host_ip = host["host"]
        username = host["user"]
        password = host["pwd"]
        brand = host["brand"]
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
                    if for_index==1:
                        config_str_ln=config_str_ln.replace("dis cu","")
                    if "---- More ----" in config_str_ln:
                        command=" "
                        config_str_ln=config_str_ln.replace("---- More ----","")
                        config_str+=config_str_ln
                    else:
                        config_str_ln=config_str_ln.replace("return\n","return")
                        config_str+=config_str_ln
                        break
                config_str=config_str.replace("<H3C>\n","").replace("<H3C>","")
                pass
            # 退出
            telnet_client.logout_host()
            # 写入文件                
            self.write_file(host_ip,config_str)
            pass
        pass

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
        