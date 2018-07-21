#!/usr/bin/python3.6
# coding:utf-8

from WallPaper.Db import Model


class Config:
    def __init__(self):
        self.conf = {'autorun': 1, 'interval': 1}
        self.model = Model()
        self.load_conf()

    def load_conf(self):
        result = self.model.load_conf()
        if result:
            for item in result:
                self.conf[item['key']] = item['value']

    def get(self, key):
        return self.conf[key]

    def update(self, key, val):
        self.conf[key] = val
        self.model.update_conf(key, val)