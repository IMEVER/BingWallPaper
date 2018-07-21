#!/usr/bin/python3.6
# coding:utf-8

import os
import sqlite3
from WallPaper.Log import Log


class Model:
    def __init__(self):
        self.logger = Log()
        dir = os.path.expanduser('~/.config/bingwallpaper/')
        if not os.path.exists(dir):
            try:
                self.logger.log('mkdir ' + dir)
                os.makedirs(dir)
            except:
                self.logger.log('\tError create dir' + dir)
        path = dir + "pic.db"

        exist = os.path.exists(path)

        self.conn = sqlite3.connect(path)

        if not exist:
            self.create_table()

    def getOneByDay(self, day):
        sql = 'SELECT * FROM pic WHERE day = ?'
        d = (day,)
        self.logger.log('execute sql: [{}], params:[{}]'.format(sql, d))
        cursor = self.conn.cursor()
        cursor.execute(sql, d)
        r = cursor.fetchall()
        cursor.close()
        if len(r) > 0:
            self.logger.log(r[0])
            return r[0]
        else:
            return None

    def save(self, day, url, file):
        cursor = self.conn.cursor()
        sql = '''INSERT INTO pic (day, url, file) VALUES (?, ?, ?)'''
        data = (day, url, file)
        self.logger.log('execute sql:[{}], params:[{}]'.format(sql, data))
        cursor.execute(sql, data)
        self.conn.commit()
        cursor.close()

    def create_table(self):
        cursor = self.conn.cursor()

        sql = '''CREATE TABLE `pic` (
        `day` varchar(10) NOT NULL,
        `url` varchar(255) NOT NULL,
        `file` varchar(255) NOT NULL,
        `time` TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`day`)
        );'''

        cursor.execute(sql)

        sql = '''CREATE TABLE `config` (
            `key` TEXT NOT NULL,
            `value` INTEGER NOT NULL,
            `desc` TEXT NOT NULL,
            PRIMARY KEY (`key`)
            );'''

        cursor.execute(sql)

        sql = '''INSERT INTO `config` (`key`, `value`, `desc`) VALUES
            ("autorun", 1, "auto run"),
            ("interval", 24, "interval time, unit: hour");
            '''
        cursor.execute(sql)

        self.conn.commit()
        cursor.close()

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            finally:
                self.conn.close()

    def load_conf(self):
        sql = 'SELECT * FROM config'
        self.logger.log('execute sql: [{}]'.format(sql))

        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()
        cursor.execute(sql)
        r = cursor.fetchall()
        cursor.close()
        if len(r) > 0:
            return r
        else:
            return None

    def update_conf(self, key, value):
        cursor = self.conn.cursor()

        sql = '''UPDATE `config` SET `value`= ? WHERE `key`= ?'''
        data = (value, key)
        self.logger.log('execute sql:[{}], params:[{}]'.format(sql, data))

        cursor.execute(sql, data)
        self.conn.commit()
        cursor.close()
