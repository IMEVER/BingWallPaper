#!/usr/bin/python
import re
import threading
import urllib2, urllib
import os
import time
from Db import Model
from Log import Log
import json


class BingImg(threading.Thread):
    def __init__(self):
        super(BingImg, self).__init__(name='BingImg')
        self.logger = Log()

    def run(self):
        self.down_img()

    def download(self, url, model):
        pattern = re.compile(r'[^/]*$')
        match = pattern.search(url)
        if match:
            file = match.group()
        else:
            return

        dir = os.path.expanduser('~/.local/share/bingwallpaper/')
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
                os.path.exists(dir)
            except:
                self.logger.error('Error create dir' + dir)

        dest = dir + file
        try:
            urllib.urlretrieve(url, dest)
            self.logger.info('Save image ' + url + ' to dir ' + dest)

            model.save(time.strftime('%Y-%m-%d'), url, file)
            os.system("gsettings set org.gnome.desktop.background picture-uri file://" + dest.replace(' ', '\ '))
        except:
            self.logger.error('Error retrieving the Url:' + url + ', to dest:' + dest)

    def parse_img_url(self):
        url = 'https://www.bing.com/'
        data = urllib2.urlopen(url)

        content = data.read()
        # print content
        pattern = re.compile(r";g_img=\{url:\s*['\"]([^'\"]*?)['\"]")
        # print pattern.pattern
        match = pattern.search(content)
        if match:
            img = match.group(1).replace('\\', '')
            if not img.startswith('http://') and not img.startswith('https://'):
                img = url + img
            self.logger.info('img url: ' + img)
            return img
        else:
            self.logger.error('Get img url failed!')
            return None

    def parse_img_url_from_json(self):
        url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
        data = urllib2.urlopen(url).read().decode('utf-8')
        ret = json.loads(data)
        imgUrl = ret['images'][0]['url']

        return imgUrl if imgUrl.startswith('http') else 'https://cn.bing.com' + imgUrl

    def down_img(self):
        while True:
            model = Model()
            item = model.getOneByDay(time.strftime('%Y-%m-%d'))
            if not item:
                url = self.parse_img_url_from_json()
                # url = self.parse_img_url()
                if url:
                    self.download(url, model)

            model.close()
            del model
            time.sleep(60 * 60 * 8)
