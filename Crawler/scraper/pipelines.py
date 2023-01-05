
from scrapy import signals
from scrapy.exporters import JsonItemExporter
import json

class CustomPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open(f'main/static/main/{spider}.json', 'w+b')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

"""class ScraperPipeline:

    def open_spider(self, spider):
        self.file = open(f'/Data-{spider}.csv', 'w')
        line =  "price, numberBedrooms, type, area, postcode, url, img" +"\n"
        self.file.write(line)
        print("STARTING#####################################")

    def close_spider(self, spider):
        self.file.close()
        print("CLOSING#####################################")
    
    def process_item(self, item, spider):
        price = item["price"]
        numberBedrooms = item["numberBedrooms"]
        type = item["type"]
        area = item["area"]
        postcode = item["postcode"]
        url = item["url"]
        img = item["img"]
        line = f'{price}, {numberBedrooms}, "{type}", "{area}", "{postcode}", "{url}", "{img}"\n'
        self.file.write(line)
        print("ITEM#####################################")        
        
"""