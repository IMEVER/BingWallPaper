#!/usr/bin/python3.6
# coding:utf-8
import os
import os.path
import random
import time
import threading
from WallPaper.Log import Log


class AutoSwitch(threading.Thread):
    def __init__(self, config):
        super(AutoSwitch, self).__init__(name='AutoSwitch')
        self.logger = Log()
        self.config = config

    def get_interval(self):
        return int(self.config.get('interval')) * 60 * 60

    def change(self):
        rootdir = os.path.expanduser('~/.local/share/bingwallpaper/')
        while True:
            for parent, dirnames, filenames in os.walk(rootdir):
                random.shuffle(filenames)
                for filename in filenames:
                    begin = time.time()
                    end = begin
                    while self.get_interval() > (end - begin):
                        time.sleep(3600)
                        end = time.time()

                    os.system("gsettings set org.gnome.desktop.background picture-uri file://" + os.path.join(parent, filename).replace(' ', '\ '))
                    self.logger.log("正在设置壁纸,壁纸来自:" + os.path.join(parent, filename))

    def run(self):
        self.change()
