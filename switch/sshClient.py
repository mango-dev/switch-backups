import paramiko
import logging

class SSHClient():
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        # 创建一个ssh的白名单
        know_host = paramiko.AutoAddPolicy()
        #加载创建的白名单
        self.ssh.set_missing_host_key_policy(know_host)

    # 此函数实现telnet登录主机
    def login_host(self,host_ip,username,password,port=22):        
        #连接服务器
        result=True
        try:
            # private_key = paramiko.RSAKey.from_private_key_file('C:\\Users\\zhonghai\\.ssh\\devicea.pub')
            self.ssh.connect(
                hostname = host_ip,
                port = port,
                username = username,
                password = password,
                # allow_agent=False,
                look_for_keys=False,
                # pkey=private_key
            )
            stdin, stdout, stderr = self.ssh.exec_command("dis cu", get_pty=True, timeout=20)
            # print ("stdin:")
            # print (stdin)
            # print ("stderr:")
            # print (stderr.readlines())
            # print ("stdout:")
            # print (stdout.readlines())
            print (stdout.read())
            # if stdout.available>0:
            #      print (stdout.readlines())
           
            pass
        except Exception as ex:
            logging.error('%s登录失败，%s'%(host_ip, repr(ex)))
            result=False
            pass        
        return result
    
    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_some_command(self,command):
        #执行命令
        stdin,stdout,stderr = self.ssh.exec_command(command)
        #stdin  标准格式的输入，是一个写权限的文件对象
        #stdout 标准格式的输出，是一个读权限的文件对象
        #stderr 标准格式的错误，是一个写权限的文件对象
        command_result=stdout.read().decode('utf-8')
        print(command_result)
        return command_result
    
    def logout_host(self):
        self.ssh.close()