import paramiko

class SSHClient():
    def __init__(self):
        self.ssh = paramiko.SSHClient()
    # 此函数实现telnet登录主机
    def login_host(self,host_ip,username,password,port=22):
        #连接服务器
        self.ssh.connect(
            hostname = host_ip,
            port = port,
            username = username,
            password = password
        )
        command_result=stdout.read().decode()
        print(command_result)
        return True
    
    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_some_command(self,command):
        #执行命令
        stdin,stdout,stderr = self.ssh.exec_command(command)
        #stdin  标准格式的输入，是一个写权限的文件对象
        #stdout 标准格式的输出，是一个读权限的文件对象
        #stderr 标准格式的错误，是一个写权限的文件对象
        command_result=stdout.read().decode()
        print(command_result)
        return command_result
    
    def logout_host(self):
        self.ssh.close()