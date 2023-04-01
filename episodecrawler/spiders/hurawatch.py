import scrapy


class HurawatchSpider(scrapy.Spider):
    name = "hurawatch"
    allowed_domains = ["hurawatch.cc"]
    start_urls = ["http://hurawatch.cc/"]

    def parse(self, response):
        pass
