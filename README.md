# switch-backups
交换机备份

# 概述
>通过telnet或者ssh的方式，登录到交换机，通过相应的交换机命令，将配置文件进行输出，再另存到指定的文件路径下，从而实现交换机配置文件的备份；
由于不同品牌的交换机查看配置文件的命令不一样，因此通过配置文件进行区分；
### 备份规则
>交换机备份，在备份路径下生成yyyy-MM-dd的文件夹，然后按照host的IP生成192.168.3.*.cfg文件
### 查看当前配置
H3C：display currentconfig 简写dis cu，翻页输入:空格

>### 依赖包
telnet：import telnetlib(系统包)
ssh:import paramiko(第三方包)

# python沙箱环境
>安装如下：
pip install virtualenv
virtualenv venv
. venv/bin/activate / windows下 使用 venv\Scripts\activate 关闭：deactivate

# pip包管理
>安装requirements.txt依赖
pip install -r requirements.txt

> pip导出依赖
导出包依赖表：pip freeze > requirements.txt



# 配置文件
>在configs\config.ini下
[HOSTS]
**switch hosts信息**
***brand:H3C***
***type:telnet/ssh***
hosts = [{"name": "192.168.3.*","host":"192.168.3.*","brand":"H3C","type": "telnet","user":"xxx","pwd":"xxx"}]
[DIR]
**备份地址**
backuppath= D:\sln\python\switch-backups\backups\

