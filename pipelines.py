# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi


class HousesPipeline(object):

    i = 110

    @classmethod
    def from_crawler(cls, crawler):
        cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME")
        cls.MYSQL_HOST = crawler.settings.get("MYSQL_HOST")
        cls.MYSQL_PORT = crawler.settings.get("MYSQL_PORT")
        cls.MYSQL_USER = crawler.settings.get("MYSQL_USER")
        cls.MYSQL_PASSWORD = crawler.settings.get("MYSQL_PASSWORD")
        return cls()

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('pymysql', host=self.MYSQL_HOST, port=self.MYSQL_PORT, user=self.MYSQL_USER,
                                            passwd=self.MYSQL_PASSWORD, db=self.MYSQL_DB_NAME, charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)

        return item

    def insert_db(self, tx, item):
        values = (
            self.i,
            item['title'],
            item['city'],
            item['region'],
            item['address'],
            "小区",
            item['rent'],
            item['rentWay'],
            "有",
            item['toward'],
            "有",
            100,
            100,
            item['feature'],
            item['acreage'],
            item['layout'],
            "游泳池",
            item['introduction'],
            1,
            'pass',
            item['picture']
        )

        introduction = (
            item['introduction'],
            self.i,
        )
        self.i += 1
        sql = 'INSERT INTO house VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        sql1 = 'UPDATE house set introduction = %s WHERE house_id = %s'

        tx.execute(sql1, introduction)