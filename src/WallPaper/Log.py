#!/usr/bin/python3.6
# coding:utf-8
import time


class Log(object):
    def __init__(self):
        self.file = open('/var/log/bingwallpaper/info.log', 'a')

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Log, cls)
            cls._instance = orig.__new__(cls, *args)
        return cls._instance

    def _log(self, type, msg):
        self.file.write(time.strftime('[%Y-%m-%d %H:%M:%S] [{}] {}{}').format(type, msg, "\n"))
        self.file.flush()

    def log(self, msg):
        self._log('LOG', msg)

    def debug(self, msg):
        self._log('DEBUG', msg)

    def info(self, msg):
        self._log('INFO', msg)

    def error(self, msg):
        self._log('ERROR', msg)