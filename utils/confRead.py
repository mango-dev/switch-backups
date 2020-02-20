from configparser import ConfigParser
import os


class Config:

    def __init__(self):
        """
        初始化
        """
        self.config = ConfigParser()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        self.conf_path = self.conf_path.replace('utils','configs')
        
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

    def set_conf(self, title, value, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def get_conf(self, title):
        """
        读取配置文件中title相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        result = self.config[title]
        return result
