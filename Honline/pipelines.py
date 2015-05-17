# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3
from scrapy import log as l
from scrapy.exceptions import DropItem

class HonlineCheckPipeline(object):
    def __init__(self):
        con = sqlite3.connect('keys.db')
        self.c = con.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS vkeys'
                            '(id INTEGER PRIMARY KEY, url VARCHAR(80), post_date VARCHAR(80), klyuchi VARCHAR(80))')
    def process_item(self,item,spider):
        iKey = item['key']
        self.c.execute("SELECT * FROM vkeys WHERE klyuchi = '%s'" % iKey)
        iExists = self.c.fetchone()

        if iExists:
            raise DropItem("Key { %s } is already in our database!" % iKey)
        else:
            return item
# Item data structure
#   class HonlineItem(scrapy.Item):
#       post_link = scrapy.Field()
#       post_time = scrapy.Field()
#       key = scrapy.Field()
#
class HonlineInsertPipeline(object):
    def __init__(self):
        self.con = sqlite3.connect('keys.db')
        self.c = self.con.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS vkeys'
                            '(id INTEGER PRIMARY KEY, url VARCHAR(80), post_date VARCHAR(80), klyuchi VARCHAR(80))')
    def process_item(self, item, spider):
        iKey = item['key']
        iLink = str(item['post_link'])
        iTime = str(item['post_time'])
        q = "INSERT INTO `vkeys`(`url`,`post_date`,`klyuchi`) VALUES (?, ?, ?)"
        self.c.execute(q, (iLink, iTime, iKey))
        self.con.commit()
        l.msg("Key { %s } stored" % iKey)
        return item
    def handle_error(self, e):
        l.err(e)