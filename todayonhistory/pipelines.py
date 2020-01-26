# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

import MySQLdb

class TodayonhistoryPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('history.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'scrapy', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        #  insert into today_on_history(year, day, day_format, title, content)
        #  VALUES (%s, %s, %s, %s, %s)
        insert_sql = """
            insert into today_on_history(year, day, title, content, weight)
            VALUES (%s, %s, %s, %s, %s)
        """
        # self.cursor.execute(insert_sql, (item["year"], item["day"], item["day_format"], item["title"], item["content"]))
        self.cursor.execute(insert_sql, (item["year"], item["day"], item["title"], item["content"], int(item["weight"])))
        self.conn.commit()

