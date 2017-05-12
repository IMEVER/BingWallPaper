#!/usr/bin/env python
# coding=utf-8
import os, gettext
from PyQt4 import QtGui, QtCore

from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QDesktopServices
from WallPaper.Log import Log

locale_path = '/data/www/python/BingWallPaper/locale/'
gettext.bindtextdomain('messages', locale_path)
gettext.textdomain('messages')
_ = gettext.gettext
zh_trans  = gettext.install('messages', names=['zh_CN'])


class MyWindow(QtGui.QWidget):
    def __init__(self, conf, app):
        super(MyWindow, self).__init__()

        self.app = app

        self.logger = Log()

        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle("BingWallPaper setting")
        self.resize(300, 200)
        self.setFixedSize(300, 200)
        self.setWindowOpacity(0.95)
        self.center()

        self.conf = conf
        self.set_label()
        self._set_systray()

        self.aboutWindow = AboutWindow()

    def set_label(self):
        vbox = QtGui.QVBoxLayout()

        time_label = QtGui.QLabel(_('Interval(hour):'))
        time_label.setAlignment(QtCore.Qt.AlignCenter)

        select = QtGui.QComboBox()
        select.addItem("1", 1)
        select.addItem("2", 2)
        select.addItems(
            ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
             "22", "23", "24"])
        select.setCurrentIndex(self.conf.get('interval') - 1)

        self.connect(select, QtCore.SIGNAL('activated(QString)'), self.on_select)

        autorun_label = QtGui.QLabel(_('Auto startup:'))
        autorun_label.setAlignment(QtCore.Qt.AlignCenter)
        self.check = QtGui.QCheckBox('')
        self.check.setChecked(self.conf.get('autorun') == 1)
        self.connect(self.check, QtCore.SIGNAL('stateChanged(int)'), self.on_check)

        grid_layout = QtGui.QGridLayout()

        grid_layout.addWidget(time_label, 0, 0)
        grid_layout.addWidget(select, 0, 1)

        grid_layout.addWidget(autorun_label, 1, 0)
        grid_layout.addWidget(self.check, 1, 1)

        vbox.addLayout(grid_layout)

        self.setLayout(vbox)

        # label.setAlignment(QtCore.Qt.AlignCenter)
        # self.setCentralWidget(label)

    def _set_systray(self):
        menu = QtGui.QMenu(self)  # 生成一个系统托盘处的菜单.就一个Quit

        browserAction = QtGui.QAction(QtCore.QString("&" + _("Browser")), self)
        self.connect(browserAction, QtCore.SIGNAL("triggered()"), self.open)
        menu.addAction(browserAction)

        settingAction = QtGui.QAction(QtCore.QString("&"+_("setting")), self)
        self.connect(settingAction, QtCore.SIGNAL("triggered()"), self.show)
        menu.addAction(settingAction)

        aboutAction = QtGui.QAction(QtCore.QString("&"+_("about")), self)
        self.connect(aboutAction, QtCore.SIGNAL("triggered()"), self.about)
        menu.addAction(aboutAction)

        quitAction = QtGui.QAction(QtCore.QString("&"+_("Quit")), self)
        self.connect(quitAction, QtCore.SIGNAL("triggered()"), self.app.quit)
        menu.addAction(quitAction)

        self.icon = QtGui.QSystemTrayIcon(QtGui.QIcon('../resource/index.png'), self)  # 加载系统托盘处的图标
        self.icon.setToolTip(QtCore.QString(u"A Alert Coming..."))
        self.icon.setContextMenu(menu)
        self.connect(self.icon, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.__icon_activated)
        self.icon.show()

    def on_check(self, check):
        self.logger.info('autorun: ' + str(check))
        if self.check.isChecked():
            self.conf.update('autorun', 1)
            os.system("cp /usr/share/applications/BingWallPaper.desktop " + os.path.expanduser('~') + "/.config/autostart/")
        else:
            self.conf.update('autorun', 0)
            os.system("rm -f " + os.path.expanduser('~') + "/.config/autostart/BingWallPaper.desktop")

    def on_select(self, text):
        self.logger.info('interval: ' + text)
        self.conf.update('interval', str(text))

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def __icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.show()

    def center(self):
        qr = self.frameGeometry()  # 返回代表窗口框架结构的矩形
        cp = QtGui.QDesktopWidget().availableGeometry().center()  # 返回屏幕（可显示区域）的中心点
        qr.moveCenter(cp)  # 将与窗口同大的矩形移动到屏幕中央
        self.move(qr.topLeft())  # 将主窗口移动到已定位的矩形处，QWidget的移动以左上角为基准点

    def about(self):
        # if not hasattr(self.__class__, 'aboutWindow'):
        #     self.aboutWindow = AboutWindow(self)
        self.aboutWindow.show()

    def open(self):
        QDesktopServices.openUrl(QUrl('file:///' + os.path.expanduser('~') + '/.local/share/WallPaper'));


class AboutWindow(QtGui.QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()
        # QtGui.QWidget.__init__(self, parent)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle(_("About"))
        self.setFixedSize(400, 300)
        self.setWindowOpacity(0.9)
        self.center()

        vbox = QtGui.QVBoxLayout()

        logo = QtGui.QImage('../resource/index.png')
        pp = QtGui.QPixmap.fromImage(logo)
        logoLabel = QtGui.QLabel()
        logoLabel.setPixmap(pp.scaled(200, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(logoLabel)

        nameLabel = QtGui.QLabel('BingWallPaper')
        nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPixelSize(20)
        font.setBold(True)
        nameLabel.setFont(font)
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.WindowText, QtCore.Qt.blue)
        nameLabel.setPalette(pe)

        vbox.addWidget(nameLabel)

        authorLabel =  QtGui.QLabel('<a href="http://www.imever.me">IMEVER(Hobart_Tian@imever.me)</a>')
        authorLabel.setOpenExternalLinks(True)
        authorLabel.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(authorLabel)

        versionLabel = QtGui.QLabel('Version: 1.0.1')
        versionLabel.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(versionLabel)

        descLabel = QtGui.QLabel(_('BingWallPaper is a app that set you desktop wallpaper with awesome image downloading from www.bing.com every hour'))
        descLabel.setWordWrap(True)
        font = QtGui.QFont()
        font.setPixelSize(14)
        descLabel.setFont(font)
        descLabel.setAlignment(QtCore.Qt.AlignCenter)

        vbox.addWidget(descLabel)

        crLabel = QtGui.QLabel('Copyright © 2012-2017 IMEVER')
        crLabel.setAlignment(QtCore.Qt.AlignCenter)
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.WindowText, QtCore.Qt.gray)
        crLabel.setPalette(pe)
        vbox.addWidget(crLabel)

        self.setLayout(vbox)

    def center(self):
        qr = self.frameGeometry()  # 返回代表窗口框架结构的矩形
        cp = QtGui.QDesktopWidget().availableGeometry().center()  # 返回屏幕（可显示区域）的中心点
        qr.moveCenter(cp)  # 将与窗口同大的矩形移动到屏幕中央
        self.move(qr.topLeft())  # 将主窗口移动到已定位的矩形处，QWidget的移动以左上角为基准点

    def closeEvent(self, event):
        self.hide()
        event.ignore()