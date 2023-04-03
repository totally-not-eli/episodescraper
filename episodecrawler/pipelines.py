# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EpisodecrawlerPipeline:
    items = []
    spider_items = []

    def open_spider(self, spider):
        self.spider_items = []
        print(f"Opening spider... {spider.name} search for {spider.search_term}")

    def process_item(self, item, spider):
        self.items.append(item)
        self.spider_items.append(item)
        return item
    
    def close_spider(self, spider):
        print(f"Closing spider... {spider.name} after search for {spider.search_term}", '\nTotal Items:', len(self.items), 'Spider Items:', len(self.spider_items))
        self.items = []
        self.spider_items = []
