#!/usr/bin/env python3.6
# coding=utf-8
from PyQt5 import QtGui, QtWidgets

import sys
from WallPaper.AutoSwitchWallPaper import AutoSwitch
from WallPaper.Config import Config
from WallPaper.GetBingWallPaper import BingImg
from Window.setting import MyWindow


class App(object):

    def __init__(self):
        config = Config()

        self.bingImg = BingImg()
        self.bingImg.setDaemon(True)
        self.bingImg.start()

        self.auto_switch = AutoSwitch(config)
        self.auto_switch.setDaemon(True)
        self.auto_switch.start()

        self.app = QtWidgets.QApplication(sys.argv)
        logger = MyWindow(config, self.app)
        logger.hide()
        sys.exit(self.app.exec_())

    def quit(self):
        self.app.quit()
        sys.exit()


if __name__ == '__main__':
    App()