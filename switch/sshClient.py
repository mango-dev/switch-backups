import paramiko
import logging
import time

class SSHClient():
    # 此函数实现SSH_transport登录主机
    def login_transport(self,host_ip,username,password,port=22):
        #连接服务器
        result=True
        try:
            # 设置SSH连接的远程主机地址和端口
            self.transport = paramiko.Transport((host_ip,22))
            # 设置登陆用户名和密码等参数
            self.transport.connect(username=username,password=password)
            # 连接成功后打开一个channel
            self.channel=self.transport.open_session()
            # 设置会话超时时间
            self.channel.settimeout(60)
            # 打开远程的terminal
            self.channel.get_pty()
            # 激活terminal   
            self.channel.invoke_shell()
            # 进行一次会话，清除欢迎信息
            self.send_some_command("display clock")
            pass
        except Exception as ex:
            logging.error('%s登录失败，%s'%(host_ip, repr(ex)))
            result=False
            pass        
        return result
    
    # 此函数实现transport执行传过来的命令，并输出其执行结果
    def send_some_command(self,command):
        logging.info("执行命令：%s" % command)
        self.channel.send(command.encode('ascii')+b'\n')       
        time.sleep(2)
        # 获取命令结果
        read_recv=self.channel.recv(65535)
        command_result=read_recv.decode('gbk')
        # 打日志
        # logging.warning('命令执行结果：\n%s' % command_result)        
        return command_result
    # transport退出
    def logout_transport(self):
        logging.info("执行命令：退出transport")
        self.transport.close()


    # 此函数实现SSH登录主机,linux访问正常，交换机无法正常执行命令
    def login_host(self,host_ip,username,password,port=22):        
        #连接服务器
        result=True
        try:
            self.ssh = paramiko.SSHClient()
            # 创建一个ssh的白名单
            know_host = paramiko.AutoAddPolicy()
            #加载创建的白名单
            self.ssh.set_missing_host_key_policy(know_host) 
            # private_key = paramiko.RSAKey.from_private_key_file('C:\\Users\\zhonghai\\.ssh\\devicea.pub')
            self.ssh.connect(
                hostname = host_ip,
                port = port,
                username = username,
                password = password,
                # allow_agent=False,
                # look_for_keys=False,
                # pkey=private_key
            )           
            pass
        except Exception as ex:
            logging.error('%s登录失败，%s'%(host_ip, repr(ex)))
            result=False
            pass        
        return result

    # 此函数实现SSH执行传过来的命令，并输出其执行结果
    def execute_some_command(self,command):
        #执行命令
        stdin,stdout,stderr = self.ssh.exec_command(command)
        #stdin  标准格式的输入，是一个写权限的文件对象
        #stdout 标准格式的输出，是一个读权限的文件对象
        #stderr 标准格式的错误，是一个写权限的文件对象
        command_result=stdout.read().decode('utf-8')
        print(command_result)
        return command_result
    # SSH退出
    def logout_host(self):
        logging.info("执行命令：退出ssh")
        self.ssh.close()