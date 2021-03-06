# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
import re
import sys
sys.path.append("..")
import mydb

class ScrapynewsPipeline:
    def process_item(self, item, spider):
        return item

class ItemAdapterPipeline:
	def process_item(self, item, spider):
		if(len(item['title'])>0):
			item['article'] = self.adapt_article(item['article'])
			item['title'] = self.adapt_text(item['title'])
			
			return item
			
	def remove_lines(self, arr):
		return [self.adapt_text(el) for el in arr]

	def adapt_article(self, article):
		return ''.join([self.adapt_text(el) for el in article])

	def adapt_author(self, authors):
		return [author for author in authors if len(author) > 1 and author != 'and']

	def adapt_text(self, text):
		text = text.rstrip().lstrip()
		return re.sub('[^a-zA-Z0-9 \n\.]', '', text)

class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class MongoDBWriterPipeline:

	def process_item(self, item, spider):
		mydb.collection.insert(dict(item))
		return item
			
